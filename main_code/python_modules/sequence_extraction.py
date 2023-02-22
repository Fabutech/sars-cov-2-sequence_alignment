from calendar import c
import json 
from datetime import datetime

from dna_to_amino import dna_to_amino

def time_now():
    return f"[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}]"

def read_json(path):
    with open(path) as json_file:
        file = json.load(json_file)
        json_file.close()
        return file

def read_file(path):
    fileObject = open(path, "r")
    data = fileObject.read()
    return data


def safe_to_txt(options, protein_sequences, number_of_sequences, date):
    now = datetime.now()

    safe_string = "" 
    safe_string += f"File created on: {now.day}.{now.month}.{now.year} {now.hour}:{now.minute}:{now.second}\n"
    safe_string += f"Inspected Protein: {options['protein_name']}\n"
    safe_string += f"Number of Sequences: {number_of_sequences}\n\n\n\n"

    for sequence_access_numb, sequence in protein_sequences.items():
        safe_string += f"Accession Numb: {sequence_access_numb}\n" 
        safe_string += f"Sequence Numb:  {sequence['seq_numb']}\n"
        safe_string += f"Release Date:   {sequence['release_date']}\n"
        safe_string += f"Lineage:        {sequence['lineage']}\n\n"
        

        safe_string += "DNA Sequence:\n"
        c = -1
        for char in sequence["dna_sequence"]:
            c += 1
            if c == 61:
                c = 0
                safe_string += "\n"
            safe_string += char   
        if c != 0:
            safe_string += "\n\n"   
        else:
            safe_string += "\n"

        safe_string += "AMINO Sequence:\n"
        c = -1
        for char in sequence["amino_sequence"]:
            c += 1
            if c == 61:
                c = 0
                safe_string += "\n"
            safe_string += char   
        if c != 0:
            safe_string += "\n\n"   
        else:
            safe_string += "\n"
        safe_string += "\n" 

    with open(f"{options['path_to_protseq_save']}{options['protein_name']}_{date}.txt", 'w') as f:
        f.write(safe_string)
        f.close()  

def safe_to_json(options, protein_sequences, date, original, prev_date):
    safe_json = {} 
    for sequence_access_numb, sequence in protein_sequences.items():
        safe_json[sequence_access_numb] = {}
        safe_json[sequence_access_numb]["seq_numb"] = sequence["seq_numb"]
        safe_json[sequence_access_numb]["release_date"] = sequence["release_date"]
        safe_json[sequence_access_numb]["collection_date"] = sequence["collection_date"]
        safe_json[sequence_access_numb]["lineage"] = sequence["lineage"]
        safe_json[sequence_access_numb]["dna_sequence"] = sequence["dna_sequence"]
        safe_json[sequence_access_numb]["amino_sequence"] = sequence["amino_sequence"]

    if original != "":
        prev_data = read_json(f"{options['path_to_protseq_save']}{options['protein_name']}_{prev_date}.json")
        safe_json[original] = prev_data[original]

    with open(f"{options['path_to_protseq_save']}{options['protein_name']}_{date}.json", 'w') as outfile:
        json.dump(safe_json, outfile) 
        outfile.close()    

def extract_dna_sequences(dna_sequence_data, access_numbs_of_sequence, protein_name):

    access_numbs_of_sequence = access_numbs_of_sequence.split("\n")[:-1]

    dna_sequences = dna_sequence_data.split(">")
    sequences = {}
    count = -1
    pol = False
    acc_rem = []
    for dna_sequence in dna_sequences:
        pro_name = dna_sequence.split("\n")[0]
        if not protein_name in pro_name and not "nucleocapsid protein" in pro_name: # and not "membrane protein" in pro_name and not "matrix protein" in pro_name:   ######!!!!!!!!!
            if "orf1ab" in pro_name.lower():
                if pol:
                    count += 1
                    try:
                        access_numbs_of_sequence[count]
                    except:
                        break
                    acc_rem.append(access_numbs_of_sequence[count])
                else:
                    pol = True
            
            continue

        count += 1
        pol = False

        seq_numb = dna_sequence.split(" ")[0] 

        info = pro_name.split("|")
        release_date = info[2].split("T")[0]
        collection_date = info[3]
        lineage = info[4]

        seq = dna_sequence.split("\n")[1:]
        seqq = ""
        for s in seq:
            #if s not in ["A", "G", "C", "T"]:
            #    s = "N"
            seqq += s
        try:
            sequences[access_numbs_of_sequence[count]] = {}
        except:
            continue
        sequences[access_numbs_of_sequence[count]]["seq_numb"] = seq_numb
        sequences[access_numbs_of_sequence[count]]["release_date"] = release_date
        sequences[access_numbs_of_sequence[count]]["collection_date"] = collection_date
        sequences[access_numbs_of_sequence[count]]["lineage"] = lineage
        sequences[access_numbs_of_sequence[count]]["dna_sequence"] = seqq

    return sequences, count+1, acc_rem



def main_extraction(options, date, original, prev_date):

    dna_sequence_data = read_file(options["path_to_raw_sequences"])
    full_accession_numbs = read_file(options["path_to_raw_accnumbs"])

    protein_sequences, number_of_sequences, acc_rem = extract_dna_sequences(dna_sequence_data, full_accession_numbs, options["protein_name"])

    for sequence_access_numb, dna_sequence in protein_sequences.items():
        amino_sequence = dna_to_amino(dna_sequence["dna_sequence"])
        protein_sequences[sequence_access_numb]["amino_sequence"] = amino_sequence

    if options["save_extracted_to_txt"]:
        safe_to_txt(options, protein_sequences, number_of_sequences, date)
  
    safe_to_json(options, protein_sequences, date, original, prev_date)
            
    return full_accession_numbs, number_of_sequences, acc_rem

if __name__ == "__main__":

    options = read_json("main_options.json")

    main_extraction(options)