# MatchFight/settings/__init__.py

import os

ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'local')

if ENVIRONMENT == 'prod':
    from .prod import *
else:
    from .local import *
