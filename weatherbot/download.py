import requests  # request img from web
import shutil  # save img locally
import os


def download_file(url, file_name):
    res = requests.get(url, stream=True)

    if os.path.exists('images/'+file_name+'.png'):
        return 'images/'+file_name+'.png'

    if res.status_code == 200:
        with open('images/' + file_name + '.png', 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        return 'images/'+file_name+'.png'
    else:
        return False
