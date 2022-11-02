import binascii
import json
import os
import pdb
import sys
import time
import traceback
from datetime import date, datetime
import requests
from google.auth.exceptions import TransportError
from gspread.exceptions import APIError, GSpreadException
from pytz import reference
import allure
from allure_commons.types import AttachmentType
from requests import ReadTimeout
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, \
    NoSuchWindowException, ElementClickInterceptedException, WebDriverException, InvalidArgumentException, \
    NoSuchFrameException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.locators_file import *


try:
    from helpers.googlesheet import *
except (TransportError, APIError, GSpreadException, ReadTimeout):
    pass
except:
    pass
import slack
try:
    Browser = os.environ['browser']
except KeyError:
    pass


def wait_for_ajax(browser):
    wait = WebDriverWait(browser, 300)
    try:
        wait.until(lambda ajwait: browser.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass





def do_click(browser, by_locator: object, sec=10):
    """
    Waits and clicks on the chosen element
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
        sec (int): default time to wait
    """
    wait_for_ajax(browser)
    try:
        WebDriverWait(browser, sec, poll_frequency=0.4).until(
            EC.element_to_be_clickable(by_locator)).click()
    except AttributeError as e:
        if str(e) == "'dict' object has no attribute 'is_displayed'":
            raise NoSuchElementException
        else:
            raise e
    # except (ElementClickInterceptedException, TimeoutException) as dcc:
    #     print(str(dcc))
    #     switch_to_iframe(browser, SKIP_OFFER_MODAL_FRAME, sec)
    #     do_click(browser, SKIP_OFFER_MODAL_BTN)
    #     browser.switch_to.default_content()
    #     WebDriverWait(browser, sec).until(
    #         EC.element_to_be_clickable(by_locator)).click()


def do_double_click(browser, by_locator, sec=5):
    """
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
        sec (int): default time to wait
    """
    wait_for_ajax(browser)
    try:
        elem = WebDriverWait(browser, sec, poll_frequency=0.4).until(
            EC.presence_of_element_located(by_locator))
        browser.execute_script("var evt = document.createEvent('MouseEvents');" +
        "evt.initMouseEvent('dblclick',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" +
        "arguments[0].dispatchEvent(evt);", elem)
    except AttributeError as e:
        if str(e) == "'dict' object has no attribute 'is_displayed'":
            raise NoSuchElementException
        else:
            raise e


def do_hover(browser, by_locator, sec=5):
    """
    Hovers over element
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
        sec (int): default time to wait
    """
    wait_for_ajax(browser)
    try:
        elem = WebDriverWait(browser, sec, poll_frequency=0.4).until(
            EC.presence_of_element_located(by_locator))
        ActionChains(browser).move_to_element(elem).perform()
    except AttributeError as e:
        if str(e) == "move_to requires a WebElement":
            raise NoSuchElementException
        else:
            raise e
    take_screenshot(browser)
    # except TimeoutException:
    #     switch_to_iframe(browser, SKIP_OFFER_MODAL_FRAME, sec)
    #     do_click(browser, SKIP_OFFER_MODAL_BTN)
    #     browser.switch_to.default_content()
    #     elem = WebDriverWait(browser, sec).until(
    #         EC.presence_of_element_located(by_locator))
    #     hov = ActionChains(browser).move_to_element(elem)
    #     hov.perform()
    # finally:
    #     raise


def drag_and_drop(browser, by_locator_source, by_locator_target, sec=5):
    """
    Drag and drop from source to targeted element
    Args:
        browser: webdriver
        by_locator_source (str): chosen source locator from locators/locators_file.py
        by_locator_target (str): chosen target locator from locators/locators_file.py
        sec (int): default time to wait
    """
    wait_for_ajax(browser)
    source = WebDriverWait(browser, sec).until(
        EC.visibility_of_element_located(by_locator_source))
    target = WebDriverWait(browser, sec).until(
        EC.visibility_of_element_located(by_locator_target))
    action = ActionChains(browser)
    action.drag_and_drop(source, target).perform()


def do_send_keys(browser, by_locator, text, sec=5):
    """
    Sends keys to the chosen element
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
        text (str): text to be send
        sec (int): default time to wait
    """
    wait_for_ajax(browser)
    try:
        WebDriverWait(browser, sec, poll_frequency=0.4).until(
            EC.visibility_of_element_located(by_locator)).send_keys(text)
    except AttributeError as e:
        if str(e) == "'dict' object has no attribute 'is_displayed'":
            raise NoSuchElementException
        else:
            raise e


def get_element_text(browser, by_locator: object):
    """
    Gets text of the chosen element
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
    """
    wait_for_ajax(browser)
    try:
        elem_text = WebDriverWait(browser, 30, poll_frequency=0.4).until(
            EC.presence_of_element_located(by_locator)).text
        return elem_text
    except AttributeError as e:
        if str(e) == "'dict' object has no attribute 'is_displayed'":
            raise NoSuchElementException
        elif str(e) == "'dict' object has no attribute 'is_displayed'":
            raise NoSuchElementException
        else:
            raise e


def get_css_value(browser, by_locator, property_name):
    """
    Gets text of the chosen element
    Args:
        property_name: add css property name
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
    """
    wait_for_ajax(browser)
    try:
        elem = WebDriverWait(browser, 30, poll_frequency=0.4).until(
            EC.presence_of_element_located(by_locator))
        elem_value = elem.value_of_css_property(property_name)
        return elem_value
    except AttributeError as e:
        if str(e) == "'dict' object has no attribute 'is_displayed'":
            raise NoSuchElementException
        elif str(e) == "'dict' object has no attribute 'is_displayed'":
            raise NoSuchElementException
        else:
            raise e


def is_visible(browser, by_locator, sec=5) -> bool:
    """
    Waits and checks if element is visible
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
        sec (int): default time to wait
    Returns:
        True or False
    """
    wait_for_ajax(browser)
    if Browser != "headless_chrome":
        take_screenshot(browser)
    else:
        pass
    elem = False
    try:
        elem = WebDriverWait(browser, sec, poll_frequency=0.4, ignored_exceptions=WebDriverException).until(EC.visibility_of_element_located(by_locator))
    except (WebDriverException, Exception, TimeoutException):
        return bool(elem)
    return bool(elem)


def is_invisible(browser, by_locator, sec=5) -> bool:
    """
    Waits and checks if element is invisible
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
        sec (int): default time to wait
    Returns:
        True or False
    """
    wait_for_ajax(browser)
    elem = False
    try:
        elem = WebDriverWait(browser, sec, poll_frequency=0.4, ignored_exceptions=WebDriverException).until(EC.invisibility_of_element_located(by_locator))
    except (WebDriverException, Exception):
        return bool(elem)
    return bool(elem)


def is_clickable(browser, by_locator, sec=5) -> bool:
    """
    Waits and checks if element is clickable
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
        sec (int): default time to wait
    Returns:
        True or False
    """
    wait_for_ajax(browser)
    elem = False
    try:
        elem = WebDriverWait(browser, sec, poll_frequency=0.4).until(EC.element_to_be_clickable(by_locator))
    except (TimeoutException, NoSuchElementException, AttributeError):
        return bool(elem)
    return bool(elem)


def switch_to_iframe(browser, by_locator, sec=10):
    """
    Switches to the chosen iframe
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
        sec (int): default time to wait
    """
    try:
        WebDriverWait(browser, sec, poll_frequency=0.4).until(EC.frame_to_be_available_and_switch_to_it(by_locator))
    except InvalidArgumentException as e:
        if ("Message: invalid argument: missing 'ELEMENT'" in str(e)) is True:
            raise NoSuchElementException
        else:
            raise e


def do_clear(browser, by_locator, sec=5):
    """
    Clears textfield or input
    Args:
        browser: webdriver
        by_locator (str): chosen locator from locators/locators_file.py
        sec (int): default time to wait
    """
    wait_for_ajax(browser)
    try:
        WebDriverWait(browser, sec, poll_frequency=0.4).until(EC.visibility_of_element_located(by_locator)).clear()
    except AttributeError as e:
        if str(e) == "'dict' object has no attribute 'is_displayed'":
            raise NoSuchElementException
        else:
            raise e







def read_creds(file_dir: str, line_num: int) -> str:
    """
    Reads credential information from the file
    Args:
        file_dir (str): path to the file
        line_num (int): line number we want to use
    Returns:
        Credentials (str)
    """
    f = open(os.getcwd() + file_dir, "r")
    read = f.readlines()
    return read[line_num]


def read_creds_chars(file_dir: str, line_num: int, char_num: int) -> str:
    """
    Reads credential information and characters from the file
    Args:
        line_num (int): line number we want to use
        char_num(int): char number we want to use
        file_dir (str): path to the file
    Returns:
        Credentials (str)
    """
    f = open(os.getcwd() + file_dir, "r")
    read = f.readlines()
    read_char = read[line_num]
    return read_char[char_num]








def get_error_console_logs(browser):
    """
    Args:
        browser:
    Returns: Error logs
    """
    error_logs = []
    browser_logs = browser.get_log('browser')
    for entry in browser_logs:
        if entry['level'] == 'SEVERE' or entry['level'] == 'ERROR' or entry['level'] == 'CRITICAL' or entry['level'] == 'INFO':
            if entry['source'] == 'javascript':
                error_logs.append(entry['message'])
            else:
                pass
        else:
            pass
    return error_logs




def bs_fail_with_traceback(browser, main_func):
    """
    Function injects a failed step to Browser Stack
    Args:
        browser: webdriver
        main_func: name of the function
    """
    func_name = main_func.__name__
    if os.environ['browser'] == 'browserstack':
        errors = get_error_console_logs(browser)
        error_string = str(', '.join(errors))
        step_logs = func_name + ", LOGs: " + error_string
        print(error_string)
        import pprint
        pprint.pprint(error_string)
        allure_screenshot(browser)
        try:
            browser.execute_script(
                f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed", "reason": "Failed Step: {step_logs}"}}}}')
        except WebDriverException:
            browser.execute_script(
                f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed", "reason": "Failed Step: {func_name}"}}}}')
    else:
        take_screenshot(browser)
        errors = get_error_console_logs(browser)
        print(errors)
        import pprint
        pprint.pprint(errors)
        pass
    raise AssertionError(func_name, traceback)

