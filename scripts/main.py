#!/usr/bin/env python
"""Script for searching tags"""
from os import walk, stat
from subprocess import run

from jinja2 import Environment, DictLoader
from frontmatter import load
from fire import Fire
from tabulate import tabulate

def searcher(tag:str, base:str="./notes")->None:
    """Search for files with specific tags"""
    hits = []
    notes = get_all_notes(base)
    for note in notes:
        with open(note, encoding="utf-8") as fp:
            post = load(fp)
            ftags = post.get("tags")
            ftitle = post.get("title")
            if ftags is not None and tag in list(ftags):
                hits.append([handle_title(ftitle), note])
    print(tabulate(sorted(hits, key=lambda x: x[0])))

def list_tags(base:str="./notes")->None:
    """list all tags in the section"""
    tags = []
    notes = get_all_notes(base)
    for note in notes:
        with open(note, encoding="utf-8") as fp:
            post = load(fp)
            ftags = post.get("tags")
            if ftags is not None:
                tags.extend(ftags)
    print(tabulate({"tags": sorted(set(tags))}))

def linter(base:str="./notes")->None:
    """run linting"""
    notes = get_all_notes(base)
    cmd = ["npx", "markdownlint-cli", "-f"]
    cmd.extend(notes)
    run(cmd, check=False)

def recent(n:int=10, base:str="./notes")->None:
    """get most recent"""
    notes = get_all_notes(base)
    print(tabulate({"notes": sorted(notes, key=lambda x: stat(x).st_mtime, reverse=True)[:n]}))


def get_all_notes(base:str)->list[str]:
    """get a list of all notes"""
    steps = walk(base)
    f = []
    for path, _, files in steps:
        test = [f"{path}/{file}" for file in files if ".md" in file]
        f.extend(test)
    return f

def new_note(title:str, tags:str="", templatepath:str="./scripts/note.jinja2"):
    """creates a new note template"""
    filename = title
    for char in ["/","_","(",")"," ", ":", "[","]"]:
        filename = filename.replace(char, "-")

    env = read_template(templatepath)
    note = env.get_template("note.md").render(title=title, tags=str(tags).split(','))

    with open(filename.lower()+".md", 'w', encoding="utf-8") as fp_out:
        fp_out.write(note)

def read_template(path:str):
    """sets up the jinja environment"""
    with open(path, encoding="utf-8") as fp:
        tpl = fp.read()

    return Environment(loader=DictLoader({"note.md": tpl}))

def handle_title(title:str)->str:
    """deal with titles from tags"""
    if title == "None" or title == "":
        return ""
    return title

if __name__ == "__main__":
    Fire({
        "search": searcher,
        "tags": list_tags,
        "lint": linter,
        "recent": recent,
        "new": new_note
        })
