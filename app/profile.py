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


@app.route('/get-details/<country_name>')
def getDetails(country_name):
    details = {}
    req = requests.get('https://knoema.com/atlas/'+country_name)
    soup = BeautifulSoup(req.content, "lxml")
    first_col = soup.find("div", {'class' : "facts"}).find_all("ul")[0].find_all("li", attrs = {'class' : None })
    details['president'] = first_col[0].find("span").find_next_siblings(text=True)[0].strip()
    details['prime_minister'] = first_col[1].find("span").find_next_siblings(text=True)[0].strip()
    details['capital'] = first_col[2].find("span").find_next_siblings(text=True)[0].strip()
    details['language'] = first_col[3].find("span").find_next_siblings(text=True)[0].strip()
    second_col =  soup.find("div", {'class' : "facts"}).find_all("ul")[1].find_all("li")
    details['population'] = second_col[0].find("span").find_next_siblings(text=True)[0].strip()
    details['area'] = second_col[1].find("span").find_next_siblings(text=True)[0].strip()
    details['GDP_per_capita'] = second_col[2].find("span").find_next_siblings(text=True)[0].strip()
    details['GDP_billion_current_US'] = second_col[3].find("span").find_next_siblings(text=True)[0].strip()
    details['GINI_index'] = second_col[4].find("span").find_next_siblings(text=True)[0].strip()
    details['business_rank'] = second_col[5].find("span").find_next_siblings(text=True)[0].strip()
    return jsonify(details)