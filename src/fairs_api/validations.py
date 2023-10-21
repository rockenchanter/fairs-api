import json
import functools
import datetime
import regex as re  # better unicode support
from os import path

email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
digit_regex = re.compile(r"\d")
upc_letter = re.compile(r"[\p{Lu}\p{Mark}]")

file_path = path.join(path.dirname(path.abspath(__file__)), "locale.json")
with open(file_path, "r") as f:
    data = json.load(f)


def required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args[0] is None or (isinstance(args[0], str) and len(args[0]) == 0):
            return ("required",)
        return func(*args, **kwargs)
    return wrapper


def get_from_locale(key: str, locale: str):
    return data[locale][key]


@required
def contains(text: str, regex: re.Pattern, locale_key: str):
    if not re.search(regex, text):
        return [locale_key,]


@required
def min_length(text: str, target: int):
    if len(text) < target:
        return ["too_short", target]
    return None


@required
def max_length(text: str, target: int):
    if len(text) > target:
        return ["too_long", target]
    return None


@required
def min(value: float, target: float):
    if value < target:
        return ["too_small", target]
    return None


@required
def max(value: float, target: float):
    if value > target:
        return ["too_big", target]
    return None


@required
def email(value):
    if not re.fullmatch(email_regex, value):
        return ["invalid_email"]
    return None


@required
def days_from_now(date: datetime.date, target: int):
    min_date = datetime.timedelta(days=target) + datetime.date.today()
    if not date:
        return ["incorrect_date"]
    elif date < min_date:
        return ["min_date", target]
    return None


def min_children(arr: list, target: int):
    if len(arr) < target:
        return ["min_children", target]
    return None


def max_children(arr: list, target: int):
    if len(arr) > target:
        return ["max_children", target]
    return None
