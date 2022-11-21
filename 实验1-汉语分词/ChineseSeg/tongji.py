"""
统计平均单词长度
"""

with open("/mnt/d/Linus/2022Autumn/NLP/dict/normal.dic", encoding='gbk') as f:
    count = 0
    chars = 0
    maxchars = 0
    for line in f:
        chars += len(line)
        maxchars = max(maxchars, len(line))
        count += 1
    print("平均句子长度",chars/count)
    print("最大单词长度",maxchars)