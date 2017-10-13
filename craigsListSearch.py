__author__ = 'Ben.Goff'
import requests
import xml.etree.ElementTree as ET
import json 


def getConfig():
    with open("cl_config.json") as f:
        params = json.load(f)
        f.close
    return params

def search(term, url):
    r = requests.get(url + term)
    tree = ET.fromstring(r.text)
    results = {}
    for x, item in enumerate(tree):
        if x > 0:
            results[item[0].text.split(' &', 1)[0]] = item[1].text
    return results


def push(pushTitle, item, params):
    token = str(params["pushover_token"])
    user_key = str(params["pushover_user"])
    for i in item:
        url = item[i]
        url_title = i
        post_data = 'token='+token+'&user='+user_key+'&title=CL Alert for '\
                +pushTitle+'&message='+url_title+'&url='+url+'&url_title='+url_title
        post_data = str.encode(post_data)
        push_url = 'https://api.pushover.net/1/messages.json'
        return requests.post(push_url, data=post_data)


def main():
    params = getConfig()
    CraigsURL = str(params["url"])
    for i in params["things_to_get"]:
        i = str(i)
        holder = search(i, CraigsURL)
        push(i, holder, params)

main()
