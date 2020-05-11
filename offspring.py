from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
from random import randint
import re
import urllib
import json
import time, threading

# open the file
f = open('ebay_product.csv','w', encoding="utf-8")
f.write('category_list_prefix,product_img_link,product_name,product_price,product_conditiion,product_condit_content,fullInfo,fullInfo_tracklist, product_number, product_specifics, product_description')

my_url = "https://www.ebay.co.uk/sch/musicmagpie/m.html?item=381550483752&hash=item58d62e5928%3Ag%3AYM8AAOSwuShaagkB&rt=nc&_trksid=p2047675.l2562"

# request part
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html page parser part
page_soup = soup(page_html, "html.parser")

# # get the detail of product
products_list = page_soup.findAll("li",{"class":"sresult lvresult clearfix li shic"})


for product in products_list:
  product_url = product.find("a",{"class":"img imgWr2"})['href']

  # uClient = uReq(product_url)
  uClient = uReq(product_url)
  page_html = uClient.read()
  uClient.close()

  product_content = soup(page_html, "html.parser")

  category_prefix = product_content.findAll("li",{"class":"bc-w"})
  category_list_prefix = category_prefix[0].text + " > " + category_prefix[1].text

  product_img_link = product_content.find('img',{"class":"img img300 vi-img-gallery-vertical-align"})['src']

  product_name = product_content.find('h1',{"class":"it-ttl"}).text.replace("Details about  ", "")
  product_condit = product_content.find('div',{"class":"u-flL condText"}).text
  product_condit_content=""
  if(product_content.find('span',{"class":"topItmCndDscMsg"}) != None):
    product_condit_content=product_content.find('span',{"class":"topItmCndDscMsg"}).text


  product_price = product_content.find("span",{"class":"notranslate"}).text


  # get product fullinfo
  product_fullInfo_url = product_content.find("iframe")["src"]

  product_fullInfo_page = requests.get(product_fullInfo_url)

  product_fullPage = soup(product_fullInfo_page.content, "html.parser")       

  product_fullInfo = product_fullPage.find(id = "fullInfo").findAll("span",{"class":"info"})
  product_fullContent=""
  for product_info in product_fullInfo:
    product_fullContent += product_info.text+","
  if(product_fullContent == ""):
    product_fullContent=product_fullPage.find(id = "fullInfo").p.text

  product_fullInfo_tracklist = ""
  if product_fullPage.find(id = "trackList") != None:
    product_fullInfo_tracklist =  re.sub("\s\s+"," ", product_fullPage.find(id = "trackList").text.replace("""Disc
    Track
    Title
    Duration""", ""))

  #get product description

  product_item_number = product_content.find("div",{"class":"u-flL iti-act-num itm-num-txt"}).text

  product_specifics = product_content.find("div",{"class":"itemAttr"}).findAll("table")
  product_specific = ""
  if(len(product_specifics) == 2): 
    product_specific = re.sub("\s\s+"," ", product_specifics[0].text + "," + product_specifics[1].text)
  else:
    product_specific =  re.sub("\s\s+"," ", product_specifics[0].text)

  product_description = ""
  if product_content.find("div",{"class":"prodDetailSec"}) != None:
    product_description=re.sub("\s\s+"," ", product_content.find("div",{"class":"prodDetailSec"}).find("table").text)
  f.write('\n')
  f.write(category_list_prefix + "," + product_img_link + "," + product_name + "," + product_price + "," + product_condit + "," + product_condit_content + "," + product_fullContent + "," + product_fullInfo_tracklist + "," + product_item_number + "," + product_specific + "," + product_description)