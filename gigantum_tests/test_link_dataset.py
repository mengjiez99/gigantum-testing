# Builtin imports
import logging
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
import testutils


def link_then_publish(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that dataset is linked to a project and the project is published successfully.

    Args:
        driver
    """
    # create a dataset
    # dataset set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    # create and publish datset
    testutils.create_dataset(driver)

    # Project set up
    driver.find_element_by_css_selector(".SideBar__nav-item--labbooks").click()
    testutils.create_project_without_base(driver)
    # Python 3 minimal base
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Link the dataset and publish project
    driver.find_element_by_css_selector(".Navigation__list-item--inputData").click()
    driver.find_element_by_css_selector(".FileBrowser__button--add-dataset").click()
    driver.find_element_by_css_selector(".LinkCard__details").click()
    driver.find_element_by_css_selector(".ButtonLoader ").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".DatasetBrowser__row")))
    driver.find_element_by_css_selector(".BranchMenu__btn--sync--publish").click()






