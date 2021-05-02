from flask import Flask
import requests
import datetime
import json

app = Flask(__name__)

@app.route("/")
def index():
    return get_slots()


def get_slots(NUMDAYS=20, AGE=18):
    DIST_IDS = {
        141: 'Central Delhi',
        145: 'East Delhi',
        140: 'New Delhi',
        146: 'North Delhi',
        147: 'North East Delhi',
        143: 'North West Delhi',
        148: 'Shahdara',
        149: 'South Delhi',
        144: 'South East Delhi',
        150: 'South West Delhi',
        142: 'West Delhi'
    }

    base = datetime.datetime.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(NUMDAYS)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    text = f'<b>Avaliable vaccination slots in NCR for 18+ as of: ({base})</b> <br><br>'
    for DIST_ID in DIST_IDS:
        for INP_DATE in date_str:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, INP_DATE)
            response = requests.get(URL)
            if response.ok:
                resp_json = response.json()
                if resp_json["centers"]:
                    for center in resp_json["centers"]:
                        for session in center["sessions"]:
                            if session["min_age_limit"] <= AGE and session["available_capacity"] > 0:
                                text += DIST_IDS[DIST_ID] + '<br>'
                                text += "Available on: {}".format(INP_DATE) + '<br>'
                                text += "\t" + str(center["name"]) + '<br>'
                                text += "\t Price: " + str(center["fee_type"]) + '<br>'
                                text += "\t Available Capacity: " + str(session["available_capacity"]) + '<br>'
                                if(session["vaccine"] != ''):
                                    text += "\t Vaccine: " + str(session["vaccine"]) + '<br>'
                                text += "<br>" + '<br>'

            else:
                text += 'No available slots on {}".format(INP_DATE)'

    return text
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
