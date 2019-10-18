# -*- coding: utf-8 -*-
import jieba
import random

import nlp_web.libs.atmosphere as lib_as
import nlp_web.code_bank.number as number
import nlp_web.libs.atmosphere as lib_cc
from nlp_web.code_bank.function import *
jieba.load_userdict(config.atmosphere_cut_path)     # 用于切词的个性化词典
jieba.load_userdict(config.atmosphere_filter_path)  # 用于过滤的词典

def to_json(sen):
    segment = filter_atmosphere(sen)
    best = get_best_match(segment.filter_text, lib_cc.atmosphere_lamp_lib)
    text = segment.raw_text
    nlp_score = best.nlp_score
    best_match = best.best_match
    print('segment.filter_text = ' + segment.filter_text)
    print("sen_max = " + best_match)
    # 场景1：打开氛围灯
    if best_match in lib_as.atmosphere_lamp_lib_open or best_match in \
            lib_as.atmosphere_lamp_lib_open_plus:
        return lamp_open(text, nlp_score)
    # 场景2：关闭氛围灯
    if best_match in lib_as.atmosphere_lamp_lib_close:
        return lamp_close(text, nlp_score)
    # 场景3：氛围灯颜色
    if best_match in lib_as.atmosphere_lamp_lib_color:
        return lamp_color(text, nlp_score)
    # 场景4：氛围灯亮度
    # 氛围灯亮度调节可以处理的更精细些、以处理氛围灯亮度调节的不同分支
    if best_match in lib_as.atmosphere_lamp_lib_brightness:
        return lamp_brightness(text, nlp_score)

def lamp_open(text, nlp_score):
    if '关' in text:
        rst = '氛围灯'
        if '前' in text:
            rst = '前排' + rst
        elif '后' in text:
            rst = '后排' + rst
        json_base = init_json_base_atmosphere()
        json_base["rawText"] = text
        json_base["nlp_score"] = nlp_score
        json_base["operation"] = "CLOSE"
        json_base['semantic']['slots']["name"] = rst
        return json_base
    if "色" in text:
        mix_color_lib = ['冷蓝', '深蓝', '浅蓝','橘红', '冷白', '暖白', '紫红', '粉红', '冰蓝', '酒红', '橙红']
        color_lib = ['红', '橙', '橘', '黄', '绿', '青', '蓝', '紫', '粉', '白', '灰']
        color_str = '红橙橘黄绿青蓝紫粉白灰'
        col_rst = ''
        text_cut = jieba.lcut(text)
        for index in range(len(text_cut)):
            if text_cut[index] in mix_color_lib:
                col_rst = text_cut[index]
                break
            for cor in text:
                if cor in color_lib:
                    col_rst = cor
                    break
        if col_rst == '':
            col_rst = randomColor(color_str)
        col_rst = col_rst + '色'
        json_base = init_json_base_atmosphere()
        json_base["rawText"] = text
        json_base["nlp_score"] = nlp_score
        json_base["operation"] = "SET"
        json_base['semantic']['slots']["color"] = col_rst
        return json_base
    rst = '氛围灯'
    if '前' in text:
        rst = '前排' + rst
    elif '后' in text:
        rst = '后排' + rst
    json_base = init_json_base_atmosphere()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "OPEN"
    json_base['semantic']['slots']["name"] = rst
    return json_base

def lamp_close(text, nlp_score):
    rst = '氛围灯'
    if '前' in text:
        rst = '前排' + rst
    elif '后' in text:
        rst = '后排' + rst
    json_base = init_json_base_atmosphere()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "CLOSE"
    json_base['semantic']['slots']["name"] = rst
    return json_base

def lamp_color(text, nlp_score):
    mix_color_lib = ['冷蓝', '深蓝', '浅蓝', '橘红', '冷白', '暖白', '紫红', '粉红', '冰蓝', '酒红', '橙红']
    color_lib = ['红', '橙', '橘', '黄', '绿', '青', '蓝', '紫', '粉', '白','灰']
    color_str = '红橙橘黄绿青蓝紫粉白灰'
    col_rst = ''
    text_cut = jieba.lcut(text)
    for index in range(len(text_cut)):
        if text_cut[index] in mix_color_lib:
            col_rst = text_cut[index]
            break
        for cor in text:
            if cor in color_lib:
                col_rst = cor
                break
    if col_rst == '':
        col_rst = randomColor(color_str)
    col_rst = col_rst + '色'
    rst = '氛围灯'
    if '前' in text:
        rst = '前排' + rst
    elif '后' in text:
        rst = '后排' + rst
    json_base = init_json_base_atmosphere()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    json_base['semantic']['slots']["color"] = col_rst
    json_base['semantic']['slots']["name"] = rst
    return json_base

def lamp_brightness(text, nlp_score):
    control_lib = ['氛围灯', '整车氛围灯', '后排氛围灯', '前排氛围灯']
    if text in control_lib:
        rst = '氛围灯'
        if '前' in text:
            rst = '前排' + rst
        elif '后' in text:
            rst = '后排' + rst
        json_base = init_json_base_atmosphere()
        json_base["rawText"] = text
        json_base["nlp_score"] = nlp_score
        json_base["operation"] = "OPEN"
        json_base['semantic']['slots']["name"] = rst
        return json_base
    rst1 = '氛围灯'
    if '前' in text:
        rst1 = '前排' + rst1
    elif '后' in text:
        rst1 = '后排' + rst1
    json_base = init_json_base_atmosphere()
    json_base["rawText"] = text
    json_base["nlp_score"] = nlp_score
    json_base["operation"] = "SET"
    value = brightness_part_test(text)
    json_base['semantic']['slots']["name"] = rst1
    json_base['semantic']['slots']["category"] = value[0]
    json_base['semantic']['slots']["nameValue"] = value[1]
    return json_base

# 颜色随机产生
def randomColor(textArr):
    length = len(textArr)
    random_number = random.randint(0, length - 1)
    return textArr[random_number]

def brightness_part_test(text):
    # 申请一个列表，返回调节方向和调节幅度
    result = []
    category = ""
    nameValue = '0'
    # 亮度调节库
    plus_lib = ["调亮", "调高", "调大", '亮', "太暗"]
    reduce_lib = ["调低", "调暗", "调小", '暗', "太亮"]
    # 亮度设置库
    max_lib = ["最大", "最高", "最亮", "最强"]
    min_lib = ["最小", "最低", "最暗", "最弱"]
    num_lib = ['1', '2', '3', '4', '5']
    chn_num_lib = ['一', '二', '三', '四', '五']
    zero_lib = ['0', '零']
    text_cut = jieba.lcut(text)
    for index in range(len(text_cut)):
        if text_cut[index] in plus_lib:
            category = "亮度+"
        elif text_cut[index] in reduce_lib:
            category = "亮度-"
        elif text_cut[index] in max_lib:
            category = "亮度调节"
            nameValue = '5'
            result.append(category)
            result.append(nameValue)
            return result
        elif text_cut[index] in zero_lib:
            category = "亮度调节"
            nameValue = '0'
            result.append(category)
            result.append(nameValue)
            return result
        elif text_cut[index] in min_lib:
            category = "亮度调节"
            nameValue = '0'
            result.append(category)
            result.append(nameValue)
            return result
        elif text_cut[index] in chn_num_lib:
            nameValue = str(number.chinese_to_number(text_cut[index]))
        elif text_cut[index] in num_lib:
            nameValue = str(text_cut[index])

    if nameValue == '0':
        nameValue = '1'
    if category == "":
        category = "亮度调节"
    result.append(category)
    result.append(nameValue)
    return result

if __name__ == '__main__':
    rst = to_json("亮一点")
    print(rst)

