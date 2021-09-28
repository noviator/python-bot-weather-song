import requests


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def play(id):
    headers = {
        'Host': 'www.jiosaavn.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 9; POCO F1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.152 Mobile Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }

    params = (
        ('__call', 'song.generateAuthToken'),
        ('url', str(id)),
        ('bitrate', '320'),
        ('api_version', '4'),
        ('_format', 'json'),
        ('ctx', 'wap6dot0'),
        ('_marker', '0'),
    )

    res = requests.get('https://www.jiosaavn.com/api.php', headers=headers, params=params)
    # print(json.dumps(res.json(),indent=4))
    if res.status_code == 200:
        return res.json()['auth_url']
    else:
        msg = 'Error occurred (inside play)'
        print(msg)
        return False


def search(qry):
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; POCO F1 Build/PQ3A.190801.002)',
        'Host': 'www.saavn.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }

    params = (
        ('cc', ''),
        ('session_device_id', ''),
        ('app_version', '7.6.1'),
        ('_marker', '0'),
        ('ctx', 'android'),
        ('tz', 'Asia/Kolkata'),
        ('query', str(qry)),
        ('params', '{"type":"songs"}'),
        ('api_version', '4'),
        ('n', '10'),
        ('manufacturer', 'Xiaomi'),
        ('p', '1'),
        ('network_operator', ''),
        ('readable_version', '7.6.1'),
        ('build', 'PQ3A.110801.002'),
        ('v', '263'),
        ('_format', 'json'),
        ('model', 'POCO+F1'),
        ('__call', 'search.getMoreResults'),
        ('network_subtype', ''),
        ('state', 'login'),
        ('network_type', 'WIFI'),
    )

    res = requests.get('https://www.saavn.com/api.php', headers=headers, params=params)
    js = []
    # print(json.dumps(res.json(),indent=4))
    for x in res.json()['results']:
        sList = {'title': x['title'].replace('amp;', '').replace('&quot;', ''), 'image': x['image'],
                 'subtitle': x['subtitle'], 'id': x['more_info']['encrypted_cache_url']}
        js.append(sList)
    return js
