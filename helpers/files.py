from pathlib import Path
from typing import Union


def create_dir_if_not_exists(path: Union[Path, str]):
    """
    Provide the path to create, either folder- or file- path
    :param path:
    :return:
    """

    path = Path(path)
    if path.name.find(".") != -1:
        path = path.parent
    if not Path(path).exists():
        path.mkdir(parents=True)
