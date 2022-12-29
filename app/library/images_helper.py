import os
import re

from typing import Union
from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet(
    "images", IMAGES
)  # "images" must be same as IMAGE_DESTINATION in 'default_config.py


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """
    save the 'image' in the 'folder' with the given 'name'
    """
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """ "
    return the full path of 'filename' from the 'folder'
    """
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str = None, folder: str = None) -> Union[str, None]:
    """
    return the 'filename' from the 'folder' of any accpted extension from IMAGE
    """
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = get_path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """
    return the path/filename.extension of 'file'
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """
    check for the valid path/filename.extension
    """
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"

    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    """
    return filename.extension of the 'file'(path/filename.extension)
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    """
    return the .extenison of the 'file'(path/filename.extension)
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
