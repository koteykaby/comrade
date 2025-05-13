import requests

url = "https://coh2-api.reliclink.com/game/login/platformlogin"
params = {
    "platformUserID": "76561198617872072",
    "alias": "player"
}
response = requests.post(url, params=params, verify=False)
response.raise_for_status() 
print("status: ", response.status_code)
print("answ: ", response.text)