# -*- coding: utf-8  -*-
import pymysql.cursors
import sys
import json
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nlp.settings")  # project_name 项目名称
django.setup()
import nlp_web.model_parts.model_manage as models



def atmosphere_check(slot_json, rawText):
    return_data = {}
    # 讯飞json(格式化json)
    json_voice_tmp = slot_json
    try:
        json_voice = json.loads(json_voice_tmp)
    except:
        return_data['error_code'] = 9170405
        return_data['raw_json'] = json_voice_tmp
        return_data['error_field'] = 9170405
        return_data['correct_field'] = 9170405
        return_data['raw_text'] = rawText
        return return_data
    service_voice = json_voice.get("service", 0)
    name_voice = json_voice.get("name")
    color_voice = json_voice.get("color")
    category_voice = json_voice.get("category")
    nameValue_voice = json_voice.get("nameValue")
    operation_voice = json_voice.get("operation", 0)
    # 本地计算json
    json_nlp = models.domain_distribute(rawText)  # dict
    service_nlp = json_nlp['service']
    if service_voice == "carControl":
        # case1:operation字段的对比
        operation_nlp = json_nlp['operation']
        if operation_voice == 'ANSWER':
            pass
        elif operation_voice != "" or operation_nlp != "":
            if operation_nlp != operation_voice:
                return_data['error_code'] = 9170401
                return_data['raw_json'] = json_voice
                return_data['error_field'] = operation_voice
                return_data['correct_field'] = operation_nlp
                return_data['raw_text'] = rawText
                return return_data
        elif operation_nlp == "" or operation_voice == "":
            return_data['error_code'] = 9170401
            return_data['raw_json'] = json_voice
            return_data['error_field'] = operation_voice
            return_data['correct_field'] = operation_nlp
            return_data['raw_text'] = rawText
            return return_data
        # case2:name字段的对比
        name_nlp = json_nlp['semantic']['slots']["name"]  # 可能出现在天窗中
        if name_voice != '':
            if name_nlp != name_voice:
                return_data['error_code'] = 9170402
                return_data['raw_json'] = json_voice
                return_data['error_field'] = name_voice
                return_data['correct_field'] = name_nlp
                return_data['raw_text'] = rawText
                return return_data
        else:  # 应对 name 字段为空的情况
            return_data['error_code'] = 9170402
            return_data['raw_json'] = json_voice
            return_data['error_field'] = name_voice
            return_data['correct_field'] = name_nlp
            return_data['raw_text'] = rawText
            return return_data
        # case3:color 字段的对比
        # 目前 如果是颜色设置且color nlp 与讯飞字段为空的情况无法解决（两个同事出错） 小概率事件
        color_nlp = json_nlp['semantic']['slots']["color"]
        if '换' in rawText or '改' in rawText:
            pass
        elif color_nlp != color_voice:
            return_data['error_code'] = 9170403
            return_data['raw_json'] = json_voice
            return_data['error_field'] = color_voice
            return_data['correct_field'] = color_nlp
            return_data['raw_text'] = rawText
            return return_data
        # case4：亮度调节的字段对比
        category_nlp = json_nlp['semantic']['slots']["category"]
        nameValue_nlp = json_nlp['semantic']['slots']["nameValue"]
        if category_voice == category_nlp and nameValue_voice == nameValue_nlp:
            return_data['error_code'] = 9170400
            return_data['raw_json'] = json_voice
            return_data['error_field'] = 9170400
            return_data['correct_field'] = 9170400
            return_data['raw_text'] = rawText
            return return_data
        elif category_voice != category_nlp or nameValue_voice != nameValue_nlp:
            temp = []
            temp.append(category_voice)
            temp.append(nameValue_voice)
            return_data['error_code'] = 9170406
            return_data['raw_json'] = json_voice
            return_data['error_field'] = temp
            return_data['correct_field'] = json_nlp['semantic']
            return_data['raw_text'] = rawText
            return return_data

    elif service_voice == 'localCmd':
        return_data['error_code'] = 9170400
        return_data['raw_json'] = json_voice
        return_data['error_field'] = 9170400
        return_data['correct_field'] = 9170400
        return_data['raw_text'] = rawText
        return return_data
    else:
        return_data['error_code'] = 9170404
        return_data['raw_json'] = json_voice
        return_data['error_field'] = service_voice
        return_data['correct_field'] = service_nlp
        return_data['raw_text'] = rawText
        return return_data
# 天窗
def roof_check(slot_json, rawText):
    return_data = {}
    # 讯飞json(格式化json)
    json_voice_tmp = slot_json
    try:
        json_voice = json.loads(json_voice_tmp)
        json_nlp = models.domain_distribute(rawText)  # dict
    except:
        return_data['error_code'] = 9170105
        return_data['raw_json'] = str(json.dumps(json_voice_tmp, ensure_ascii=False))
        return_data['error_field'] = "Json_format_error"
        return_data['correct_field'] = json_voice_tmp.replace('"{', '{')
        return_data['correct_field'] = json_voice_tmp.replace('}"', '}')
        return_data['raw_text'] = rawText
        return return_data
    else:
        service_voice = json_voice.get("service", 0)
        operation_voice = json_voice.get("operation", 0)
        # 本地计算json
        service_nlp = json_nlp['service']
        if service_voice == "carControl":
            # case1:operation字段的对比
            operation_nlp = json_nlp['operation']
            if operation_voice == 'ANSWER':
                pass
            elif operation_voice != "" and operation_nlp != "":
                if operation_nlp != operation_voice:
                    return_data['error_code'] = 9170101
                    return_data['raw_json'] = json_voice
                    return_data['error_field'] = operation_voice
                    return_data['correct_field'] = operation_nlp
                    return_data['raw_text'] = rawText
                    return return_data
                else:
                    return_data['error_code'] = 9170100
                    return_data['raw_json'] = json_voice
                    return_data['error_field'] = 9170100
                    return_data['correct_field'] = 9170100
                    return_data['raw_text'] = rawText
                    return return_data
            elif operation_voice == "":
                return_data['error_code'] = 9170101
                return_data['raw_json'] = json_voice
                return_data['error_field'] = operation_voice
                return_data['correct_field'] = operation_nlp
                return_data['raw_text'] = rawText
                return return_data
        elif service_voice == 'localCmd':
            return_data['error_code'] = 9170100
            return_data['raw_json'] = json_voice
            return_data['error_field'] = 9170100
            return_data['correct_field'] = 9170100
            return_data['raw_text'] = rawText
            return return_data
        else:
            return_data['error_code'] = 9170104
            return_data['raw_json'] = json_voice
            return_data['error_field'] = service_voice
            return_data['correct_field'] = service_nlp
            return_data['raw_text'] = rawText
            return return_data

# 座椅
def chair_check(slot_json, rawText):
    return_data = {}
    # 格式化json
    json_voice_tmp = slot_json
    json_nlp = models.domain_distribute(rawText)
    try:
        json_voice = json.loads(json_voice_tmp)
    except ValueError:
        return_data['error_code'] = 9170299
        return_data['raw_json'] = str(json.dumps(json_voice_tmp, ensure_ascii=False))
        return_data['error_field'] = "Json_format_error"
        return_data['correct_field'] = json_voice_tmp.replace('"{','{')
        return_data['correct_field'] = json_voice_tmp.replace('}"','}')
        return_data['raw_text'] = rawText
    # 第一级--localCmd全部算对
    else:
        if json_voice.get("service") == "localCmd":
            return_data['error_code'] = 9170200
            return_data['raw_json'] = json_voice
            return_data['error_field'] = 9170200
            return_data['correct_field'] = 9170200
            return_data['raw_text'] = rawText
            return return_data
        # 再不是localCmd的集合中继续进行比较
        else:
            operation_voice_operation = json_voice.get("operation", "")
            operation_nlp_operation = json_nlp.get("operation")
            operation_voice_target = json_voice.get("name", "座椅")
            operation_nlp_target = json_nlp.get("semantic").get("slots").get("name")
            operation_voice_level = json_voice.get("level", 0)
            if operation_voice_level == "":
                operation_voice_level = 0
            operation_nlp_level = json_nlp.get("level", 0)
            if operation_voice_operation != operation_nlp_operation:
                return_data['error_code'] = 9170201
                return_data['raw_json'] = json_voice
                return_data['error_field'] = operation_voice_operation
                return_data['correct_field'] = operation_nlp_operation
                return_data['raw_text'] = rawText
                return return_data
            elif operation_voice_target != operation_nlp_target:
                return_data['error_code'] = 9170202
                return_data['raw_json'] = json_voice
                return_data['error_field'] = operation_voice_target
                return_data['correct_field'] = operation_nlp_target
                return_data['raw_text'] = rawText
                return return_data
            elif operation_voice_level != operation_nlp_level:
                return_data['error_code'] = 9170208
                return_data['raw_json'] = json_voice
                return_data['error_field'] = operation_voice_level
                return_data['correct_field'] = operation_nlp_level
                return_data['raw_text'] = rawText
                return return_data
            else:
                return_data['error_code'] = 9170200
                return_data['raw_json'] = json_voice
                return_data['error_field'] = 9170200
                return_data['correct_field'] = 9170200
                return_data['raw_text'] = rawText
                return return_data

# 空调
def aircontrol_check(slot_json, rawText):
    return_data = {}
    # 格式化json
    json_voice_tmp = slot_json
    try:
        json_voice = json.loads(json_voice_tmp)
    except ValueError:
        json_voice_tmp = json_voice_tmp.replace('"fanSpeed":"{"', '"fanSpeed":{"')
        json_voice_tmp = json_voice_tmp.replace('"temperature":"{"', '"temperature":{"')
        json_voice_tmp = json_voice_tmp.replace('"}","', '"},"')
    json_voice = json.loads(json_voice_tmp)

    json_nlp = models.domain_distribute(rawText)

    # case1:第一级---operation的区分
    operation_voice = json_voice['operation']
    operation_nlp = json_nlp['operation']
    if operation_nlp != operation_voice:
        return_data['error_code'] = 9106001
        return_data['raw_json'] = json_voice
        return_data['error_field'] = operation_voice
        return_data['correct_field'] = operation_nlp
        return_data['raw_text'] = rawText
        return return_data
    else:
        if operation_nlp == 'OPEN' or operation_nlp == 'CLOSE':
            return_data['error_code'] = 9106000
            return_data['raw_json'] = json_voice
            return_data['error_field'] = 9106000
            return_data['correct_field'] = 9106000
            return_data['raw_text'] = rawText
            return return_data
        else:
            # TODO(YJT)-2018年11月23日11:28:13: 这里需要增加模式的判断，现在不判别模式。
            # case2:第二级---具体参数的差异，如temperature，fanSpeed
            # case2.1 temperature是数值
            # case2.2 temperature是字典
            temperature_voice = ''
            fanSpeed_voice = ''
            direct_voice = ''
            offset_voice = ''
            mode_voice = ''

            temperature_nlp = ''
            fanSpeed_nlp = ''
            direct_nlp = ''
            offset_nlp = ''
            mode_nlp = ''
            # 解析mode字段
            try:
                mode_voice = str(json_voice['mode'])
            except:
                mode_voice = ''
            try:
                mode_voice = str(json_voice['mode'])
            except:
                mode_voice = ''

            try:
                temperature_voice = str(json_voice['temperature'])
                direct_voice = json_voice['temperature']['direct']
                offset_voice = json_voice['temperature']['offset']
                temperature_voice = 'is'  # 这里置1是为了便于后续判断
            except:
                # 如果报错，则意味着不包含direct或offset字段
                try:
                    temperature_voice = str(json_voice['temperature'])
                except:
                    # 如果报错，则意味着不包含temperature字段
                    temperature_voice = ''
            try:
                fanSpeed_voice = str(json_voice['fanSpeed'])
                direct_voice = json_voice['fanSpeed']['direct']
                offset_voice = json_voice['fanSpeed']['offset']
                fanSpeed_voice = 'is'  # 这里置1是为了便于后续判断
            except:
                # 如果报错，则意味着不包含direct或offset字段
                try:
                    fanSpeed_voice = str(json_voice['fanSpeed'])
                except:
                    # 如果报错，则意味着不包含fanSpeed字段
                    fanSpeed_voice = ''
            try:
                temperature_nlp = str(json_nlp['semantic']['slots']['temperature'])
                direct_nlp = json_nlp['semantic']['slots']['temperature']['direct']
                offset_nlp = json_nlp['semantic']['slots']['temperature']['offset']
                temperature_nlp = 'is'  # 这里置1是为了便于后续判断
            except:
                # 如果报错，则意味着不包含direct或offset字段
                try:
                    temperature_nlp = str(json_nlp['semantic']['slots']['temperature'])
                except:
                    # 如果报错，则意味着不包含temperature字段
                    temperature_nlp = ''
            try:
                fanSpeed_nlp = str(json_nlp['semantic']['slots']['fanSpeed'])
                direct_nlp = json_nlp['semantic']['slots']['fanSpeed']['direct']
                offset_nlp = json_nlp['semantic']['slots']['fanSpeed']['offset']
                fanSpeed_nlp = 'is'  # 这里置1是为了便于后续判断
            except:
                # 如果报错，则意味着不包含direct或offset字段
                try:
                    fanSpeed_nlp = str(json_nlp['semantic']['slots']['fanSpeed'])
                except:
                    # 如果报错，则意味着不包含fanSpeed字段
                    fanSpeed_nlp = ''
            if temperature_voice == temperature_nlp and \
                    fanSpeed_voice == fanSpeed_nlp and \
                    direct_voice == direct_nlp and \
                    offset_voice == offset_nlp:
                return_data['error_code'] = 9106000
                return_data['raw_json'] = json_voice
                return_data['error_field'] = 9106000
                return_data['correct_field'] = 9106000
                return_data['raw_text'] = rawText
                return return_data
            else:
                if (temperature_voice == '+' or temperature_voice == '-') and \
                        temperature_voice == direct_nlp and \
                        offset_nlp == '1':  # '我好热啊'仅返回direct，返回的offset为''
                    return_data['error_code'] = 9106000
                    return_data['raw_json'] = json_voice
                    return_data['error_field'] = 9106000
                    return_data['correct_field'] = 9106000
                    return_data['raw_text'] = rawText
                    return return_data
                elif (fanSpeed_voice == '+' or fanSpeed_voice == '-') and \
                        fanSpeed_voice == direct_nlp and \
                        offset_nlp == '1':  # '我好热啊'仅返回direct，返回的offset为''
                    return_data['error_code'] = 9106000
                    return_data['raw_json'] = json_voice
                    return_data['error_field'] = 9106000
                    return_data['correct_field'] = 9106000
                    return_data['raw_text'] = rawText
                    return return_data
                elif (fanSpeed_voice == '最小' or fanSpeed_voice == 'min' or fanSpeed_voice == '1') and (
                        fanSpeed_nlp == '1' or fanSpeed_nlp == 'min'):
                    return_data['error_code'] = 9106000
                    return_data['raw_json'] = json_voice
                    return_data['error_field'] = 9106000
                    return_data['correct_field'] = 9106000
                    return_data['raw_text'] = rawText
                    return return_data
                elif (fanSpeed_voice == '最大' or fanSpeed_voice == 'max' or fanSpeed_voice == '7') and (
                        fanSpeed_nlp == '7' or fanSpeed_nlp == 'max'):
                    return_data['error_code'] = 9106000
                    return_data['raw_json'] = json_voice
                    return_data['error_field'] = 9106000
                    return_data['correct_field'] = 9106000
                    return_data['raw_text'] = rawText
                    return return_data
                elif (
                        temperature_voice == '最小' or temperature_voice == 'min' or temperature_voice == '17') and (
                        temperature_nlp == '17' or temperature_nlp == 'min'):
                    return_data['error_code'] = 9106000
                    return_data['raw_json'] = json_voice
                    return_data['error_field'] = 9106000
                    return_data['correct_field'] = 9106000
                    return_data['raw_text'] = rawText
                    return return_data
                elif (
                        temperature_voice == '最大' or temperature_voice == 'max' or temperature_voice == '33') and (
                        temperature_nlp == '33' or temperature_nlp == 'max'):
                    return_data['error_code'] = 9106000
                    return_data['raw_json'] = json_voice
                    return_data['error_field'] = 9106000
                    return_data['correct_field'] = 9106000
                    return_data['raw_text'] = rawText
                    return return_data
                else:
                    return_data['error_code'] = 9106010
                    return_data['raw_json'] = json_voice
                    return_data['error_field'] = temperature_voice
                    return_data['correct_field'] = temperature_nlp
                    return_data['raw_text'] = rawText
                    return return_data

# 电话
# 任务一：添加service=localCmd的逻辑判断——已实现
# 任务二：添加rc=8的判断逻辑——已解决
# 任务三：尝试模拟通讯率逻辑实现
# 任务四：chat类型的话束尝试解决
# 崩溃id：47978、47478、47447、43282——已解决
def phone_check(slot_json, rawText):
    return_data = {}
    # 讯飞json(格式化json)
    json_voice_tmp = slot_json
    try:  # 若无法解析、表示讯飞乱码
        json_voice = json.loads(json_voice_tmp)
    except:
        return_data['error_code'] = 9170505
        return_data['raw_json'] = json_voice_tmp
        return_data['error_field'] = 9170505
        return_data['correct_field'] = 9170505
        return_data['raw_text'] = rawText
        return return_data
    service_voice = json_voice.get("service", 0)
    operation_voice = json_voice.get("operation")
    nameOrig_voice = json_voice.get("nameOrig")
    rc_voice = json_voice.get("rc")
    # 本地计算json
    json_nlp = models.domain_distribute(rawText)  # dict
    service_nlp = json_nlp['service']  # nlp解析的json
    if service_voice == 'localCmd':
        return_data['error_code'] = 9170500
        return_data['raw_json'] = json_voice
        return_data['error_field'] = 9170500
        return_data['correct_field'] = 9170500
        return_data['raw_text'] = rawText
        return return_data
    else:
        if rc_voice == '8':
            return_data['error_code'] = 9170500
            return_data['raw_json'] = json_voice
            return_data['error_field'] = 9170500
            return_data['correct_field'] = 9170500
            return_data['raw_text'] = rawText
            return return_data
        # case1:operation字段的对比
        if service_voice == service_nlp:  # telephone
            pass
        else:
            return_data['error_code'] = 9170504
            return_data['raw_json'] = json_voice
            return_data['error_field'] = service_voice
            return_data['correct_field'] = service_nlp
            return_data['raw_text'] = rawText
            return return_data
        # case2:operation字段的对比
        operation_nlp = json_nlp['operation']  # 可能出现在天窗中
        if operation_voice == operation_nlp :
            pass
        else:
            return_data['error_code'] = 9170501
            return_data['raw_json'] = json_voice
            return_data['error_field'] = operation_voice
            return_data['correct_field'] = operation_nlp
            return_data['raw_text'] = rawText
            return return_data
        # case3:nameOrig字段的对比
        nameOrig_nlp = json_nlp['nameOrig']
        if nameOrig_voice == nameOrig_nlp :
            return_data['error_code'] = 9170500
            return_data['raw_json'] = json_voice
            return_data['error_field'] = 9170500
            return_data['correct_field'] = 9170500
            return_data['raw_text'] = rawText
            return return_data
        else:
            return_data['error_code'] = 9170513
            return_data['raw_json'] = json_voice
            return_data['error_field'] = nameOrig_voice
            return_data['correct_field'] = nameOrig_nlp
            return_data['raw_text'] = rawText
            return return_data

# 其他应用 如 APP 行车记录仪等
def other_check(slot_json,rawText):
    return_data = {}
    json_voice_tmp = slot_json
    try:
        json_voice = json.loads(json_voice_tmp)
    except:
        return_data['error_code'] = 9999905
        return_data['raw_json'] = json_voice_tmp
        return_data['error_field'] = 9999905
        return_data['correct_field'] = 9999905
        return_data['raw_text'] = rawText
        return return_data
    return_data['error_code'] = 9999999
    return_data['raw_json'] = json_voice
    return_data['error_field'] = 9999999
    return_data['correct_field'] = 9999999
    return_data['raw_text'] = rawText
    return return_data
