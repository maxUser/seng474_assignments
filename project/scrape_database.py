'''
The data gets dumped into match_data3.py.
This is arbitrary. If you decide to get
more data ask me first. There is a little
set up to do before you run this script.
'''

import json
import requests
import argparse
import time

def scrape_matches(n, key, match_id, invalid_ids):
    '''
    Use this function to fill the file.
    The file must already contain 1 dictionary.
    This function:
        * runs get_match n times.
        * appends ']' to close the list
    '''
    count = 1
    for i in range(n):
        result = get_match(key, match_id, count)
        count += 1
        time.sleep(2)
        match_id += 1
        if result == 1:
            invalid_ids += 1


    with open('match_data3.json', 'a') as file:
        file.write(']')

    with open('match_data3.json', 'r') as file:
        d = json.load(file)


    print('{} matches loaded'.format(len(d)))
    print('{} invalid match IDs'.format(invalid_ids))

def get_match(key, match_id, count):
    '''
    This function appends a comma followed
    by a match dictionary to the json file
    '''

    data_request = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?match_id={}&key={}'.format(match_id, key))

    '''
    data_request is a requests.model.Response object. See link for its methods:
    https://github.com/psf/requests/blob/master/requests/models.py#L587
    '''
    print('Response {}: {}'.format(count, data_request))
    if 'Too Many Requests' in data_request.text:
        print(data_request.headers)
        print(data_request.text)
    match_data = data_request.json()

    '''
    Check if match ID returns a match
    '''
    try:

        if 'error' in match_data['result'].keys():
            print(match_data['result']['error'])
            return 1
        else:
            with open('match_data3.json', 'a') as file:
                file.write(', ')
                json.dump(match_data, file, indent=4, sort_keys=True)
    except KeyError:
        print('KeyError: {}'.format(match_id))
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='API key', required=True)
    args = parser.parse_args()
    match_id = 5000012750
    invalid_ids = 0
    loops = 5000

    scrape_matches(loops, args.key, match_id, invalid_ids)
