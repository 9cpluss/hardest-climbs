import requests
import os


username = os.environ["PYTHON_ANYWHERE_USER"]
domain_name = "www.hardestclimbs.com"
host = "www.pythonanywhere.com"
token = os.environ["PYTHON_ANYWHERE_TOKEN"]


response = requests.post(
    url=f"{host}/api/v0/user/{username}/webapps/{domain_name}/reload/",
    headers={"Authorization": f"Token {token}"}
)

if response.status_code != 200:
    raise Exception(f"Failed to refresh website! Got status code {response.status_code}")
