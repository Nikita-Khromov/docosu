import vk_api
import os
import time
import requests
from datetime import datetime

if __name__ == "__main__":

    today = datetime.now()
    group_id = int(input('group id: '))
    token = input('token: ')
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    images = sorted(os.listdir("./img"))

    postponed = vk.wall.get(owner_id=-group_id, filter="postponed", count = 151)
    if postponed['count'] > 100:
        postponed = vk.wall.get(owner_id=-group_id, offset=99, filter="postponed", count=52)
    if postponed['count'] != 0 and postponed['items'][-1]["date"] >= time.mktime(today.timetuple()):
        today = datetime.fromtimestamp(postponed['items'][-1]["date"])
        if int(today.strftime("%H")) != 0:
            hour = int(today.strftime("%H")) + 2
        else:
            hour = 8
    elif postponed['count'] == 0:
        if hour % 2 == 0:
            hour = int(today.strftime("%H")) + 2
        else:
            hour = int(today.strftime("%H")) + 1
    else:
        hour = int(today.strftime("%H"))

    year = 2000 + int(today.strftime("%y"))
    month = int(today.strftime("%m"))
    day = int(today.strftime("%d"))
    minute = int(today.strftime("%M"))

    for img in images:
        photo = "./img/" + img
        server = vk.photos.getWallUploadServer(group_id=group_id)
        post = requests.post(server["upload_url"], files={'photo': open(photo, 'rb')}).json()
        result = vk.photos.saveWallPhoto(server=post["server"], photo=post["photo"],
                                         hash=post["hash"], group_id=group_id)[0]
        string = "photo" + str(result["owner_id"]) + "_" + str(result["id"])
        if 23 >= hour >= 8:
            today = datetime(year, month, day, hour, 30, 0, 0)
        else:
            if hour == 2:
                hour = 8
            else:
                hour = 0
                day += 1
            try:
                today = datetime(year, month, day, hour, 30, 0, 0)
            except:
                day = 1
                month += 1
                try:
                    today = datetime(year, month, day, hour, 30, 0, 0)
                except:
                    month = 1
                    year += 1
                    today = datetime(year, month, day, hour, 30, 0, 0)
        vk.wall.post(owner_id=-210600187, attachments=string,
                     from_group=1, publish_date=int(time.mktime(today.timetuple())))
        hour += 2
        os.replace(photo, "./done/" + img)
