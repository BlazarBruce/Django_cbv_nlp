import synonyms
from nlp_web.code_bank.config import Word

common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key] = common_used_numerals_tmp[key]

def replace_chinese(sen):
    if "零" in sen:
        sen = sen.replace("零", "0")
    if "幺" in sen:
        sen = sen.replace("幺", "1")
    if "一" in sen:
        sen = sen.replace("一", "1")
    if "二" in sen:
        sen = sen.replace("二", "2")
    if "三" in sen:
        sen = sen.replace("三", "3")
    if "四" in sen:
        sen = sen.replace("四", "4")
    if "五" in sen:
        sen = sen.replace("五", "5")
    if "六" in sen:
        sen = sen.replace("六", "6")
    if "七" in sen:
        sen = sen.replace("七", "7")
    if "八" in sen:
        sen = sen.replace("八", "8")
    if "九" in sen:
        sen = sen.replace("九", "9")
    if "点" in sen:
        sen = sen.replace("点", ".")
    return sen

def chinese_to_arab(number):
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(number) - 1, -1, -1):
        val = common_used_numerals.get(number[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return str(total)



def chinese2digits(uchars_chinese):
    if '点'in uchars_chinese:
        index = uchars_chinese.index('点')
        integer_number = chinese_to_arab(uchars_chinese[0:index])
        decimal_number = replace_chinese(uchars_chinese[index:])
        arab_decimal = str(integer_number) + str(decimal_number)
        return arab_decimal
    else:
        return chinese_to_arab(uchars_chinese)



num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九',
                        '十']
more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿', '点']


def changeChineseNumToArab(oriStr):
    lenStr = len(oriStr)
    aProStr = ''
    if lenStr == 0:
        return aProStr
    hasNumStart = False
    numberStr = ''
    for idx in range(lenStr):
        if oriStr[idx] in num_str_start_symbol:
            if not hasNumStart:
                hasNumStart = True

            numberStr += oriStr[idx]
        else:
            if hasNumStart:
                if oriStr[idx] in more_num_str_symbol:
                    numberStr += oriStr[idx]
                    continue
                else:
                    numResult = chinese2digits(numberStr)
                    numberStr = ''
                    hasNumStart = False
                    aProStr += numResult

            aProStr += oriStr[idx]
            pass

    if len(numberStr) > 0:
        resultNum = chinese2digits(numberStr)
        aProStr += str(resultNum)
    print(aProStr)

    return aProStr



def Chinese_to_arabic(sen):
    if '十' in sen or '百' in sen:
        print('话术中有十' + changeChineseNumToArab(sen))
        return changeChineseNumToArab(sen)
    else:
        print('替换之后的话术： ' + replace_chinese(sen))
        return replace_chinese(sen)




def to_json(sen):
    new_sen = Chinese_to_arabic(sen)
    words = []
    sens_seg = synonyms.seg(new_sen)
    for index in range(len(sens_seg[0])):
        word = Word(
            string=str(
                sens_seg[0][index]), tag=str(
                sens_seg[1][index]))
        words.append(word)
    text = sen
    nlp_score = 1.0
    radio_dict = {
        "nlp_score": nlp_score,
        "service": "radio",
        "rawText": text,
        "rc": 0,
        "semantic": {
            "slots": {
                "code": "",
                "waveband": "fm",
                "location": "",
            }
        },
        "operation": "LAUNCH"
    }
    for word in words:
        if word.tag == 'm':
            try:
                radio_dict["semantic"]["slots"]["code"] = '{:.0f}'.format(
                    eval(word.string) * 1000)
            except:
                pass
        elif word.string == 'am':
            radio_dict["semantic"]["slots"]["waveband"] = 'am'
    return radio_dict

