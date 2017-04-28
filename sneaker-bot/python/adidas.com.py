# https://www.youtube.com/watch?v=Jji_MrdUbNc
# http://www.adidas.com/us/ultraboost-x-shoes/BB1696.html?forceSelSize=BB1696_650 	(size 11)
import RandomUserAgent
import requests
import bs4
import webbrowser
import threading
import sys

# define global variables
THREADS 	= 1
PROXIES 	= {
	'http': 	"",
	'https': 	""
}
# grab needed headers (random user agent)
HEADER 	= RandomUserAgent.load()

# our main method to 
def shoebot(model,size,qty,evt):
	# grab URL of our product
	url 		= product(model,size)
	# loop as long as thread event is not set
	while not evt.isSet():
		# lets check whether or not it is in stock
		if stocked(url,size):
			# lets double check event isnt yet set
			if not evt.isSet():
				# set threading event so other threads stop working
				evt.set()

				# item is in stock, lets buy some shoes
				print('----------------------------------')
				print('item is in stock')
				print('purchasing model: %s' % model)
				print('purchasing size: %s' % size)
				print('purchasing qty: %s' % qty)

				checkout(model,size,qty)

				# after successful purchase(s), close thread
				print('purchase success')
				print('----------------------------------')
			else:
				print('item has already been purchased')
		else:
			print('item is not in stock')


# method to grab the product URL
def product(model,size):
	code 	= shoecode(model,size)
	url 	= 'http://www.adidas.com/us/' + str(model) + '.html?forceSelSize=' + str(model) + '_' + str(code)
	return url

# method to check if this item is in stock
def stocked(url,size):
	HTML 	= requests.get(url,headers=HEADER,proxies=PROXIES)
	page 	= bs4.BeautifulSoup(HTML.text,"lxml")
	avail 	= page.select('.size-dropdown-block')
	avail 	= str(avail[0].getText()).replace('\n\n','')
	avail 	= avail.split()
	avail.remove('Select')
	avail.remove('size')

	# convert available to float
	avail 	= [float(i) for i in avail]

	# if size is available, select it
	if size in avail:
		return True
	else:
		return False

def checkout(model,size,qty):

	# start a persistent session
	persist = requests.session()

	############################################
	## Add to Cart

	print('>> adding to cart')
	url 	= 'http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct'
	code 	= shoecode(model,size)
	params 	= {
		'layer': 					'Add+To+Bag+overlay',
		'pid': 						str(model) + '_' + str(code),
		'Quantity': 				str(qty),
		'masterPid': 				str(model),
		'sessionSelectedStoreID': 	'null',
		'ajax': 					'true'
	}
	#print(params)
	# post data to add to cart
	HTML 	= persist.post(url,data=params,headers=HEADER,proxies=PROXIES)
	#HTML 	= requests.post(url,data=params)
	page 	= bs4.BeautifulSoup(HTML.text,"lxml")

	write('adding.html',page)

	'''
	# view cart
	HTML 	= persist.get('https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show',headers=HEADER,proxies=PROXIES)
	page 	= bs4.BeautifulSoup(HTML.text,"lxml")

	write('getting.html',page)

	# if we were unable to view cart page, then Adidas has detected a bot

	# grab .formcheckout action & POST to it
	for form in page.find_all('form',class_="formcheckout"):
		action 	= form.get('action') 	# grab action of the first .formcheckout form found
		break

	# POST to start checkout
	print(action)
	HTML 	= persist.get(action,headers=HEADER,proxies=PROXIES)
	page 	= bs4.BeautifulSoup(HTML.text,"lxml")
	'''

	#HTML 	= persist.get('https://www.adidas.com/us/delivery-start',headers=HEADER,proxies=PROXIES)
	HTML 	= persist.get('https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COSummary-Start',headers=HEADER,proxies=PROXIES)
	page 	= bs4.BeautifulSoup(HTML.text,"lxml")

	# write markup of page to .html file (so we can review later if needed)
	write('carting.html',page)

	'''
	# grab needed form action
	for form in page.find_all('form',class_="fancyform clearfix"):
		action 	= form.get('action')
		break

	# grab dwfrm_login_securekey
	dwfrm_login_securekey 	= ''
	for hidden in page.find_all('input'):
		print(hidden)
		if hidden['name'] == 'dwfrm_login_securekey':
			dwfrm_login_securekey 	= hidden['value']
			break


	print(action)
	print(dwfrm_login_securekey)
	sys.exit()

	# lets continue checkout as a guest
	HTML 	= persist.post(action,data=data)

	write('checkout.html',page)
	
	sys.exit()
	'''

	############################################
	## Billing Information
	print('>> submit billing information')
	'''
	# grab #dwfrm_delivery action URL
	dwfrm_delivery 				= 'https://www.adidas.com/us/delivery-start?dwcont=C99536075';
	# grab dwfrm_delivery_securekey (hidden field)
	dwfrm_delivery_securekey 	= '1198697413';
	'''
	dwfrm_delivery 				= page.find('form', {'id': 'dwfrm_delivery'}).get('action')
	dwfrm_delivery_securekey 	= page.find('input', {'name': 'dwfrm_delivery_securekey'}).get('value')

	# need to set cookie?
	# Set-Cookie[__cqact=[{"activityType":"beginCheckout","parameters":{"cookieId":"abqMac9OKddq9kTGJBKs3uTA32","userId":"","amount":180.00,"currencyCode":"USD","products":[{"id":"BB1696","sku":"BB1696_660","quantity":1,"price":180.00}]}}];

	# create params to submit
	params 	= {
		# mandatory hidden fields
		'dwfrm_delivery_shippingOriginalAddress': 										'false',
		'dwfrm_delivery_shippingSuggestedAddress': 										'false',
		'dwfrm_delivery_singleshipping_shippingAddress_isedited': 						'false',
		# shipping information
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_firstName': 		'John',
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_lastName': 		'Thompson',
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address1': 		'123 Test Ave',
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address2': 		'',
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_city': 			'Canton',
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_countyProvince': 	'OH',
		'state': 																		[],
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_zip': 				'44714',
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_country': 			'US',
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_phone': 			'3305556666',
		# billing information
		'dwfrm_delivery_singleshipping_shippingAddress_useAsBillingAddress': 			'true',			# use shipping address as billing address?
		'dwfrm_delivery_securekey': 													dwfrm_delivery_securekey, 	# this is a hidden field we need to grab the value from=
		# these only need values if billing is different than shipping (and above hidden field is false)
		'dwfrm_delivery_billingOriginalAddress': 										'false',
		'dwfrm_delivery_billingSuggestedAddress': 										'false',
		'dwfrm_delivery_billing_billingAddress_isedited': 								'false',
		'dwfrm_delivery_billing_billingAddress_addressFields_country': 					'US',
		'dwfrm_delivery_billing_billingAddress_addressFields_firstName': 				'John',
		'dwfrm_delivery_billing_billingAddress_addressFields_lastName': 				'Thompson',
		'dwfrm_delivery_billing_billingAddress_addressFields_address1': 				'123 Test Ave',
		'dwfrm_delivery_billing_billingAddress_addressFields_address2': 				'',
		'dwfrm_delivery_billing_billingAddress_addressFields_city': 					'Canton',
		'dwfrm_delivery_billing_billingAddress_addressFields_countyProvince': 			'OH',
		'dwfrm_delivery_billing_billingAddress_addressFields_zip': 						'44714',
		'dwfrm_delivery_billing_billingAddress_addressFields_phone': 					'3305556666',
		# foreign address fields (not needed)
		'dwfrm_foreignaddress_country': 												'',
		'dwfrm_foreignaddress_firstName': 												'',
		'dwfrm_foreignaddress_lastName': 												'',
		'dwfrm_foreignaddress_address1': 												'',
		'dwfrm_foreignaddress_address2': 												'',
		'dwfrm_foreignaddress_city': 													'',
		'dwfrm_foreignaddress_zip': 													'',
		'dwfrm_foreignaddress_phone': 													'',
		'dwfrm_foreignaddress_countyProvince': 											'',
		# email/order details
		'dwfrm_delivery_singleshipping_shippingAddress_email_emailAddress': 			'thompson20_91@hotmail.com',
		'signup_source': 																'shipping', 	# hidden field
		'dwfrm_delivery_singleshipping_shippingAddress_ageConfirmation': 				'true', 		# age verification
		'shipping-group-0': 															'Standard', 	# shipping
		# more hidden fields
		'dwfrm_cart_shippingMethodID_0': 												'Standard',
		'shippingMethodType_0': 														'inline',
		'dwfrm_cart_selectShippingMethod': 												'ShippingMethodID',
		'referer': 																		'Cart-Show',
		# submit button
		'dwfrm_delivery_savedelivery': 													'Review and Pay',
		'dwfrm_delivery_singleshipping_shippingAddress_agreeForSubscription': 			'true', 		# you agree for them to spam you
		'dwfrm_cart_checkoutCart': 														'Checkout'
		#'format': 																		'ajax'
	}
	#print(params)
	
	# submit form
	HTML 	= persist.post(dwfrm_delivery,data=params,headers=HEADER,proxies=PROXIES)
	page 	= bs4.BeautifulSoup(HTML.text,"lxml")

	# write markup of page to .html file (so we can review later if needed)
	write('billing.html',page)
	sys.exit()

	############################################
	## CC Details
	print('>> submit credit card information')

	# grab #dwfrm_payment action URL
	dwfrm_payment 				= 'https://secureacceptance.cybersource.com/silent/pay'
	# grab dwfrm_payment_securekey value
	dwfrm_payment_securekey 	= '1428350296'

	# create params to submit
	params 			= {
		# hidden fields
		'dwfrm_payment_creditCard_type': 		'001', 	# 001 = Visa, 002 = Mastercard, 003 = American Express, 004 = Discover, 005 = Diners Club
		'selectedPaymentMethodID': 				'CREDIT_CARD',
		'dwfrm_payment_securekey': 				dwfrm_payment_securekey,
		'dwfrm_payment_signcreditcardfields': 	'sign',
		# CC fields
		'dwfrm_payment_creditCard_owner': 		'John Thompson',
		'dwfrm_payment_creditCard_number': 		'4111111111111111',
		'dwfrm_payment_creditCard_month': 		'01',
		'dwfrm_payment_creditCard_year': 		'2018',
		'dwfrm_payment_creditCard_cvn': 		'123',
		'dwfrm_payment_creditCard_creditcard': 	'Check out now'
	}
	#print(params)

	# submit form
	HTML 	= persist.post(dwfrm_payment,data=params,headers=HEADER,proxies=PROXIES)
	page 	= bs4.BeautifulSoup(HTML.text,"lxml")

	# write markup of page to .html file (so we can review later if needed)
	write('checkout.html',page)

	# if not successful, resubmit form? continue other threads?

	return True

def shoecode(model,size):
	base 	= 560 	# base is for shoe size 6.5
	shoe 	= size - 6.5
	shoe 	= shoe * 20
	raw 	= shoe + base
	code 	= int(raw)
	return code

def write(file,markup):
	pointer 	= open(file,'w')
	pointer.write(str(markup))
	pointer.close()

# application start
model 	= input('Enter Model #: ')
#sku 	= input('Enter SKU: ')
size 	= float(input('Enter Shoe Size: (e.g. 11.0, 13.5, etc..) '))
qty 	= int(input('Enter Quantity: '))

# array of sizes
sizes 	= [size]

# setup threads
evt 	= threading.Event()
threads = [threading.Thread(name='ThreadNumber{}'.format(n), target=shoebot, args=(model,size,qty,evt)) for n in range(THREADS)]

# lets start our threads
for t in threads: 
	t.start()

