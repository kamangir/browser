import os.path
from abcli import fullname
from abcli import file
from abcli.plugins import cache
from abcli.plugins import tags
from abcli.plugins import relations
from abcli.plugins.storage import instance as storage
from abcli.plugins.storage import object_prefix
from . import html
from .constants import *
from .utils import *
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def view_object(request, object_path):
    object_name = object_path.split("/")[0]
    logger.info(f"browser.view_object({object_path})")

    is_single_object = storage.exists(object_path)

    content = (
        [object_path]
        if is_single_object
        else [
            os.path.join(object_path, thing)
            for thing in storage.list_of_objects(
                prefix=f"{object_path}/"
                if not object_path.endswith("/")
                else object_path,
                include_folders=True,
                count=int(request.GET.get("count", str(ITEM_PER_PAGE))),
            )
        ]
    )

    description = {
        "object": object_name,
        "# things": len(content),
    }

    if "/" in object_path:
        description["⬆️"] = "/".join(object_path.split("/")[:-1])

    description.update(
        {
            keyword.replace("-", " "): value
            for keyword, value in relations.search(object_name).items()
        }
    )

    description.update(
        {
            string.after(keyword, f"{object_name}."): value
            for keyword, value in cache.search(f"{object_name}.%").items()
        }
    )

    list_of_tags = tags.get(object_name)
    description.update({"tags": list_of_tags})

    def thing_is_log(thing):
        thing = thing.split("/")
        return False if len(thing) != 2 else thing[0] == thing[1]

    items = []
    urls = []
    for thing in content:
        prefix = "/".join(
            (2 + len([char for char in thing if char == "/"])) * [".."] + [""]
        )
        items += (
            [
                html.add_cloud_image(
                    f"{object_prefix}/{thing}",
                    prefix=prefix,
                    width="100%" if is_single_object else html.default_image_width,
                )
            ]
            if file.extension(thing) in "jpg,png,jpeg".split(",")
            else [
                html.add_cloud_image_(
                    "log.png"
                    if thing_is_log(thing)
                    else "json.png"
                    if thing.endswith(".json")
                    else "numpy.png"
                    if thing.endswith(".pyndarray")
                    else "folder.png",
                    prefix=prefix,
                    width="100%" if is_single_object else html.default_image_width,
                )
            ]
        )

        storage.download_file(
            f"{object_prefix}/{thing}",
            filename="static",
            civilized=True,
        )

        urls += (
            [
                "http://127.0.0.1:8000/static/{}".format(
                    f"{object_prefix}/{thing}".replace("/", "-")
                )
            ]
            if is_single_object
            or thing_is_log(thing)
            or file.extension(thing) in "json,pyndarray".split(",")
            else [f"/object/{thing}"]
        )

    return render(
        request,
        "item.html" if is_single_object else "grid.html",
        {
            "abcli_fullname": fullname(),
            "title_postfix": " | ".join(object_path.split("/")),
            "description": add_urls(description, object_name),
            "items_n_urls": zip(items, urls),
            "content": " ".join(
                [f'<a href="{url}">{item}</a>' for item, url in zip(items, urls)]
            ),
            "autorefresh": int(
                request.GET.get("autorefresh", str(AUTO_REFRESH_SECONDS))
                if "open" in list_of_tags
                else "9999999"
            ),
        },
    )
