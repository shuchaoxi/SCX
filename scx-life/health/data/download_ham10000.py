"""Download HAM10000 dataset."""
# HAM10000 is available via kaggle or direct URL
# For now, write a script that uses the official source
import urllib.request
import zipfile
import os

def download_ham10000(data_dir='./data'):
    # HAM10000 metadata and images
    # Source: Harvard Dataverse
    print('HAM10000 requires manual download from:')
    print('https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T')
    print('Place the downloaded files in ./data/ham10000/')
    # Create placeholder
    os.makedirs(f'{data_dir}/ham10000', exist_ok=True)
    with open(f'{data_dir}/ham10000/README.md', 'w') as f:
        f.write('# HAM10000\nDownload from Harvard Dataverse\n')

if __name__ == '__main__':
    download_ham10000()
