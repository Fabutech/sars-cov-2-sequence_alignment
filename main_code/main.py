# Import of own Modules
from re import A
from python_modules.sequence_download import download_data
from python_modules.sequence_extraction import main_extraction
from python_modules.sequence_alignment import main_alignment
from python_modules.alignment_reader import read_alignment, save_mutation_data

# Import of other Modules
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import os
from os.path import exists
import json
from datetime import datetime, date
import pandas
from tqdm import tqdm
import random

def time_now():
    return f"[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}]"

def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data

def main():
    print(f"{time_now()} Program successfully started")

    # Read main_options file
    print(f"{time_now()} Starting to read main_options file") 
    options = read_json("main_options.json")
    print(f"{time_now()} Successfully read main_options file")

    # Create the driver
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--disable-blink-features=AutomationControlled')
    driver_options.add_argument('log-level=OFF')
    driver_options.add_argument('--start-maximized')
    driver_options.add_experimental_option("prefs", {"download.default_directory": options["path_to_download"], "download.prompt_for_download": False,})
    if not options["showBrowser"]:
        driver_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)

    dates = [] 
    sdate, edate = date(options["date_from"][0], options["date_from"][1], options["date_from"][2]), date(options["date_to"][0], options["date_to"][1], options["date_to"][2])
    dates_raw = pandas.date_range(sdate,edate,freq='d')
    for d in dates_raw:
        dates.append(str(d).split(" ")[0])
    
    #print("\n\nProgress bar per day:")
    #for i in tqdm(range(len(dates))):
    original = ""
    or_date = "2022-03-23"
    for i in range(len(dates)):

        # Download sequences for specific day 
        print(f"\n{time_now()} Starting process for date: {dates[i]}")
        print(f"{time_now()} Starting to download sequences data from the NCBI Virus website")
        download_data(dates[i], dates[i], options, driver) 
        print(f"{time_now()} Successfully downloaded sequences data")
        
        # Extract wanted protein sequences from downloaded sequences
        #print(f"{time_now()} Starting with the protein sequences extraction process")
        if i != 0:
            access_numbs_of_sequences, number_of_sequences, acc_rem = main_extraction(options, dates[i], original, dates[i-1]) 
        else:
            access_numbs_of_sequences, number_of_sequences, acc_rem = main_extraction(options, dates[i], original, or_date) 
        access_numbs_of_sequences = access_numbs_of_sequences.split("\n")[:number_of_sequences]
        if access_numbs_of_sequences != []:
            if access_numbs_of_sequences[-1] == "":
                access_numbs_of_sequences = access_numbs_of_sequences[:-1]
        if original != "":
            access_numbs_of_sequences.append(original)
        for rem in acc_rem:
            print(f"Removed: {rem}")
            number_of_sequences -= 1
            access_numbs_of_sequences.remove(rem)
        #os.unlink(f"{options['path_to_raw_save']}sequences.fasta")
        #os.unlink(f"{options['path_to_raw_save']}sequences.acc")
        #print(f"{time_now()} Successfully extracted all protein sequences")
        # Sequence alignment 
        #print(f"{time_now()} Starting with the sequence alignment process")
        if len(access_numbs_of_sequences) > 1:
            original = access_numbs_of_sequences[0]
            access_numbs_of_sequences = access_numbs_of_sequences[1:] 
            if len(access_numbs_of_sequences) > options["random_per_day"] and options["pick_random"]:
                l = access_numbs_of_sequences[-1] 
                access_numbs_of_sequences = random.sample(access_numbs_of_sequences[:-1], options["random_per_day"]-1)
                access_numbs_of_sequences.append(l)

            main_alignment(access_numbs_of_sequences, original, options, dates[i]) 
            #print(f"{time_now()} Successfully aligned all sequences")

            print(f"{time_now()} Starting to read alignments")
            mutation_data = read_alignment(options, dates[i])
            print(f"{time_now()} Successfully read all alignments")

            print(f"{time_now()} Starting to save data")
            save_mutation_data(mutation_data, options, dates[i])
            print(f"{time_now()} Successfully saved all data")

            if options["delete_alignment_files"]:    
                os.unlink(f"{options['path_to_alignment_save']}{options['protein_name']}_{dates[i]}_alignments.json")
                if options["save_aligned_to_txt"]:
                    os.unlink(f"{options['path_to_alignment_save']}{options['protein_name']}_{dates[i]}_alignments.txt")

        else:
            print(f"{time_now()} No data found for this date")

        if i != 0:
            if options["delete_protseq_files"]:
                #print(f"{time_now()} Starting to delete protein sequences and alignment files")
                os.unlink(f"{options['path_to_protseq_save']}{options['protein_name']}_{dates[i-1]}.json")
                if options["save_extracted_to_txt"]:
                    os.unlink(f"{options['path_to_protseq_save']}{options['protein_name']}_{dates[i-1]}.txt")

        print(f"{time_now()} Successfully completed process for date {dates[i]}")

    
    if options["delete_protseq_files"]:
        os.unlink(f"{options['path_to_protseq_save']}{options['protein_name']}_{dates[i]}.json")
        if options["save_extracted_to_txt"]:
            os.unlink(f"{options['path_to_protseq_save']}{options['protein_name']}_{dates[i]}.txt")
    
    driver.close()

if __name__ == '__main__':
    main()


# ON573478