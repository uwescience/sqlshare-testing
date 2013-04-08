# Testing SQLShare with Selenium

## Useful Resources
* [Selenium project page](seleniumhq.org)
* [Instructions for installing Selenium with Python](http://python.dzone.com/articles/python-getting-started)
* [ChromeDriver bindings for Selenium](https://code.google.com/p/selenium/wiki/ChromeDriver)

## Getting started

### Setup Selenium with Python bindings on your machine

I found [these Python instructions](http://python.dzone.com/articles/python-getting-started) easy to follow, and they translated directly into MacPorts from Ubuntu.

### Download the Chrome Webdriver bindings

* Get [ChromeDriver](https://code.google.com/p/selenium/wiki/ChromeDriver), making sure to download the binary that is suitable for your OS
* Copy the `chromedriver` binary into this directory

### Run the utility

    ./login_to_sqlshare.py

This will:

1. open a new Chrome window. (Note this instance of Chrome shares no state with your Chrome, thus it is a separate process and has no access to your cookies, etc.)
2. Navigate to [SQLShare](https://sqlshare.escience.washington.edu)'s login screen.
3. Choose the Google option.
4. Login with the credentials supplied in `sqlshare-selenium.cfg`.
5. Approve using SQLShare with those Google credentials.
6. Load the supplied account's SQLShare home screen.

Now you can add whatever scripted testing you with to do.


## Navigating web pages

Selenium makes it pretty easy to script and navigate through websited. Of course, this requires the website to have well-named elements. The same principles that make a page easily scriptable with jQuery make it easily scriptable with Selenium. Consider the code to enter the Google account credentials:

    # Find the Email field
    email = browser.find_element_by_id('Email')
    # Type in the email address
    email.send_keys(config[USERNAME])

    # Find the Password field
    passwd = browser.find_element_by_id('Passwd')
    # Type in the password
    passwd.send_keys(config[PASSWORD])
    passwd.send_keys('\r\n')

First you find the element you wish to perform some action upon. You can find elements:

* by XPath: `google = browser.find_element_by_xpath('//button[@class=\'google\']')`
* by id: `email = browser.find_element_by_id('Email')`
* and many more ways, [documented here](http://selenium-python.readthedocs.org/en/latest/locating-elements.html).

Then you perform the actions. You can

* click: `google.click()`
* type: `email.send_keys(config[USERNAME])`
* clear a form or text area: `element.clear()`
* and more, [documented here](http://selenium-python.readthedocs.org/en/latest/navigating.html)
