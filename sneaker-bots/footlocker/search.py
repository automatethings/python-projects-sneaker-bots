from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
import time

# construct the argument parser and parse the arguments
ap 		= argparse.ArgumentParser()
ap.add_argument("-url","--website", required = True, help = "enum of companies we have crawlers for")
args 	= vars(ap.parse_args())
 
# init global variables
#json 	= 
SHOE 	= {
	'model': 	'190074',
	'sku': 		'55088007',
	'slug': 	'',
	'quantity': 1,
	'size': 	'13.0'
}

# we need to use a proxy
# https://www.us-proxy.org/
PROXY 	= "104.198.252.120:80" # IP:PORT or HOST:PORT
PROXY 	= False

if PROXY:

	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--proxy-server=http://%s' % PROXY)

	# setup
	chrome 	= webdriver.Chrome(chrome_options=chrome_options)

else:

	chrome 	= webdriver.Chrome()

chrome.implicitly_wait(1)

####################################
## LOG INTO FOOTLOCKER
chrome.get(args['website'])
assert "Foot Locker" in chrome.title

# generate buttons needed
button 	= {
	'login': 	chrome.find_element_by_css_selector('#header_account_access')
}

# click login button
button['login'].click()
chrome.switch_to.frame(chrome.find_element_by_css_selector('iframe[id="loginIFrame"]'))
time.sleep(.5)

# lets login
email 		= chrome.find_element_by_css_selector('#login_email')
# set email address to login
email.send_keys('thomasjrowley@gmail.com')
email.send_keys(Keys.TAB)
time.sleep(.1)
# set password to login
password 	= chrome.find_element_by_css_selector('#login_password')
password.send_keys('1sheaforme')
password.send_keys(Keys.TAB)
time.sleep(.1)
# submit data
submit 		= chrome.find_element_by_css_selector('.cta_button')
submit.click()
time.sleep(1)
## we are logged in
####################################


####################################
## ADD SHOE TO CART
# lets go to the shoe we want
chrome.get('http://www.footlocker.com/product/model:%s/sku:%s/%s' % (SHOE['model'],SHOE['sku'],SHOE['slug']))
# lets fill out the form fields
# add quantity
for i in range((SHOE['quantity']-1)):
	quantity 	= chrome.find_element_by_css_selector('.add_quantity')
	quantity.click()
	time.sleep(0.1)

# select size
chrome.find_element_by_css_selector('#pdp_size_select_mask').click()
# we need to wait for footlocker animation
time.sleep(0.5)
chrome.find_element_by_css_selector('a[value="%s"]' % SHOE['size']).click()
time.sleep(0.1)

# add to cart
chrome.find_element_by_css_selector("#pdp_addtocart_button").click()
time.sleep(3.5)
chrome.find_element_by_css_selector('#header_cart_button').click()
## we have added our shoe to the cart
####################################

'''
####################################
## LET'S CHECKOUT
chrome.get('http://www.footlocker.com/shoppingcart/default.cfm')
chrome.switch_to_default_content()
time.sleep(0.5)
'''


# click Checkout button
chrome.execute_script("if (typeof sharedCart_panel !== 'undefined'){ sharedCart_panel.close(); }")
chrome.find_element_by_css_selector('#cart_checkout_button').click()

'''
chrome.find_element_by_css_selector('#billFirstName').send_keys("Thomas");
chrome.find_element_by_css_selector('#billLastName').send_keys("Rowley");
chrome.find_element_by_css_selector('#billAddress1').send_keys("433 Bishop Rd");
chrome.find_element_by_css_selector('#billPostalCode').send_keys("44143");
chrome.find_element_by_css_selector('#billCity').send_keys("Highland Heights");
chrome.find_element_by_css_selector('#billState[value="OH"]').click();
chrome.find_element_by_css_selector('#billHomePhone').send_keys("9513188790");
chrome.find_element_by_css_selector('#billEmailAddress').send_keys("thomasjrowley@gmail.com");
chrome.find_element_by_css_selector('#billPaneContinue]').click();
time.sleep(.5)

chrome.find_element_by_css_selector('#shipMethodPaneContinue').click();
time.sleep(.5)
chrome.find_element_by_css_selector('#promoCodePaneContinue').click();
'''

# select pay method
chrome.find_element_by_css_selector('#CardNumber').send_keys('4695965060288681')
chrome.find_element_by_css_selector('#CardExpireDateMM').send_keys('09')
chrome.find_element_by_css_selector('#CardExpireDateYY').send_keys('18')
chrome.find_element_by_css_selector('#CardCCV').send_keys('614')

# next step
chrome.find_element_by_css_selector('#payMethodPaneContinue').click()
time.sleep(0.5)

# submit order
#chrome.find_element_by_css_selector('#orderSubmit').click()
chrome.execute_script("spco.skipConfirm();finishCMMiniCartCheckoutEvent();return false;")
chrome.find_element_by_css_selector('#spcoForm').submit()
# check if submission successful, if not - resubmit
####################################

time.sleep(1)
chrome.find_element_by_css_selector('#orderSubmit').click();

print('found foot locker')
try:
	time.sleep(5000)
finally:
	chrome.close()








'''
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
time.sleep(5)
assert "No results found." not in driver.page_source
'''
#chrome.close()




