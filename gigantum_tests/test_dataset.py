# Builtin imports
import logging
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Local packages
import testutils


def test_dataset(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that dataset is created and linked successfully.

    Args:
        driver
    """
    # dataset set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    testutils.create_dataset(driver)
    time.sleep(2)
    testutils.publish_dataset(driver)
    time.sleep(5)

    # clean up datasets local and remote








