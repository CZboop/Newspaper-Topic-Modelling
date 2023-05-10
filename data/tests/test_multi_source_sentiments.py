import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
import src
from src.multi_source_sentiments import SentimentGetter
import os
import glob
from pathlib import Path
import pandas as pd
import shutil

class TestMultiSourceModeller(unittest.TestCase):

    maxDiff = None

if __name__ == "__main__":
    unittest.main()