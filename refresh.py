import requests
import os


username = os.environ["PYTHON_ANYWHERE_USER"]
domain_name = "www.hardestclimbs.com"
host = "www.pythonanywhere.com"
token = os.environ["PYTHON_ANYWHERE_TOKEN"]

response = requests.post(
    url=f"https://{host}/api/v0/user/{username}/consoles/23278512/send_input/",
    headers={"Authorization": f"Token {token}"},
    data={"input": "cd ~/mysite; git pull \n"}
)

if response.status_code != 200:
    raise Exception(f"Failed to pull from Github! Got status code {response.status_code}")

response = requests.post(
    url=f"https://{host}/api/v0/user/{username}/webapps/{domain_name}/reload/",
    headers={"Authorization": f"Token {token}"}
)

if response.status_code != 200:
    raise Exception(f"Failed to refresh website! Got status code {response.status_code}")
