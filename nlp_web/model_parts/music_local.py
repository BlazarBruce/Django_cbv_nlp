# Author:feng.yuzhang
# Time:2019/7/22 17:23
# Project:nlp3
# -*- coding: utf-8  -*-
# Another Version
# 基于以下几种假设:
# 1.歌手名字中不带‘的’字
# 2.曲风识别时自带歌字
# 3.说歌曲XX时默认是歌曲名
import jieba
import nlp_web.config as config
keywords = ['播放', '放', '一首', '点播', '听']
style = ['流行歌', '国语歌', '粤语歌', '古典歌', '爵士歌', '摇滚歌']
de = '的'
blue_tooth = '蓝牙'
local = '本地'
song = '歌曲'


def local_music_json(sen):
    basic_json = {"album": "", "appName": "", "artist": "",
                  "category": "", "song": "", "source": "",
                  "operation": "", "rawText": sen, "rc": "0",
                  "service": "music"}
    # 返回的字的位置
    jieba.load_userdict(config.music_path)
    cut_results = jieba.lcut(sen)

    # 采用enumerate函数，返回可遍历对象的下标和值，这里用来确定所有de的位置
    de_location = [i for i, x in enumerate(cut_results) if x == '的']
    if len(de_location) == 0:
        for word in cut_results:
            if word in keywords:
                basic_json['operation'] = 'PLAY'
                # 起始词的位置
                sl = cut_results.index(word)
                basic_json['song'] = ''.join(cut_results[sl + 1:])
                song_cut = jieba.lcut(basic_json['song'])
                for song_word in song_cut:
                    if song_word == '音乐':
                        basic_json['song'] = ''
                        break
                    elif song_word in keywords:
                        basic_json['song'] = basic_json['song'].replace(
                            song_word, '')
                        break
                break
            else:
                basic_json['operation'] = 'PLAY'
                basic_json['song'] = sen

    elif len(de_location) == 1:  # 的字歌名存在BUG
        for word in cut_results:
            if word in keywords:
                basic_json['operation'] = 'PLAY'
                sl = cut_results.index(word)  # start location
                dl = de_location[0]  # de location
                el = len(sen) - 1   # end location 下同
                basic_json['artist'] = ''.join(cut_results[sl + 1:dl])
                basic_json['song'] = ''.join(cut_results[dl + 1:el])
                # 处理歌字和其他一些特殊情况，剩余情况待定
                if basic_json['song'] == '歌' or basic_json['song'] == '歌曲':
                    basic_json['artist'] = ''.join(cut_results[sl + 1:dl])
                    basic_json['song'] = ''
                    break
                elif basic_json['song'] in style:
                    basic_json['artist'] = ''.join(cut_results[sl + 1:dl])
                    basic_json['category'] = str(
                        basic_json['song']).replace(
                        '歌', '')
                    basic_json['song'] = ''
                    break
            else:
                dl = de_location[0]  # de location
                el = len(sen) - 1  # end location 下同
                basic_json['artist'] = ''.join(cut_results[0:dl - 1])
                basic_json['song'] = ''.join(cut_results[dl + 1:el])
                break
    elif len(de_location) == 2:
        for word in cut_results:
            if word in keywords:
                basic_json['operation'] = 'PLAY'
                sl = cut_results.index(word)
                dl1 = de_location[0]  # 第一个de的位置
                basic_json['artist'] = ''.join(cut_results[sl + 1:dl1])
                basic_json['song'] = ''.join(cut_results[dl1 + 1:])
                break
    if blue_tooth in cut_results:
        basic_json['operation'] = 'PLAY'
        basic_json['source'] = '蓝牙音乐'
        basic_json['song'] = ''
    elif song in cut_results:
        basic_json['operation'] = 'PLAY'
        song_location = cut_results.index(song)
        basic_json['song'] = ''.join(cut_results[song_location + 1:])
    else:
        basic_json['operation'] = 'PLAY'
        basic_json['song'] = sen
    return basic_json


