import requests
from bs4 import BeautifulSoup as bs
import random
import selenium.webdriver as webdriver
import time
import install_modules
from myconfig import first_name, last_name, phone, email, address2, birth_day, birth_month, birth_year, address1, zipcode, city, card_type, cc_numb, cc_name, cc_code, cc_exp_mo, cc_exp_year

session = requests.session()
headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
session.headers.update(headers)


def get_sizes():
    global session
    try:
        endpoint = raw_input("\n copy+paste the link then hit enter:")
        response = session.get(endpoint, headers=headers)
        soup = bs(response.text,"html.parser")
        option = soup.find_all("option",{"data-value":True})
        sizes_in_stock = []
        for size in option:
            if "available" in size["data-status"]:
                size_id = size['data-value']            
                sizes_in_stock.append(size_id)
        return sizes_in_stock
    except:
        print "Sizes not in stock"

def add_to_cart():
    global session
    sizes0 = get_sizes()
    size_chosen = random.choice(sizes0)
    endpoint = 'http://www.avenuestore.be/en/cart/add/' + (size_chosen)
    print 'link to cart is ' + endpoint
    response = session.get(endpoint,headers=headers)
    return response

def checkout():
    global session
  
    payload1 = {
        "mode":"guest",
        "customer[gender]":"male",
        "customer[firstname]":first_name,#first name
        "customer[lastname]":last_name,#last name
        "customer[email]":email,#email
        "customer[type]":"private",
        "customer[email2]":email,#email
        "customer[phone]":phone,# phone number
        "customer[company]":"",
        "customer[cocnumber]":"",
        "customer[vatnumber]":"",
        "customer[birthdate][d]":birth_day,#birth day
        "customer[birthdate][m]":birth_month,#birth month
        "customer[birthdate][y]":birth_year,#birth year
        "billing_address[format]":"international",
        "billing_address[address1]":address1,#street address
        "billing_address[address2]":"",
        "billing_address[number]":"",
        "billing_address[extension]":"",
        "billing_address[zipcode]":zipcode,#zip code
        "billing_address[city]":city,# city
        "billing_address[country]":"us",
        "customer[password]":"",
        "customer[password2]":"",
        "customer[sameaddress]":"1",
        "shipping_address[name]":first_name + last_name,
        "shipping_address[company]":"",
        "shipping_address[format]":"international",
        "shipping_address[address1]":address1,
        "shipping_address[address2]":"",
        "shipping_address[number]":"",
        "shipping_address[extension]":"",
        "shipping_address[zipcode]":zipcode,
        "shipping_address[city]":city,
        "shipping_address[country]":"us",
        "shipment_method":"core|321014|634301",
        "ideal[issuer]":"",
        "payment_method":"multisafepay|" + card_type,
        }
    endpoint0 = 'https://avenue.webshopapp.com/en/checkout/onepage/'
    response0 = session.post(endpoint0,data=payload1)
    endpoint2 = 'https://pay.multisafepay.com/pay/external-details/'
    payload2= {
        "action":"external-prepare",
        "type":"directmerchantdeposit",
        "extvar[extvar1]":cc_numb,#cc number
        "extvar[extvar4]":cc_code,#cc cvc number
        "extvar[extvar2]":cc_name,# name on cc
        "extvar[extvar3][1]":cc_exp_mo,#expir month
        "extvar[extvar3][0]":cc_exp_year,#expir year
        }
    response2 = session.post(endpoint2, data=payload2)
    soup = bs(response2.text,"html.parser")
    print 'success'
    
    
def main():
    add_to_cart()
    checkout()

main()
