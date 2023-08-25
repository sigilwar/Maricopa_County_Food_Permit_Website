# ------------- Imports ------------- #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
# ------------- Variables ------------- #
input_csv_path = r'C:\Users\Brian\Desktop\sous\Maricopa County Food Permit Website\Sous_Maricopa_County_Food_Permit_sheet1.csv'
output_csv_path = r'C:\Users\Brian\Desktop\sous\Maricopa County Food Permit Website\Sous_Maricopa_County_Food_Permit_sheet2.csv'
# ------------- Functions ------------- #
def initialize_driver():
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def visit_url(driver, url):
    driver.get(url)

def quit_driver(driver):
    driver.quit()

def scrape_row_data(driver):
    table_xpath = '//*[@id="colorMe"]'
    row_elements = driver.find_elements(By.XPATH, f'{table_xpath}/tbody/tr[position() > 1]')

    rows_data = []

    wait = WebDriverWait(driver, 30)

    for row_number, _ in enumerate(row_elements, start=2):
        permit_id_text_xpath = '/html/body/div[2]/div[1]/h2[2]'
        inspected_date_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[1]/a'
        purpose_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[2]'
        grade_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[3]'
        priority_violation_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[4]'
        cutting_edge_participant_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[5]'

        permit_id_text_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, permit_id_text_xpath))
        )
        inspected_date_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, inspected_date_xpath))
        )
        purpose_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, purpose_xpath))
        )
        grade_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, grade_xpath))
        )
        priority_violation_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, priority_violation_xpath))
        )
        cutting_edge_participant_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, cutting_edge_participant_xpath))
        )

        row_data = {
            'Permit_ID_Text': permit_id_text_element.text,
            'Inspected_Date': inspected_date_element.text,
            'Purpose': purpose_element.text,
            'Grade': grade_element.text,
            'Priority_Violation': priority_violation_element.text,
            'Cutting_Edge_Participant': cutting_edge_participant_element.get_attribute('src')
        }

        rows_data.append(row_data)

    return rows_data

def scrape_and_save_to_csv_parallel(driver, input_csv_path, output_csv_path, batch_size=10):
    with open(input_csv_path, 'r') as input_csv_file, open(output_csv_path, 'a', newline='', encoding='utf-8') as output_csv_file:
        csv_reader = csv.DictReader(input_csv_file)
        fieldnames = csv_reader.fieldnames + ['Permit_ID_Text', 'Inspected_Date', 'Purpose', 'Grade', 'Priority_Violation', 'Cutting_Edge_Participant']
        csv_writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)

        for _, row in enumerate(csv_reader):
            permit_id_link = row.get('Permit_ID_Link')
            if permit_id_link:
                visit_url(driver, permit_id_link)
                row_data = scrape_row_data(driver)
                if row_data:
                    for data in row_data:
                        csv_writer.writerow(data)

# ------------- Run Script ------------- #
if __name__ == "__main__":
    driver = initialize_driver()

    try:
        scrape_and_save_to_csv_parallel(driver, input_csv_path, output_csv_path)
    finally:
        quit_driver(driver)