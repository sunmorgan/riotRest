import re
import requests

response = requests.get('https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/philip/ugly?api_key=RGAPI-685f2a3d-4044-4da1-a04c-1df556720d98')

riot_list = response.json()
print(riot_list)