# Vedette
This is a *very* simple Static site generator.

It takes a file structure, and copies it. If any of the file are .md convert them to .html files. uses jinja2 templates

## To use
1. Make sure dependancies are installed
2. Write content and place it in the correct file structure
3. Make sure to place correctly named templates in \_\_templates\_\_
4. Run Generator.py

## Dependancies
- [Python-Frontmatter](https://pypi.org/project/python-frontmatter/)
- [Markdown2](https://pypi.org/project/markdown2/)
- [Click](https://pypi.org/project/click/)
- [Jinja2](https://pypi.org/project/Jinja2/)

## Options
- -s or --source: The root directory containing all resources (default is current directory)
- -t or --target: The place to put the output (default is current directory)
- -d/-D or --dither/--no-Dither: Enable/disable dithering of PNG files (default is true)  NOTE: Not implimented yet
- -m/-M or --markdown/--no-Markdown: Enable/disable copying the .md files to the output (default is false)
