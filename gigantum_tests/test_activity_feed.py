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


def test_pip_packages(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that pip packages install successfully.

    Args:
        driver
    """
    # project set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    testutils.create_project_without_base(driver)
    time.sleep(2)
    # python 3 minimal base
    testutils.add_py3_min_base(driver)
    # wait
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex > .Stopped")))
    time.sleep(3)
    # pip packages
    testutils.add_pip_package(driver)
    time.sleep(2)
    # wait until container status is stopped
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex > .Stopped")))
    time.sleep(2)
    assert testutils.is_container_stopped(driver), "Expected stopped container"

    # check pip packages version from jupyterlab
    driver.find_element_by_css_selector(".Btn--text").click()
    time.sleep(10)
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[title = code]")))
    driver.find_element_by_css_selector(".jp-LauncherCard-label").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".CodeMirror-line")))
    el = driver.find_element_by_css_selector(".CodeMirror-line")
    actions = ActionChains(driver)
    # implement script the import packages and print the versions.
    plot_script = "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n" \
                     "%matplotlib inline\n" \
                     "x = pd.DataFrame(np.random.randint(100, size=(10,10)))\n" \
                     "x.plot()\nplt.show()"
    actions.move_to_element(el).click(el).send_keys(plot_script).perform()
    driver.find_element_by_css_selector(".jp-RunIcon").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".jp-mod-active")))

    # check activity feed
    driver.switch_to.window(window_handles[0])
    activity = testutils.elements.ActivityElements(driver)
    activity.activity_tab_button.click()
    top_activity = driver.find_element_by_css_selector(".ActivityCard__commit-message").text
    print(top_activity)


