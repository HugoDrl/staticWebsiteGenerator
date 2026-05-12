# Static website generator

This program allows user to generate a static website using markdown files

This program converts markdown files to html.
User still have to provide CSS files in order to style the website.

## What this program does

- Converts markdown titles \(# - ###### to h1 - h6\)
- Converts lists
- Converts quotes
- Converts code
- Converts **bold** and _italic_
- Converts \!\[images\] and \[links\]

This program copies every files from \.\/static folder to \.\/docs, and process every **markdown** file from \.\/content to \.\/public, in respect to file tree.

## Syntax

## What this tool doesn't do :

Please note that **bold** content is only processed with \*\* and _italic_ only with \_.

This tool currently doesn't handle escape characters (e.g. \\\[\\\]). It is planned to make this feature available in the future.

This static website generator is built following boot.dev course.
