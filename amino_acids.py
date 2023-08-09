
all_aa = 'ACDEFGHIKLMNPQRSTVWY'

wt_seq = ['A', 'C', 'F', 'F', 'D', 'E', 'T', 'S', 'S', 'S']
mut_seq = ['A', 'C', 'E', 'F', 'E', 'E', 'F', 'S', 'H', 'S']

aa_dict = {
    "positive": [['R', 'H', 'K'], [1]],
    "negative": [['D', 'E'], [2]],
    "polar": [['A', 'V', 'I', 'L', 'M', 'F', 'Y', 'W'], [3]],
    "special": [['C', 'G', 'P'], [4]],
}

for x in aa_dict.values():
    aa = x[0]
    for a in aa:
        print(a)