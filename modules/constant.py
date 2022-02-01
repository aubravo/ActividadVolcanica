"""----------------------------------------------------------------------------
This is the core of the parsing stage:
    *re_find comments will search for everything between the $$ and EOL

    *re_findDataLabels will search for everything between the start of a tag
    (##) and the start of the next tag ignoring the contents of next tag,
    while grouping into tag name and tag contents
----------------------------------------------------------------------------"""
re_findComments = r'\$\$[\s\S]*?(?=\n)'
re_findBlocks = r'(##TITLE\=[\W\w]*?##END=)'
re_findDataLabels = r'##([\w\W]*?)=([\w\W]*?(?=\n##[\w\W]))'
FILE = True
DIR = False
