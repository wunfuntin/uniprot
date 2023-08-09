import requests
import json
import pandas as pd
import sys
import time


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


UNIPROT_ENDPOINT = 'https://rest.uniprot.org'
QUERY = 'gdf8'
EXPECTED_LENGTH = 375
MIN_SEQ_LENGTH = EXPECTED_LENGTH - (EXPECTED_LENGTH * 0.05)

# taxonomy_ids = {
#     'Homo sapiens': '9606',
#     'mus musculus': '10090',
#     'rat': '10114',
#     'cow': '9913',
#     'zebrafish': '7955',
#     'cat': '9685',
# }


df = pd.read_csv('species_dataset.csv',
                 usecols=['Taxon Id', 'Common name', 'Scientific name'])

result = df.to_dict(orient='records')

taxon_id_list = []
scientific_name_list = []

for ids in result:
    for key in ids:
        if key == 'Taxon Id':
            taxon_id = ids[key]
            taxon_id_list.append(taxon_id)
        if key == 'Scientific name':
            scientific_name = ids[key]
            scientific_name_list.append(scientific_name)

taxonomy_dict = dict(zip(scientific_name_list, taxon_id_list))


accession_list = []
accession_dict = {}

for taxid in taxonomy_dict.values():
    r = get_url(f"{UNIPROT_ENDPOINT}/uniprotkb/search?query={QUERY} AND (taxonomy_id: {taxid})")
    data = r.json()
    # n_results = len(data["results"])
    # print(f"Number of results: {n_results}\n")
    for sequences in data['results']:
        protein_existence = sequences['proteinExistence']

        if (protein_existence == '1: Evidence at protein level' or
                protein_existence == '2: Evidence at transcript level' or
                protein_existence == '3: Inferred from homology'):

            seq_len = int(sequences['sequence']['length'])
            # if sequences['entryType'] == 'UniProtKB reviewed (Swiss-Prot)':
                # name = [n for n, y, in taxonomy_ids.items() if y == taxid]
                # if sequences['organism']['scientificName'] == name[0]:
            if seq_len >= MIN_SEQ_LENGTH:
                accession_id = sequences['primaryAccession']
                sequence = sequences['sequence']
                accession_dict[accession_id] = sequence
                accession_list.append(sequences['primaryAccession'])
                break


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


while status_check():
    job_status = get_url(f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/{job_id}")
    time.sleep(5)
show_alignment()




