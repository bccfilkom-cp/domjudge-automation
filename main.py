#================================================================================================
import requests
import json
import secrets
import string
import os 
import pandas as pd
from requests.auth import HTTPBasicAuth
from nanoid import generate
from pandas import DataFrame
from dotenv import load_dotenv
#================================================================================================

# constants
load_dotenv()
BORDER_LENGTH       = 50
ACCOUNTS_JSON_PATH  = 'data/accounts.json'
TEAMS_JSON_PATH     = 'data/teams.json'
DOM_API_URL         = os.getenv('DOMJUDGE_API_URL')
DOM_ADMIN_USERNMAE  = os.getenv('DOMJUDGE_ADMIN_USERNAME')
DOM_ADMIN_PASSWORD  = os.getenv('DOMJUDGE_ADMIN_PASSWORD')

def logger(message: str) :
    print('\n')
    print('-' * BORDER_LENGTH)
    print(message)


# generating random password with simple algo
def generate_random_password(length: int) :
    letters = string.ascii_letters
    digits = string.digits
    list_selection = letters + digits 
    password = ''.join(secrets.choice(list_selection) for _ in range(length))
    return password 


# write list of dictionary to json files
def write_to_json(accounts: list, teams: list) :
    logger('writing data to json file')
    
    # writing accounts list to data/accounts.json
    with open(ACCOUNTS_JSON_PATH, 'w') as acc_file :
        json.dump(accounts, acc_file, indent=2)
    
    # writing teams list to data/teams.json
    with open(TEAMS_JSON_PATH, 'w') as tim_file :
        json.dump(teams, tim_file, indent=2)

    print('writing data done')


# generating domjudge data including teams and accounts
# for the data required and how to import it, you can look the url below
# https://www.domjudge.org/docs/manual/main/import.html#importing-teams
def generate_domjudge_jsondata(df: DataFrame) :        
    logger('generating domjudge data')
    accounts = []
    teams = []

    for _, row in df.iterrows() :
        account_id = f"user-{generate()}"
        team_id = f"team-{generate()}"

        account = {
            "id": account_id,
            "username": row['Email'],
            "password": generate_random_password(8),
            "type": "team",
            "name": row['Nama'],
            "team_id": row['Nama']
        }

        team = {
            "id": team_id,
            "name": row['Nama'],
        }

        accounts.append(account)
        teams.append(team)

    print('generating data done')
    return accounts, teams


# sending request with file to API_URL
def __send_request(files, url: str) :

    auth_data = HTTPBasicAuth(DOM_ADMIN_USERNMAE, DOM_ADMIN_PASSWORD)
    resp = requests.post(DOM_API_URL + url, files=files, auth=auth_data)

    if resp.ok :
        print(f'success importing data to url {url}')
    else :
        print(f'failed sending to url {url} with status code {resp.status_code}')
        print(f'message: {resp.text}')

    
# import data accounts and teams with DOMJUDGE API
def import_with_domapi() :
    logger('Import Accounts to Domjudge')
    # read data in csv file
    # make sure the csv file use comma as separator

    filepath = os.getenv('CSV_FILE_PATH')
    df = pd.read_csv(filepath)

    accounts, teams = generate_domjudge_jsondata(df)
    write_to_json(accounts, teams)

    logger('sending POST request to domjudge API')

    teams_file = {'json': ('teams.json', open('data/teams.json', 'rb'), 'application/json')}
    accounts_file = {'json': ('accounts.json', open('data/accounts.json'), 'application/json')}

    # dont swap the orders below
    # __send_request(teams_file, '/users/teams')
    __send_request(accounts_file, '/users/accounts')

    print('importing data done')

# automating create contest metadata
def create_contest_metadata() :
    logger('Creating Contest Metadata')

    id              = f"contest-{generate()}"
    name            = str(input('Contest Name : '))
    start_time      = str(input('Start Time : '))
    duration        = str(input('Duration : '))
    freeze_duration = str(input('Scoreboard Freeze Duration : '))
    penalty_time    = str(input(''))

    metadata_dict = {
        "id": id,
        "name": name,
        "start_time": start_time,
        "duration": duration,
        "scoreboard_freeze_duration": freeze_duration,
        "penalty_time": penalty_time
    }

if __name__ == '__main__' :
    
    print('-' * BORDER_LENGTH)
    print('DOMJUDGE AUTOMATION')
    print('-' * BORDER_LENGTH)

    print('1. Import accounts to domjudge')
    print('2. Create contest metadata')

    choice = str(input('Fill your choice: '))

    if choice == '1' :
        import_with_domapi()
        exit(0)
    
    if choice == '2' :
        create_contest_metadata()
        exit(0)

    print('\nInvalid choices\nExiting...')

