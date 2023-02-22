import json
from datetime import datetime
import xlsxwriter
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from time import sleep


def time_now():
    return f"[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}]"

def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data

def read_file(path):
    fileObject = open(path, "r")
    data = fileObject.read()
    return data

def read_alignment(options, date):
    alignments = read_json(f"{options['path_to_alignment_save']}{options['protein_name']}_{date}_alignments.json")

    mutation_data = {}

    for access, alignment in alignments.items():
        dna_q, dna_s, amino_q, amino_s = alignment["dna_q"], alignment["dna_s"], alignment["amino_q"], alignment["amino_s"]
        silent_mutations, non_silent_mutations = [], []
        
        for i in range(len(dna_q)):
            if dna_s[i] == ".":
                continue
            try:
                if amino_s[i//3] == ".":
                    if dna_s[i] not in ["A", "C", "T", "G"]:
                        continue
                    silent_mutations.append(f"{dna_q[i]}{i+1}{dna_s[i]}") 
                    continue 
            except:
                if i//3 == len(amino_q):
                    silent_mutations.append(f"{dna_q[i]}{i+1}{dna_s[i]}")
                    continue
                #print(access)
                #break
                raise ValueError

            if amino_q[i//3] == "*" or amino_s[i//3] == "*":
                silent_mutations.append(f"*{i+1}")
                continue
            non_silent_mutations.append(f"{dna_q[i]}{i+1}{dna_s[i]} ({amino_q[i//3]}{i//3+1}{amino_s[i//3]})")

        mutation_data[access] = {}
        mutation_data[access]["sil_mut"] = silent_mutations
        mutation_data[access]["non_sil_mut"] = non_silent_mutations
    
    return mutation_data

def save_mutation_data(mutation_data, options, date):
    workbook = xlsxwriter.Workbook(f"{options['path_to_final_save']}{options['protein_name']}_{date}.xlsx")
    worksheet = workbook.add_worksheet() 

    seq_data = read_json(f"{options['path_to_protseq_save']}{options['protein_name']}_{date}.json")

    headers = ["Accession1", "Accession2", "Silent Mutations", "Non Silent Mutations", "SeqNumb1", "SeqNumb2", "RelDate1", "RelDate2", "Pangolin1", "Pangolin2"]

    row, col = 0, 0
    for header in headers:
        worksheet.write(row, col, header) 
        col += 1
    
    row, col = 2, 0
    for accession, mutations in mutation_data.items():
        accession1, accession2 = accession.split("-")[0], accession.split("-")[1]
        s_mut, ns_mut = "", ""
        for mut in mutations["sil_mut"]:
            s_mut += f"{mut}, "
        for mut in mutations["non_sil_mut"]:
            ns_mut += f"{mut}, "
        if s_mut != "":
            s_mut = s_mut[:-2]
        if ns_mut != "":
            ns_mut = ns_mut[:-2]
        seqnumb1, seqnumb2 = seq_data[accession1]["seq_numb"], seq_data[accession2]["seq_numb"]
        reldate1, reldate2 = seq_data[accession1]["release_date"], seq_data[accession2]["release_date"]
        pangolin1, pangolin2 = seq_data[accession1]["lineage"], seq_data[accession2]["lineage"]
        elems = [accession1, accession2, s_mut, ns_mut, seqnumb1, seqnumb2, reldate1, reldate2, pangolin1, pangolin2]
        for elem in elems:
            worksheet.write(row, col, elem)
            col += 1

        col = 0
        row += 1

    worksheet.set_column(0, 9, 17)

    workbook.close()


if __name__ == "__main__":
    options = read_json("main_options.json")

    access_numbs = ()
    read_alignment(access_numbs, options)

    