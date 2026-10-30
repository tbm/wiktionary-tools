# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Various cleanups
"""

__license__ = "GPL-3.0-or-later"

import re

import mwparserfromhell

_NUMBERED_PARAM = re.compile(r"^(.+?)(\d+)$")


# Templates that don't support inline parameter syntax.
SKIP_TEMPLATES = {
    "&lit",
}


def convert_inline_params(text):
    """
    Convert templates to inline parameters, e.g.
    {{<af|sw|foo|alt1=-foo>}} to {{af|sw|foo<alt:-foo>}}"
    """
    code = mwparserfromhell.parse(text)

    for template in code.filter_templates(recursive=True):
        template_name = str(template.name).strip()

        if template_name in SKIP_TEMPLATES:
            continue

        positional = [param for param in template.params if not param.showkey]

        if len(positional) < 2:
            continue

        additions = {}
        remove = []

        for param in template.params:
            if not param.showkey:
                continue

            name = str(param.name).strip()
            value = str(param.value).strip()

            match = _NUMBERED_PARAM.fullmatch(name)

            if match:
                prefix, number = match.groups()
                number = int(number)
            else:
                continue

            # foo1 -> positional[1]
            # foo2 -> positional[2]
            if number >= len(positional):
                continue

            # gloss -> t
            if prefix == "gloss":
                prefix = "t"

            additions.setdefault(number, []).append(f"<{prefix}:{value}>")
            remove.append(param)

        for index, inline in additions.items():
            positional[index].value = str(positional[index].value).rstrip() + "".join(
                inline
            )

        for param in remove:
            template.remove(param)

    return str(code)
