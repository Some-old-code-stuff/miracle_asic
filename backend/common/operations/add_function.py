# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db.migrations import RunSQL
from pathlib import Path


class AddFunction(RunSQL):
    def __init__(self, sql_file, reverse_sql_file):
        file_path = os.path.join(settings.BASE_DIR, 'sql', sql_file + '.sql')
        sql_statement = Path(file_path).read_text()
        file_path = os.path.join(settings.BASE_DIR, 'sql', reverse_sql_file + '.sql')
        reverse_sql_statement = Path(file_path).read_text()

        super().__init__(sql_statement, reverse_sql_statement)

    def describe(self):
        # This is used to describe what the operation does in console output.
        return "add sql function from file"
