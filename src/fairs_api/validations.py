from flask import session

import json
import re

email_regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

with open("locale.json", "r") as f:
    data = json.load(f)


def get_from_locale(locale: str, key: str):
    return data[locale][key]


def min_length(text: str, target: int):
    if len(text) < target:
        return get_from_locale(session["locale"], "too_short")
    return None


def max_length(text: str, target: int):
    if len(text) > target:
        return get_from_locale(session["locale"], "too_long")
    return None


def min(value: float, target: float):
    if value < target:
        return get_from_locale(session["locale"], "too_small")
    return None


def max(value: float, target: float):
    if value > target:
        return get_from_locale(session["locale"], "too_big")
    return None


def email(value):
    if not re.fullmatch(email_regex, value):
        return get_from_locale(session["locale"], "invalid_email")
    return None
