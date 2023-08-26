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

def scrape_row_data(driver, permit_id_text):
    table_xpath = '//*[@id="colorMe"]'
    row_elements = driver.find_elements(By.XPATH, f'{table_xpath}/tbody/tr[position() > 1]')

    rows_data = []

    wait = WebDriverWait(driver, 60)

    for row_number, _ in enumerate(row_elements, start=2):
        inspected_date_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[1]/a'
        purpose_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[2]'
        grade_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[3]'
        priority_violation_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[4]'
        cutting_edge_participant_xpath = f'{table_xpath}/tbody/tr[{row_number}]/td[5]'

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
            'Permit_ID_Text': permit_id_text,
            'Inspected_Date': inspected_date_element.text,
            'Purpose': purpose_element.text,
            'Grade': grade_element.text,
            'Priority_Violation': priority_violation_element.text,
            'Cutting_Edge_Participant': cutting_edge_participant_element.get_attribute('src')
        }

        rows_data.append(row_data)

    return rows_data

def scrape_and_save_to_csv_parallel(driver, input_csv_path, output_csv_path, start_row=0, end_row=26733, batch_size=10):
    with open(input_csv_path, 'r') as input_csv_file, open(output_csv_path, 'a', newline='', encoding='utf-8') as output_csv_file:
        csv_reader = csv.DictReader(input_csv_file)
        fieldnames = csv_reader.fieldnames + ['Permit_ID_Text', 'Inspected_Date', 'Purpose', 'Grade', 'Priority_Violation', 'Cutting_Edge_Participant']
        csv_writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)

        for row_index, row in enumerate(csv_reader):
            if row_index < start_row:
                continue

            permit_id_text = row.get(next(iter(row)))
            permit_id_link = row.get('Permit_ID_Link')

            if permit_id_link:
                visit_url(driver, permit_id_link)
                row_data = scrape_row_data(driver, permit_id_text)
                if row_data:
                    for data in row_data:
                        csv_writer.writerow(data)

            if end_row is not None and row_index >= end_row:
                break

# ------------- Run Script ------------- #
if __name__ == "__main__":
    pass
    # driver = initialize_driver() 

    # try:
    #     scrape_and_save_to_csv_parallel(driver, input_csv_path, output_csv_path)
    # finally:
    #     quit_driver(driver)