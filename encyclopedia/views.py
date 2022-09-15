from urllib import request
from django.shortcuts import render
import markdown
from . import util
import random

def convert_md_to_html(title):
    content=util.get_entry(title)
    md=markdown.Markdown()
    if content == None:
        return None
    else:
        return md.convert(content)
def index(request):
    return render(request,"encyclopedia/index.html",{
       "entries":util.list_entries()
    }) 

def entry(request,title):
  html_content=convert_md_to_html(title)
  if html_content == None:
     return render(request,"encyclopedia/error.html",{
        "message":"this page doesn't exist"
     })
  else:
    return render(request,"encyclopedia/entry.html",{
       "title":title,
       "content":html_content
    } )


def search(reqrest):
    if reqrest.method == "POST" :
        entry_search=reqrest.POST["q"]
        html_content=convert_md_to_html(entry_search)
        if html_content is not None:
            return render(reqrest,"encyclopedia/entry.html",{
                "title":entry_search,
                "content":html_content})
        else:
            allEntries=util.list_entries()
            recommeation=[]
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommeation.append(entry)
            return render(request,"encyclopedia/search.html",{
                "recommeation":recommeation
            })    

def new_page(request):
    if request.method=="GET":
        return render(request,"encyclopedia/new.html")
    else:
        title=request.POST["title"]
        content=request.POST["content"]
        titleExist=util.get_entry(title)
        if titleExist is not None:
            return render(request,"encyclopedia/error/html",{
                "message":"Entry Page already exist"
            })    
        else:
                html_content=convert_md_to_html(title)
                util.save_entry(title,content)
                return render ( request,"encyclopedia/new.html",
                {
                "title":title,
                "content":html_content
                })
def edit(request):

    if request.method =="POST":
        title=request.POST['entry_title']
        content=util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title":title,
            "content":content
        })
def save_edit(request):
    if request.method=="POST":
        title=request.POST["title"]
        content=request.POST["content"] 
        util.save_entry(title,content)  
        html_content=convert_md_to_html(title)
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })
def rand(request):
    allEntries=util.list_entries()
    rand_entry=random.choice(allEntries)
    html_content=convert_md_to_html(rand_entry)
    return render(request,"encyclopedia//entry.html",{
        "title":rand_entry,
        "content":html_content
    })
            


