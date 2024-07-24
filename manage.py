#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

if __name__ == "__main__":
    # Default to development settings for local development
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiki.settings.development')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
