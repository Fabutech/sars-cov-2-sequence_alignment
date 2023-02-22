from Bio import Align

def bp_alignment(sequence1, sequence2):
    sequence1, sequence2 = sequence1.split("\n"), sequence2.split("\n")
    sequence1, sequence2 = "".join(sequence1), "".join(sequence2)

    #Check if algorithm is needed 
    if sequence1 == sequence2:
        return sequence1, "."*len(sequence1)

    aligner = Align.PairwiseAligner()
    aligner.query_gap_score = -2

    alignments = aligner.align(sequence1, sequence2)
    alignment = str(alignments[0])
    alignment = alignment.split("\n")
    al1, al2, al3 = alignment[0], alignment[1], alignment[2]
    aligned1, aligned2 = "", ""
    for i in range(len(al1)):
        if al2[i] == "|":
            aligned1 += al1[i]
            aligned2 += "." 
        elif al2[i] == ".": 
            aligned1 += al1[i] 
            aligned2 += al3[i] 
        elif al2[i] == "-":
            aligned1 += al1[i] 
            aligned2 += al3[i]
        else:
            print(alignment)
            raise ValueError("ALignment gave unexpected output!")
    
    return aligned1, aligned2