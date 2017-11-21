#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(sys.path[0])
    sys.path.insert(0, BASE_DIR)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apolo.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
