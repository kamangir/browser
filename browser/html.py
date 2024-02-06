import cv2
import os
import os.path
from abcli import file
from abcli.plugins.storage import instance as storage
from abcli.path import abcli_object_root
from abcli import string
from abcli import logging
import logging

logger = logging.getLogger(__name__)

abcli_path_static = os.getenv("abcli_path_static", "")

default_image_width = "16%"


def add_cloud_image(
    object_name,
    alternative="",
    overwrite=False,
    thumbnail=False,
    upload_thumbnail=False,
    **kwargs,
):
    """add cloud image to web page.

    Args:
        object_name (str): object name.
        alternative (str, optional): alternative. Defaults to "". "object_name" uses object_name.
        overwrite (bool, optional): overwrite. Defaults to False.
        thumbnail (bool, optional): use thumbnail. Defaults to False.
        upload_thumbnail (bool, optional): upload the thumbnail, if had to create it. Defaults to True.

    Returns:
        bool: success.
    """
    if alternative == "object_name":
        alternative = object_name

    logger.info(f"html.add_cloud_image({object_name})")

    if "void" in object_name:
        return add_cloud_image_("", **kwargs)

    create_thumbnail = False
    object_thumbnail_name = file.add_postfix(object_name, "thumbnail")
    if thumbnail:
        if storage.download_file(
            object_name=object_thumbnail_name,
            filename="static",
            civilized=True,
            overwrite=overwrite,
        ):
            return add_cloud_image_(object_thumbnail_name, **kwargs)
        else:
            logger.info(f"{object_name}: thumbnail not found, will create.")
            create_thumbnail = True

    if storage.download_file(
        object_name=object_name,
        filename="static",
        civilized=True,
        overwrite=overwrite,
    ):
        if create_thumbnail:
            logger.info(f"creating thumbnail for {object_name}.")

            success, image = file.load_image(
                os.path.join(abcli_path_static, object_name.replace("/", "-"))
            )

            if success:
                image = cv2.resize(
                    image,
                    dsize=(320, int(image.shape[0] / image.shape[1] * 320)),
                    interpolation=cv2.INTER_AREA,
                )

                success = file.save_image(
                    os.path.join(
                        abcli_path_static, object_thumbnail_name.replace("/", "-")
                    ),
                    image,
                )

            if success and upload_thumbnail:
                storage.upload_file(
                    os.path.join(
                        abcli_path_static, object_thumbnail_name.replace("/", "-")
                    ),
                    storage.bucket_name,
                    object_thumbnail_name,
                )

        return add_cloud_image_(
            object_thumbnail_name if create_thumbnail else object_name,
            **kwargs,
        )

    if alternative:
        object_name_ = object_name
        list_of_files = [
            thing
            for thing in sorted(
                storage.list_of_objects("/".join(alternative.split("/")[1:-1]))
            )
            if file.extension(thing) in "jpg,jpeg,png".split(",")
            and "thumbnail" not in file.name(thing)
        ]
        object_name = "/".join(
            alternative.split("/")[:-1] + [(list_of_files + ["void"])[0]]
        )
        logger.info(f"{object_name_} not found, switching to: {object_name}.")

        return add_cloud_image(
            object_name,
            alternative=False,
            overwrite=overwrite,
            thumbnail=thumbnail,
            **kwargs,
        )

    return add_cloud_image_("", **kwargs)


def add_cloud_image_(
    object_name,
    border=False,
    height="",
    prefix="",
    width=default_image_width,
):
    """add cloud image, internal version.

    Args:
        object_name (str): object name.
        border (bool, optional): add border. Defaults to False.
        height (str, optional): height. Defaults to "".
        prefix (str, optional): prefix. Defaults to "".
        width (str, optional): width. Defaults to default_image_width.

    Returns:
        bool: success.
    """

    logger.info(f"html.add_cloud_image_({object_name})")

    return '<img src="{}static/{}" {} {} {}>'.format(
        prefix,
        object_name.replace("/", "-"),
        f'width="{width}"' if width else "",
        f'height="{height}"' if height else "",
        'border="5"' if border else "",
    )


def add_local_image(
    filename,
    border=False,
    height="",
    prefix="",
    width=default_image_width,
):
    """add local image.

    Args:
        filename (str): filename.
        border (bool, optional): add border. Defaults to False.
        height (str, optional): height. Defaults to "".
        prefix (str, optional): prefix. Defaults to "".
        width (str, optional): width. Defaults to default_image_width.

    Returns:
        bool: success
    """
    logger.info(f"html.add_local_image({filename})")

    if "void" in filename:
        filename = ""

    image_filename = "void"
    if filename:
        if filename.startswith(abcli_path_static):
            image_filename = string.after(
                filename,
                abcli_path_static,
            )
        else:
            image_filename = string.after(
                filename,
                abcli_object_root,
            ).replace("/", "-")

            filename_ = os.path.join(
                abcli_path_static,
                image_filename,
            )

            if not file.copy(filename, filename_):
                return False

    logger.info(f"html.add_local_image({image_filename})")

    return '<img src="{}static/{}" {} {} {}>'.format(
        prefix,
        image_filename,
        f'width="{width}"' if width else "",
        f'height="{height}"' if height else "",
        'border="5"' if border else "",
    )


def add_navigation(prefix, page, page_count):
    return " ".join(
        [
            f'<a href="{prefix}">|<</a>' if page > 1 else "|<",
            f'<a href="{prefix}?page={page - 1}"><</a>' if page > 1 else "<",
            f"{page}/{page_count}",
            f'<a href="{prefix}?page={page + 1}">></a>' if page < page_count else ">",
            f'<a href="{prefix}?page={page_count}">>|</a>'
            if page < page_count
            else ">|",
        ]
    )
