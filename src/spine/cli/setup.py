"""
.. module:: setup
    :platform: Unix, Windows
    :synopsis: Command Line Interface (CLI) setup functions
"""

# Python Standard Libraries
import argparse
from collections import OrderedDict
import json
import logging
import os

# 3rd Party Libraries


# Project Specific Libraries
from spine.fobj.find_obj import check

LOGGER = logging.getLogger(__name__)


# TODO Add support for parents https://docs.python.org/3/library/argparse.html#parents


def build(path: str = None, arg_dict: dict = None) -> argparse.ArgumentParser:
    """Build an argparse.ArgumentParser object from json config file or dict

    Args:
        path (str, Optional): Path to the foncif file, defaults to None

        arg_dict (dict, Optional): Arg config in dictionary format, defaults
        to None

    Raises:
        AttributeError: If path is invalid/empty and arg_dict is None

        FileNotFoundError: If file path does not exist

        TypeError: If file is not properly formatted

        TypeError: If arg_dict is not dict type

    Returns:
        argparse.ArgumentParser
    """
    LOGGER.debug(
        "Checking/retrieving argparse configuration",
        extra={"path": path, "arg_dict_empty": arg_dict is None},
    )

    if path is not None:
        if not check(*os.path.split(path)):
            raise FileNotFoundError(f"Arg config path {path} not found")

        # TODO Add support for other file formats (YAML, INI/TOML)
        with open(path, "r") as f:
            config = json.load(f)

        # config = load_file.load(*os.path.split(path))
    else:
        config = arg_dict

    if config is None:
        raise AttributeError("Valid path or arg_dict value must be provided")
    elif not isinstance(config, (dict, OrderedDict)):
        raise TypeError(
            f"Invalid type of {type(config)} for path"
            " content or arg_dict value",
        )

    parser_obj = argparse.ArgumentParser(
        description=config.get("description", None)
    )

    LOGGER.debug("Start processing configuration")

    __process_config(parser_obj, config)

    LOGGER.debug("Finished processing configuration")

    return parser_obj


def __add_argument(parser_obj: object, **kwargs):
    """Add an argument to parser object

    Args:
        parser_obj (object): Parser object to add argument

        kwargs (dict): Dictionary of values to pass into new argument
    """
    name = kwargs.pop("name", None)
    flag = kwargs.pop("flag", None)

    if name is not None and flag is not None:
        parser_obj.add_argument(name, flag, **kwargs)
    else:
        parser_obj.add_argument(name or flag, **kwargs)


def __process_group_arguments(parser_obj: object, config: dict):
    """Process arguments for a group

    Args:
        parser_obj (object): Parser object to add items

        arg_list (list): List of arguments to process
    """
    LOGGER.debug("Argument type is group, creating")

    group = parser_obj.add_mutually_exclusive_group()

    for arg_item in config.get("arguments", []):
        __add_argument(group, **arg_item)


def __process_arguments(parser_obj: object, arg_list: list):
    """Process arguments

    Args:
        parser_obj (object): Parser object to add items

        arg_list (list): List of arguments to process
    """
    LOGGER.debug(f"Processing {len(arg_list)} arguments")

    for item in arg_list:
        item_type = item.pop("type", "argument")

        if item_type == "group":
            __process_group_arguments(parser_obj, item)
        elif item_type in ["argument", "str", "int"]:
            __add_argument(parser_obj, **item)


def __process_subparsers(parser_obj: object, config: dict):
    """Process subparser configuration

    Args:
        parser_obj (object): Parser object to add items

        config (dict): Dictionary of configuration
    """
    subparser_obj = parser_obj.add_subparsers()

    for item in config.get("subparsers", []):
        sub_parser = subparser_obj.add_parser(
            item.get("command"), help=item.get("help", None)
        )

        __process_config(sub_parser, item)


def __process_config(parser_obj: object, config: dict):
    """Process subparser configuration

    Args:
        parser_obj (object): Parser object to add items

        config (dict): Dictionary of configuration
    """
    if "subparsers" in config.keys():
        LOGGER.debug("subparsers key found in config, processing")

        __process_subparsers(parser_obj, config)

    __process_arguments(parser_obj, config.get("arguments", []))

    if "defaults" in config.keys():
        LOGGER.debug("defaults key found in config, setting")

        parser_obj.set_defaults(**config.get("defaults", {}))
