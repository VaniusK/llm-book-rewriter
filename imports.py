import os
from google import genai
import time
from abc import ABC, abstractmethod
from google.genai import types as genai_types
from lxml import etree
import re
import yaml
import importlib
from typing import List, Dict, Tuple
import docx
