import jieba
from nlp_web.code_bank.number import chinese_to_number as cn
import re
jieba.add_word('soc')


def init_json(sen):
    init_soc_json = dict(
        category='SOC',
        color='',
        level='',
        model='',
        name='目标值',
        nameValue='',
        value='',
        operation='SET',
        rawText=sen,
        rc='0',
        service='carControl')
    return init_soc_json


def soc_to_json(sen):
    sen.lower()
    result_json = init_json(sen)
    tmp = jieba.lcut(sen)
    # soc...25
    if re.match('\\w{0,10}soc\\w{0,30}\\d$', sen):
        if cn(sen) != 0:
            result_json['value'] = cn(sen)
        else:
            result_json['value'] = tmp[-1]
    # soc ...25%
    elif re.match('\\w{0,10}soc\\w{0,30}%$', sen):
        result_json['value'] = tmp[-1].replace('%', '')
    # soc ...什食十拾
    elif re.match('\\w{0,10}soc\\w{0,30}[什食十拾时]$', sen):
        result_json['value'] = '10'
        if re.match('\\w{0,10}soc\\w{0,30}[一二三四五六七八九][什食十拾时]$', sen):
            result_json['value'] = cn(sen)
    elif re.match('\\w{0,10}soc\\w{0,30}[一二三四五六七八九十百]$', sen):
        result_json['value'] = cn(sen)
    for key_words in tmp:
        if key_words in ['打开', '开']:
            result_json['name'] = 'name'
            result_json['value'] = 'value'
            break
        elif key_words in ['最大', '最高', '最大值']:
            result_json['name'] = '目标值max'
            result_json['value'] = 'value'
            break
        elif key_words in ['最低', '最小', '最少', '最小值']:
            result_json['name'] = '目标值min'
            result_json['value'] = 'value'
            break
        elif key_words in ['中间', '中等']:
            result_json['name'] = '目标值mid'
            result_json['value'] = 'value'
            break
        elif key_words in ['增加', '增大', '调大', '大点', '大', '加', '调高']:
            result_json['name'] = '目标值+'
            if cn(sen) != 0:
                result_json['value'] = cn(sen)
                if result_json['value'] == 1:
                    result_json['value'] = ''
            break
        elif key_words in ['减少', '减小', '调小', '小点', '小', '调低']:
            result_json['name'] = '目标值-'
            if cn(sen) != 0:
                result_json['value'] = cn(sen)
                if result_json['value'] == 1:
                    result_json['value'] = ''
            break
        elif key_words in ['默认值']:
            result_json['name'] = '目标值默认值'
    if result_json == init_json(sen):
        return {"commandId": 100005,
                "operation": "query",
                "rawText": sen,
                "rc": "4",
                "service": "pattern"}
    return result_json
