from . import *
from browser.plugins.objects import *
from browser.plugins.tags import *
from browser.utils import *
from browser import html
from abcli.plugins.message.agent import instance as messenger
import abcli.logging
import logging

logger = logging.getLogger(__name__)

global home_content
home_content = {}  # {message.sender: (object_path, filename)}


def view_help(request):
    return render(
        request,
        "home.html",
        {
            "abcli_fullname": fullname(),
            "content": "<br/>".join(
                [
                    '<a href="/Kanata">Kanata</a>',
                    '<a href="/live">live</a>',
                    '<a href="/private">private</a>',
                ]
            ),
            "title_postfix": "help",
        },
    )


def view_home(request, *args, **kwargs):
    global home_content

    success, messages = messenger.request("stream")
    if success:
        home_content.update(
            {
                message.sender: (
                    "/".join(message.data.get("object_name", "").split("/")[1:]),
                    message.filename,
                )
                for message in messages
                if message.filename
            }
        )

    return render(
        request,
        "grid.html",
        {
            "abcli_fullname": fullname(),
            "autorefresh": int(request.GET.get("autorefresh", str(autorefresh))),
            "description": add_urls({}),
            "title_postfix": "home",
            "items_n_urls": zip(
                [
                    html.add_local_image(filename)
                    for _, filename in home_content.values()
                ],
                [f"/object/{url_postfix}" for url_postfix, _ in home_content.values()],
            ),
        },
    )
