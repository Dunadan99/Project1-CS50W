from django.core.files.base import ContentFile
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
import markdown2, random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    for filename in util.list_entries():
        if title.lower() == filename.lower():
            content = markdown2.markdown(util.get_entry(filename)).split('</h1>', 1)
            content = content[0] + '</h1> \n <div class="separation"></div>' + content[1]
            return render(request, "encyclopedia/article.html", {
                "article": content, "title": filename + " - Encyclopedia", "name": filename
            })
    
    return render(request, "encyclopedia/404.html", { 
                "name": title, "title": title + " - Encyclopedia"
            })

def search(request):
    if request.method == "POST":
        search = request.POST.get('q')
        entries = []
        for entry in util.list_entries():
            if search.lower() == entry.lower():
               return HttpResponseRedirect(reverse('art', args=[entry])) 
            elif str(search.lower()) in entry.lower():
                entries.append(entry)
        
        return render(request, "encyclopedia/search.html", {
            "entries" : entries
        })

def randomSite(request):
    return HttpResponseRedirect(reverse('art', args=[random.choice(util.list_entries())]))

def new(request):
    if request.method == "POST":
        title = str(request.POST.get('artTitle'))
        body = str(request.POST.get('artBody'))

        for article in util.list_entries():
            if title.lower() == article.lower():
                return render(request, "encyclopedia/error.html", {
                    "title" : article + " - Encyclopedia", "name" : article
                })

        body = f"# {title}\n{body}"
        util.save_entry(title, body)
        return HttpResponseRedirect(reverse('art', args=[title]))

    elif request.method == "GET":
        return render(request, "encyclopedia/new.html")

def edit(request):
    if request.method == "POST" and request.POST.get("source") == "edit":
        title = str(request.POST.get("artTitle")).strip()
        body  = str(request.POST.get("artBody")).strip()
        content = ''
        for line in body.split('\n'):
            content = content + '\n' + line.strip()
        util.save_entry(title, f"# {title.strip()}\n{content}")
        return HttpResponseRedirect(reverse('art', args=[title]))

    elif request.method == "POST" and request.POST.get("source") == "article":
        title = str(request.POST.get("artTitle"))
        body = str(util.get_entry(title)).split('\n', 1)[1].strip()
        return render(request, "encyclopedia/edit.html", {
            "title" : title, "body" : body
        })

