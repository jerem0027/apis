#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server.instance import server
from werkzeug.datastructures import FileStorage

api = server.api

# Upload DAT file
upload_file = api.parser()
upload_file.add_argument('file', location='files', type=FileStorage, required=True)
doc_file = {"file": "Documentation fichier (peut contenir de l'HTML)"}
