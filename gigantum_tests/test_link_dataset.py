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


def test_published_dataset_link(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that published dataset is linked to a project and the project is published successfully.

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
    dataset_title_local = testutils.create_dataset(driver)
    testutils.publish_dataset(driver)
    # check published dataset in the cloud
    time.sleep(3)
    dataset_title_cloud = driver.find_element_by_css_selector(".RemoteDatasets__panel-title:first-child span span").text

    assert dataset_title_local == dataset_title_cloud, "Expected dataset to be the first one in cloud tab"

    # Project set up
    driver.find_element_by_css_selector(".SideBar__nav-item--labbooks").click()
    project_title_local = testutils.create_project_without_base(driver)
    # Python 3 minimal base
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Link the dataset
    testutils.link_dataset(driver)
    linked_dataset_title = driver.find_element_by_css_selector(".DatasetBrowser__name").text

    assert linked_dataset_title == dataset_title_local, "Expected dataset linked to project"

    # Publish the project with dataset linked
    testutils.publish_project(driver)
    project_title_cloud = driver.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text
    assert project_title_local == project_title_cloud, "Expected project to be the first project in the cloud tab"

    # Delete project from cloud
    testutils.delete_project_cloud(driver, project_title_local)

    project_title_cloud = driver.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text
    assert project_title_cloud != project_title_local, "Expected project no longer the first one in cloud tab"

    # Delete dataset from cloud
    testutils.delete_dataset_cloud(driver, dataset_title_local)
    dataset_title_cloud = driver.find_element_by_css_selector(".RemoteDatasets__panel-title:first-child span span").text

    assert dataset_title_local != dataset_title_cloud, "Expected dataset no longer the first one in cloud tab"


def test_unpublished_dataset_link(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that unpublished dataset is linked to a project and the project is published successfully.

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
    dataset_title_local = testutils.create_dataset(driver)

    # Project set up
    driver.find_element_by_css_selector(".SideBar__nav-item--labbooks").click()
    project_title_local = testutils.create_project_without_base(driver)
    # Python 3 minimal base
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Link the dataset
    testutils.link_dataset(driver)
    linked_dataset_title = driver.find_element_by_css_selector(".DatasetBrowser__name").text

    assert linked_dataset_title == dataset_title_local, "Expected dataset linked to project"

    # Publish the project with dataset linked
    logging.info("Publishing project with local dataset")
    publish_elts = testutils.PublishProjectElements(driver)
    publish_elts.publish_project_button.click()
    publish_elts.publish_continue_button.click()
    time.sleep(3)
    publish_elts.publish_private_project_button.click()
    publish_elts.publish_private_dataset_button.click()
    publish_elts.publish_all_button.click()
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".PublishDatasetsModal")))
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    time.sleep(5)
    side_bar_elts = testutils.SideBarElements(driver)
    side_bar_elts.projects_icon.click()
    publish_elts.cloud_tab.click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))

    project_title_cloud = driver.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text
    assert project_title_local == project_title_cloud, "Expected project to be the first project in the cloud tab"

    # Delete project from cloud
    testutils.delete_project_cloud(driver, project_title_local)
    project_title_cloud = driver.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text
    assert project_title_cloud != project_title_local, "Expected project no longer the first one in cloud tab"

    # Delete dataset from cloud
    testutils.delete_dataset_cloud(driver, dataset_title_local)
    dataset_title_cloud = driver.find_element_by_css_selector(".RemoteDatasets__panel-title:first-child span span").text

    assert dataset_title_local != dataset_title_cloud, "Expected dataset no longer the first one in cloud tab"


def test_published_dataset_link_sync(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that published dataset is linked to a project and the project is published successfully.

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
    dataset_title_local = testutils.create_dataset(driver)
    testutils.publish_dataset(driver)
    # check published dataset in the cloud
    time.sleep(3)
    dataset_title_cloud = driver.find_element_by_css_selector(".RemoteDatasets__panel-title:first-child span span").text

    assert dataset_title_local == dataset_title_cloud, "Expected dataset to be the first one in cloud tab"

    # Project set up
    driver.find_element_by_css_selector(".SideBar__nav-item--labbooks").click()
    project_title_local = testutils.create_project_without_base(driver)
    # Python 3 minimal base
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # Publish the project itself
    testutils.publish_project(driver)
    project_title_cloud = driver.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text
    assert project_title_local == project_title_cloud, "Expected project to be the first project in the cloud tab"

    # Link the dataset and sync
    testutils.link_dataset(driver)
    linked_dataset_title = driver.find_element_by_css_selector(".DatasetBrowser__name").text
    assert linked_dataset_title == dataset_title_local, "Expected dataset linked to project"
    driver.find_element_by_css_selector(".BranchMenu__btn--sync--upToDate").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Delete project from cloud
    testutils.delete_project_cloud(driver, project_title_local)

    project_title_cloud = driver.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text
    assert project_title_cloud != project_title_local, "Expected project no longer the first one in cloud tab"

    # Delete dataset from cloud
    testutils.delete_dataset_cloud(driver, dataset_title_local)
    dataset_title_cloud = driver.find_element_by_css_selector(".RemoteDatasets__panel-title:first-child span span").text

    assert dataset_title_local != dataset_title_cloud, "Expected dataset no longer the first one in cloud tab"



