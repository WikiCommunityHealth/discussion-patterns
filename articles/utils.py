import datetime

def date_hook(json_dict: dict):
    # the hook is executed in nested json objects
    if 'timestamp' in json_dict:
        try:
            json_dict['timestamp'] = datetime.datetime.strptime(
                json_dict['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        except:
            print('Error parsing datetime in input file')
    return json_dict

def get_year_month_from_timestamp(timestamp):
    return f"{timestamp.year}-{timestamp.month}"

def get_username(record: dict):
    username = ''
    if 'user' in record and 'text' in record['user']:
        username = record['user']['text']
    elif 'user' in record and 'ip' in record['user']:
        username = record['user']['ip']
    else:
        username = 'unknown'