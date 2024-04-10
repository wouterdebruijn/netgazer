#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Set loglevel according to environment variable
if os.environ.get('DEBUG', 'False').lower() == 'true':
    logging.getLogger().setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)

# Enable colored logging
logging.addLevelName(
    logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
logging.addLevelName(
    logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
logging.addLevelName(
    logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(
    logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(
    logging.CRITICAL, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))


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
    from discovery import discover

    commands = {
        'list_devices': management.list_devices,
        'discover': discover.discover,
    }

    if len(sys.argv) < 2:
        print("Usage: netgazer_cli.py <command>")
        sys.exit(1)

    command = sys.argv[1]
    if command not in commands:
        print(f"Command '{command}' not found")
        print(f"Available commands: {', '.join(commands.keys())}")
        sys.exit(1)

    commands[command]()


if __name__ == '__main__':
    main()
