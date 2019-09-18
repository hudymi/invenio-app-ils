# -*- coding: utf-8 -*-
#
# Copyright (C) 2018-2019 CERN.
#
# invenio-app-ils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resolve the Document referenced in the DocumentRequest."""

import jsonresolver
from werkzeug.routing import Rule

from ...api import Document, DocumentRequest
from ..resolver import get_field_value_for_record as get_field_value

# Note: there must be only one resolver per file,
# otherwise only the last one is registered


@jsonresolver.hookimpl
def jsonresolver_loader(url_map):
    """Resolve the referred Document for an DocumentRequest record."""
    from flask import current_app

    def get_document(document_pid):
        """Return the Document record."""
        document = Document.get_record_by_pid(document_pid)
        authors = []
        for author in document.get("authors", []):
            if "full_name" in author:
                authors.append(author["full_name"])
        return {
            "pid": document.get("pid"),
            "title": document.get("title", {}).get("title", ""),
            "authors": authors,
        }

    def document_resolver(document_request_pid):
        """Get the Document record for the given DocumentRequest or raise."""
        try:
            document_pid = get_field_value(
                DocumentRequest,
                document_request_pid,
                "document_pid"
            )
            if not document_pid:
                return {}
            return get_document(document_pid)
        except KeyError:
            return {}

    url_map.add(
        Rule(
            "/api/resolver/document-requests/<document_request_pid>/document",
            endpoint=document_resolver,
            host=current_app.config.get("JSONSCHEMAS_HOST"),
        )
    )
