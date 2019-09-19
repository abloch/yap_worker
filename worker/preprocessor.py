#!/usr/bin/env python
import re
import json
import sys

REGEXES_TO_REMOVE = [
    re.compile(r'http[\w\.\/\:\?\&\=\-]*'),  # remove all links
    re.compile(r'pic\.twitter\.com[\w\/]*'),  # remove images
    re.compile(r'\#[\wא-ת]+'),  # remove hashtags
    re.compile(r'\(צילום.*'),  # remove photo credits
    re.compile(r'[^\w\sא-ת\:\-\"\,\.\@\(\)\;"]'),  # remove all non alphanumerics
]

WHITESPACE = re.compile(r"\s+")


def preprocess(string):
    for regex in REGEXES_TO_REMOVE:
        string = regex.sub(string=string, repl="")
    string.replace("\n", ".")
    return WHITESPACE.sub(string=string, repl=" ").strip()

