# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# invenio-app-ils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resolve the Tag referenced in the Series."""

import jsonresolver
from werkzeug.routing import Rule

from ...api import Series, Tag
from ..resolver import get_field_value_for_record as get_field_value

# Note: there must be only one resolver per file,
# otherwise only the last one is registered


@jsonresolver.hookimpl
def jsonresolver_loader(url_map):
    """Resolve the referred Tags for a Series record."""
    from flask import current_app

    def tags_resolver(series_pid):
        """Return the Tag records for the given Tag or raise."""
        tag_pids = get_field_value(Series, series_pid, "tag_pids")

        tags = []
        for tag_pid in tag_pids:
            tag = Tag.get_record_by_pid(tag_pid)
            del tag["$schema"]

            tags.append(tag)

        return tags

    url_map.add(
        Rule(
            "/api/resolver/series/<series_pid>/tags",
            endpoint=tags_resolver,
            host=current_app.config.get("JSONSCHEMAS_HOST"),
        )
    )