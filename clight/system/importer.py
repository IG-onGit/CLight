import os
import sys

__path__ = os.path.dirname(os.path.realpath(__file__))
sys.pycache_prefix = __path__ + "/__pycache__"

import re
import time
import json
import yaml
import string
import random

sys.stdout = open(os.devnull, "w")
sys.stderr = open(os.devnull, "w")
import pygame

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

import signal
import shutil
import base64
import ctypes
import pyttsx3
import hashlib
import pkgutil
import builtins
import inquirer
import datetime
import platform
import sysconfig
import importlib
import subprocess
from colored import fg, bg, attr
import speech_recognition as speech
from cryptography.fernet import Fernet
from clight.system.modules.cli import cli
