from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import shutil
from os.path import exists
import json
from datetime import datetime

def time_now():
    return f"[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}]"

def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data

def download_data(search_date_from, search_date_to, options, driver):

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': options["path_to_download"]}}
    driver.execute("send_command", params)

    driver.get(f"https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=SARS-CoV-2,%20taxid:2697049&Completeness_s=complete&HostLineage_ss=Homo%20sapiens%20(human),%20taxid:9606&CreateDate_dt={search_date_from}T00:00:00.00Z%20TO%20{search_date_to}T23:59:59.00Z")
    sleep(0.2)

    # Download DNA-Sequences
    co = 0
    while True:
        co += 1
        try:
            driver.find_element(By.CLASS_NAME, "ncbi-report-download").click()
            break 
        except:
            if co == 5000:
                raise ValueError
            continue
    sleep(0.11)

    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/form/div/div[1]/div[2]").click()
    sleep(0.05) 
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/button").click()
    sleep(0.02)
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/button[2]").click()
    sleep(0.11) 
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/span[2]/form/div/div[2]").click() 
    sleep(0.08)

    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/span[2]/form/div/span/uswds-ncbi-app-custom-listbox/div/div[1]/div/ul/li[4]").click()
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/span[2]/form/div/span/uswds-ncbi-app-custom-listbox/div/div[1]/div/ul/li[23]").click()
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/span[2]/form/div/span/uswds-ncbi-app-custom-listbox/div/div[1]/div/ul/li[5]").click() 
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/span[2]/form/div/span/uswds-ncbi-app-custom-listbox/div/div[1]/div/ul/li[2]").click()
    sleep(0.03) 

    driver.find_element(By.NAME, "addBtn").click()
    sleep(0.12) 
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/span[2]/button[2]").click()


    # Download Accession numbers
    sleep(1.6) 
    driver.find_element(By.CLASS_NAME, "ncbi-report-download").click()
    sleep(0.12)

    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/form/div/div[2]/div[1]").click()
    sleep(0.05) 
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/button").click() 
    sleep(0.1) 
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/button[2]").click() 
    sleep(0.09) 
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/span[1]/form/div/div[1]").click() 
    sleep(0.25) 
    driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/uswds-ncbi-app-muti-step-form/div/div/div/span[1]/button[2]").click() 
    
    while True:
        if exists(f"{options['path_to_download']}sequences.fasta") and exists(f"{options['path_to_download']}sequences.acc"):
            break 
        sleep(0.3)
    shutil.move(f"{options['path_to_download']}sequences.fasta", f"{options['path_to_raw_save']}sequences.fasta")
    shutil.move(f"{options['path_to_download']}sequences.acc", f"{options['path_to_raw_save']}sequences.acc")




if __name__ == "__main__":
    options = read_json("sd_options.json")

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--disable-blink-features=AutomationControlled')
    driver_options.add_argument('log-level=OFF')
    driver_options.add_argument('--start-maximized')
    driver_options.add_experimental_option("prefs", {"download.default_directory": "/Users/fabutech/Downloads/","download.prompt_for_download": False,})
    if options["showBrowser"] == 0:
        driver_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)

    download_data("2022-05-20", "2022-05-23", options, driver)

    driver.close()