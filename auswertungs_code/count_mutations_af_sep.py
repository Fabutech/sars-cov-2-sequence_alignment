import xlsxwriter
import pandas as pd 
from os import listdir
from os.path import isfile, join
from time import sleep
from copy import deepcopy

#original_dna_e = "ATGTACTCATTCGTTTCGGAAGAGACAGGTACGTTAATAGTTAATAGCGTACTTCTTTTTCTTGCTTTCGTGGTATTCTTGCTAGTTACACTAGCCATCCTTACTGCGCTTCGATTGTGTGCGTACTGCTGCAATATTGTTAACGTGAGTCTTGTAAAACCTTCTTTTTACGTTTACTCTCGTGTTAAAAATCTGAATTCTTCTAGAGTTCCTGATCTTCTGGTCTAA"
#original_amino_e = "MYSFVSEETGTLIVNSVLLFLAFVVFLLVTLAILTALRLCAYCCNIVNVSLVKPSFYVYSRVKNLNSSRVPDLLV"

#original_dna_m = "ATGGCAGATTCCAACGGTACTATTACCGTTGAAGAGCTTAAAAAGCTCCTTGAACAATGGAACCTAGTAATAGGTTTCCTATTCCTTACATGGATTTGTCTTCTACAATTTGCCTATGCCAACAGGAATAGGTTTTTGTATATAATTAAGTTAATTTTCCTCTGGCTGTTATGGCCAGTAACTTTAGCTTGTTTTGTGCTTGCTGCTGTTTACAGAATAAATTGGATCACCGGTGGAATTGCTATCGCAATGGCTTGTCTTGTAGGCTTGATGTGGCTCAGCTACTTCATTGCTTCTTTCAGACTGTTTGCGCGTACGCGTTCCATGTGGTCATTCAATCCAGAAACTAACATTCTTCTCAACGTGCCACTCCATGGCACTATTCTGACCAGACCGCTTCTAGAAAGTGAACTCGTAATCGGAGCTGTGATCCTTCGTGGACATCTTCGTATTGCTGGACACCATCTAGGACGCTGTGACATCAAGGACCTGCCTAAAGAAATCACTGTTGCTACATCACGAACGCTTTCTTATTACAAATTGGGAGCTTCGCAGCGTGTAGCAGGTGACTCAGGTTTTGCTGCATACAGTCGCTACAGGATTGGCAACTATAAATTAAACACAGACCATTCCAGTAGCAGTGACAATATTGCTTTGCTTGTACAGTAA"
#original_amino_m = "MADSNGTITVEELKKLLEQWNLVIGFLFLTWICLLQFAYANRNRFLYIIKLIFLWLLWPVTLACFVLAAVYRINWITGGIAIAMACLVGLMWLSYFIASFRLFARTRSMWSFNPETNILLNVPLHGTILTRPLLESELVIGAVILRGHLRIAGHHLGRCDIKDLPKEITVATSRTLSYYKLGASQRVAGDSGFAAYSRYRIGNYKLNTDHSSSSDNIALLVQ"

#original_dna_s = "ATGTTTGTTTTTCTTGTTTTATTGCCACTAGTCTCTAGTCAGTGTGTTAATCTTACAACCAGAACTCAATTACCCCCTGCATACACTAATTCTTTCACACGTGGTGTTTATTACCCTGACAAAGTTTTCAGATCCTCAGTTTTACATTCAACTCAGGACTTGTTCTTACCTTTCTTTTCCAATGTTACTTGGTTCCATGCTATACATGTCTCTGGGACCAATGGTACTAAGAGGTTTGATAACCCTGTCCTACCATTTAATGATGGTGTTTATTTTGCTTCCACTGAGAAGTCTAACATAATAAGAGGCTGGATTTTTGGTACTACTTTAGATTCGAAGACCCAGTCCCTACTTATTGTTAATAACGCTACTAATGTTGTTATTAAAGTCTGTGAATTTCAATTTTGTAATGATCCATTTTTGGGTGTTTATTACCACAAAAACAACAAAAGTTGGATGGAAAGTGAGTTCAGAGTTTATTCTAGTGCGAATAATTGCACTTTTGAATATGTCTCTCAGCCTTTTCTTATGGACCTTGAAGGAAAACAGGGTAATTTCAAAAATCTTAGGGAATTTGTGTTTAAGAATATTGATGGTTATTTTAAAATATATTCTAAGCACACGCCTATTAATTTAGTGCGTGATCTCCCTCAGGGTTTTTCGGCTTTAGAACCATTGGTAGATTTGCCAATAGGTATTAACATCACTAGGTTTCAAACTTTACTTGCTTTACATAGAAGTTATTTGACTCCTGGTGATTCTTCTTCAGGTTGGACAGCTGGTGCTGCAGCTTATTATGTGGGTTATCTTCAACCTAGGACTTTTCTATTAAAATATAATGAAAATGGAACCATTACAGATGCTGTAGACTGTGCACTTGACCCTCTCTCAGAAACAAAGTGTACGTTGAAATCCTTCACTGTAGAAAAAGGAATCTATCAAACTTCTAACTTTAGAGTCCAACCAACAGAATCTATTGTTAGATTTCCTAATATTACAAACTTGTGCCCTTTTGGTGAAGTTTTTAACGCCACCAGATTTGCATCTGTTTATGCTTGGAACAGGAAGAGAATCAGCAACTGTGTTGCTGATTATTCTGTCCTATATAATTCCGCATCATTTTCCACTTTTAAGTGTTATGGAGTGTCTCCTACTAAATTAAATGATCTCTGCTTTACTAATGTCTATGCAGATTCATTTGTAATTAGAGGTGATGAAGTCAGACAAATCGCTCCAGGGCAAACTGGAAAGATTGCTGATTATAATTATAAATTACCAGATGATTTTACAGGCTGCGTTATAGCTTGGAATTCTAACAATCTTGATTCTAAGGTTGGTGGTAATTATAATTACCTGTATAGATTGTTTAGGAAGTCTAATCTCAAACCTTTTGAGAGAGATATTTCAACTGAAATCTATCAGGCCGGTAGCACACCTTGTAATGGTGTTGAAGGTTTTAATTGTTACTTTCCTTTACAATCATATGGTTTCCAACCCACTAATGGTGTTGGTTACCAACCATACAGAGTAGTAGTACTTTCTTTTGAACTTCTACATGCACCAGCAACTGTTTGTGGACCTAAAAAGTCTACTAATTTGGTTAAAAACAAATGTGTCAATTTCAACTTCAATGGTTTAACAGGCACAGGTGTTCTTACTGAGTCTAACAAAAAGTTTCTGCCTTTCCAACAATTTGGCAGAGACATTGCTGACACTACTGATGCTGTCCGTGATCCACAGACACTTGAGATTCTTGACATTACACCATGTTCTTTTGGTGGTGTCAGTGTTATAACACCAGGAACAAATACTTCTAACCAGGTTGCTGTTCTTTATCAGGATGTTAACTGCACAGAAGTCCCTGTTGCTATTCATGCAGATCAACTTACTCCTACTTGGCGTGTTTATTCTACAGGTTCTAATGTTTTTCAAACACGTGCAGGCTGTTTAATAGGGGCTGAACATGTCAACAACTCATATGAGTGTGACATACCCATTGGTGCAGGTATATGCGCTAGTTATCAGACTCAGACTAATTCTCCTCGGCGGGCACGTAGTGTAGCTAGTCAATCCATCATTGCCTACACTATGTCACTTGGTGCAGAAAATTCAGTTGCTTACTCTAATAACTCTATTGCCATACCCACAAATTTTACTATTAGTGTTACCACAGAAATTCTACCAGTGTCTATGACCAAGACATCAGTAGATTGTACAATGTACATTTGTGGTGATTCAACTGAATGCAGCAATCTTTTGTTGCAATATGGCAGTTTTTGTACACAATTAAACCGTGCTTTAACTGGAATAGCTGTTGAACAAGACAAAAACACCCAAGAAGTTTTTGCACAAGTCAAACAAATTTACAAAACACCACCAATTAAAGATTTTGGTGGTTTTAATTTTTCACAAATATTACCAGATCCATCAAAACCAAGCAAGAGGTCATTTATTGAAGATCTACTTTTCAACAAAGTGACACTTGCAGATGCTGGCTTCATCAAACAATATGGTGATTGCCTTGGTGATATTGCTGCTAGAGACCTCATTTGTGCACAAAAGTTTAACGGCCTTACTGTTTTGCCACCTTTGCTCACAGATGAAATGATTGCTCAATACACTTCTGCACTGTTAGCGGGTACAATCACTTCTGGTTGGACCTTTGGTGCAGGTGCTGCATTACAAATACCATTTGCTATGCAAATGGCTTATAGGTTTAATGGTATTGGAGTTACACAGAATGTTCTCTATGAGAACCAAAAATTGATTGCCAACCAATTTAATAGTGCTATTGGCAAAATTCAAGACTCACTTTCTTCCACAGCAAGTGCACTTGGAAAACTTCAAGATGTGGTCAACCAAAATGCACAAGCTTTAAACACGCTTGTTAAACAACTTAGCTCCAATTTTGGTGCAATTTCAAGTGTTTTAAATGATATCCTTTCACGTCTTGACAAAGTTGAGGCTGAAGTGCAAATTGATAGGTTGATCACAGGCAGACTTCAAAGTTTGCAGACATATGTGACTCAACAATTAATTAGAGCTGCAGAAATCAGAGCTTCTGCTAATCTTGCTGCTACTAAAATGTCAGAGTGTGTACTTGGACAATCAAAAAGAGTTGATTTTTGTGGAAAGGGCTATCATCTTATGTCCTTCCCTCAGTCAGCACCTCATGGTGTAGTCTTCTTGCATGTGACTTATGTCCCTGCACAAGAAAAGAACTTCACAACTGCTCCTGCCATTTGTCATGATGGAAAAGCACACTTTCCTCGTGAAGGTGTCTTTGTTTCAAATGGCACACACTGGTTTGTAACACAAAGGAATTTTTATGAACCACAAATCATTACTACAGACAACACATTTGTGTCTGGTAACTGTGATGTTGTAATAGGAATTGTCAACAACACAGTTTATGATCCTTTGCAACCTGAATTAGACTCATTCAAGGAGGAGTTAGATAAATATTTTAAGAATCATACATCACCAGATGTTGATTTAGGTGACATCTCTGGCATTAATGCTTCAGTTGTAAACATTCAAAAAGAAATTGACCGCCTCAATGAGGTTGCCAAGAATTTAAATGAATCTCTCATCGATCTCCAAGAACTTGGAAAGTATGAGCAGTATATAAAATGGCCATGGTACATTTGGCTAGGTTTTATAGCTGGCTTGATTGCCATAGTAATGGTGACAATTATGCTTTGCTGTATGACCAGTTGCTGTAGTTGTCTCAAGGGCTGTTGTTCTTGTGGATCCTGCTGCAAATTTGATGAAGACGACTCTGAGCCAGTGCTCAAAGGAGTCAAATTACATTACACATAA"  
#original_amino_s = "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPRRARSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCCSCLKGCCSCGSCCKFDEDDSEPVLKGVKLHYT"

original_dna = "ATGTCTGATAATGGACCCCAAAATCAGCGAAATGCACCCCGCATTACGTTTGGTGGACCCTCAGATTCAACTGGCAGTAACCAGAATGGAGAACGCAGTGGGGCGCGATCAAAACAACGTCGGCCCCAAGGTTTACCCAATAATACTGCGTCTTGGTTCACCGCTCTCACTCAACATGGCAAGGAAGACCTTAAATTCCCTCGAGGACAAGGCGTTCCAATTAACACCAATAGCAGTCCAGATGACCAAATTGGCTACTACCGAAGAGCTACCAGACGAATTCGTGGTGGTGACGGTAAAATGAAAGATCTCAGTCCAAGATGGTATTTCTACTACCTAGGAACTGGGCCAGAAGCTGGACTTCCCTATGGTGCTAACAAAGACGGCATCATATGGGTTGCAACTGAGGGAGCCTTGAATACACCAAAAGATCACATTGGCACCCGCAATCCTGCTAACAATGCTGCAATCGTGCTACAACTTCCTCAAGGAACAACATTGCCAAAAGGCTTCTACGCAGAAGGGAGCAGAGGCGGCAGTCAAGCCTCTTCTCGTTCCTCATCACGTAGTCGCAACAGTTCAAGAAATTCAACTCCAGGCAGCAGTAGGGGAACTTCTCCTGCTAGAATGGCTGGCAATGGCGGTGATGCTGCTCTTGCTTTGCTGCTGCTTGACAGATTGAACCAGCTTGAGAGCAAAATGTCTGGTAAAGGCCAACAACAACAAGGCCAAACTGTCACTAAGAAATCTGCTGCTGAGGCTTCTAAGAAGCCTCGGCAAAAACGTACTGCCACTAAAGCATACAATGTAACACAAGCTTTTGGCAGACGTGGTCCAGAACAAACCCAAGGAAATTTTGGGGACCAGGAACTAATCAGACAAGGAACTGATTACAAACATTGGCCGCAAATTGCACAATTTGCCCCCAGCGCTTCAGCGTTCTTCGGAATGTCGCGCATTGGCATGGAAGTCACACCTTCGGGAACGTGGTTGACCTACACAGGTGCCATCAAATTGGATGACAAAGATCCAAATTTCAAAGATCAAGTCATTTTGCTGAATAAGCATATTGACGCATACAAAACATTCCCACCAACAGAGCCTAAAAAGGACAAAAAGAAGAAGGCTGATGAAACTCAAGCCTTACCGCAGAGACAGAAGAAACAGCAAACTGTGACTCTTCTTCCTGCTGCAGATTTGGATGATTTCTCCAAACAATTGCAACAATCCATGAGCAGTGCTGACTCAACTCAGGCCTAA"
original_amino = "MSDNGPQNQRNAPRITFGGPSDSTGSNQNGERSGARSKQRRPQGLPNNTASWFTALTQHGKEDLKFPRGQGVPINTNSSPDDQIGYYRRATRRIRGGDGKMKDLSPRWYFYYLGTGPEAGLPYGANKDGIIWVATEGALNTPKDHIGTRNPANNAAIVLQLPQGTTLPKGFYAEGSRGGSQASSRSSSRSRNSSRNSTPGSSRGTSPARMAGNGGDAALALLLLDRLNQLESKMSGKGQQQQGQTVTKKSAAEASKKPRQKRTATKAYNVTQAFGRRGPEQTQGNFGDQELIRQGTDYKHWPQIAQFAPSASAFFGMSRIGMEVTPSGTWLTYTGAIKLDDKDPNFKDQVILLNKHIDAYKTFPPTEPKKDKKKKADETQALPQRQKKQQTVTLLPAADLDDFSKQLQQSMSSADSTQA"

path = "/Users/fabutech/Documents/Schule/Matura_Arbeit/Alignment_Daten/Nucleocapsid/"
path_safe = "/Users/fabutech/Documents/Schule/Matura_Arbeit/Alignment_Daten/Auswertung_aktuell/"

files = [f for f in listdir(path) if isfile(join(path, f))]

files = sorted(files)[1:]

data_s = {}
data_ns = {}

for file in files:
    name = file.split(" ")[1].split("_")[1].split(".")[0]

    df = pd.read_excel(path+file, sheet_name=0)

    silent = df["Silent Mutations"][1:]
    non_silent = df["Non Silent Mutations"][1:]

    data_s_cop = deepcopy(data_s)

    for mutt in silent:
        for mut in str(mutt).split(", "):
            p = False
            if mut == "nan" or isinstance(mut, float) or mut.startswith("*") or mut[0] not in ["A", "T", "G", "C"] or mut[-1] not in ["A", "T", "G", "C"]:
                continue
            if int(mut[1:-1]) not in data_s:
                data_s[int(mut[1:-1])] = [1, mut[0], mut[-1]] 
                continue
            if mut[0] not in data_s[int(mut[1:-1])]:
                data_s[int(mut[1:-1])].append(mut[0])
                if not p:
                    data_s[int(mut[1:-1])][0] += 1
                p = True
            if mut[-1] not in data_s[int(mut[1:-1])]:
                data_s[int(mut[1:-1])].append(mut[-1]) 
                if not p:
                    data_s[int(mut[1:-1])][0] += 1
            elif mut[0] in data_s[int(mut[1:-1])] or mut[-1] in data_s[int(mut[1:-1])]:
                if not p:
                    data_s[int(mut[1:-1])][0] += 1

    for key, elem in data_s.items():
        if key in data_s_cop.keys():

            if (elem[0] - data_s_cop[key][0]) > len(silent)//2 and len(silent) > 20:
                #print(data_s[key])
                #print(elem[0] - data_s_cop[key][0])
                data_s[key][0] = data_s_cop[key][0] + (len(silent) - (elem[0] - data_s_cop[key][0]))
                #print(data_s[key])
                #print(elem[0] - data_s_cop[key][0])
                #print(len(silent))
        else:
            if elem[0] > len(silent)//2 and len(silent) > 20:
                #print(data_s[key])
                data_s[key][0] = len(silent)-elem[0]
                #print(data_s[key])
                #print(len(silent))

    """
    data_ns_cop = deepcopy(data_ns)

    for mutt in non_silent:
        hh = []
        for mut in str(mutt).split(", "):
            p = False
            if mut == "nan" or isinstance(mut, float) or mut.startswith("*"):
                continue
            mut1, mut = mut.split(" ")[0], mut.split(" ")[1][1:-1]

            if mut[1:-1] in hh:
                p = True
            hh.append(mut[1:-1])

            if mut1[0] not in ["A", "T", "G", "C"] or mut1[-1] not in ["A", "T", "G", "C"]:
                continue
            #print(mut1, mut)
            if int(mut[1:-1]) not in data_ns:
                #print(1.1)
                data_ns[int(mut[1:-1])] = [1, mut[0], mut[-1]] 
                continue
            if mut[0] not in data_ns[int(mut[1:-1])]:
                #print(2)
                data_ns[int(mut[1:-1])].append(mut[0])
                if not p:
                    data_ns[int(mut[1:-1])][0] += 1
                p = True
            if mut[-1] not in data_ns[int(mut[1:-1])]:
                #print(3)
                data_ns[int(mut[1:-1])].append(mut[-1])
                if not p: 
                    #print(3.1)
                    data_ns[int(mut[1:-1])][0] += 1
            elif mut[0] in data_ns[int(mut[1:-1])] or mut[-1] in data_ns[int(mut[1:-1])]:
                #print(4)
                if not p:
                    #print(4.1)
                    data_ns[int(mut[1:-1])][0] += 1

    for key, elem in data_ns.items():
        if key in data_ns_cop.keys():

            if elem[0] - data_ns_cop[key][0] > len(silent): 
                #print(elem[0], data_ns_cop[key][0], len(non_silent), key, elem)
                #print(file)
                raise ValueError

            if (elem[0] - data_ns_cop[key][0]) > len(silent)//2 and len(silent) > 20:
                #print(data_ns[key])
                #print(elem[0] - data_ns_cop[key][0])
                #print(1, ":", key, ":", data_ns_cop[key][0] + (len(silent) - (elem[0] - data_ns_cop[key][0])))
                data_ns[key][0] = data_ns_cop[key][0] + (len(silent) - (elem[0] - data_ns_cop[key][0]))
                #print(data_ns[key])
                #print(elem[0] - data_ns_cop[key][0])
                #print(len(non_silent))
        else:
            if elem[0] > len(silent)//2 and len(silent) > 20:
                #print(data_ns[key])
                data_ns[key][0] = len(silent)-elem[0]
                #print(2, ":", len(silent)-elem[0])
                #print(data_ns[key])
                #print(len(non_silent))"""
    
    data_ns_cop = deepcopy(data_ns)

    for mutt in non_silent:
        for mut in str(mutt).split(", "):
            mut = mut.split(" ")[0]
            p = False
            if mut == "nan" or isinstance(mut, float) or mut.startswith("*") or mut[0] not in ["A", "T", "G", "C"] or mut[-1] not in ["A", "T", "G", "C"]:
                continue
            if int(mut[1:-1]) not in data_ns:
                data_ns[int(mut[1:-1])] = [1, mut[0], mut[-1]] 
                continue
            if mut[0] not in data_ns[int(mut[1:-1])]:
                data_ns[int(mut[1:-1])].append(mut[0])
                if not p:
                    data_ns[int(mut[1:-1])][0] += 1
                p = True
            if mut[-1] not in data_ns[int(mut[1:-1])]:
                data_ns[int(mut[1:-1])].append(mut[-1]) 
                if not p:
                    data_ns[int(mut[1:-1])][0] += 1
            elif mut[0] in data_ns[int(mut[1:-1])] or mut[-1] in data_ns[int(mut[1:-1])]:
                if not p:
                    data_ns[int(mut[1:-1])][0] += 1

    for key, elem in data_ns.items():
        if key in data_ns_cop.keys():

            if (elem[0] - data_ns_cop[key][0]) > len(silent)//2 and len(silent) > 20:
                #print(data_s[key])
                #print(elem[0] - data_s_cop[key][0])
                data_ns[key][0] = data_ns_cop[key][0] + (len(silent) - (elem[0] - data_ns_cop[key][0]))
                #print(data_s[key])
                #print(elem[0] - data_s_cop[key][0])
                #print(len(silent))
        else:
            if elem[0] > len(silent)//2 and len(silent) > 20:
                #print(data_s[key])
                data_ns[key][0] = len(silent)-elem[0]
                #print(data_s[key])
                #print(len(silent))

#print(dict(sorted(data_ns.items())))

data_ns = dict(sorted(data_ns.items()))
data_s = dict(sorted(data_s.items()))
#print(data_s)



"""
workbook = xlsxwriter.Workbook(f"{path_safe}index_diversity_envelope_silent_oo1_test.xlsx")
worksheet = workbook.add_worksheet() 

headers = ["Stelle", "1", "2", "3", "4", "muts"]

row, col = 0, 0
for header in headers:
    worksheet.write(row, col, header) 
    col += 1

row, col = 0, 0
for i in range(len(original_dna)):
    row += 1
    col = 0
    worksheet.write(row, col, i+1)
    try:
        data_s[i+1]
        col += 1
        worksheet.write(row, col, original_dna[i])
        for t in data_s[i+1][1:]:
            if t != original_dna[i] and t != "-" and t in ["A", "T", "G", "C"]:
                col += 1
                worksheet.write(row, col, t)
        worksheet.write(row, 5, data_s[i+1][0])
    except:
        col += 1
        worksheet.write(row, col, original_dna[i])

workbook.close()"""


workbook = xlsxwriter.Workbook(f"{path_safe}index_diversity_nucleocapsid_nonSilent_dna_oo.xlsx")
worksheet = workbook.add_worksheet() 

headers = ["Stelle", "1", "2", "3", "4", "muts"]

row, col = 0, 0
for header in headers:
    worksheet.write(row, col, header) 
    col += 1

row, col = 0, 0
for i in range(len(original_dna)):
    row += 1
    col = 0
    worksheet.write(row, col, i+1)
    try:
        data_ns[i+1]
        col += 1
        worksheet.write(row, col, original_dna[i])
        for t in data_ns[i+1][1:]:
            if t != original_dna[i] and t != "-": #and t in ["A", "T", "G", "C"]:
                col += 1
                worksheet.write(row, col, t)
        worksheet.write(row, 5, data_ns[i+1][0])
    except:
        col += 1
        worksheet.write(row, col, original_dna[i])

workbook.close()