from bs4 import BeautifulSoup as soup
from random import randint
import requests
import re
import random
import time
import xlwt


# def main():

#   product_list_contents = requests.get("https://www.ebay.co.uk/sch/musicmagpie/m.html?item=301829202695&hash=item46466c2307%3Ag%3AKAUAAOSwGqpdhZpq&rt=nc&_trksid=p2047675.l2562")
#   product_list_content = soup(product_list_contents.content, 'html.parser')

#   result_number = product_list_content.find('span',{'class', 'rcnt'}).text.replace(',','')
#   per_unit = len(product_list_content.findAll('div',{'class':'lvpicinner full-width picW'}))
#   row=0
#   result_num = 0
#   print(result_number)
#   for x in range(int(int(result_number)/per_unit)):

#       print("------------------------------------"+str(x+1)+"th page---------------------------------------------")
#       product_content_page = requests.get("https://www.ebay.co.uk/sch/m.html?item=301829202695&hash=item46466c2307%3Ag%3AKAUAAOSwGqpdhZpq&_ssn=musicmagpie&_pgn="+str(x+1)+"&_skc="+str(x*50)+"&rt=nc")
#       product_content_list = soup(product_content_page.content, 'html.parser')

#       product_lists = product_content_list.findAll('div',{'class':'lvpicinner full-width picW'})
#       for x in range(len(product_lists)):
#         row += 1
#         col = 0
#         result_num += 1
#         print(str(result_num)+"th product")
        # get the product_info
product_info = ['','','','','','','','','','','','','','','','','','','','','','','','','','']
product_info[0] = "https://www.ebay.co.uk/itm/Sex-and-the-City-The-Essential-Collection-Series-1-6-DVD-2009-Sarah/381883369272?hash=item58ea05c738:g:PIYAAOSwusdaYQFn"


product_page = requests.get(product_info[0])
product = soup(product_page.content, 'html.parser')

product_info[11] = product.findAll('li', {'class': 'bc-w'})[0].text + ' > ' + product.findAll('li', {'class': 'bc-w'})[1].text

product_info[4] = product.find('h1', {'class': 'it-ttl'}).text.replace('Details about   ', '')

product_info[6] = product.find('div', {'class': 'u-flL condText'}).text

if (product.find('span', {'class', 'topItmCndDscMsg'}) != None):
  product_info[7] = product.find('span', {'class': 'topItmCndDscMsg'}).text
product_info[25] = product.find('span', {'class': 'notranslate'}).text

# get image list
image_list = []
if (product.find('ul',{'class':'lst icon'}) != None):
  images = product.find('ul',{'class':'lst icon'}).findAll('img')
  for image in images:
    if(len(image_list) > 6):
      break
    image_list.append(image['src'])
else:
  image = product.find(id = 'icImg')['src']
  image_list.append(image)
index = 18
for x in range(len(image_list)):
  product_info[index] = image_list[x]
  index += 1
# get the item_specifics
product_info[3] = product.find(id = 'descItemNumber').text
item_specific_contents = product.find(id = 'viTabs_0_is').findAll("tr")
item_specific_content =""
for item_content in item_specific_contents:
  # print(re.sub("\s\s+", " ", item_content.text))
  product_info[14] += re.sub("\s\s+", " ", item_content.text)+"\n"
product_info[14] = product_info[14][1:]
print(product_info[14])
if (product.find(id = 'itmSellerDesc') != None):
  item_specific = product.find(id = 'viTabs_0_is').findAll('table')[1].findAll('td')
  product_info[1] = item_specific[len(item_specific)-1].span.text
  if (len(product_info[1]) !=13):
    product_info[1]=""
  product_info[2] = item_specific[len(item_specific)-3].span.text
  if (product_info[1] != item_specific[len(item_specific)-3].span.text):
    product_info[2] = ""
  for x in range(len(item_specific)):
    if(item_specific[x].text == """
									 			Format: """ ):
      product_info[8] = item_specific[x+1].span.text
    elif (item_specific[x].text == """
                    Publisher: """ ):
      product_info[10] = item_specific[x+1].span.text

else:
  item_specific = product.find(id = 'viTabs_0_is').div.table.findAll('td')
  product_info[1] = item_specific[len(item_specific)-1].span.text
  if (len(product_info[1]) !=13):
    product_info[1]=""
  product_info[2] = item_specific[len(item_specific)-3].span.text
  if (product_info[1] != item_specific[len(item_specific)-3].span.text):
    product_info[2] = ""  
  for x in range(len(item_specific)):
    if(item_specific[x].text == """
									 			Format: """ ):
      product_info[8] = item_specific[x+1].span.text
      print(product_info[8])
    elif (item_specific[x].text == """
                    Publisher: """ ):
      product_info[10] = item_specific[x+1].span.text

# get the about_content

if (product.find(id = 'viTabs_0_pd') != None ):
  about_this_product = product.find(id = 'viTabs_0_pd').findAll("td")
  for x in range(len(about_this_product)):
    if(about_this_product[x].text == "Author(s)" or about_this_product[x].text == "Author"):
      product_info[9] = re.sub("\s\s+"," ", about_this_product[x+1].text)
  about_this = product.find(id = 'viTabs_0_pd').findAll("tr")
  about_content = ""
  for about_each in about_this:
    product_info[12] += re.sub("\s\s+"," ", about_each.text) +"\n"
  # print(product_info[12])
if(product.find(id = 'desc_ifr') != None):
  description_page_url = product.find(id = 'desc_ifr')['src']

description_content_page = requests.get(description_page_url)
description_content = soup(description_content_page.content, 'html.parser')
product_info[13] = re.sub("\s\s+"," ", description_content.find(id = 'itemInfo').text)
# print(product_info)

# main()
