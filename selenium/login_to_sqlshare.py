#!/usr/bin/env python

import ConfigParser
import sys
from selenium import webdriver

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
    # Type in the email address
    passwd.send_keys(config[PASSWORD])
    passwd.send_keys('\r\n')

    # Find the Allow button
    approve = browser.find_element_by_id('approve_button')
    approve.click()

if __name__ == "__main__":
    main()
