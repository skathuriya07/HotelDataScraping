from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def linkedin_login():
    browser.get("https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fsearch%2Fresults%2Fcompanies%2F%3FcompanyHqGeo%3D%255B%2522105490917%2522%252C%2522101165590%2522%252C%2522103644278%2522%252C%2522101452733%2522%255D%26keywords%3Dhotel%2520management%2520software%26origin%3DFACETED_SEARCH%26sid%3Dv7*&fromSignIn=true&trk=cold_join_sign_in")
    username= browser.find_element(By.ID, "username")
    username.send_keys(email_input)
    time.sleep(3)
    password= browser.find_element(By.ID, "password")
    password.send_keys(pass_input)
    time.sleep(3)
    login_button = browser.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button').click()
    time.sleep(3)


def companies():
    companies_data = []
    links = set()
    for page in range(1,51,1): 
        url = 'https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22105490917%22%2C%22101165590%22%2C%22103644278%22%2C%22101452733%22%5D&keywords=hotel%20management%20software&origin=FACETED_SEARCH&page='+str(page)
        browser.get(url)
        allLinks = browser.find_elements(By.TAG_NAME, "a")
        for link in allLinks:
            company_link = link.get_attribute("href")
            if 'https://www.linkedin.com/company/' in str(company_link): 
                links.add(company_link)
    for company in links:
        url = company + 'about'
        browser.get(url)
        time.sleep(3)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        item = {} 
        try:
            item["Name"] = soup.find('h1').get_text()
        except:
            item["Name"] = "NA"
        try:
            item['website'] = soup.find("a", {"class": "link-without-visited-state"}).get('href')
        except:
            item["website"] = "NA"
        try:
            item['Company Size'] = soup.find("dd", {"class": "text-body-small t-black--light mb1"}).get_text()
        except:
            item["Company Size"] = "NA"
        try:
            item['Headquarter and Number of Offices'] = soup.find("h3", {"class": "t-20 t-bold"}).get_text()
        except:
            item["Headquarter and Number of Offices'"] = "NA"
        try:
            item['Products'] = soup.find_all("dd", {"class": "mb4 text-body-small t-black--light"})[-1].get_text()
        except:
            item["Products"] = "NA"
        companies_data.append(item)
        
        

    export_data(companies_data)
        
def export_data(data):
    df = pd.DataFrame(data)
    df.to_excel("Companies.xlsx")


email_input = input("Please enter yous LinkedIn Login Email: ")
pass_input = input("Please enter yous LinkedIn Login Password: ")
browser = webdriver.Chrome("chromedriver.exec")
linkedin_login()
companies()