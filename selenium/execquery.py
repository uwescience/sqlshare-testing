#!/usr/bin/env python

import ConfigParser
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

USERNAME="username"
PASSWORD="password"

def parse_config(filename="sqlshare-selenium.cfg"):
    "extract the SQLShare username and password from a configuration file"
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    return { USERNAME : config.get('SQLShare', USERNAME),
             PASSWORD : config.get('SQLShare', PASSWORD) }

def main():
    if len(sys.argv) > 2:
        print >> sys.stderr, "Usage: %s [sqlshare-selenium.cfg]" % (sys.argv[0],)
        print >> sys.stderr, """
The configuration file has the format:
    [SQLShare]
    %s=<username>
    %s=<password>
""" % (USERNAME, PASSWORD)
        sys.exit(1)

    # Get the username and password from the configuration file
    config = parse_config()

    # Load Chrome
    browser = webdriver.Chrome('./chromedriver')

    # Go the SQLShare start page
    browser.get('https://sqlshare.escience.washington.edu/')

    # Find Google button
    google = browser.find_element_by_xpath('//button[@class=\'google\']')
    # .. click it
    google.click()

    # Find the Email field
    email = browser.find_element_by_id('Email')
    # Type in the email address
    email.send_keys(config[USERNAME])

    # Find the Password field
    passwd = browser.find_element_by_id('Passwd')
    # Type in the password
    passwd.send_keys(config[PASSWORD])
    passwd.send_keys(Keys.RETURN)

    # Find the Allow button
    approve = browser.find_element_by_id('approve_button')
    approve.click()

    # Click the New Query link
    newquery = browser.find_element_by_link_text('New query')
    newquery.click()


    # Select the DIV containing the IFRAME with the text box
    div = None
    for i in range(50):
        try:
            div = browser.find_element_by_id('ss_app_workspace_query_wrapper')
            break
        except:
            time.sleep(0.1)
    if div is None:
        print >> sys.stderr, "Unable to get the DIV containing text box"
        sys.exit(1)

    # Wait for DIV to be visible
    for i in range(50):
        if div.is_displayed():
            break
        time.sleep(0.1)

    # TODO FIX XXX
    # Sleep arbitrary large amount of time to let page finish rendering
    time.sleep(3)

    # Click the DIV
    div.click()

    # Get the element the browser is currently focused on, to get inside the
    # IFRAME
    querybox = browser.switch_to_active_element()
    querybox.send_keys('select * from [sagarc@washington.edu].[g111]')

    runquerybutton = browser.find_element_by_id('ss_app_workspace_run_query')
    runquerybutton.click()
if __name__ == "__main__":
    main()
