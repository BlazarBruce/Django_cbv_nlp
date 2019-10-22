import nlp_web.config as config


def to_json(sen):
    text = sen
    nlp_score = 1.0
    shade_base_json = {
        "rawText": text,
        'nlp_score': nlp_score,
        'service': 'carControl',
        "rc": 0,
        'operation': '',
        'version': str(config.version),
        'semantic': {
            "slots": {
                'name': ''
            }
        }
    }
    open_lib = ['开']
    close_lib = ['关', '收', '拉', '官', '晚', '冠']
    stop_lib = ['停']
    half_lib = ['半']
    open_debug = False
    close_debug = False
    stop_debug = False
    half_debug = False
    open_index = 0
    close_index = 0
    for w in text:
        if w in stop_lib:
            stop_debug = True
        elif w in half_lib:
            half_debug = True
        if w in open_lib:
            open_index = sen.index(w)
            open_debug = True
        elif w in close_lib:
            close_index = sen.index(w)
            close_debug = True
    # 半闭遮阳帘
    if half_debug and close_debug:
        shade_base_json['semantic']['slots']['name'] = '一半遮阳帘'
        shade_base_json['operation'] = 'ClOSE'
    # 一半遮阳帘
    elif half_debug:
        shade_base_json['semantic']['slots']['name'] = '一半遮阳帘'
        shade_base_json['operation'] = 'OPEN'
    # 停止遮阳帘
    elif stop_debug:
        shade_base_json['semantic']['slots']['name'] = '遮阳帘'
        shade_base_json['operation'] = 'STOP'
    # 开遮阳帘
    elif open_debug and open_index >= close_index:
        shade_base_json['semantic']['slots']['name'] = '遮阳帘'
        shade_base_json['operation'] = 'OPEN'
    # 关遮阳帘
    elif close_debug:
        shade_base_json['semantic']['slots']['name'] = '遮阳帘'
        shade_base_json['operation'] = 'CLOSE'
    else:
        shade_base_json['semantic']['slots']['name'] = '遮阳帘'
        shade_base_json['operation'] = 'OPEN'
    return shade_base_json
