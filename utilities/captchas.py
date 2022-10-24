import json, requests, os sys, time


def captchai(site,settings,xheader,scookies):

    proxy = settings['proxies'].replace('http://','').split('@')
    proxies = settings['proxies'].replace('http://','').split('@')
    link = 'https://api.captchaai.io/createTask'
    params =    {
          "clientKey":captchai_key,
            "task":
                {
                    "type":"HCaptchaTask",
                    "websiteURL":site,
                    "websiteKey":settings['captcha_sitekey'],
                    "proxyType":"http",
                    "proxyAddress":proxy[1].split(':')[0],
                    "proxyPort":int(proxy[1].split(':')[1]),
                    "proxyLogin":proxy[0].split(':')[0], #This parameter is optional
                    "proxyPassword":proxies[0].split(':')[1], #This parameter is optional
                    "userAgent":xheader, #This parameter is optional
                    "isInvisible": True, #This parameter is optional
                    "isEnterprise": True, #This parameter is optional
                    "enterprisePayload": #This parameter is optional
                    {
                        "rqdata":settings["captcha_rqdata"]
                    }
                }
        }

    resp = requests.post(link,json=params)
    task_id = resp.json()['taskId']
    if resp.json()['errorId'] != 0:
        print(resp.json())
        return 'Err','Err',None

    link = 'https://api.captchaai.io/getTaskResult'
    params = {'clientKey' : captchai_key,'taskId':task_id}

    while True:

        resp = requests.post(link,json=params)
        data = resp.json()

        if data['errorId'] != 0:
            return 'Err','Err', None

        if data['status'] != 'ready':
            time.sleep(7)
        else:
            res = {}
            res['code'] = data['solution']['gRecaptchaResponse']
            return 'Solved',res, None

