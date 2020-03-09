import requests
from os import path
def doUpdateCheck():
    URL = 'https://api.github.com/repos/ChristopherJTrent/StudioCues/releases/latest'
    params = {'User-Agent':'StudioCues-Updater'}
    data = requests.get(URL)
    json_ = data.json()
    id = 0
    if path.exists('current.id'):
        id = int(open('current.id').read())
        if json_['id'] == id:
            return False
        else:
            return True
    else:
        return True
print(doUpdateCheck())