import abcli
from abcli.plugins import tags
from browser import ITEM_PER_PAGE as ITEM_PER_PAGE_
from browser import html
from browser.utils import *
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def view_tag(request, tag):
    try:
        ITEM_PER_PAGE = int(request.GET.get("count", str(ITEM_PER_PAGE_)))
        page = int(request.GET.get("page", str(1)))
    except:
        pass

    list_of_objects = [object for object in tags.search(tag)[::-1] if object]
    logger.info(f"{len(list_of_objects):,} object(s) found.")

    object_count = len(list_of_objects)

    list_of_objects = list_of_objects[(page - 1) * ITEM_PER_PAGE : page * ITEM_PER_PAGE]

    return render(
        request,
        "grid.html",
        {
            "abcli_fullname": abcli.fullname(),
            "description": add_urls(
                {
                    "page": html.add_navigation(
                        f"/tag/{tag}",
                        page,
                        int(object_count / ITEM_PER_PAGE) + 1,
                    ),
                    "tag": tag,
                    "# object(s)": f"{object_count:,}",
                }
            ),
            "title_postfix": " | ".join(["tag", tag]),
            "items_n_urls": zip(
                [
                    html.add_cloud_image_("folder.png", prefix="../")
                    for _ in list_of_objects
                ],
                [f"/object/{object}" for object in list_of_objects],
            ),
        },
    )
