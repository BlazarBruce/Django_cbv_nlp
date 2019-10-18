# -*- coding: utf-8 -*-
def chinese_to_number(s):
    nums = {
        '一': 1,
        '二': 2,
        '两': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9}
    # 可能量词无法分词处理,比如空调风谅七档
    s = [ch for ch in s if ch in '零一二两三四五六七八九十百千万']
    # print(s)
    if len(s) == 0:
        return 0
    total = 0
    if len(s) >= 0:
        if s[len(s) - 1] in nums:
            total += nums[s[len(s) - 1]]

    for i in range(0, len(s)):
        if s[i] == '万':
            if i - 1 >= 0 and s[i - 1] in nums:
                total += 10000 * nums[s[i - 1]]
        if s[i] == '千':
            if i - 1 >= 0 and s[i - 1] in nums:
                total += 1000 * nums[s[i - 1]]
        if s[i] == '百':
            if i - 1 >= 0 and s[i - 1] in nums:
                total += 100 * nums[s[i - 1]]
        if s[i] == '十':
            if i - 1 >= 0 and s[i - 1] in nums:
                total += 10 * nums[s[i - 1]]
            elif i - 1 < 0:
                total += 10
    return total
