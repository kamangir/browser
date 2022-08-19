from django.shortcuts import render
from abcli import fullname
from abcli.plugins.cache import functions
from abcli.plugins import relations
from abcli import string
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def add_urls(description, object=""):
    for keyword in "object,⬆️".split(","):
        if keyword in description:
            description[keyword] = ", ".join(
                [
                    f'<a href="/object/{item}">{item}</a>'
                    for item in description[keyword].split(",")
                    if item
                ]
            )

    for keyword in "data,dataset,model,parent,source,video_id".split(","):
        if keyword in description:
            description[keyword] = ", ".join(
                [
                    f'<a href="/object/{item}">{item}</a>'
                    for item in description[keyword].split(",")
                    if item
                ]
            )

    for keyword in "video,json".split(","):
        if keyword in description:
            description[keyword] = ", ".join(
                [
                    f'<a href="/object/{object}/{item}">{item}</a>'
                    for item in description[keyword].split(",")
                    if item
                ]
            )

    for keyword in "model_code".split(","):
        if keyword in description:
            description[keyword] = '<a href="/release/{}">{}</a>'.format(
                description[keyword], description[keyword]
            )

    for keyword in "tags,object tags".split(","):
        if keyword in description:
            description[keyword] = " | ".join(
                [f'<a href="/tag/{tag}">{tag}</a>' for tag in description[keyword]]
            )

    for keyword in "type,tag".split(","):
        if keyword in description:
            description[keyword] = '<a href="/tag/{}">{}</a>'.format(
                description[keyword], description[keyword]
            )

    for keyword in "class_names".split(","):
        if keyword in description:
            description[keyword] = "/".join(string.shorten(description[keyword]))

    for keyword in [thing.replace("-", " ") for thing in relations.list_of]:
        if keyword in description:
            description[keyword] = ", ".join(
                [
                    f'<a href="/object/{thing}">{thing}</a>'
                    for thing in description[keyword]
                ]
            )

    return description
