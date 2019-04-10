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
    # Project set up
    username = testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    project_title = testutils.create_project_without_base(driver)

    # Python 3 minimal base
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Publish project
    publish_elts = testutils.PublishProjectElements(driver)
    publish_elts.publish_project_button.click()
    publish_elts.publish_confirm_button.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Add collaborator with admin permission
    logging.info(f"Adding a collaborator with Admin permission to private project {project_title}")
    publish_elts.collaborators_button.click()
    time.sleep(2)
    username2 = testutils.load_credentials(user_index=1)
    print(username, username2)
    publish_elts.collaborators_input.send_keys(username2)
    publish_elts.select_permission_button.click()
    publish_elts.select_admin_button.click()
    publish_elts.add_collaborators_button.click()
    time.sleep(2)
    publish_elts.close_collaborators_button.click()
    testutils.log_out(driver)

    # Add file to input data and sync project
    logging.info("Owner adding a file to the project")
    with open('/tmp/sample-upload.txt', 'w') as example_file:
        example_file.write('{username}')
    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title,
                              'input')
    shutil.copy(example_file.name, input_path)
    time.sleep(2)

    logging.info(f"Syncing {project_title}")
    publish_elts.sync_project_button.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Collaborator log in
    logging.info(f"Logging in as {username2[0].rstrip()}")
    testutils.log_in(driver, user_index=1)
    time.sleep(2)
    try:
        testutils.remove_guide(driver)
    except:
        pass
    time.sleep(2)
    publish_elts.cloud_tab.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))

    # Collaborator imports the project from cloud
    publish_elts.import_first_cloud_project_button.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Collaborator added a file using same name with different content
    logging.info("Collaborator adding a file to the project")
    with open('/tmp/sample-upload.txt', 'w') as example_file:
        example_file.write('{username2}')
    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username2, username, 'labbooks', project_title,
                              'input')
    shutil.copy(example_file.name, input_path)
    time.sleep(2)

    # Collaborator sync
    logging.info("Collaborator syncing project {project_title} to the cloud")
    publish_elts.sync_project_button.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # log out
    testutils.log_out(driver)

    # Owner load the project and sync
    logging.info(f"Logging in as {username2[0].rstrip()}")
    testutils.log_in(driver, user_index=1)
    time.sleep(2)
    try:
        testutils.remove_guide(driver)
    except:
        pass
    time.sleep(2)
    driver.find_element_by_css_selector("LocalLabbooks__panel-title").click()
    publish_elts.sync_project_button.click()
    time.sleep(5)
    # Owner get conflict and solve by using mine.
    assert driver.find_element_by_css_selector(".ForceSync__buttonContainer").isDisplayed(),\
        "Owner expected merge conflict"
    driver.find_element_by_xpath("//button[contains(text(), 'Use Mine']").click()

    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title,
                              'input')
    with open(input_path + 'sample-upload.txt', 'r') as example_file:
        file_content = example_file.read()

    assert file_content == username, "The file content is expected to match the owner's username"


    # Owner deletes cloud project
    testutils.log_in(driver)
    time.sleep(2)
    try:
        testutils.remove_guide(driver)
    except:
        pass
    time.sleep(2)
    logging.info(f"{username} deleting shared {project_title} from cloud")
    publish_elts.cloud_tab.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))
    publish_elts.delete_project_button.click()
    time.sleep(2)
    publish_elts.delete_project_input.send_keys(project_title)
    time.sleep(2)
    publish_elts.delete_confirm_button.click()
    time.sleep(5)
    project_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username,
                                'labbooks', project_title)
    git_get_remote_command_1 = Popen(['git', 'remote', 'get-url', 'origin'],
                                     cwd=project_path, stdout=PIPE, stderr=PIPE)
    del_stderr = git_get_remote_command_1.stderr.readline().decode('utf-8').strip()

    assert "fatal" in del_stderr, f"Expected to not see a remote set for {project_title}, but got {del_stderr}"


