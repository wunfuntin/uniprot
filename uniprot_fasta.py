import requests
import sys

UNIPROT_ENDPOINT = 'https://rest.uniprot.org'

def get_url(url, **kwargs):
    response = requests.get(url, **kwargs)
    print(response.text)
    if not response.ok:
        print(response.text)
        response.raise_for_status()
        sys.exit()

    return response


r = get_url(f"{UNIPROT_ENDPOINT}/uniprotkb/Q8TEU8")
print(r.json()['sequence'])


