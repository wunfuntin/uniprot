import time

import requests
import sys
import json


UNIPROT_ENDPOINT = 'https://rest.uniprot.org'
SUBSTRING = 'WAP'
QUERY = 'wfikkn2'
EXPECTED_LENGTH = 571
MIN_SEQ_LENGTH = EXPECTED_LENGTH - (EXPECTED_LENGTH * 0.05)

def get_url(url, **kwargs):
    response = requests.get(url, **kwargs)
    if not response.ok:
        print(response.text)
        response.raise_for_status()
        sys.exit()

    return response

def status_check():
    if job_status.text == 'RUNNING' or job_status.text == 'QUEUED':
        print(job_status.text)
        return True

def show_alignment():
    alignment = get_url(f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/{job_id}/aln-clustal_num")
    print(alignment.text)

# r = get_url(f"{UNIPROT_ENDPOINT}/uniprotkb/Q8TEU8")
# print(r.json()['sequence'])

# r = get_url(f"{UNIPROT_ENDPOINT}/uniprotkb/search?query=wfikkn2 AND (taxonomy_id: 9606)")
r = get_url(f"{UNIPROT_ENDPOINT}/uniprotkb/stream?query={QUERY}")
data = r.json()

# print(json.dumps(r.json(), indent=2))

# print(r.json())
accession_list = []

accession_dict = {}
for protein_name in data['results']:
    protein_existence = protein_name['proteinExistence']
    # print(protein_existence)
    if (protein_existence == '1: Evidence at protein level' or
            protein_existence == '2: Evidence at transcript level' or
            protein_existence == '3: Inferred from homology'):

        seq_len = int(protein_name['sequence']['length'])
        if seq_len >= MIN_SEQ_LENGTH:
            accession_id = protein_name['primaryAccession']
            sequence = protein_name['sequence']
            accession_dict[accession_id] = sequence
            accession_list.append(protein_name['primaryAccession'])
            # seq_len_list.append(seq_len)

joined = ','.join(accession_list)
align_response = get_url(f"{UNIPROT_ENDPOINT}/uniprotkb/accessions?accessions={joined}&format=fasta")
fasta = align_response.text


response_alignment = requests.post("https://www.ebi.ac.uk/Tools/services/rest/clustalo/run", data={
    "email": "walker3@ucmail.uc.edu",
    "iterations": 0,
    "outfmt": "clustal_num",
    "order": "aligned",
    "sequence": fasta
})

job_id = response_alignment.text
job_status = get_url(f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/{job_id}")
print(response_alignment.text)
# time.sleep(60)
while status_check():
    job_status = get_url(f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/{job_id}")
    time.sleep(5)
show_alignment()
