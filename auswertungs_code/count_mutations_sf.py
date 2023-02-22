import xlrd
import pandas as pd 

# Give the location of the file
loc = input("Please enter the name of the file:\n")

df = pd.read_excel("/Users/fabutech/Documents/Schule/Matura_Arbeit/Alignment_Daten/Envelope/"+loc, sheet_name=0)

silent = df["Silent Mutations"][1:]
non_silent = df["Non Silent Mutations"][1:]


silent_mutations = {}

for mut in silent:
    if mut == "nan" or isinstance(mut, float) or mut.startswith("*"):
        continue
    mu = mut[:-1]
    if mu in silent_mutations:
        if mut[-1] in silent_mutations[mu]:
            silent_mutations[mu][mut[-1]] += 1
        else:
            silent_mutations[mu][mut[-1]] = 1
    else:
        silent_mutations[mu] = {mut[-1]: 1}

print("Silent Mutations:")
print(silent_mutations)

non_silent_mutations = {}

for mut in non_silent:
    if mut == "nan" or isinstance(mut, float):
        continue
    mu = mut[:-1]
    if mu in non_silent_mutations:
        if mut[-1] in non_silent_mutations[mu]:
            non_silent_mutations[mu][mut[-1]] += 1
        else:
            non_silent_mutations[mu][mut[-1]] = 1
    else:
        non_silent_mutations[mu] = {mut[-1]: 1}

print("Non Silent Mutations:")
print(non_silent_mutations)