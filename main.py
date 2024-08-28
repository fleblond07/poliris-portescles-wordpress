from ftplib import FTP
import os
import json
import secrets
import wget
import zipfile
import pandas as pd
from pandas.errors import EmptyDataError

def download_file(url, name):
    url = f'https://www.lesportescles.com/agents/{url}.poliris'
    wget.download(url, f'{name}.zip')
    with zipfile.ZipFile(f'{name}.zip', 'r') as zip_ref:
        zip_ref.extractall()

def replace_separator(file_name, initial_separator, new_separator):
    text = open(f'{file_name}.csv', "r")
    text = ''.join([i for i in text]) \
        .replace(initial_separator, new_separator)
    x = open(f'{file_name}_sandr.csv',"w")
    x.writelines(text)
    x.close()

def manipulate_file(filename):
    try:
        df = pd.read_csv(f'{filename}', sep=';' , on_bad_lines='skip', dtype=str, header=None)
        df.iloc[:,32] = df.iloc[:,32].replace("128", 'Radiator')
        df.iloc[:,32] = df.iloc[:,32].replace("256", 'Floor')
        df.iloc[:,32] = df.iloc[:,32].replace("512", 'Gas')
        df.iloc[:,32] = df.iloc[:,32].replace("1024", 'Fuel')
        df.iloc[:,32] = df.iloc[:,32].replace("2048", 'Electric')
        df.iloc[:,32] = df.iloc[:,32].replace("4096", 'Collective')
        df.iloc[:,32] = df.iloc[:,32].replace("8192", 'Individual')
        df.iloc[:,32] = df.iloc[:,32].replace("16384", 'Reversible air conditioning')

        df.iloc[:,33] = df.iloc[:,33].replace("1", 'None')
        df.iloc[:,33] = df.iloc[:,33].replace("2", 'Open-plan')
        df.iloc[:,33] = df.iloc[:,33].replace("3", 'Separate')
        df.iloc[:,33] = df.iloc[:,33].replace("4", 'Industrial')
        df.iloc[:,33] = df.iloc[:,33].replace("5", 'Kitchenette')
        df.iloc[:,33] = df.iloc[:,33].replace("6", 'Equipped open-plan')
        df.iloc[:,33] = df.iloc[:,33].replace("7", 'Equipped separate')
        df.iloc[:,33] = df.iloc[:,33].replace("8", 'Equipped kitchenette')
        df.iloc[:,33] = df.iloc[:,33].replace("9", 'Equipped')
        df.to_csv(f'{filename}', sep=';', header=None)
    except EmptyDataError:
        print(f'{filename} is empty')
        pass
    except Exception as e:
        print(f'An unknown error occured : {e}')

def send_through_ftp(filename, location):
    creds_file = open('secrets/secrets.json', 'r')
    credentials = json.load(creds_file)
    session = FTP(credentials["ftp_url"],credentials["ftp_username"],credentials["ftp_password"])
    file = open(f'{filename}','rb')
    if location:
        session.cwd(f'/www/wp-content/uploads/wpallimport/uploads/{location}')
    else:
        session.cwd(f'/www/wp-content/uploads/wpallimport/uploads/{secrets.token_hex(32 // 2)}')
    session.storbinary('STOR {filename}.csv', file)
    file.close()
    session.quit()

def cleaning_files():
    os.system('del annonces_*')
    os.system(f'del *.zip')

f = open('link_list.json')
cleaning_files()
link_list = json.load(f)
for key, item in link_list.items():
    name = item.get('name')
    location = item.get('location', None)
    download_file(item.get('url'), name)
    os.rename('annonces.csv', f'annonces_{name}.csv')
    replace_separator(f'annonces_{name}', '!#', ';')
    manipulate_file(f'annonces_{name}_sandr.csv')
    send_through_ftp(f'annonces_{name}_sandr.csv', location)
    cleaning_files()
    print(f'********************* {name} done *************************')