#!/bin/bash

pandoc ${@} --standalone --filter pandoc-crossref --citeproc --css css/science.css --from markdown+yaml_metadata_block+implicit_figures+fenced_divs+citations+table_captions --to html5 --webtex
# pandoc ${@} --standalone --embed-resources --filter pandoc-crossref --citeproc --css css/science.css --from markdown+yaml_metadata_block+implicit_figures+fenced_divs+citations+table_captions --to html5 --webtex

# set -e

# opts=()
# opts+=(--standalone)
# # opts+=(--resource-path "$PWD")
# opts+=(--filter pandoc-crossref)
# opts+=(--citeproc)

# ## Add here your global citation style (if you like)
# opts+=(--css "css/md-publisher.css")

# ## Add here your global BibTex library.
# # I use Zotero with the BetterBibTex plugin for automatically exporting the current
# # bibliography to Nextcloud (you could use Dropbox or any other synchronization as well). 
# #opts+=(--bibliography "$HOME/Nextcloud/Notes/Library.bib")
# opts+=(--from markdown+yaml_metadata_block+implicit_figures+fenced_divs+citations+table_captions)
# opts+=(--to html5)

# ## Formula support
# opts+=(--webtex)
# opts+=("${@}")
# pandoc "${opts[@]}"