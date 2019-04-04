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


def test_link_dataset(driver: selenium.webdriver, *args, **kwargs):
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
    dataset_title = testutils.create_dataset(driver)

    # Project set up
    driver.find_element_by_css_selector(".SideBar__nav-item--labbooks").click()
    project_title = testutils.create_project_without_base(driver)
    # Python 3 minimal base
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Link the dataset
    logging.info("Linking the dataset to project")
    driver.find_element_by_css_selector(".Navigation__list-item--inputData").click()
    driver.find_element_by_css_selector(".FileBrowser__button--add-dataset").click()
    driver.find_element_by_css_selector(".LinkCard__details").click()
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".Footer__message-title")))
    driver.find_element_by_css_selector(".ButtonLoader ").click()
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".LinkModal__container")))
    linked_dataset_title = driver.find_element_by_css_selector(".DatasetBrowser__name").text

    assert linked_dataset_title == dataset_title, "Expected dataset linked to project"

    # Publish the project with dataset linked
    logging.info("Publishing project")
    publish_elts = testutils.PublishProjectElements(driver)
    publish_elts.publish_project_button.click()
    publish_elts.publish_confirm_button.click()
    time.sleep(5)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    time.sleep(5)
    side_bar_elts = testutils.SideBarElements(driver)
    side_bar_elts.projects_icon.click()
    publish_elts.cloud_tab.click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))

    cloud_tab_first_project_title_publish = driver.find_element_by_css_selector(
        ".RemoteLabbooks__panel-title:first-child span span").text
    assert cloud_tab_first_project_title_publish == project_title, \
        "Expected project to be the first project in the cloud tab"
