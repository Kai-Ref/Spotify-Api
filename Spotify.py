import requests

response = requests.get("https://api.thedogapi.com/")
print(response.text)