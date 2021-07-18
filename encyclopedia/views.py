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
            content = content[0] + '</h1> \n <div id="separation"></div>' + content[1]
            return render(request, "encyclopedia/article.html", {
                "article": content, "title": filename + " - Encyclopedia"
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
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('art', args=[entry]))


