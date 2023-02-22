from numpy import save
from biopython_alignment import bp_alignment
from datetime import datetime
import json
from tqdm import tqdm

def time_now():
    return f"[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}]"

def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data

def save_to_json(alignments, options, date):
    save_json = {} 
    for alignment in alignments:
        save_json[f"{alignment[0]}-{alignment[1]}"] = {}
        save_json[f"{alignment[0]}-{alignment[1]}"]["dna_q"] = alignment[2][0]
        save_json[f"{alignment[0]}-{alignment[1]}"]["dna_s"] = alignment[2][1]
        save_json[f"{alignment[0]}-{alignment[1]}"]["amino_q"] = alignment[2][2]
        save_json[f"{alignment[0]}-{alignment[1]}"]["amino_s"] = alignment[2][3]

    with open(f"{options['path_to_alignment_save']}{options['protein_name']}_{date}_alignments.json", 'w') as outfile:
        json.dump(save_json, outfile) 
        outfile.close()

def save_to_txt(alignments, options, date):
    now = datetime.now()

    save_string = "" 
    save_string += f"File created on: {now.day}.{now.month}.{now.year} {now.hour}:{now.minute}:{now.second}\n"
    save_string += f"Inspected Protein: {options['protein_name']}\n\n\n\n"

    for alignment in alignments:
        save_string += f"Sequences Aligned:  {alignment[0]} : {alignment[1]}\n\n" 
        save_string += f"DNA-Alignment\n"  
        save_string += f"{alignment[2][0]}\n"
        save_string += f"{alignment[2][1]}\n\n"
        save_string += f"AMINO-Alignment\n"  
        save_string += f"{alignment[2][2]}\n"
        save_string += f"{alignment[2][3]}\n\n\n"

    with open(f"{options['path_to_alignment_save']}{options['protein_name']}_{date}_alignments.txt", 'w') as f:
        f.write(save_string)
        f.close()  


def main_alignment(access_numbs, original, options, date):
    protein_sequences = read_json(f"{options['path_to_protseq_save']}{options['protein_name']}_{date}.json")

    alignments = []


    print(f"\nAlignment progress bar of {date}:")
    for i in tqdm(range(len(access_numbs))):
    #for i in range(len(access_numbs)):
        k = ["dna", "amino"]
        aligned = []
        for d_or_a in k:
            aligned1, aligned2 = bp_alignment(protein_sequences[original][f"{d_or_a}_sequence"], protein_sequences[access_numbs[i]][f"{d_or_a}_sequence"])
            aligned.append(aligned1)
            aligned.append(aligned2)
        
        alignments.append((original, access_numbs[i], aligned)) 
    
    print("")

    save_to_json(alignments, options, date)
    if options["save_aligned_to_txt"]:
        save_to_txt(alignments, options, date)
    

if __name__ == '__main__':
    main_alignment()