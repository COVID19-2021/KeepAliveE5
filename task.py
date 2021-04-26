import json
import random
import requests

CONFIG_FILE = './config/app.json'


def config(data=None):
    with open(CONFIG_FILE, mode="r+") as conf:
        if not data:
            return json.load(conf)

        json.dump(data, conf, sort_keys=True, indent=4)


app = config()


def get_access_token():
    data = requests.post(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': app['refresh_token'],
            'client_id': app['client_id'],
            'client_secret': app['client_secret'],
            'redirect_uri': app['redirect_uri']
        }
    ).json()

    app['refresh_token'] = data['refresh_token']
    config(app)

    return data['access_token']


def invoke_api():
    apis = [
        'https://graph.microsoft.com/v1.0/groups',
        'https://graph.microsoft.com/v1.0/sites/root',
        'https://graph.microsoft.com/v1.0/sites/root/sites',
        'https://graph.microsoft.com/v1.0/sites/root/drives',
        'https://graph.microsoft.com/v1.0/sites/root/columns',
        'https://graph.microsoft.com/v1.0/me/',
        'https://graph.microsoft.com/v1.0/me/events',
        'https://graph.microsoft.com/v1.0/me/people',
        'https://graph.microsoft.com/v1.0/me/contacts',
        'https://graph.microsoft.com/v1.0/me/calendars',
        'https://graph.microsoft.com/v1.0/me/drive',
        'https://graph.microsoft.com/v1.0/me/drive/root',
        'https://graph.microsoft.com/v1.0/me/drive/root/children',
        'https://graph.microsoft.com/v1.0/me/drive/recent',
        'https://graph.microsoft.com/v1.0/me/drive/sharedWithMe',
        'https://graph.microsoft.com/v1.0/me/onenote/pages',
        'https://graph.microsoft.com/v1.0/me/onenote/sections',
        'https://graph.microsoft.com/v1.0/me/onenote/notebooks',
        'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
        'https://graph.microsoft.com/v1.0/me/mailFolders',
        'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
        'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        'https://graph.microsoft.com/v1.0/me/messages',
        "https://graph.microsoft.com/v1.0/me/messages?$filter=importance eq 'high'",
        'https://graph.microsoft.com/v1.0/me/messages?$search="hello world"',
        'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top',
    ]

    headers = {'Authorization': f'Bearer {get_access_token()}'}

    for period in range(1, random.randint(10, 50)):
        print('=========================================================================================')
        random.shuffle(apis)
        for api in apis:
            try:
                if requests.get(api, headers=headers).status_code == 200:
                    print('{:>8s} | {:<50s}'.format(
                        f'周期: {period}', f'成功: {api}'))
            except Exception:
                pass


if __name__ == '__main__':
    invoke_api()
