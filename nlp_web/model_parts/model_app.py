# Author:feng.yuzhang
# Time:2019/8/19 15:48
# Project:nlp3
"应用模块"

def app_to_json(sen):
    basic_json = {
        "category": "",
        "keyword": "",
        "name": "",
        "nameType": "nameType",
        "packageName": "",
        "price": "",
        "prompt": "",
        "operation": "LAUNCH",
        "rawText": str(sen),
        "rc": "0",
        "service": "app"}
    return basic_json


