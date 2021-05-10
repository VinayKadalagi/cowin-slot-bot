import json
import requests
from datetime import date
today = date.today()
todays_date = today.strftime("%d-%m-%Y")
cowin_endpoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=264&date={}".format(
    todays_date)


def lambda_handler(event, context):
    request_json = json.dumps(event)
    print(request_json)
    frombot = False
    if request_json != "{\"trigger\": \"cron\"}":
        frombot = True
    count = cowinApi()
    roger_that(count, frombot)
    return 200


def cowinApi():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    try:
        response = requests.request("GET", cowin_endpoint, headers=headers)
        parsed = json.loads(response.content)
    except:
        return "error in api call" + str(response.content)

    counter = 0
    centers = ""
    for sessions in parsed["centers"]:
        for session in sessions["sessions"]:
            if (session["min_age_limit"] == 18 and session["available_capacity"] > 0):
                centers = centers + "," + str(sessions["name"]) + " --- " + str(
                    session["available_capacity"]) + "--on--" + str(session["date"])
                counter = counter+1

    if counter > 0:
        return centers
    else:
        return "No slots"


def roger_that(message, frombot):
    reply = "?chat_id=" + str(1181284103) + \
        "&parse_mode=Markdown&text=" + str(message)
    send_text = 'https://api.telegram.org/bot1789004084:AAHaAbgIY_dZZTzKSlUhMEWrizO-UDBlUqg/sendMessage?chat_id=' + \
        str(1181284103) + '&parse_mode=Markdown&text='

    if message != "No slots" or frombot:
        if len(message) > 4096:
            for x in range(0, len(message), 4096):
                resp = requests.get(send_text + message[x:x+4096])
        else:
            resp = requests.get(send_text + message)
        print(resp.content)
    else:
        print("Slots not available yet")
