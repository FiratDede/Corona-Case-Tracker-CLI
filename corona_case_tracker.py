import requests
from bs4 import BeautifulSoup
import sys

url="https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?"

response=requests.get(url)
content_in_url=response.content
soup_object=BeautifulSoup(content_in_url,"html.parser")

countries=soup_object.find_all("a",{"class":"mt_a"})
simplified_countries=[]
all_cases=[]
country_with_case=[] 
for country in countries:
    if(country.text not in simplified_countries):
        simplified_countries.append(country.text)
        case_of_country=country.parent.next_sibling.next_sibling.text
        case_of_country=case_of_country.replace(",","")
        country_with_case.append((country.text,int(case_of_country)))

def sort_to_case(e):
    return e[1]
country_with_case.sort(reverse=True,key=sort_to_case)

def show_countries_with_cases_limit(limit=1):
    global country_with_case
    printed_amount=0
    print("{:25} {}".format("Countries","All Cases"))
    print(35*"-")
    for country,case_amount in country_with_case:
        print("{:27} {}".format(country,case_amount))
        print(35*"-")
        printed_amount+=1
        if(printed_amount==limit):
            return

def show_countries_with_cases():
    global country_with_case
    print("{:25} {}".format("Countries","All Cases"))
    print(35*"-")
    for country,case_amount in country_with_case:
        print("{:27} {}".format(country,case_amount))
        print(35*"-")
        
if(sys.argv[1]=="search"):
    if(len(sys.argv)==2):
        sys.stderr.write("Invalid arguments. Run this program with help argument for seeing appropriate arguments")
        sys.exit()
    wanted_country=""
    for i in range(2,len(sys.argv)):
        wanted_country+=sys.argv[i]
        wanted_country+=" "
    wanted_country=wanted_country.strip()
    dictionary_version=dict(country_with_case)
    dictionary_version_keys=list(dictionary_version.keys())
    for i in dictionary_version_keys:
        dictionary_version[i.lower()]=dictionary_version.pop(i)
    try:
        case_number=dictionary_version[wanted_country.lower()]
        print("There are {} cases in {}".format(case_number,wanted_country))
    except(KeyError):
        print("Country is not found")   

elif(len(sys.argv)==2):
    if(sys.argv[1]=="show"):
        show_countries_with_cases()
    elif(sys.argv[1]=="help"):
        print("All Commands")
        print("* show --all =  Show all countries with corona cases in descending order ")
        print("* show <number> = Show top <number> countries  with corona cases in descending order ")
        print("* search <country_name> = Show the total case of <country_name> ")
    else:
        sys.stderr.write("Invalid arguments. Run this program with help argument for seeing appropriate arguments")

elif(sys.argv[1]=="show"):
    if(sys.argv[2]=="--all"):
        show_countries_with_cases()
    elif(sys.argv[2].isnumeric()):
        if(int(sys.argv[2])>=len(country_with_case)):
            show_countries_with_cases()
        else:
            show_countries_with_cases_limit(int(sys.argv[2]))
    else:
        sys.stderr.write("Invalid arguments. Run this program with help argument for seeing appropriate arguments")

else:
    sys.stderr.write("Invalid arguments. Run this program with help argument for seeing appropriate arguments")