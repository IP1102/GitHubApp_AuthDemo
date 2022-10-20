from django.shortcuts import render
from django.http import JsonResponse
import json, requests
from rest_framework.decorators import api_view
from .constants import USER_AUTH_TOKEN_URL,CLIENT_ID,CLIENT_SECRET,PEM_FILEPATH,APP_ACCESS_TOKEN_URL,APP_INSTALLATIONS_URL,REPO_PULLS_URL
from .jwtapptoken import GetJwtToken

# Create your views here.

def home(request):
    try:
        code = request.GET.get('code')
        headers={
            'accept':'application/json'
        }
        data={
            'client_id':CLIENT_ID,
            'client_secret':CLIENT_SECRET,
            'code':code
        }
        user_token_req = requests.post(USER_AUTH_TOKEN_URL,data=data,headers=headers)
        print(user_token_req.json()["access_token"])
    except Exception as e:
        print(e)

    return JsonResponse({"message":"Installation successful!"},safe=False)

def fetch_Header(access_token):
    headers_users = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    return headers_users  

def pr(request):

    jwt_access_token = GetJwtToken(PEM_FILEPATH).getToken()
    print(jwt_access_token)


    app_installations = requests.get(APP_INSTALLATIONS_URL,headers=fetch_Header(jwt_access_token))

    print(app_installations.json())

    #Step not required if AppID is stored initially
    for ins in app_installations.json():
        if ins['account']['login'] == "IP1102":
            userAppInstallId = ins['id']

    req_installid = requests.post(APP_ACCESS_TOKEN_URL.format(installation_id=userAppInstallId),
                                headers=fetch_Header(access_token=jwt_access_token))
    
    

    install_apptoken = req_installid.json()['token']

    pr_repo = requests.get(REPO_PULLS_URL.format(OWNER="IP1102",REPO="SpringBoot-Demo"),
                            headers=fetch_Header(access_token=install_apptoken))
    print(pr_repo.json())

    return JsonResponse(pr_repo.json(),safe=False)
