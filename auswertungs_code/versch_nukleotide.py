import pandas as pd 
import xlsxwriter

path = "/Users/fabutech/Documents/Schule/Matura_Arbeit/Alignment_Daten/Auswertung_aktuell/"
file = input()

df = pd.read_excel(path+file, sheet_name=0)

stelle = df["Stelle"]
s1, s2, s3, s4 = df["1"], df["2"], df["3"], df["4"]

for i in range(len(stelle)):
    try:
        int(stelle[i])
    except:
        stelle = stelle[:i]
        break

versch_nuc = []
for i in range(len(stelle)):
    c = 0
    if s1[i] in ["A", "G", "T", "C"]:
        c += 1
    if s2[i] in ["A", "G", "T", "C"]:
        c += 1
    if s3[i] in ["A", "G", "T", "C"]:
        c += 1
    if s4[i] in ["A", "G", "T", "C"]:
        c += 1
    
    versch_nuc.append(c) 

workbook = xlsxwriter.Workbook(f"{path}Nucleocapsid_nonSilent_diffNuc.xlsx")
worksheet = workbook.add_worksheet() 

headers = ["Stelle", "Anzahl Versch Nukleotide"]

row, col = 0, 0
for header in headers:
    worksheet.write(row, col, header) 
    col += 1

row = 0
for i in range(len(stelle)):
    row += 1
    worksheet.write(row, 0, stelle[i]) 
    worksheet.write(row, 1, versch_nuc[i])

workbook.close()