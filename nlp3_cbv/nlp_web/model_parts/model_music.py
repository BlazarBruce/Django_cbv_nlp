import jieba
import requests
import re
from nlp_web.model_parts.music_local import local_music_json


keywords = ['播放', '放', '一首', '点播', '听', '放首', '播放歌曲']
style = ['流行', '国语', '粤语', '古典', '爵士', '民乐',
         '摇滚', '怀旧', '蓝调', '原创', '原生']
local = ['本地', '蓝牙', 'u盘', 'U盘']
control = ['上一首', '上一个', '上一曲', '下一个', '下一首', '下一曲']


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def netease_music_api(text):
    try:
        base_url = 'http://39.108.166.55:3000/search?keywords='  # 接口部署到外网
        url = base_url + text
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        api_json = r.json()
        # 目前暂时先取第一个，若后续需要多重展示，再取后续让用户选择
        try:
            result = api_json['result']['songs'][0]
            # 取出歌曲
            song = result.get('name', 0)
            # 取出歌手
            artist = result['artists'][0]['name']
        except KeyError:
            song = '未获取到该值'
            artist = '未获取到该值'

    except requests.exceptions.ConnectionError:
        # 想办法给用户提示框，或者语音播报他没有联网
        print('您还没有联网，请检查网络连接')
        song = local_music_json(text).get('song', '未获取到该值')
        artist = local_music_json(text).get('artist', '为获取到该值')
    return song, artist


def music_json(text, word_list,  part_list):
    basic_json = {"album": "", "appName": "", "artist": "",
                  "category": "", "song": "", "source": "",
                  "operation": "", "rawText": text, "rc": "0",
                  "service": "music"}
    if 'song'in part_list or 'singer'in part_list:
        singer_name = ""
        song_name = ""
        try:
            singer_name = word_list[part_list.index('singer')]
        except ValueError:
            song_name = word_list[part_list.index('song')]
        try:
            song_name = word_list[part_list.index('song')]
        except ValueError:
            singer_name = word_list[part_list.index('singer')]
        basic_json["artist"] = singer_name
        basic_json["song"] = song_name
        return basic_json

    jieba.load_userdict('nlp_web/data/level_one_dict.txt')
    jieba.add_word('u盘')
    jieba.add_word('U盘')

    cut_results = jieba.lcut(text)

    # 采用enumerate函数，返回可遍历对象的下标和值，这里用来判断执行什么
    final_results = enumerate(cut_results)
    # 先处理特殊的
    for word in cut_results:
        if word in style:
            basic_json['operation'] = 'PLAY'
            basic_json['category'] = word
            return basic_json
        elif word in control:
            special_json = {"category": "曲目控制", "keycode": "", "name": word,
                            "nameScn": "", "nameValue": 0, "time": "", "operation": "",
                            "rawText": text, "rc": "0", "service": "cmd"}
            return special_json
        elif word in local:
            basic_json['operation'] = 'PLAY'
            basic_json['source'] = word
            return basic_json

    # 再处理一般的

    send_to_api_sentence = text
    for index, word in final_results:
        if word in keywords:
            # 当关键词在头尾时，直接去掉丢进api
            if word == cut_results[0] or word == cut_results[-1]:
                send_to_api_sentence = send_to_api_sentence.replace(word, '')
            # 否则就把关键词前面的一长串丢掉，然后丢进api
            else:
                tmp = cut_results[0:index+1]
                # 去除关键词本身和之前的噪音
                key_words_noise = ''.join(tmp)
                send_to_api_sentence = send_to_api_sentence.replace(key_words_noise, '')
    # 当一切的一切都不执行时，那就丢整句话吧！ლ(ó﹏òლ)
    other_noise = re.findall(r'听|音乐|，|,|小迪|小弟|好吧|你好|歌曲|放个|打开|请问|有没有|'
                             r'我要点|一下|一个|帮我|找|一首|来|我要|呃|我想|嗯|录音',
                             send_to_api_sentence)
    # 人工降噪算法，是不是很()这个词你来补充
    for noise in other_noise:
        send_to_api_sentence = send_to_api_sentence.replace(noise, '')
    if send_to_api_sentence == '':
        basic_json['operation'] = 'PLAY'
        return basic_json
    # 这里看看送入的词语
    song, artist = netease_music_api(send_to_api_sentence)
    basic_json['operation'] = 'PLAY'
    basic_json['song'] = song
    basic_json['artist'] = artist
    return basic_json

