needs-file:
ifndef FILE
	$(error FILE is not set)
endif

needs-tag:
ifndef TAG
	$(error TAG is not set)
endif

## setup:		installs prereqs for searching and exporting
setup:
	@brew bundle
	@pipenv install

## xport-pdf:	generates a pdf of the markdown based on filepath without extension
xport-pdf: needs-file
	@pandoc --pdf-engine xelatex -t pdf -o ${FILE}.pdf ${FILE}.md

## search:	lists titles and files for notes matching tag
search: needs-tag
	@pipenv run ./scripts/main.py search ${TAG}

## all-tags:	lists all the tags in the various notes
all-tags: 
	@pipenv run ./scripts/main.py tags

## lint:		runs markdown lint on all files
lint:
	@pipenv run ./scripts/main.py lint

## help:		prints make target help information from comments in makefile.
help: Makefile
	@sed -n 's/^##//p' $< | sort

.phony: setup search all-tags xport-pdf help