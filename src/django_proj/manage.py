#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import secrets
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_proj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def gen_token():
    with open('main_app/telegram_bot/token.txt', 'w') as file:
        file.write(str(secrets.token_bytes()))


if __name__ == '__main__':
    gen_token()
    main()

