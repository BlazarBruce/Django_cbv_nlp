import nlp_web.config as config
import synonyms
from nlp_web.code_bank.config import Word
from nlp_web.code_bank.function import get_best_match
from nlp_web.libs.model_libs import domain_moon_roof_lib


def to_json(sen, item):
    words = []
    sens_seg = synonyms.seg(sen)
    for index in range(len(sens_seg[0])):
        word = Word(
            string=str(
                sens_seg[0][index]), tag=str(
                sens_seg[1][index]))
        words.append(word)
    text = sen
    best = get_best_match(item, domain_moon_roof_lib, debug=True)
    nlp_score = best.nlp_score
    open_debug = False
    close_debug = False
    half_debug = False
    stop_debug = False
    ventilate_debug = False
    sunshade_json = {
        "rawText": text,
        'nlp_score': nlp_score,
        'service': 'carControl',
        "rc": 0,
        'operation': '',
        'version': str(config.version),
        'semantic': {
            "slots": {
                'name': '',
                'mode': ''
            }
        }
    }
    if item == '天窗':
        open_lib = ['开', '升', '拉']
        close_lib = ['管', '关', '收', '锁', '毕', '官', '晚', '冠']
        half_lib = ['半']
        stop_lib = ['停']
        ventilate_lib = ['风', '透']
        open_index = 0
        close_index = 0
        for w in text:
            if w in open_lib:
                open_index = sen.index(w)
                open_debug = True
            elif w in close_lib:
                close_index = sen.index(w)
                close_debug = True
            elif w in half_lib:
                half_debug = True
            elif w in stop_lib:
                stop_debug = True
            elif w in ventilate_lib:
                ventilate_debug = True
        # 半闭天窗
        if half_debug and close_debug:
            sunshade_json['operation'] = 'CLOSE'
            sunshade_json['semantic']['slots']['name'] = '一半天窗'
        # 半开天窗
        elif half_debug:
            sunshade_json['operation'] = 'OPEN'
            sunshade_json['semantic']['slots']['name'] = '一半天窗'
        # 开天窗通风
        elif ventilate_debug and not close_debug:
            sunshade_json['operation'] = 'OPEN'
            sunshade_json['semantic']['slots']['name'] = '天窗'
            sunshade_json['semantic']['slots']['mode'] = '通风'
        # 停止天窗
        elif stop_debug:
            sunshade_json['operation'] = 'STOP'
            sunshade_json['semantic']['slots']['name'] = '天窗'
        # 关天窗通风
        elif ventilate_debug and close_debug:
            sunshade_json['operation'] = 'CLOSE'
            sunshade_json['semantic']['slots']['name'] = '天窗'
            sunshade_json['semantic']['slots']['mode'] = '通风'
        # 打开天窗
        elif open_debug and open_index >= close_index:
            sunshade_json['operation'] = 'OPEN'
            sunshade_json['semantic']['slots']['name'] = '天窗'
        # 关闭天窗
        elif close_debug:
            sunshade_json['operation'] = 'CLOSE'
            sunshade_json['semantic']['slots']['name'] = '天窗'
        else:
            sunshade_json['operation'] = 'OPEN'
            sunshade_json['semantic']['slots']['name'] = '天窗'
    else:
        word_lib = ['不', '不想', '不看']
        for w in words:
            if w.string in word_lib:
                close_debug = True
        # 关闭天窗
        if close_debug:
            sunshade_json['operation'] = 'CLOSE'
            sunshade_json['semantic']['slots']['name'] = '天窗'
        # 打开天窗
        else:
            sunshade_json['operation'] = 'OPEN'
            sunshade_json['semantic']['slots']['name'] = '天窗'
    return sunshade_json
