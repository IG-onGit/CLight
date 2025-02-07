import os
import sys

__path__ = os.path.dirname(os.path.realpath(__file__))
sys.pycache_prefix = __path__ + "/__pycache__"

import re
import json
import signal
import shutil
import base64
import ctypes
import hashlib
import pkgutil
import builtins
import inquirer
import datetime
import platform
import sysconfig
import importlib
import subprocess
from colored import fg, bg, attr  # pip
from cryptography.fernet import Fernet
from clight.system.modules.cli import cli
