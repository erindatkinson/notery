needs-file:
ifndef FILE
	$(error FILE is not set)
endif

needs-tag:
ifndef TAG
	$(error TAG is not set)
endif

needs-tags:
ifndef TAGS
	$(error TAGS is not set)
endif

needs-name:
ifndef NAME
	$(error NAME is not set)
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

recent:
	@pipenv run ./scripts/main.py recent

new: needs-name
	@pipenv run ./scripts/main.py new "${NAME}"

new-tagged: needs-name needs-tags
	@pipenv run ./scripts/main.py new --tags ${TAGS} "${NAME}"


## help:		prints make target help information from comments in makefile.
help: Makefile
	@sed -n 's/^##//p' $< | sort

.phony: setup search all-tags xport-pdf help