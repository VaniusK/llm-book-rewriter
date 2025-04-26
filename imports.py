import os
from google import genai
import time
from abc import ABC, abstractmethod
from google.genai import types as genai_types
from lxml import etree
import re
import yaml
import importlib
from typing import List, Dict
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import zipfile
import shutil