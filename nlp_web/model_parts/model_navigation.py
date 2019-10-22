"""导航业务逻辑实现"""
from nlp_web.libs.navigation import *
from nlp_web.code_bank.function import get_best_match
from nlp_web.code_bank.function import init_json_base_navigation

# 词性标注解决原理：一个事物万钢有多重“身份”（标签）
# 例如 “北京”——名词、地名、城市、首都、清华大学、故宫、直辖市、北京的状况.....
# 例如 “张碧晨”—— 人名、歌手、天津音乐学艳......
# 例如 “比亚迪”—— 汽车、总部深圳、王传福、新能源领导者、全新一代唐.......
# 例如 “王传福”—— 名词、人名、不是歌手、比亚迪创始人......
# “不智能”用另一个词说是“傻”、之所以说傻是因为知道的少！！！！
# 现在的问题是
# 问题一：怎样让机器知道的多？
# 问题二：怎样将这些信息网络起来？怎样存储？怎样不丢失信息的编码？

# 从句子的层面上考虑
# 例如 “你听说过李白吗？”
# “你听说过吗”：分发、将要讨论的问题分发（引导）到要谈论的换题（分发需要解决的问题;"氛围灯四什么东西？“、”打开氛围灯“
# 是两个完全不一样的分支）
# “李白”： 重要的执行逻辑、礼拜的所有知识、唐代诗人、豪放派、放荡不羁、杜甫的偶像......

# things not strings 不要无意义的字符串，需要文本背后的对象或事物
# 知识图谱：https://www.cnblogs.com/leoxk/p/9099090.html
# 知识图谱的一种定义：A knowledge graph consists of a set of interconnected typed entities and their attributes.
# 知识图谱是由一些相互连接的实体以及它们的属性构成的。知识图谱由一条条知识组成，每条知识可以表示为一个SPO三元组(Subject-Predicate-Object)。
# 特定场景特定词性建构、怎样知道“预置”知识

def to_json(rawText, word_list, part_list):
    """
    # 导航到国际大酒店、导航到背景天安门
    # 我想去大润发超市
    # 附近的4s店
    # 导航到附近的酒店、导航去.....
    # 我想去附近的酒店、想要去.....
    # 游乐场、市民中心、万达广场
    # “莲花山公园导航去”、“莲花山公园，导航到”

    # 打开导航、开启导航
    # 退出导航、结束导航

    进阶问题：
    你好，我想去附近的商场
    """
    if 'shop' in part_list:
        json_base = init_json_base_navigation()
        json_base["rawText"] = rawText
        json_base["endLoc"] = '附近的超市'
        return json_base
    best = get_best_match(rawText, navigayion_libs)
    best_match = best.best_match
    print("sen_max = " + best_match)
    # 正常逻辑处理
    if best_match in navigayion_lib_process:
        return navigation_processing(rawText, word_list, part_list)
    # 打开导航
    if best_match in navigayion_lib_open:
        return navigation_open(rawText)
    # 退出导航
    if best_match in navigayion_lib_close:
        return navigation_close(rawText)

# 处理除打开、退出外的其他逻辑
def navigation_processing(rawText,word_list, part_list):
    # 该逻辑有待优化！！！！！！
    json_base = init_json_base_navigation()
    json_base["rawText"] = rawText
    if 'destination' in part_list:
        destination = word_list[part_list.index('destination')]
        json_base["endLoc"] = destination
        return json_base
    else:  # 需要解决有“停用词”的问题、“小迪你好，导航到莲花山公园吧”
        if "导航" in rawText:
            level_pro = rawText.replace("导航去", '')
            level_one = level_pro.replace("导航到", '')
            level_two = level_one.replace("导航去", '')
            level_three = level_two.replace("附近的", '')
            level_four = level_three.replace("周边的", '')
            destination = level_four.replace("最近的", '')
            json_base["endLoc"] = destination
            return json_base
        if "我想去" in rawText:
            level_pro = rawText.replace("我想去", '')
            level_one = level_pro.replace("附近的", '')
            level_two = level_one.replace("周边的", '')
            destination = level_two.replace("最近的", '')
            json_base["endLoc"] = destination
            return json_base
        if "我要去" in rawText:
            level_pro = rawText.replace("我要去", '')
            level_one = level_pro.replace("附近的", '')
            level_two = level_one.replace("周边的", '')
            destination = level_two.replace("最近的", '')
            json_base["endLoc"] = destination
            return json_base


# 打开导航
def navigation_open(rawText):
    json_base = init_json_base_navigation()
    json_base["rawText"] = rawText
    json_base["operation"] = 'OPEN'
    return json_base

# 退出导航
def navigation_close(rawText):
    json_base = init_json_base_navigation()
    json_base["rawText"] = rawText
    json_base["operation"] = 'CLOSE'
    return json_base

# 对导航业务、应用场景、业务特点进行分析！！！！！！
# 那些话我会对你说，那些话我不会对你说！！！！！







