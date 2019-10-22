"""
能量回馈标准模式
能量回馈强度默认值
能量回馈强度设置为标准
能量回馈强度设置为较大
能量回馈较大模式
能量回馈强度较大
能量回馈强度
"""
def to_json(sen):
    entry_json = {
        "category": "能量回馈强度",
        "rc": 0,
        "rawText": sen,
        "service": "carControl",
        "operation": "SET",
        "semantic": {
            "slots": {
                "name": '',
                "mode": '',
                "color": '',
                "level": '',
                "nameValue": '',
                "value": '',
            }
        }
    }
    if '标准' in sen:
        entry_json["semantic"]["slots"]["name"] = '标准'
    elif '大' in sen or '较强' in sen or '高' in sen:
        entry_json["semantic"]["slots"]["name"] = '较大'
    return entry_json