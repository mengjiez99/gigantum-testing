# Builtin imports
import logging
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
from testutils import elements
from testutils import testutils



# create project
def log_in(driver: selenium.webdriver) -> str:
    """
    Log in to Gigantum.

    Args:
        driver

    Returns:
        Username of user just logged in
    """
    driver.get("http://localhost:10000/projects/local#")
    logging.info("Logging in")
    auth0_elts = elements.Auth0LoginElements(driver)
    auth0_elts.login_green_button.click()
    time.sleep(2)
    username,password = testutils.load_credentials()
    auth0_elts.username_input.click()
    auth0_elts.username_input.send_keys(username)
    auth0_elts.password_input.click()
    auth0_elts.password_input.send_keys(password)
    try:
        auth0_elts.login_grey_button.click()
    except:
        pass

    return username.strip()


def remove_guide(driver: selenium.webdriver):
    """
    Remove'Got it!', guide, and helper.

    Args:
        driver
    """
    logging.info("Getting rid of 'Got it!'")
    guide_elts = elements.GuideElements(driver)
    guide_elts.got_it_button.click()
    logging.info("Turning off guide and helper")
    guide_elts.guide_button.click()
    guide_elts.helper_button.click()


def create_project_without_base(driver: selenium.webdriver) -> str:
    """
    Create a project without a base.

    Args:
        driver
    
    Returns:
        Name of project just created
    """
    unique_project_name = testutils.unique_project_name()
    logging.info(f"Creating a new project: {unique_project_name}")
    project_elts = elements.AddProjectElements(driver)
    project_elts.create_new_button.click()
    project_elts.project_title_input.click()
    project_elts.project_title_input.send_keys(unique_project_name)
    project_elts.project_description_input.click()
    project_elts.project_description_input.send_keys(testutils.unique_project_description())
    project_elts.project_continue_button.click()
    return unique_project_name


# bases
def add_py2_min_base(driver: selenium.webdriver):
    """
    Add a Python2 Minimal base.

    Args:
        driver
    """
    logging.info("Creating new project with Python2 Minimal base")
    py2_base_elts = elements.AddProjectBaseElements(driver)
    try:
        py2_base_elts.py2_tab_button.click()
    except:
        pass
    while not py2_base_elts.py2_minimal_base_button.is_displayed():
        logging.info("Searching for Python2 Minimal base...")
        py2_base_elts.arrow_button.click()
    py2_base_elts.py2_minimal_base_button.click()
    py2_base_elts.create_project_button.click()


def add_py3_min_base(driver: selenium.webdriver):
    """
    Add a Python3 Minimal base.

    Args:
        driver
    """
    logging.info("Creating new project with Python3 Minimal base")
    py3_base_elts = elements.AddProjectBaseElements(driver)
    try:
        py3_base_elts.py3_tab_button.click()
    except:
        pass
    while not py3_base_elts.py3_minimal_base_button.is_displayed():
        logging.info("Searching for Python3 Minimal base...")
        py3_base_elts.arrow_button.click()
    py3_base_elts.py3_minimal_base_button.click()
    py3_base_elts.create_project_button.click()


def add_py3_ds_base(driver: selenium.webdriver):
    """
    Add a Python3 Data Science Quick-start base.

    Args:
        driver
    """
    logging.info("Creating new project with Python3 Data Science Quick-start base")
    py3_base_elts = elements.AddProjectBaseElements(driver)
    try:
        py3_base_elts.py3_tab_button.click()
    except:
        pass
    while not py3_base_elts.py3_minimal_base_button.is_displayed():
        logging.info("Searching for Python3 Data Science Quick-start base...")
        py3_base_elts.arrow_button.click()
    py3_base_elts.py3_data_science_base_button.click()
    py3_base_elts.create_project_button.click()


def add_rtidy_base(driver: selenium.webdriver):
    """
    Add a R Tidyverse base.

    Args:
        driver
    """
    logging.info("Creating new project with R Tidyverse base")
    r_base_elts = elements.AddProjectBaseElements(driver)
    try:
        r_base_elts.r_tab_button.click()
    except:
        pass
    while not r_base_elts.r_tidyverse_base_button.is_displayed():
        logging.info("Searching for R Tidyverse base...")
        r_base_elts.arrow_button.click()
    r_base_elts.r_tidyverse_base_button.click()
    r_base_elts.create_project_button.click()


# environment
def add_pip_package(driver: selenium.webdriver):
    """
    Add pip packages.

    Args:
        driver
    """
    logging.info("Adding pip packages")
    environment = elements.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    time.sleep(3)
    driver.execute_script("window.scrollBy(0, -400);")
    driver.execute_script("window.scrollBy(0, 400);")
    environment.add_packages_button.click()
    pip_list = ["pandas", "numpy", "matplotlib"]
    for pip_pack in pip_list:
        environment.package_name_input.send_keys(pip_pack)
        time.sleep(3)
        environment.add_button.click()
        time.sleep(3)
    environment.install_packages_button.click()


def add_conda3_package(driver: selenium.webdriver):
    """
    Add conda3 packages.

    Args:
        driver
    """
    logging.info("Adding conda3 package")
    environment = elements.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    time.sleep(3)
    environment.conda3_tab_button.click()
    driver.execute_script("window.scrollBy(0, -400);")
    driver.execute_script("window.scrollBy(0, 400);")
    environment.add_packages_button.click()
    environment.package_name_input.send_keys("pyflakes")
    time.sleep(3)
    environment.add_button.click()
    time.sleep(3)
    environment.install_packages_button.click()


def add_apt_package(driver: selenium.webdriver):
    """
    Add apt packages.

    Args:
        driver
    """
    logging.info("Adding apt packages")
    environment = elements.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    time.sleep(3)
    environment.apt_tab_button.click()
    driver.execute_script("window.scrollBy(0, -400);")
    driver.execute_script("window.scrollBy(0, 400);")
    environment.add_packages_button.click()
    environment.package_name_input.send_keys("apache2")
    time.sleep(3)
    environment.add_button.click()
    time.sleep(3)
    environment.install_packages_button.click()


def add_valid_custom_docker(driver: selenium.webdriver):
    """
    Add valid custom Docker.

    Args:
        driver
    """
    logging.info("Adding valid custom Docker")
    environment = elements.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    driver.execute_script("window.scrollBy(0, 600);")
    environment.custom_docker_edit_button.click()
    environment.custom_docker_text_input.send_keys(testutils.valid_custom_docker_instruction())
    driver.execute_script("window.scrollBy(0, 300);")
    environment.custom_docker_save_button.click()


def add_invalid_custom_docker(driver: selenium.webdriver):
    """
    Add invalid custom Docker.

    Args:
        driver
    """
    logging.info("Adding invalid custom Docker")
    environment = elements.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    driver.execute_script("window.scrollBy(0, 600);")
    environment.custom_docker_edit_button.click()
    environment.custom_docker_text_input.send_keys(testutils.invalid_custom_docker_instruction())
    driver.execute_script("window.scrollBy(0, 300);")
    environment.custom_docker_save_button.click()


def create_dataset(driver: selenium.webdriver) -> str:
    """
    Create a dataset.

    Args:
        driver

    Returns:
        Name of dataset just created
    """
    unique_dataset_name = testutils.unique_dataset_name()
    logging.info(f"Creating a new dataset: {unique_dataset_name}")
    dataset_elts = elements.AddDatasetElements(driver)
    dataset_elts.dataset_page_tab.click()
    dataset_elts.create_new_button.click()
    dataset_elts.dataset_title_input.click()
    dataset_elts.dataset_title_input.send_keys(unique_dataset_name)
    dataset_elts.dataset_description_input.click()
    dataset_elts.dataset_description_input.send_keys(testutils.unique_project_description())
    dataset_elts.dataset_continue_button.click()
    dataset_elts.gigantum_cloud_button.click()
    dataset_elts.create_dataset_button.click()
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".TitleSection")))
    return unique_dataset_name


def publish_dataset(driver: selenium.webdriver):
    """
    Publish a dataset to cloud.

    Args:
        driver

    """
    logging.info("Publish dataset to cloud")
    dataset_elts = elements.AddDatasetElements(driver)
    dataset_elts.publish_dataset_button.click()
    dataset_elts.publish_confirm_button.click()
    time.sleep(5)
    dataset_elts.dataset_page_tab.click()
    time.sleep(5)
    dataset_elts.dataset_cloud_page.click()
    wait = WebDriverWait(driver, 200)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".VisibilityModal__buttons")))


def link_dataset(driver: selenium.webdriver):
    """
    Link a dataset to a project.

    Args:
        driver

    """
    # Link the dataset
    logging.info("Linking the dataset to project")
    driver.find_element_by_css_selector(".Navigation__list-item--inputData").click()
    driver.find_element_by_css_selector(".FileBrowser__button--add-dataset").click()
    driver.find_element_by_css_selector(".LinkCard__details").click()
    wait = WebDriverWait(driver, 200)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".Footer__message-title")))
    driver.find_element_by_css_selector(".ButtonLoader ").click()
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".LinkModal__container")))


def publish_project(driver: selenium.webdriver):
    """
        Publish a project to cloud.

        Args:
            driver

        """
    logging.info("Publishing project")
    publish_elts = elements.PublishProjectElements(driver)
    publish_elts.publish_project_button.click()
    publish_elts.publish_confirm_button.click()
    time.sleep(5)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    time.sleep(5)
    side_bar_elts = elements.SideBarElements(driver)
    side_bar_elts.projects_icon.click()
    publish_elts.cloud_tab.click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))


def delete_dataset_cloud(driver: selenium.webdriver, dataset):
    """
    Delete a dataset from cloud.

    Args:
        driver
        dataset

    """
    logging.info(f"Removing dataset {dataset} from cloud")
    driver.find_element_by_xpath("//a[contains(text(), 'Datasets')]").click()
    driver.find_element_by_css_selector(".Datasets__nav-item--cloud").click()
    time.sleep(2)
    driver.find_element_by_css_selector(".RemoteDatasets__icon--delete").click()
    driver.find_element_by_css_selector("#deleteInput").send_keys(dataset)
    time.sleep(2)
    driver.find_element_by_css_selector(".ButtonLoader").click()
    time.sleep(5)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".DeleteDataset")))


def delete_project_cloud(driver: selenium.webdriver, project):
    """
    Delete a project from cloud.

    Args:
        driver
        project

    """
    logging.info(f"Removing project {project} from cloud")
    publish_elts = elements.PublishProjectElements(driver)
    publish_elts.project_page_tab.click()
    publish_elts.cloud_tab.click()
    time.sleep(2)
    publish_elts.delete_project_button.click()
    time.sleep(2)
    publish_elts.delete_project_input.send_keys(project)
    time.sleep(2)
    publish_elts.delete_confirm_button.click()
    time.sleep(5)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".DeleteLabbook")))





