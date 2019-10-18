import os
import jieba
import requests
from lxml import etree

import nlp_web.config as config                                    # 文件路径配置文件
from nlp_web.code_bank.function import query_json                  # 查询基础json
from nlp_web.code_bank.function import word_data_solution          # 话束预处理函数
from nlp_web.code_bank.function import init_json_base_music        # 音乐基础json
from nlp_web.code_bank.function import init_json_base_navigation   # 导航基础json
from nlp_web.model_parts import model_domain_atmosphere            # 氛围灯逻辑处理
from nlp_web.model_parts import model_domain_phone                 # 电话逻辑处理
from nlp_web.model_parts import model_roof                         # 天窗逻辑处理
from nlp_web.model_parts import model_shade                        # 遮阳帘逻辑处理
from nlp_web.model_parts import model_radio                        # 电台逻辑处理
from nlp_web.model_parts import model_chair                        # 座椅逻辑处理
from nlp_web.model_parts import model_music                        # 音乐逻辑处理
from nlp_web.model_parts import model_aircontrol                   # 空调逻辑处理
from nlp_web.model_parts import model_soc                          # SOC逻辑处理
from nlp_web.model_parts import model_energy_feedback              # 能量回馈逻辑处理
from nlp_web.model_parts import model_navigation                   # 导航逻辑处理
from nlp_web.model_parts import model_app                          # 应用模块
from nlp_web.libs.model_libs import domain_atmosphere_lib          # 氛围灯关键词库
from nlp_web.libs.model_libs import domain_phone_lib               # 电话关键词库
from nlp_web.libs.model_libs import domain_dis_phone_lib           # 电话业务干扰词库
from nlp_web.libs.model_libs import domain_air_conditioners_lib    # 空调关键词库
from nlp_web.libs.model_libs import domain_moon_roof_lib           # 天窗关键词库
from nlp_web.libs.model_libs import domain_shade_screens_lib       # 遮阳帘关键词库
from nlp_web.libs.model_libs import domain_seat_lib                # 座椅关键词库
from nlp_web.libs.model_libs import domain_music_lib               # 音乐关键词库
from nlp_web.libs.model_libs import domain_novel_lib               # 小说关键词库
from nlp_web.libs.model_libs import domain_navigation_lib          # 导航关键词库
from nlp_web.libs.model_libs import domain_radio_lib               # 电台关键词库
from nlp_web.libs.model_libs import domain_energy_lib              # 能量反馈关键词库
from nlp_web.libs.model_libs import domain_total_libs              # 支持业务关键词总库


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

def getHtml(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except:
        print('-----error-----')

def domain_distribute(sen):
    """
    input:   用户话束
    :return: 对应的正确json
    """
    # 该个性化词库需要按照新逻辑重新加载
    jieba.load_userdict(config.personal_dict_path)
    # jieba.load_userdict(config.level_one_dict_path)  # 将词典合并层一个词库
    jieba.suggest_freq(('开', '天窗'), True)
    jieba.suggest_freq(('看', '星星'), True)
    jieba.suggest_freq(('看', '月亮'), True)
    jieba.suggest_freq(('看', '太阳'), True)
    jieba.add_word('一半')
    word_list, part_list = word_data_solution(sen)  # 话束预处理
    print(word_list)
    print(part_list)  # 问题：分发分不对——词性标注解决！！1
    if '我不想听' in sen or '换一首' in sen or '换一个' in sen:
        return {"operation": "query", "rawText": "你想听什么？？？",
                "rc": "4", "service": "question"}
    if '成都' == sen:
        return {"operation": "query", "rawText": "请问是要导航去成都还是要听歌曲成都？",
                "rc": "4", "service": "question"}
    if '晴天' == sen:
        return {"operation": "query", "rawText": "请说明是歌曲晴天还是天气晴天？",
                "rc": "4", "service": "question"}

    for item in word_list:
        if item in domain_total_libs:
            # 氛围灯
            if item in domain_atmosphere_lib:
                return model_domain_atmosphere.to_json(sen)
            # 空调
            elif item in domain_air_conditioners_lib:
                return model_aircontrol.to_json(sen)
            # 天窗
            elif item in domain_moon_roof_lib:
                return model_roof.to_json(sen, item)
            # 遮阳帘
            elif item in domain_shade_screens_lib:
                return model_shade.to_json(sen)
            # 座椅
            elif item in domain_seat_lib:
                return model_chair.to_json(sen)
            # 电话
            elif item in domain_phone_lib:
                is_phone = True
                for index in range(len(domain_dis_phone_lib)):
                    if domain_dis_phone_lib[index] in sen:
                        is_phone = False
                        break
                if is_phone:
                    return model_domain_phone.to_json(sen)
                else:
                    pass
            # 音乐
            elif item in domain_music_lib:
                return model_music.music_json(sen, word_list, part_list)
            # 小说
            elif item in domain_novel_lib:
                return {'rawText': sen, 'domain': '小说'}
                # 同上
            # 导航
            elif item in domain_navigation_lib:
                return model_navigation.to_json(sen, word_list, part_list)
            # 电台
            elif item in domain_radio_lib:
                return model_radio.to_json(sen)
            # SOC
            elif item in ['soc']:
                return model_soc.soc_to_json(sen)
            # 能量回馈
            elif item in domain_energy_lib:
                return model_energy_feedback.to_json(sen)
        # 应用模块
        elif 'app' in part_list:
            data_json = model_app.app_to_json(sen)
            data_json['name'] = word_list[part_list.index('app')]
            if '退出' in sen or '关闭' in sen or '关了' in sen:
                data_json['operation'] = 'CLOSE'
            return data_json
        # 音乐业务、歌手、歌曲名
        elif 'singer' in part_list or 'song'in part_list:
            data_json = init_json_base_music()
            singer_name = ''
            song_name = ''
            try:
                singer_name = word_list[part_list.index('singer')]
            except ValueError:
                song_name = word_list[part_list.index('song')]
            try:
                song_name = word_list[part_list.index('song')]
            except ValueError:
                singer_name = word_list[part_list.index('singer')]
            if 'song' in part_list and 'singer'in part_list:
                data_json['song'] = song_name
                data_json['artist'] = singer_name
                data_json['rawText'] = sen
                return data_json
            elif 'singer'in part_list:
                data_json['artist'] = singer_name
                data_json['rawText'] = sen
                return data_json
            elif 'song'in part_list:
                data_json['song'] = song_name
                data_json['rawText'] = sen
                return data_json
        # 导航业务
        elif 'destination' in part_list:
            data_json = init_json_base_navigation()
            destination = word_list[part_list.index('destination')]
            data_json["endLoc"] = destination
            data_json['rawText'] = sen
            return data_json

    try:
        url = 'https://www.baidu.com/s?wd=' + sen
        search_html = getHtml(url)
        selector = etree.HTML(search_html)
        search_result = selector.xpath("//div[@id='content_left']/div/h3/a")[0]
        search_content = search_result.xpath('string(.)').strip()
        print(search_content)
        if '歌' in search_content or '音乐' in search_content or '原唱' in search_content:
            return model_music.music_json(sen, word_list, part_list)
        else:
            data_json = query_json()
            data_json["rawText"] = sen
            return data_json
    except:
        print("请求百度出现错误")
        data_json = query_json()
        data_json["rawText"] = sen
        return data_json


# 考虑在不同位置加载不同的词库

