import requests as req
import pandas as pd
import os

url = "https://api.qrcode-monkey.com/qr/custom"
payload = {
    "data": "",
    "config": {
        "body": "circle-zebra-vertical",
        "eye": "frame14",
        "eyeBall": "ball18",
        "erf1": [],
        "erf2": [],
        "erf3": [],
        "brf1": [],
        "brf2": [],
        "brf3": [],
        "bodyColor": "#000000",
        "bgColor": "#FFFFFF",
        "eye1Color": "#021326",
        "eye2Color":"#021326",
        "eye3Color":"#021326",
        "eyeBall1Color":"#074f03",
        "eyeBall2Color":"#074f03",
        "eyeBall3Color":"#074f03",
        "gradientColor1":"#12a637",
        "gradientColor2":"#0b509e",
        "gradientType":"linear",
        "gradientOnEyes":"true",
        "logo":"",
        "logoMode":"default"
    },
    "size":1000,
    "download": "imageUrl",
    "file":"png"
}

teams = pd.read_csv("./data/teams.csv")
teams = teams.values.squeeze()

for team in teams:
    payload['data'] = team

    # Hit the endpoint
    resp = req.post(url, json=payload)

    if resp.status_code == 200:
        output = resp.json()

        # Get the link to download the QR
        link = "https:" + output.get('imageUrl')
        response = req.get(link)

        # Init the QR File
        directory = "./qr/"
        file_name = directory + team + ".png"

        # Check if the directory exists (just in case)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the QR
        with open(file_name, "wb") as file:
            file.write(response.content)

        print(f"QR for {team} created successfully")
    else:
        print(f"Failed to request to the endpoint!\nStatus - Error: {resp.status_code}")