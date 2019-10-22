import synonyms
import nlp_web.config as config
from nlp_web.code_bank.config import Best
from nlp_web.code_bank.config import Word, Segment


def get_best_match(sentence, library, debug=False, seg=True, ignore=False):
    """
    句子相似度对比取得最相似句子和值
    :param sentence: 处理后的话束
    :param library: 句库
    :param debug: 输出日志开关
    :param seg: 是否分词
    :param ignore: 是否忽略错误
    :return: BestSentence对象
    """
    nlp_score = 0
    best_sentence = ''
    for param in library:
        rate = synonyms.compare(sentence, param, seg=seg, ignore=ignore)
        if rate >= nlp_score:
            nlp_score = rate
            best_sentence = param
        if debug:
            print('param = ' + param + ',rate = %s' % rate)
    if debug:
        print(
            'the final best_sentence is %s , nlp_score is：%s' %
            (best_sentence, nlp_score))
    return Best(text=sentence, best_match=best_sentence, nlp_score=nlp_score)

# 氛围灯得分提升函数
def filter_atmosphere(sen):
    interfere_word = ['请', '帮', '亮度', '想']
    plus_word = ['气氛', '氛围', '七彩', '最亮', '最暗','白光']  # 一些名词也具有有意义的词性——得分问题仍未解决!!!!!!!!
    sen_filter = ''
    sens_seg = synonyms.seg(sen)
    for index in range(len(sens_seg[0])):
        word = Word(
            string=str(
                sens_seg[0][index]), tag=str(
                sens_seg[1][index]))
        print(word.string, word.tag)
        if (word.tag == 'v' or word.tag == 'ne'or word.tag ==
                'm'or word.tag == 'n'or word.string in plus_word) and word.string not in interfere_word:
            sen_filter += word.string
    return Segment(raw_text=sen, filter_text=sen_filter)

# 电话模块得分提升函数
def phone_filter(sen):
    # 这个过滤函数还存在一些问题！！！！！！！
    interfere_word = ['请', '帮', '想']
    raw_text_soution = {'打电话给打电话给':'打电话给', '打给打电话给':'打电话给','给打电话给':'打电话给'}  # 目的：将不标准的话束转换为完全等价的说法
    key_list = [key for key, value in raw_text_soution.items()]  # 列表推导
    value_list = [value for key, value in raw_text_soution.items()]
    # 原始话束进行处理
    rawtext_solution = sen
    for item in range(len(key_list)):
        if key_list[item] in sen:
            rawtext_solution = sen.replace(key_list[item], value_list[item])
            break
    # 话束过滤处理
    sen_filter = ''
    sens_seg = synonyms.seg(sen)
    for index in range(len(sens_seg[0])):
        word = Word(
            string=str(
                sens_seg[0][index]), tag=str(
                sens_seg[1][index]))
        print(word.string, word.tag)
        if (word.tag == 'v' or word.tag ==
                'ne') and word.string not in interfere_word:
            sen_filter += word.string
    return Segment(raw_text=sen, filter_text=sen_filter, rawtext_solution=rawtext_solution)

# 氛围灯基础json
def init_json_base_atmosphere():
    return {
        "rawText": "",
        'nlp_score': 0,
        'service': "carControl",
        "rc": 0,
        'operation': "",
        'semantic': {
            'slots': {
                "category": "",
                'name': "氛围灯",
                        "nameValue": "",
                        "color": ""
            }
        },
        'version': str(config.version),
        "wstext": ""
    }
# 查询基础json
def query_json():
    return {
        "commandId": 100005,
        "operation": "query",
        "rawText": "",
        "rc": "4",
        "service": "pattern"
    }

# 电话业务基础json
def init_json_base_phone():
    return {
        "category": "",
        "code": "",
        "rawText": "",
        "nlp_score": 0,
        "service": "telephone",
        "rc": 0,
        "operation": "DIAL",
        "name": "",
        "nameOrig": "",
        "teleOperator": "",
        "commandId": 103003,
        "version": str(config.version),
        "wstext": ""
    }
# 音乐歌曲名，歌手名基础json
def init_json_base_music():
    return {
        'album': '',
        'appName': '',
        'artist': '',
        'category': '',
        'song': '',
        'source': '',
        'operation': 'PLAY',
        'rawText': '',
        'rc': '0',
        'service': 'music'
    }
# 导航基础json
def init_json_base_navigation():
    return {
        "city":"CURRENT_CITY",  # 目前所在城市（该字段目前不予赋值）
        "endLoc":"",            # 导航目的地（结束地点）
        "nameType":"",
        "passLoc":"",           # 途经点
        "startLoc":"",          # 起点
        "commandId":102002,
        "operation":"ROUTE",
        "rawText":"",
        "rc":"0",
        "service":"map"
    }

# 话束预处理函数
def word_data_solution(sen):
    word_list = []  # 分词词语
    part_list = []  # 分词词性
    sens_seg = synonyms.seg(sen)
    for index in range(len(sens_seg[0])):
        word_list.append(sens_seg[0][index])
        part_list.append(sens_seg[1][index])
    return word_list, part_list









