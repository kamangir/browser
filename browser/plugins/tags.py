from .. import *
from .. import item_per_page as item_per_page_
from .. import html
from ..utils import *
from abcli.plugins import tags
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def view_tag(request, tag):
    try:
        item_per_page = int(request.GET.get("count", str(item_per_page_)))
        page = int(request.GET.get("page", str(1)))
    except:
        pass

    list_of_objects = [object for object in tags.search(tag)[::-1] if object]
    logger.info(f"{len(list_of_objects):,} object(s) found.")

    object_count = len(list_of_objects)

    list_of_objects = list_of_objects[(page - 1) * item_per_page : page * item_per_page]

    return render(
        request,
        "grid.html",
        {
            "abcli_fullname": fullname(),
            "description": add_urls(
                {
                    "page": html.add_navigation(
                        f"/tag/{tag}",
                        page,
                        int(object_count / item_per_page) + 1,
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
