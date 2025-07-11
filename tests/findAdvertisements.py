import requests
url = "https://coh2-api.reliclink.com/game/advertisement/findAdvertisements?appBinaryChecksum=24336&callNum=26&connect_id=1&dataChecksum=237719574&lastCallTime=2071&matchType_id=21&modDLLChecksum=0&modDLLFile=INVALID&modName=INVALID&modVersion=INVALID&profile_ids=[2,2,2,2,2]&race_ids=[0,1,2,3,4]&sessionID=1&statGroup_ids=[2,2,2,2,2]&versionFlags=0"
response = requests.post(url, verify=False)
response.raise_for_status() 
print("status: ", response.status_code)
print("answ: ", response.text)