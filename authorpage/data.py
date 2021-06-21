#
# data.py
#
# scp-author-page - Tools for generating my author page.
# Copyright (c) 2021 Ammon Smith
#
# scp-author-page is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

import re

import toml

from .wikidot import normalize

SCP_NAME_REGEX = re.compile(r"SCP-[1-9]?[0-9]{3}(?:-(?:J|EX))?")


def load_data(data_path: str) -> dict:
    with open(data_path) as file:
        data = toml.load(file)

    # Hydrate data according to structures
    for article in data["articles"]:
        name = article["name"]

        if "type" not in article:
            if SCP_NAME_REGEX.match(name):
                article["type"] = "scp"
            else:
                raise ValueError(f"No article type specified for '{name}'")

        if article["type"] == "goi-format":
            if "goi" not in article:
                raise ValueError(f"No GoI specified for goi-format document '{name}'")

        if "slug" not in article:
            article["slug"] = normalize(name)
            article["normal-slug"] = True

        if "title" not in article:
            article["title"] = name

        if "co-authors" not in article:
            article["co-authors"] = []

        if "contest" not in article:
            article["contest"] = None

        # Add snake_case version of kebab-case keys
        for key, value in tuple(article.items()):
            if "-" in key:
                snake_key = key.replace("-", "_")
                article[snake_key] = value

    return data
