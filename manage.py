#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    env = os.getenv('ATMATR_ENVIRONMENT') or 'dev'
    if env not in ('dev', 'test', 'staging', 'prod'):
        env = 'dev'
    elif env == 'staging':
        env = 'prod'
    os.environ.setdefault("ATMATR_ENVIRONMENT", env)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atmatr.settings.%s" % env)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
