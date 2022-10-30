from django.test import TestCase
import requests
# Create your tests here.
import pydriller,os,json
from jwtapptoken import GetJwtToken
from github import Github
import pygit2


pem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"gapp-demotest.2022-10-19.private-key.pem")

jwt_token = GetJwtToken(pempath=pem_path).getToken()

def create_header(token):
    header = {
        'accept':'application/json',
        'Authorization':'Bearer '+token
    }
    return header

app_installations = requests.get("https://api.github.com/app/installations",headers=create_header(jwt_token))

for ins in app_installations.json():
    if ins["account"]["login"]=="IP1102":
        app_token_url = ins["access_tokens_url"]

app_token = requests.post(app_token_url,headers=create_header(jwt_token))

print(app_token.json())

# using an access token
# g = Github(str(app_token.json()["token"]))

# for repo in g.get_user("IP1102").get_repos():
#     print(repo.name)

# print(g.get_repo("Node-RESTApis"))

# repos = requests.get("https://api.github.com/installation/repositories",headers=create_header(str(app_token.json()["token"])))

# for repo in repos.json()["repositories"]:
#     if repo["private"]==True:
#         print(repo["clone_url"])

clone_url = "https://x-access-token:"+str(app_token.json()["token"])+"@github.com/IP1102/CovidCoughDetection.git"
repoClone = pygit2.clone_repository(clone_url,"C:/Users/indra/OneDrive/Documents/Temp")

for commit in pydriller.Repository("https://github.com/tushartushar/DJ").traverse_commits():
    print(commit.hash)
    print(commit.msg)
    print(commit.files)
    print(commit.committer_date)
    print(commit.committer.name)
    print(commit.modified_files)
