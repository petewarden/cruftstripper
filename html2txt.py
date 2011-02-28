#!/usr/bin/env python

import sys, string
from BeautifulSoup import *

ignored_elements = {
    "script": True,
    "noscript": True,
    "form": True
}

inline_elements = {
    "b": True, 
    "big": True, 
    "i": True, 
    "small": True, 
    "tt": True,
    "abbr": True, 
    "acronym": True, 
    "cite": True, 
    "code": True, 
    "dfn": True, 
    "em": True, 
    "kbd": True, 
    "strong": True, 
    "samp": True, 
    "var": True,
    "a": True, 
    "bdo": True, 
    "br": True, 
    "img": True, 
    "map": True, 
    "object": True, 
    "q": True, 
    "script": True, 
    "span": True, 
    "sub": True, 
    "sup": True,
    "button": True, 
    "input": True, 
    "label": True, 
    "select": True, 
    "textarea": True
}

block_elements = {
    "p": True,
    "h1": True, 
    "h2": True, 
    "h3": True, 
    "h4": True, 
    "h5": True, 
    "h6": True,
    "ol": True, 
    "ul": True,
    "pre": True,
    "address": True,
    "blockquote": True,
    "dl": True,
    "div": True,
    "fieldset": True,
    "form": True,
    "hr": True,
    "noscript": True,
    "table": True,
    "li": True
}

def html2txt(element):

    result = ''

    anchor_length = 0
    for child in element.contents:
        myclass = child.__class__
        if myclass == NavigableString:
            result += child.string.replace("\n", " ")
        elif myclass == Comment or myclass == Declaration:
            continue
        else:
            name = child.name
            if name in ignored_elements:
                continue
            child_string = html2txt(child)
            if len(child_string) == 0:
                continue
            result += child_string

            if name == 'a':
                anchor_length += len(child_string)

            if name in block_elements:
                result += "\n"
    
    if len(result) > 0 and (anchor_length/float(len(result))) > 0.5:
        return ''
    
    return result

if __name__ == '__main__':
    html = sys.stdin.read()
    document = BeautifulSoup(html, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

    output = html2txt(document.body)

    print unicode(output).encode("utf-8")