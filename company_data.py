from flask import Flask, jsonify
import re
from bs4 import BeautifulSoup
import requests
import whois
from collections import OrderedDict
import urllib.parse
import os
from PIL import Image
import io
from selenium import webdriver


app = Flask(__name__)

'''@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name'''

@app.route('/<domain>')
def domain_name(domain):
    pre = "https://www."
    url = pre + domain
    # Send a GET request to the website and retrieve the HTML content
    response = requests.get(url)
    html = response.text

    # Use BeautifulSoup to parse the website's HTML code
    soup = BeautifulSoup(html, 'html.parser')

    # Find function is used to find a single element if there are more than once it always returns the first element.
    title = soup.find('title')  # place your html tagg in parentheses that you want to find from html.
    # print("Company name :", title.get_text())
    # title = whois.whois(domain)
    qwery = soup.find('h1')  # here i find first h1 tagg in my website using find operation.

    # use .text for extract only text without any html tags
    # print("Company tag :", qwery.text)

    # Use regular expressions to search for the Facebook, Twitter, and LinkedIn IDs
    facebook_id_regex = re.compile(r'(?:https?:\/\/)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?'
                                   r'(?:[\w\-]*\/)*([\w\-]*)')
    twitter_id_regex = re.compile(r'(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:'
                                  r'[\w\-]*\/)*([\w\-]*)')
    linkedin_id_regex = re.compile(r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/(?:(?:\w)*#!\/)?(?:company\/)'
                                   r'?(?:[\w\-]*\/)*([\w\-]*)')

    # Use the regex pattern to find all phone numbers in the source code
    pattern = r"(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}"
    # pattern = r"^[\.-)( ]*([0-9]{3})[\.-)( ]*([0-9]{3})[\.-)( ]*([0-9]{4})$"
    # pattern = r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}" \
              # r"[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))"
    phone_numbers = re.findall(pattern, html)
    phone_numbers = list(OrderedDict.fromkeys(phone_numbers))
    # Use the findall method to extract the IDs from the website's HTML code
    facebook_id = facebook_id_regex.findall(soup.prettify())
    twitter_id = twitter_id_regex.findall(soup.prettify())
    linkedin_id = linkedin_id_regex.findall(soup.prettify())

    # Use findall method to extract email address
    emailpattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
    emails = re.findall(emailpattern, html)

    '''
    # Extract the company name from the match
    print('Facebook ID:', facebook_id)
    print('Twitter ID:', twitter_id)
    print('LinkedIn ID:', linkedin_id)
    print('Phone numbers:', phone_numbers)
    print('Email:', emails)'''

    #return [title.get_text(), qwery.text,facebook_id,twitter_id,linkedin_id,phone_numbers, emails]
    return jsonify(ComapanyName = title.get_text(),
                   CompanyTitle = qwery.text,
                   FacebookID = facebook_id,
                   TwitterID = twitter_id,
                   LinkedinID = linkedin_id,
                   Phonenumbers = str(phone_numbers),
                   Email = emails)

@app.route('/logos/<website>')
def find_info(website):
    url = "https://logo.clearbit.com/" + website

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    # data = response.content
    # return data
    in_memory_file = io.BytesIO(response.content)
    im = Image.open(in_memory_file)
    data = im.show()
    return data

if __name__ == "__main__":
    app.run()