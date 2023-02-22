import json

def get_data(file):
    with open(file) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data 

def dna_to_amino(dna_sequence):
    transcription_table = get_data("data_tables/dna_to_amino.json")
    nucletide_symbols = get_data("data_tables/nucleotide_symbols.json")
    dna_sequence = dna_sequence.upper()
    amino_sequence = ""
    c = 0 
    three = ""
    normal = ["A", "C", "T", "G"]
    pos = []
    for nucleotide in dna_sequence:
        c += 1
        if nucleotide not in normal:
            pos.append(c-1)
        three += nucleotide
        if c == 3:
            if len(pos) >= 2:
                amino_acid = "*"
            elif len(pos) == 1:
                ex = ""
                first = True

                for el in nucletide_symbols[three[pos[0]]]:
                    if first:
                        first = False
                        if pos[0] == 0:
                            ex = transcription_table[el + three[1:]]
                        elif pos[0] == 1:
                            ex = transcription_table[three[0] + el + three[2]]
                        else:
                            ex = transcription_table[three[:2] + el]
                        e = 0
                    else:
                        if pos[0] == 0:
                            e = transcription_table[el + three[1:]]
                        elif pos[0] == 1:
                            e = transcription_table[three[0] + el + three[2]]
                        else:
                            e = transcription_table[three[:2] + el]
                        if e != ex:
                            amino_acid = "*"
                            break
                amino_acid = ex
        
            else:
                amino_acid = transcription_table[three]
            if amino_acid == "END":
                return amino_sequence
            amino_sequence += amino_acid
            c = 0
            pos = []
            three = ""
    
    return amino_sequence

if __name__ == "__main__":
    dna_sequence = "ATGTTCCTTAAGCTAGTGGATGATCATGCTTTGATTGTTAATGTACTACTCTGGTGTGTGGTGCTTATAGTGATACTACTAGTGTGTATTACAATAATTAAACTAATTAAGCTTTGTTTCACTTGCCATATGTTTTGTAATAGAACAGTTTATGGCCCCATTAAAAATGTGTACCACATTTACCAATCATATATGCACATAGACCCTTTCCCTAAACGAGTTATTGATTTCTAA"

    transcription_table =get_data() 
    amino_sequence = dna_to_amino(dna_sequence, transcription_table)
    print(amino_sequence)