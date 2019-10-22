# -*- coding: utf-8 -*-
import nlp_web.libs.aircontrol as lib_ac
import nlp_web.code_bank.number as number
import nlp_web.config as config
from nlp_web.code_bank.config import Word
from nlp_web.code_bank.function import *
import jieba
# jieba.load_userdict(config.personal_dict_path)  # 用于切词的个性化词典

def to_json(sen, debug=False):
    best = get_best_match(sen, lib_ac.air_control_lib)
    nlp_score = best.nlp_score
    best_match = best.best_match
    print("sen_max = " + best_match)
    words = []
    sens_seg = synonyms.seg(sen)
    for index in range(len(sens_seg[0])):
        word = Word(string=str(sens_seg[0][index]), tag=str(sens_seg[1][index]))
        words.append(word)

    # 场景1：打开空调（包括打开空调和调节温度）
    if best_match in lib_ac.air_control_lib_open:
        if debug:
            print("best_match in lib_ac.air_control_lib_open")
        return loads_open(sen, nlp_score, words, debug)
    # 场景1：关闭空调
    if best_match in lib_ac.air_control_lib_close:
        if debug:
            print("best_match in lib_ac.air_control_lib_close")
        return loads_close(sen, nlp_score, words, debug)
    # 场景3：空调设置温度
    if best_match in lib_ac.air_control_lib_temperature:
        if debug:
            print("best_match in lib_ac.air_control_lib_temperature")
        if "风" in sen or "档" in sen or "挡" in sen:
            return loads_fanSpeed(sen, nlp_score, words, debug)
        else:
            return loads_temperature(sen, nlp_score, words, debug)
    # 场景4：空调设置风量
    if best_match in lib_ac.air_control_lib_wind:
        if debug:
            print("best_match in lib_ac.air_control_lib_wind")
        return loads_fanSpeed(sen, nlp_score, words, debug)
    # 场景5：空调设置通风模式（包括设置通风模式和调节风量）
    if best_match in lib_ac.air_control_lib_mode_ventilate or best_match == "空调档":
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_ventilate")
        if "挡" or "档" in sen:
            return loads_fanSpeed(sen, nlp_score, words, debug)
        else:
            return loads_ventilate(sen, nlp_score, words, debug)
    # 场景6：空调设置冷热（包括设置冷热和调节温度和风量）
    # 发现‘空调低’，‘空调高’，‘空调调低’，‘空调调高’之前的辨识有难度
    if best_match in (lib_ac.air_control_lib_mode_hot + lib_ac.air_control_lib_mode_cold):
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_hot or lib_ac.air_control_lib_mode_cold")
        if "风" in sen or "档" in sen or "挡" in sen:
            return loads_fanSpeed(sen, nlp_score, words, debug)
        return loads_temperature(sen, nlp_score, words, debug)
    # 场景mode：空调设置模式
    if best_match in lib_ac.air_control_lib_mode_loop_inner:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_loop_inner")
        return loads_loop_inner(sen, nlp_score, words, debug)
    if best_match in lib_ac.air_control_lib_mode_loop_outside:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_loop_outside")
        return loads_loop_outside(sen, nlp_score, words, debug)
    if best_match in lib_ac.air_control_lib_mode_face:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_face")
        return loads_face(sen, nlp_score, words, debug)
    if best_match in lib_ac.air_control_lib_mode_foot:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_foot")
        return loads_foot(sen, nlp_score, words, debug)
    if best_match in lib_ac.air_control_lib_mode_branch:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_branch")
        return loads_branch(sen, nlp_score, words, debug)
    if best_match in lib_ac.air_control_lib_mode_automatic:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_automatic")
        return loads_automatic(sen, nlp_score, words, debug)
    if best_match in lib_ac.air_control_lib_mode_manual:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_manual")
        return loads_manual(sen, nlp_score, words, debug)
    if best_match in lib_ac.air_control_lib_mode_defrost:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_defrost")
        return loads_defrost(sen, nlp_score, words, debug)
    if best_match in lib_ac.air_control_lib_mode_ac:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_ac")
        if "制冷" in sen or "冷风" in sen :
            return loads_ac(sen, nlp_score, words, debug)
        else:
            return loads_temperature(sen, nlp_score, words, debug)

    if best_match in lib_ac.air_control_lib_mode_hot_mode:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_hot_mode")
        if "加热" in sen or "暖风" in sen:
            return loads_hot_mode(sen, nlp_score, words, debug)
        else:
            return loads_temperature(sen, nlp_score, words, debug)
    if best_match in lib_ac.air_control_lib_mode_demist:
        if debug:
            print("best_match in lib_ac.air_control_lib_mode_demist")
        return loads_demist(sen, nlp_score, words, debug)


def init_json_base():
    return {
        "rawText": "",
        "nlp_score": 0,
        "service": "airControl",
        "rc": 0,
        "operation": "",
        "version": str(config.version),
        "semantic": {
            "slots": {
                "device": "空调"
            }
        }
    }


def loads_open(text, nlp_score, words, debug=False):
    if debug:
        print("loads_open")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    if "风" in text or "档" in text or "挡" in text:
        value = fanSpeed_part(words, debug)
        if value == "":
            device = device_part(words, debug)
            json_base["semantic"]["slots"]["device"] = device
            area = area_part(words, debug)
            if area != "":
                json_base["semantic"]["slots"]["area"] = area
            if "加热" in text or "暖风" in text:
                json_base["semantic"]["slots"]["mode"] = "制热"
            elif "制冷" in text or "冷风" in text:
                json_base["semantic"]["slots"]["mode"] = "制冷"
            else:
                if "关" in text:
                    json_base["operation"] = "CLOSE"
                else:
                    json_base["operation"] = "OPEN"
            # return json.dumps(json_base, ensure_ascii=False)
            return json_base
        else:
            device = device_part(words, debug)
            json_base["semantic"]["slots"]["device"] = device
            area = area_part(words, debug)
            if area != "":
                json_base["semantic"]["slots"]["area"] = area
            json_base["operation"] = "SET"
            json_base["semantic"]["slots"]["fanSpeed"] = value
            # return json.dumps(json_base, ensure_ascii=False)
            return json_base
    else:
        value = temperature_part(words, debug)
        if value == "":
            device = device_part(words, debug)
            json_base["semantic"]["slots"]["device"] = device
            area = area_part(words, debug)
            if area != "":
                json_base["semantic"]["slots"]["area"] = area
            if "加热" in text or "暖风" in text:
                json_base["semantic"]["slots"]["mode"] = "制热"
            elif "制冷" in text or "冷风" in text:
                json_base["semantic"]["slots"]["mode"] = "制冷"
            else:
                if "关" in text:
                    json_base["operation"] = "CLOSE"
                else:
                    json_base["operation"] = "OPEN"
            # return json.dumps(json_base, ensure_ascii=False)
            return json_base
        else:
            device = device_part(words, debug)
            json_base["semantic"]["slots"]["device"] = device
            area = area_part(words, debug)
            if area != "":
                json_base["semantic"]["slots"]["area"] = area
            json_base["operation"] = "SET"
            json_base["semantic"]["slots"]["temperature"] = value
            # return json.dumps(json_base, ensure_ascii=False)
            return json_base



def loads_close(text, nlp_score, words, debug=False):
    if debug:
        print("loads_close")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "CLOSE"
    value = temperature_part(words, debug)
    if value == "":
        device = device_part(words, debug)
        json_base["semantic"]["slots"]["device"] = device
        area = area_part(words, debug)
        if area != "":
            json_base["semantic"]["slots"]["area"] = area
        if "加热" in text or "暖风" in text:
            json_base["semantic"]["slots"]["mode"] = "制热"
        elif "制冷" in text or "冷风" in text:
            json_base["semantic"]["slots"]["mode"] = "制冷"
        else:
            if "关" in text:
                json_base["operation"] = "CLOSE"
            else:
                json_base["operation"] = "OPEN"
        # return json.dumps(json_base, ensure_ascii=False)
        return json_base
    else:
        device = device_part(words, debug)
        json_base["semantic"]["slots"]["device"] = device
        area = area_part(words, debug)
        if area != "":
            json_base["semantic"]["slots"]["area"] = area
        json_base["operation"] = "SET"
        json_base["semantic"]["slots"]["temperature"] = value
        # return json.dumps(json_base, ensure_ascii=False)
        return json_base


def loads_temperature(text, nlp_score, words, debug=False):
    if debug:
        print("loads_temperature")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    value = temperature_part(words, debug)
    if value == "":
        if "加热" in text or "暖风" in text :
            json_base["semantic"]["slots"]["mode"] = "制热"
        elif "制冷" in text or "冷风" in text :
            json_base["semantic"]["slots"]["mode"] = "制冷"
        else:
            json_base["operation"] = "OPEN"
        # return json.dumps(json_base, ensure_ascii=False)
        return json_base
    else:
        device = device_part(words, debug)
        json_base["semantic"]["slots"]["device"] = device
        area = area_part(words, debug)
        if area != "":
            json_base["semantic"]["slots"]["area"] = area
        json_base["semantic"]["slots"]["temperature"] = value
        # return json.dumps(json_base, ensure_ascii=False)
        return json_base


def loads_fanSpeed(text, nlp_score, words, debug=False):
    if debug:
        print("loads_fanSpeed")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    value = fanSpeed_part(words, debug)
    if value == "":
        json_base["operation"] = "OPEN"
        # return json.dumps(json_base, ensure_ascii=False)
        return json_base
    else:
        json_base["semantic"]["slots"]["fanSpeed"] = value
        #return json.dumps(json_base, ensure_ascii=False)
        return json_base



def loads_ventilate(text, nlp_score, words, debug=False):
    if debug:
        print("loads_ventilate")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "通风"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_loop_inner(text, nlp_score, words, debug=False):
    if debug:
        print("loads_loop_inner")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "内循环"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_loop_outside(text, nlp_score, words, debug=False):
    if debug:
        print("loads_loop_outside")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "外循环"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_face(text, nlp_score, words, debug=False):
    if debug:
        print("loads_face")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["airflowDirection"] = "面"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_foot(text, nlp_score, words, debug=False):
    if debug:
        print("loads_face")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["airflowDirection"] = "脚"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_branch(text, nlp_score, words, debug=False):
    if debug:
        print("loads_branch")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "分控"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_automatic(text, nlp_score, words, debug=False):
    if debug:
        print("loads_automatic")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "自动"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_manual(text, nlp_score, words, debug=False):
    if debug:
        print("loads_manual")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "手动"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_defrost(text, nlp_score, words, debug=False):
    if debug:
        print("loads_defrost")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "除霜"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_ac(text, nlp_score, words, debug=False):
    if debug:
        print("loads_ac")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "制冷"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_hot_mode(text, nlp_score, words, debug=False):
    if debug:
        print("loads_ac")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "制热"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base


def loads_demist(text, nlp_score, words, debug=False):
    if debug:
        print("loads_ac")
    json_base = init_json_base()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base["semantic"]["slots"]["mode"] = "除雾"
    # return json.dumps(json_base, ensure_ascii=False)
    return json_base



def temperature_part(words, debug=False):
    # step1:将话束进行分词
    temperature = 0
    direct = ""
    offset = 1
    is_statue = False
    poi = 0
    for w in words:
        # step1.1:将其中出现的小幅度调整的词进行分析
        if (w.tag == "d" or w.tag == "dl") and len(words) > words.index(w)+1:
            poi = words.index(w)
            next_w = words[poi+1]
            if next_w.tag == "a":
                print(next_w.string)
                is_statue = True
                # "a"为形容词，"v"为动词
                plus = ["高", "多", "大", "加",
                        "调高", "调多", "调大", "增强",
                        "加高", "加多", "加大",
                        "增高", "增多", "增大",
                        "热", "制热", "暖", '上调']
                reduce = ["低", "少", "小", "减",
                          "调低", "调少", "调小",'下调',
                          "减低", "减少", "减小", "关小",
                          "降低", "冷"
                          ]
                max = ["最大", "最高", "最热"]
                min = ["最小", "最低", "最冷"]
                length = len(next_w.string)
                if next_w.string in plus:
                    direct = "-"
                elif next_w.string in reduce:
                    direct = "+"
                elif next_w.string in max:
                    if debug:
                        print(temperature, direct, offset)
                    return "max"
                elif next_w.string in min:
                    if debug:
                        print(temperature, direct, offset)
                    return "min"
                else:
                    print(str(temperature))
                    for i in range(0,length):
                        tempW = next_w.string[i:(i + 1)]
                        if tempW in plus:
                            direct = "-"
                        elif tempW in reduce:
                            direct = "+"
                        else:
                            is_statue = False


        if w.string == "好" and len(words) > words.index(w)+1:
            poi = words.index(w)
            next_w = words[poi+1]
            if next_w.tag == "a":
                print(next_w.string)
                is_statue = True
                # "a"为形容词，"v"为动词
                plus = ["高", "多", "大", "加",
                        "调高", "调多", "调大", "增强",
                        "加高", "加多", "加大",
                        "增高", "增多", "增大",
                        "热", "制热", "暖", '上调']
                reduce = ["低", "少", "小", "减",
                          "调低", "调少", "调小",'下调',
                          "减低", "减少", "减小", "关小",
                          "降低", "冷"
                          ]
                max = ["最大", "最高", "最热"]
                min = ["最小", "最低", "最冷"]
                length = len(next_w.string)
                if next_w.string in plus:
                    direct = "-"
                elif next_w.string in reduce:
                    direct = "+"
                elif next_w.string in max:
                    if debug:
                        print(temperature, direct, offset)
                    return "max"
                elif next_w.string in min:
                    if debug:
                        print(temperature, direct, offset)
                    return "min"
                else:
                    print(str(temperature))
                    for i in range(0,length):
                        tempW = next_w.string[i:(i + 1)]
                        if tempW in plus:
                            direct = "-"
                        elif tempW in reduce:
                            direct = "+"
                        else:
                            is_statue = False


        if w.tag == "m" or w.tag == "x" or w.tag == "nz" \
                or w.tag == "mq" or w.tag == "vn" or w.tag == "i" \
                or w.tag == "ns" or w.tag == "b":
            # "m"为量词，“一下”、“大点”也是数词
            value = 0
            if w.string == "一下":
                pass
            elif w.string == "大点":
                value = 1
                direct = "+"
                temperature = value
            else:
                try:
                    value = int(w.string)
                except:
                    value = number.chinese_to_number(w.string)
                    pass
                temperature = temperature + value
        # step1.2:将其中出现的增减趋势输出
        if w.tag == "a":
            if poi == words.index(w) - 1 and is_statue:
                pass
            else:
                # "a"为形容词，"v"为动词
                plus = ["高", "多", "大", "加",
                        "调高", "调多", "调大", "增强",
                        "加高", "加多", "加大",
                        "增高", "增多", "增大",
                        "热", "制热", "暖", '上调']
                reduce = ["低", "少", "小", "减",
                          "调低", "调少", "调小", '下调',
                          "减低", "减少", "减小", "关小",
                          "降低", "冷"
                          ]
                max = ["最大", "最高", "最热"]
                min = ["最小", "最低", "最冷"]
                length = len(w.string)
                if w.string in plus:
                    direct = "+"
                elif w.string in reduce:
                    direct = "-"
                elif w.string in max:
                    if debug:
                        print(temperature, direct, offset)
                    return "max"
                elif w.string in min:
                    if debug:
                        print((temperature, direct, offset))
                    return "min"
                else:
                    print((str(temperature)))
                    for i in range(0,length):
                        tempW = w.string[i:(i + 1)]
                        if tempW in plus:
                            direct = "+"
                        elif tempW in reduce:
                            direct = "-"
        if w.tag == "v" or w.tag == "vn" \
                or w.tag == "n" or w.tag == "nz":
            # "a"为形容词，"v"为动词
            plus = ["高", "多", "大", "加",
                    "调高", "调多", "调大", "增强",
                    "加高", "加多", "加大",
                    "增高", "增多", "增大",
                    "热", "制热", "暖", '上调']
            reduce = ["低", "少", "小", "减",
                      "调低", "调少", "调小", '下调',
                      "减低", "减少", "减小", "关小",
                      "降低", "冷"
                      ]
            max = ["最大", "最高", "最热"]
            min = ["最小", "最低", "最冷"]
            length = len(w.string)
            if w.string in plus:
                direct = "+"
            elif w.string in reduce:
                direct = "-"
            elif w.string in max:
                if debug:
                    print(temperature, direct, offset)
                return "max"
            elif w.string in min:
                if debug:
                    print(temperature, direct, offset)
                return "min"
            else:
                print(str(temperature))
                for i in range(0,length):
                    tempW = w.string[i:(i + 1)]
                    if tempW in plus:
                        direct = "+"
                    elif tempW in reduce:
                        direct = "-"
    if direct != "":
        if temperature != 0:
            offset = temperature
            temperature = 0
        else:
            if direct == "-" or direct == "+":
                for w in words:
                    try:
                        value = int(w.string)
                    except:
                        value = number.chinese_to_number(w.string)
                        pass
                    temperature = temperature + value
            if temperature != 0:
                offset = temperature
                temperature = 0
            else:
                offset = 1
                temperature = 0
        if debug:
            print(temperature, direct, offset)
        return {"direct": str(direct), "offset": str(offset)}
    elif temperature != 0:
        if debug:
            print(temperature, direct, offset)
        return str(temperature)
    else:
        if debug:
            print(temperature, direct, offset)
        return ""


def fanSpeed_part(words, debug=False):
    # step1:将话束进行分词
    fanSpeed = 0
    direct = ""
    offset = 1
    is_statue = False
    poi = 0
    for w in words:
        # step1.2:将其中出现的量词之和转化为数字（阿拉伯）输出
        if (w.tag == "d" or w.tag == "dl") and len(words) > words.index(w)+1:
            poi = words.index(w)
            next_w = words[poi+1]
            if next_w.tag == "a":
                is_statue = True
                plus = ["高", "多", "大", "加",
                        "调高", "调多", "调大",
                        "加高", "加多", "加大", "增强",
                        "增高", "增多", "增大",
                        "冷",  "上调"]
                reduce = ["低", "少", "小", "减",
                          "调低", "调少", "调小", "下调",
                          "减低", "减少", "减小", "关小",
                          "降低", "热", "暖", "制热"
                          ]
                max = ["最大", "最高", "最冷"]
                min = ["最小", "最低", "最热"]
                length = len(next_w.string)
                if next_w.string in plus:
                    direct = "-"
                elif next_w.string in reduce:
                    direct = "+"
                elif next_w.string in max:
                    if debug:
                        print(fanSpeed, direct, offset)
                    return "min"
                elif next_w.string in min:
                    if debug:
                        print(fanSpeed, direct, offset)
                    return "max"
                else:
                    for i in range(0,length):
                        tempW = next_w.string[i:(i + 1)]
                        if debug:
                            print(str(i), length, tempW)
                        if tempW in plus:
                            direct = "-"
                        elif tempW in reduce:
                            direct = "+"
                        else:
                            is_statue = False

        if w.string == "好" and len(words) > words.index(w)+1:
            poi = words.index(w)
            next_w = words[poi+1]
            if next_w.tag == "a":
                is_statue = True
                plus = ["高", "多", "大", "加",
                        "调高", "调多", "调大",
                        "加高", "加多", "加大", "增强",
                        "增高", "增多", "增大",
                        "冷",  "上调"]
                reduce = ["低", "少", "小", "减",
                          "调低", "调少", "调小", "下调",
                          "减低", "减少", "减小", "关小",
                          "降低", "热", "暖", "制热"
                          ]
                max = ["最大", "最高", "最冷"]
                min = ["最小", "最低", "最热"]
                length = len(next_w.string)
                if next_w.string in plus:
                    direct = "-"
                elif next_w.string in reduce:
                    direct = "+"
                elif next_w.string in max:
                    if debug:
                        print(fanSpeed, direct, offset)
                    return "min"
                elif next_w.string in min:
                    if debug:
                        print(fanSpeed, direct, offset)
                    return "max"
                else:
                    for i in range(0,length):
                        tempW = next_w.string[i:(i + 1)]
                        if debug:
                            print(str(i), length, tempW)
                        if tempW in plus:
                            direct = "-"
                        elif tempW in reduce:
                            direct = "+"
                        else:
                            is_statue = False


        if w.tag == "m" or w.tag == "x" or w.tag == "nz" \
                or w.tag == "mq" or w.tag == "vn" or w.tag == "i" \
                or w.tag == "ns" or w.tag == "b":
            # "m"为量词，“一下”、“大点”也是数词
            value = 0
            if w.string == "一下" or w.string == "一些":
                pass
            elif w.string == "大点":
                value = 1
                direct = "+"
                fanSpeed = value
            else:
                try:
                    value = int(w.string)
                except:
                    value = number.chinese_to_number(w.string)
                    pass
                fanSpeed = fanSpeed + value
        # step1.3:将其中出现的增减趋势输出
        if w.tag == "a":
            if poi == words.index(w)-1 and is_statue:
                pass
            else:
                # "a"为形容词，"v"为动词
                plus = ["高", "多", "大", "加",
                        "调高", "调多", "调大", "增强",
                        "加高", "加多", "加大",
                        "增高", "增多", "增大",
                        "冷", "上调"]
                reduce = ["低", "少", "小", "减",
                          "调低", "调少", "调小", "下调",
                          "减低", "减少", "减小", "关小",
                          "降低", "热", "暖", "制热"
                          ]
                max = ["最大", "最高", "最冷"]
                min = ["最小", "最低", "最热"]
                length = len(w.string)
                if w.string in plus:
                    direct = "+"
                elif w.string in reduce:
                    direct = "-"
                elif w.string in max:
                    if debug:
                        print(fanSpeed, direct, offset)
                    return "max"
                elif w.string in min:
                    if debug:
                        print(fanSpeed, direct, offset)
                    return "min"
                else:
                    for i in range(0,length):
                        tempW = w.string[i:(i + 1)]
                        if debug:
                            print(str(i), length, tempW)
                        if tempW in plus:
                            direct = "+"
                        elif tempW in reduce:
                            direct = "-"

        if w.tag == "v" or w.tag == "vn" \
                or w.tag == "n" or w.tag == "nz":
            # "a"为形容词，"v"为动词
            plus = ["高", "多", "大", "加",
                    "调高", "调多", "调大", "增强",
                    "加高", "加多", "加大",
                    "增高", "增多", "增大",
                    "冷", "上调"]
            reduce = ["低", "少", "小", "减",
                      "调低", "调少", "调小", "下调",
                      "减低", "减少", "减小", "关小",
                      "降低", "热", "暖", "制热"
                      ]
            max = ["最大", "最高", "最冷"]
            min = ["最小", "最低", "最热"]
            length = len(w.string)
            if w.string in plus:
                direct = "+"
            elif w.string in reduce:
                direct = "-"
            elif w.string in max:
                if debug:
                    print(fanSpeed, direct, offset)
                return "max"
            elif w.string in min:
                if debug:
                    print(fanSpeed, direct, offset)
                return "min"
            else:
                for i in range(0,length):
                    tempW = w.string[i:(i + 1)]
                    if debug:
                        print(str(i), length, tempW)
                    if tempW in plus:
                        direct = "+"
                    elif tempW in reduce:
                        direct = "-"

    if direct != "":
        if fanSpeed != 0:
            offset = fanSpeed
            fanSpeed = 0
        else:
            if direct == "-" or direct == "+":
                for w in words:
                    try:
                        value = int(w.string)
                    except:
                        value = number.chinese_to_number(w.string)
                        pass
                        fanSpeed = fanSpeed + value
            if fanSpeed != 0:
                offset = fanSpeed
                fanSpeed = 0
            else:
                offset = 1
                fanSpeed = 0
        if debug:
            print(fanSpeed, direct, offset)
        return {"direct": str(direct), "offset": str(offset)}
    elif fanSpeed != 0:
        return str(fanSpeed)
    else:
        return ""


def device_part(words, debug=False):
    name = "空调"
    for w in words:
        if w.tag == "vn" or w.tag == "v" or w.tag == "f" :
            # 前面f 前排v 后排vn
            if debug:
                print(w.string)
            behind = ["后排", "后面", "后"]
            front = ["前排", "前面", "前"]
            if w.string in behind:
                name = "后排空调"
    return name


def area_part(words, debug=False):
    area = ""
    for w in words:
        if w.tag == "nz" or w.tag == "b":
            # 主驾nz 主b 副b
            if debug:
                print(w.string)
            main = ["主驾驶", "主驾", "主"]
            deputy = ["副驾驶", "副驾", "副"]
            if w.string in main:
                area = "主驾"
            if w.string in deputy:
                area = "副驾"
    return area
