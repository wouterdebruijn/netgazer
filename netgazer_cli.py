#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netgazer.settings')
    try:
        from django import setup
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    setup()

    from netgazer import management

    commands = {
        'list_devices': management.list_devices
    }

    if len(sys.argv) < 2:
        print("Usage: netgazer_cli.py <command>")
        sys.exit(1)

    command = sys.argv[1]
    if command not in commands:
        print(f"Command '{command}' not found")
        sys.exit(1)

    commands[command]()


if __name__ == '__main__':
    main()
