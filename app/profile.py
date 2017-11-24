from app import app
import requests
from bs4 import BeautifulSoup
from flask import jsonify
import string
import sys

@app.route('/')
@app.route('/get-countries')
def getCountries():
    countries = [] 
    req = requests.get('https://knoema.com/atlas')
    soup = BeautifulSoup(req.content, "lxml")
    parent_li_list = soup.find("div", id = "hash-country-profiles").find_all("div")[-1].find("ul").find_all("li", attrs={'class': None})
    print(parent_li_list[1].encode('ascii'))
    for li_ele in  parent_li_list:   
        country_name = li_ele.find("a")
        countries.append(country_name.string)
    return jsonify(countries)