
import markdown
from markdown import *
from django.shortcuts import render

from . import util
import random

md = Markdown()


def convert_md_to_html(title):
    content = util.get_entry(title)

    if content == None:
        return None
    else:
        return md.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "this page doesn't exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    q = request.POST.get('q', '')
    entries = util.list_entries()
    for entry in entries:
        if str(q.upper()) == str(entry.upper()):
            content = util.get_entry(entry)
            return render(request, "encyclopedia/entry.html", context={
                "title": entry,
                "content": md.convert(str(content))})
        elif str(q.upper()) in entry.upper():
            return render(request, "encyclopedia/index.html", context={
                "entries": [entry]
            })

    return render(request, "encyclopedia/error.html")


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry Page already exist"
            })
        else:
            html_content = convert_md_to_html(title)
            util.save_entry(title, content)
            return render(request, "encyclopedia/new.html",
                          {
                              "title": title,
                              "content": html_content
                          })


def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia//entry.html", {
        "title": rand_entry,
        "content": html_content
    })
