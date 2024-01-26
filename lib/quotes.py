import tinkoff.invest as ti
import pandas as pd
import id.basek
import id.accid
import os
from pathlib import Path

class Quotes():
    def __init__(self, token, id):
        self.token = token
        self.id = id