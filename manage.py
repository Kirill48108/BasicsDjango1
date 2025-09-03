import os
import sys
from typing import Final, Sequence

DJANGO_SETTINGS_ENV_VAR: Final[str] = "DJANGO_SETTINGS_MODULE"
DEFAULT_SETTINGS_MODULE: Final[str] = "config.settings"
DJANGO_IMPORT_ERROR_MESSAGE: Final[str] = (
    "Couldn't import Django. Are you sure it's installed and available on your "
    "PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
)

Argv = Sequence[str]


def configure_django(settings_module: str = DEFAULT_SETTINGS_MODULE) -> None:
    """Ensure the Django settings module is configured via environment."""
    os.environ.setdefault(DJANGO_SETTINGS_ENV_VAR, settings_module)


def main(argv: Argv | None = None) -> None:
    """Entrypoint for Django administrative tasks."""
    configure_django()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(DJANGO_IMPORT_ERROR_MESSAGE) from exc

    args = argv or sys.argv
    execute_from_command_line(args)


if __name__ == "__main__":
    main()
