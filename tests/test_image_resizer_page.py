from pytest_bdd import when, then, given
from selenium.common.exceptions import WebDriverException
from pages.templates_page import *
from pages.new_sign_up_page import *
from pages.editor_page import *
from pages.new_login_page import *
from pages.image_resizer_page import *


@then('I go to image resizer page')
def go_to_ir_page(browser):
    try:
        navigate_image_resizer_page(browser)
        analytics_cookie(browser)
    except (Exception, WebDriverException):
        bs_fail_with_traceback(browser, go_to_ir_page)


@then('I upload the image on image resizer')
def upload_image_on_ir(browser):
    try:
        upload_ir(browser)
    except (Exception, WebDriverException):
        bs_fail_with_traceback(browser, upload_image_on_ir)


@then('I change IR Image Ratio')
def ir_change_ratio(browser):
    try:
        change_ir_width_height(browser)
    except (Exception, WebDriverException):
        bs_fail_with_traceback(browser, ir_change_ratio)


@then('I select Social Image Ratios and download')
def ir_change_social_ratios(browser):
    try:
        select_diff_social_ratios(browser)
    except (Exception, WebDriverException):
        bs_fail_with_traceback(browser, ir_change_social_ratios)


@then('I download IR Image and verify redirection to signup page')
def ir_download_and_redirected_to_sign_up(browser):
    try:
        ir_download_to_login(browser)
        ir_download_without_login(browser)
        get_signup_title(browser)
        assert_analytics_events_with_slack(ir_google_events, ir_without_login_google_events, ir_mixpanel_events,
                                           ir_without_login_mixpanel_events, 'IR no logged in')
    except (Exception, WebDriverException):
        bs_fail_with_traceback(browser, ir_download_and_redirected_to_sign_up)


@then('I convert IR Image to video')
def ir_image_to_video(browser):
    try:
        convert_it_image_to_video(browser)
        assert_analytics_events_with_slack(ir_google_events, ir_after_login_google_events, ir_mixpanel_events, ir_after_login_mixpanel_events,
                                           'IR After login')
    except (Exception, WebDriverException):
        bs_fail_with_traceback(browser, ir_image_to_video)