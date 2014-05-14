from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import ConfigParser

time_out_interval = 1
browser = None
previous_page = None
config_filename="sqlshare-selenium.cfg"


def claen_up_and_quit():
	#clean up
	browser.delete_all_cookies();
	browser.quit()

def get_account_info():
	print "type in 'google' for Google account login, 'uw' for UW account login"
	account_type = raw_input()
	config = ConfigParser.RawConfigParser()
	config.read(config_filename)

	e_mail = None
	passwd = None

	if account_type == 'google':
		e_mail = config.get('Google-account', 'id')
		passwd = config.get('Google-account', 'pw')
	elif account_type == 'uw':
		e_mail = config.get('UW-NetID', 'id')
		passwd = config.get('UW-NetID', 'pw')
	else:
		print 'incorrect parameter for account type'
		claen_up_and_quit()

	return {'E-mail': e_mail,
			'passwd': passwd,
			'account_type': account_type}

#if no element specified, wait for some time, else wait for the element for some time
def wait_for_some_element(element_id='', time=10):
	if element_id == '':
		WebDriverWait(browser, time)
	else:
		WebDriverWait(browser, time).until(EC.presence_of_element_located((By.ID, element_id)))

def wait_for_next_page(time=10):
	#function that check whether the browser had finished loading the new page
	def compare_source(browser):
		return previous_page != browser.page_source
	WebDriverWait(browser, time).until(compare_source)
	global previous_page 
	previous_page = browser.page_source



def select_side_bar_button(button_name):
	itme_id = None
	if button_name == 'Your datasets':
		item_id = 'your_queries_li'
	if button_name == 'All datasets':
		item_id = 'all_queries_li'
	if button_name == 'Shared datasets':
		item_id = 'shared_queries_li'
	if button_name == 'Recent activity':
		item_id = 'query_list_li'
	if button_name == 'Recently viewed':
		item_id = 'recent_queries'
	if button_name == 'Upload dataset':
		item_id = 'new_upload_li'
	if button_name == 'New query':
		item_id = 'new_query_li'
	new_query_link = browser.find_element_by_xpath("//*[@id='" + item_id + "']/a")
	href = new_query_link.get_attribute('href')
	browser.get(href)

def login(account_info):
	previous_page = browser.page_source
	if account_info['account_type'] == 'uw':
		browser.find_elements_by_tag_name('button')[0].click()
	elif account_info['account_type'] == 'google':
		browser.find_elements_by_tag_name('button')[1].click()


	#continue when finished loading the new page
	wait_for_next_page(5)

	time.sleep(time_out_interval)
	#login using google/UW account
	previous_page = browser.page_source
	if account_info['account_type'] == 'google':
		#input e-mail address and password
		email = browser.find_element_by_id('Email')
		#email.send_keys('fshhr46@gmail.com')
		email.send_keys(account_info['E-mail'])
		
		passwd = browser.find_element_by_id('Passwd')
		#passwd.send_keys('hhr446213852')
		passwd.send_keys(account_info['passwd'])
		#browser.execute_script("document.getElementById('signIn').click()")
		passwd.send_keys(Keys.RETURN)
	else:
		#input e-mail address and password
		email = browser.find_element_by_id('weblogin_netid')
		#email.send_keys('fshhr46@gmail.com')
		email.send_keys(account_info['E-mail'])
		
		passwd = browser.find_element_by_id('weblogin_password')
		#passwd.send_keys('hhr446213852')
		passwd.send_keys(account_info['passwd'])
		passwd.send_keys(Keys.RETURN)

def set_browser_and_start(browser_name='Chrome'):
	global browser
	browser = browser = webdriver.Chrome()
	browser.get('https://sqlshare.escience.washington.edu/accounts/login/?next=/sqlshare/%3F__hash__%3D')
	global previous_page 
	previous_page = browser.page_source


#unfinished method
def New_query(query=''):

	#navigate to the New query page by click on the side bar
	select_side_bar_button('New query')
	wait_for_next_page(5)


	time.sleep(time_out_interval)
	#switch to the inner HTML Frame for the query
	inner_iframe = browser.find_element_by_xpath('//*[@id="ss_app_workspace_query_wrapper"]//iframe')
	browser.switch_to_frame(inner_iframe)
	print browser.find_element_by_xpath('//body').get_attribute('class')

	#some code to insert the query
	browser.execute_script("document.getElementsByClassName('editbox')[0].innerHTML = document.createTextNode('span') ")


def main():

	#create chrome browser and go to sqlshare mainpage
	set_browser_and_start()
	
	#get login information from command line
	account_info = get_account_info()
	
	

	#login
	login(account_info)
	#wait until finish loading
	wait_for_some_element('solstice_document_body', 10)


	#navigate to some page by click on some button on the side bar
	select_side_bar_button('Your datasets')
	wait_for_next_page()
	time.sleep(5)	

	select_side_bar_button('All datasets')
	wait_for_next_page()
	time.sleep(5)

	select_side_bar_button('Shared datasets')
	wait_for_next_page()
	time.sleep(5)
	
	select_side_bar_button('Recent activity')
	wait_for_next_page()
	time.sleep(5)
	

	#bug with this one
	#select_side_bar_button('Recently viewed')
	#wait_for_next_page()
	#time.sleep(5)
	
	select_side_bar_button('Upload dataset')
	wait_for_next_page()
	time.sleep(5)
	
	select_side_bar_button('New query')
	wait_for_next_page()
	time.sleep(5)
	

	
	time.sleep(time_out_interval)
	New_query('some query goes here, method not completed yet');




	time.sleep(time_out_interval)
	#quit
	claen_up_and_quit()

if __name__ == '__main__':
    main()
