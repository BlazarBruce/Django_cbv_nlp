# -*- coding: utf-8 -*-

import nlp_web.config as config
import nlp_web.code_bank.number as change
import jieba
wind = ["通风", "吹风", "开通", "制冷", "风扇", "通气", "东风", "电吹风", "屁股"]
hot = ["加热", "空调", "加温", "好凉"]
words_open = ["开", "打开", "开启", "有没有", "能不能"]
close = ["关", "关上", "关闭", "关掉", "退出", "停止", "取消", "关了", "不", "不要"]
main_chair = [
    "主驾",
    "驾驶",
    "主驾驶",
    "主驾驶位",
    "驾驶员",
    "主驾驶员",
    "驾驶座位",
    "驾驶座",
    "前排左边",
    "驾驶位",
    "左边",
    "左侧"]
deputy_chair = ["副驾", "副驾驶", "副驾驶位","副驾驶员", "前排右边", "右边的", "右边", "右侧"]
gear = ["零", "〇", "一", "二", "两", "三", "四", "五", "六", "七", "八", "九"]
maximum = ["最大", "最高", "极大"]
minimum = ["最小", "最低", "极小"]


def to_json(sen):
    chair_base_json = {
        "nlp_score": 1.0,
        "rawText": sen,
        "version": str(config.version),
        "service": "carControl",
        "rc": 0,
        "operation": "",
        "semantic": {
            "slots": {
                "name": '座椅',
            }
        },
    }
    # jieba.load_userdict(config.personal_dict_path)
    temp = jieba.lcut(sen)
    #  逻辑判断起点
    for action in temp:
        # 通风大类
        if action in wind:
            chair_base_json["operation"] = "OPEN"
            chair_base_json['semantic']['slots']['mode'] = '通风'
            # 位置类
            for location in temp:
                # 主驾类
                if location in main_chair:
                    chair_base_json["operation"] = "OPEN"
                    chair_base_json['semantic']['slots']['name'] = "主驾座椅"
                    # 主驾档位类
                    for gear_number in sen:
                        if gear_number in gear:
                            chair_base_json["operation"] = "SET"
                            chair_base_json['semantic']['slots']["level"] = str(
                                change.chinese_to_number(sen))
                        else:
                            continue
                # 副驾类
                elif location in deputy_chair:
                    chair_base_json["operation"] = "OPEN"
                    chair_base_json['semantic']['slots']["name"] = "副驾座椅"
                    # 副驾档位类
                    for gear_number in sen:
                        if gear_number in gear:
                            chair_base_json["operation"] = "SET"
                            chair_base_json['semantic']['slots']["level"] = str(
                                change.chinese_to_number(sen))
                        else:
                            continue
                # 单独档位类
                for number in sen:
                    if number in gear:
                        chair_base_json["operation"] = "SET"
                        chair_base_json['semantic']['slots']["level"] = str(
                            change.chinese_to_number(sen))
                # 最大通风
                if location in maximum:
                    chair_base_json["operation"] = "OPEN"
                    chair_base_json['semantic']['slots']["level"] = str(2)
                # 最小通风
                elif location in minimum:
                    chair_base_json["operation"] = "OPEN"
                    chair_base_json['semantic']['slots']["level"] = str(1)
                else:
                    continue
            for status in temp:
                if status in close:
                    chair_base_json["operation"] = "CLOSE"
                    for location in temp:
                        # 主驾关闭类
                        if location in main_chair:
                            chair_base_json['semantic']['slots']["name"] = "主驾座椅"
                            break
                        # 副驾关闭类
                        elif location in deputy_chair:
                            chair_base_json['semantic']['slots']["name"] = "副驾座椅"
                            break
                        else:
                            continue
                else:
                    continue
        # 加热大类
        elif action in hot:
            chair_base_json["operation"] = "OPEN"
            chair_base_json['semantic']['slots']["mode"] = "加热"
            # 位置类
            for location in temp:
                # 主驾加热
                if location in main_chair:
                    chair_base_json["operation"] = "OPEN"
                    chair_base_json['semantic']['slots']["name"] = "主驾座椅"
                    # 主驾档位加热
                    for gear_number in sen:
                        if gear_number in gear:
                            chair_base_json["operation"] = "SET"
                            chair_base_json['semantic']['slots']["level"] = str(
                                change.chinese_to_number(sen))
                        else:
                            continue
                            # 副驾加热
                elif location in deputy_chair:
                    chair_base_json["operation"] = "OPEN"
                    chair_base_json['semantic']['slots']["name"] = "副驾座椅"
                    # 副驾档位加热
                    for action_hot in sen:
                        if action_hot in gear:
                            chair_base_json["operation"] = "SET"
                            chair_base_json['semantic']['slots']["level"] = str(
                                change.chinese_to_number(sen))
                        else:
                            continue
                # 单独档位类
                for number in sen:
                    if number in gear:
                        chair_base_json["operation"] = "SET"
                        chair_base_json['semantic']['slots']["level"] = str(
                            change.chinese_to_number(sen))
                # 最大加热
                if location in maximum:
                    chair_base_json["operation"] = "OPEN"
                    chair_base_json['semantic']['slots']["level"] = str(2)
                # 最小加热
                elif location in minimum:
                    chair_base_json["operation"] = "OPEN"
                    chair_base_json['semantic']['slots']["level"] = str(1)
            for status in temp:
                if status in close:
                    chair_base_json["operation"] = "CLOSE"
                    for location in temp:
                        # 主驾关闭类
                        if location in main_chair:
                            chair_base_json['semantic']['slots']["name"] = "主驾座椅"
                            break
                        # 副驾关闭类
                        elif location in deputy_chair:
                            chair_base_json['semantic']['slots']["name"] = "副驾座椅"
                            break
                        else:
                            continue
                else:
                    continue
        else:
            continue
    return chair_base_json
