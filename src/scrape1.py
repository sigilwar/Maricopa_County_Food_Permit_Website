# ------------- Imports ------------- #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
# ------------- Variables ------------- #
base_url = 'http://envapp.maricopa.gov/EnvironmentalHealth/BusinessSearchResults?page='
csv_filename1 = r"C:\Users\Brian\Desktop\sous\proj1\Sous_Maricopa_County_Food_Permit_sheet1.csv"
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
            permit_id_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[1]/a'
            permit_type_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[2]'
            business_name_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[3]'
            address_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[4]/a'
            cutting_edge_participant_xpath = f'//*[@id="colorMe"]/tbody/tr[{count}]/td[5]'

            permit_id_link_element = wait.until(EC.visibility_of_element_located((By.XPATH, permit_id_xpath)))

            permit_id_text = permit_id_link_element.text
            permit_id_href = permit_id_link_element.get_attribute('href')

            permit_type = wait.until(EC.visibility_of_element_located((By.XPATH, permit_type_xpath))).text
            business_name = wait.until(EC.visibility_of_element_located((By.XPATH, business_name_xpath))).text
            address = wait.until(EC.visibility_of_element_located((By.XPATH, address_xpath))).text
            cutting_edge_participant = wait.until(EC.visibility_of_element_located((By.XPATH, cutting_edge_participant_xpath))).text

            csv_writer.writerow([permit_id_text, permit_id_href, permit_type, business_name, address, cutting_edge_participant])

# ------------- Run Script ------------- #
if __name__ == "__main__":
    pass
    # driver = initialize_driver()

    # for page_number in range(0, 2675):
    #     url = f"{base_url}{page_number}"
    #     scrape_and_save_to_csv(driver, url, csv_filename1)

    # quit_driver(driver)