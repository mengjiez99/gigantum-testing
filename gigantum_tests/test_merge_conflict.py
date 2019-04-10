# Builtin imports
import logging
import time
import os
import shutil
from subprocess import Popen, PIPE

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
import testutils

def test_merge_conflict_project(driver: selenium.webdriver, *args, **kwargs):
    """
        Test that merge conflict is handled correctly.

        Args:
            driver
    """

