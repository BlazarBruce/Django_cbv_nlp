# -*- coding: utf-8  -*-
import jieba
import nlp_web.libs.phone as lib_ph

from nlp_web.code_bank.function import *
jieba.load_userdict(config.phone_path)
# 问题;“回个电话”逻辑不可用——已解决
# 问题：“给我电话”——已解决
# 问题：“给打电话给爱丽丝”、“给打电话给希瑞”——已解决
# 问题：“播放音乐哦坐打电话”——已解决

# 新问题：给吴子玉拨打电话
# 新问题：给吴子玉拨电话
# 新问题：给吴子玉波电话
def to_json(sen):
    sen = sen.replace("波电话", "打电话")  # 目前先暂时提花！！！！！！！！！
    segment = phone_filter(sen)  # 可以考虑对原始话束进行处理
    best = get_best_match(segment.filter_text, lib_ph.phone_call)
    print("best_match = " + best.best_match)
    noise_list = ['改个名', "改名"]  # 噪声词库
    pass_list = ['打电话', '拨打电话', '帮我打电话', '帮我拨打电话', '呼叫', '我要呼叫', '帮我呼叫', '我要打电话',
                 "我想打电话", "电话", "开启电话", "进入电话", "使用电话", "打开电话", "蓝牙电话", '给我电话']
    text = segment.raw_text
    rawtext_solution = segment.raw_text_solution
    nlp_score = best.nlp_score
    json_base = init_json_base_phone()
    # 去除噪声 如'我给你改个名字叫姚电话吧'
    for index in range(len(noise_list)):
        if noise_list[index] in rawtext_solution:
            data_json = query_json()
            data_json["rawText"] = text
            return data_json
    if '给打电话' in rawtext_solution and rawtext_solution[0] == '给':  # 解决“给打电话给于大头”
        rawtext_solution = rawtext_solution[1:-1] + rawtext_solution[-1]
    text_cut = jieba.lcut(rawtext_solution)
    json_base["nlp_score"] = nlp_score
    json_base["rawText"] = text
    if rawtext_solution in pass_list or '给' == rawtext_solution[-1]:
        return json_base
    # 查询刘亚楠的电话
    if "查询" in rawtext_solution:  # 查询逻辑
        json_base["operation"] = "QUERY"
        json_base["service"] = "contacts"
        text1 = rawtext_solution.replace("查询", "")
        real_name = text1.replace("的电话", "")
        json_base["name"] = real_name
        json_base["nameOrig"] = real_name
        return json_base
    if '呼叫' in rawtext_solution:  # 呼叫电话逻辑
        indx1 = rawtext_solution.index('呼叫')
        rawtext_solution = rawtext_solution[indx1:-1] + rawtext_solution[-1]
        if '电话'in rawtext_solution:
            indx1 = rawtext_solution.index('呼叫')
            indx2 = rawtext_solution.index('电话')
            if indx2-indx1 == 2:
                real_name = rawtext_solution[indx2+2:-1] + rawtext_solution[-1]
                json_base["name"] = real_name
                json_base["nameOrig"] = real_name
                return json_base
            else:
                temp = rawtext_solution.replace('呼叫', '')
                temp = temp.replace('的电话', '')
                real_name = temp.replace('电话', '')
                json_base["name"] = real_name
                json_base["nameOrig"] = real_name
                return json_base
        else:
            real_name = rawtext_solution.replace('呼叫', '')
            json_base["name"] = real_name
            json_base["nameOrig"] = real_name
            return json_base

    if "给" in rawtext_solution and "回电话"not in rawtext_solution and "回个电话" not in rawtext_solution:
        try:
            idx1 = text_cut.index("给")
            idx2 = text_cut.index("电话")
        except ValueError:
            idx1 = rawtext_solution.index("给")
            idx2 = rawtext_solution.index("电话")
        if idx1 > idx2:
            num = rawtext_solution.index('给') + 1
            temp_name = rawtext_solution[num:-1] + rawtext_solution[-1]
            if temp_name[0] == '我':
                temp_name = temp_name[1:-1] + temp_name[-1]
            json_base["name"] = temp_name
            json_base["nameOrig"] = temp_name
            return json_base
        else:
            num1 = rawtext_solution.index('给') + 1
            try:
                num2 = rawtext_solution.index('打')  # 给刘亚楠的电话  会使程序崩溃
            except ValueError:
                text = rawtext_solution.replace("的", "打")
                num2 = rawtext_solution.index('打')
            temp_name = rawtext_solution[num1:num2]
            if temp_name[0] == '我':
                temp_name = temp_name[1:-1] + temp_name[-1]
            json_base["name"] = temp_name
            json_base["nameOrig"] = temp_name
            return json_base
    else:  # 可以在此处添加“回电话”的逻辑
        if "回"in rawtext_solution:  # 实现“回电话”的逻辑
            try:
                idx6 = rawtext_solution.index("回电话")
            except ValueError:
                try:
                    idx6 = rawtext_solution.index("回个电话")
                except ValueError:
                    idx6 = None
            if idx6 != None:  # 给刘大头回电话、刘大头回电话
                if rawtext_solution[0] == "给":
                    temp_name = rawtext_solution[1:-1] + rawtext_solution[-1]
                    temp_name = temp_name.replace("回电话", "")
                    temp_name = temp_name.replace("回个电话", "")
                    json_base["name"] = temp_name
                    json_base["nameOrig"] = temp_name
                    return json_base
                else:
                    temp_name = rawtext_solution.replace("回电话", "")
                    temp_name = temp_name.replace("回个电话", "")
                    if temp_name[0] == "给":
                        temp_name = temp_name.replace("给", "")
                    json_base["name"] = temp_name
                    json_base["nameOrig"] = temp_name
                    return json_base
            else:  # 解决“回刘大头的电话”
                name = ""
                temp_name = rawtext_solution.replace("电话", "")
                temp_name = temp_name.replace("回", "")
                if temp_name[-1] == "的":
                    name = temp_name[:-1]
                json_base["name"] = name
                json_base["nameOrig"] = name
                return json_base
        try:  # “拨打xx” 的问题
            idx3 = text_cut.index("打")
            idx4 = text_cut.index('电话')
        except ValueError:
            if "拨打" in text_cut and "电话" not in text_cut:
                name = text.replace("拨打", "")
                json_base["name"] = name
                json_base["nameOrig"] = name
                return json_base
            try:
                idx3 = text_cut.index("拨打")
                idx4 = text_cut.index('电话')
            except ValueError:  # 处理 查询逻辑
                data_json = query_json()
                data_json["rawText"] = text
                return data_json

        if idx4 == 1:
            length = len(text_cut)
            temp_name = ''
            for idx5 in range(2, length):
                temp_name += text_cut[idx5]
            if temp_name[0] == '我':
                temp_name = temp_name[1:-1] + temp_name[-1]
            json_base["name"] = temp_name
            json_base["nameOrig"] = temp_name
            return json_base
        # 问题：“刘大头打电话”
        elif text_cut[-2] == '打' and text_cut[-1] == '电话':
            temp_name = rawtext_solution[0:-3]
            if temp_name[0] == '我':
                temp_name = temp_name[1:-1] + temp_name[-1]
            json_base["name"] = temp_name
            json_base["nameOrig"] = temp_name
            return json_base
        elif idx4 == 3:
            json_base["name"] = text_cut[idx3 + 1]
            json_base["nameOrig"] = text_cut[idx3 + 1]
            return json_base
        elif idx4 == 4:
            temp_name = text_cut[idx3 + 1] + text_cut[idx3 + 2]
            if temp_name[0] == '我':
                temp_name = temp_name[1:-1] + temp_name[-1]
            json_base["name"] = temp_name
            json_base["nameOrig"] = temp_name
            return json_base
        else:
            return json_base

# 呼叫小迪，你好----未解决
if __name__ == "__main__":
    # sen = '请帮我呼叫刘大头'
    # segment = phone_filter(sen)
    # print(segment.raw_text, segment.filter_text)

    # text = "给打电话给爱丽丝"
    # jieba.load_userdict(config.phone_path)
    # text_cut = jieba.lcut(text)
    # print(text_cut)

    rst = to_json('呼叫二愣子')
    print(rst)

# 说明：synonym 与jieba 的分词效果不同——重要，有待研究
