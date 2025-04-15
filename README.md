# Notes

A notes setup for vscode and the terminal.

![leather bound journal](./.assets/notebook-420011_1920.jpg)

## Installation

run `make setup`

(technically this also needs NPX but you can install it via ASDF, brew, nvm, etc.)

## Usage

TBD, eventually want to have `NAME=type/filename TAGS=notes,bullshit,ticket make new`
create templated file skeleton.

### Linting

run `make lint` to lint all the markdown

### Exporting to PDF

run `FILE=path/to/filename-without-extension make xport-pdf`
and it should write a pdf to the same path with the same name.

### Searching Tags

tags in the frontmatter yaml are searchable

with a frontmatter yaml like so in a file `./notes/addenda/addenda.md`

```yaml
---
title: Addenda
tags:
    - random
    - notes
---
```

you can search like so:

```shell
~/Notes (main|✔) $ TAG=random make search
pipenv run ./scripts/main.py search random
-------  --------------------------
Addenda  ./notes/addenda/addenda.md
-------  --------------------------
```

### Listing Tags

run `make all-tags`
