# ------------- Imports ------------- #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import time
# ------------- Variables ------------- #
base_url = 'http://envapp.maricopa.gov/EnvironmentalHealth/BusinessSearchResults?page='

csv_filename1 = r"C:\Users\Brian\Desktop\sous\proj1\Sous_Maricopa_County_Food_Permit_sheet1.csv"
csv_filename2 = r"C:\Users\Brian\Desktop\sous\proj1\Sous_Maricopa_County_Food_Permit_sheet2.csv"

csv1 = {
    "Col1" : "Permit_ID_Text",
    "Col2" : "Permit_ID_Link",
    "Col3" : "Permit_Type",
    "Col4" : "Business_Name",
    "Col5" : "Address",
    "Col6" : "Cutting_Edge_Participant"}

csv2 = {
    "Col1" : "Permit_ID_Text",
    "Col2" : "Permit_ID_Link",
    "Col3" : "Inspected_Date",
    "Col4" : "Purpose",
    "Col5" : "Grade",
    "Col6" : "Priority_Violation",
    "Col7" : "Cutting_Edge_Participant"}

# ------------- Functions ------------- #
def initialize_driver():
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def visit_url(driver, url):
    driver.get(url)

def quit_driver(driver):
    driver.quit()

def scrape_and_save_to_csv(driver, url, csv_filename):
    visit_url(driver, url)

    wait = WebDriverWait(driver, 30)  

    with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        row_count = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        for count in row_count:
            one_one_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[1]/a'
            one_two_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[2]'
            one_three_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[3]'
            one_four_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[4]/a'
            one_five_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[5]'

            permit_id_link_element = wait.until(EC.visibility_of_element_located((By.XPATH, one_one_xpath)))

            permit_id_text = permit_id_link_element.text
            permit_id_href = permit_id_link_element.get_attribute('href')

            permit_type = wait.until(EC.visibility_of_element_located((By.XPATH, one_two_xpath))).text
            business_name = wait.until(EC.visibility_of_element_located((By.XPATH, one_three_xpath))).text
            address = wait.until(EC.visibility_of_element_located((By.XPATH, one_four_xpath))).text
            cutting_edge_participant = wait.until(EC.visibility_of_element_located((By.XPATH, one_five_xpath))).text

            csv_writer.writerow([permit_id_text, permit_id_href, permit_type, business_name, address, cutting_edge_participant])

# ------------- Run Script ------------- #
if __name__ == "__main__":
    pass
    # driver = initialize_driver()

    # for page_number in range(0, 2675):
    #     url = f"{base_url}{page_number}"
    #     scrape_and_save_to_csv(driver, url, csv_filename1)

    # quit_driver(driver)