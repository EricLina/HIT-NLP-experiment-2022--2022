from BaseSeg import BaseSeg
from Score import score
from dict import Dict
from fileProcess import read_gold, read_sent, writefile
from builddict import buildNormalDict,buildAwesomeTrieDict



class BMMSeg(BaseSeg):
    '''
    反向最大匹配分词（从右到左）
    '''
    def __init__(self, dict:Dict):
        super().__init__(dict)
    
    def BMM_seg(self, sentence: str):
        word_startidx = 0
        word_endidx = len(sentence)
        while(word_endidx > 0):
            word = ''
            for word_startidx in range(max(0, word_endidx - self.dict.max_word_len), word_endidx, 1):
                word = sentence[word_startidx : word_endidx]
                if(self.dict.search(word)):
                    word_endidx = word_startidx + 1
                    break
            word_endidx = word_endidx - 1
            yield word
    
    
    def seg(self, sentence: str):
        res = []
        for x in self.BMM_seg(sentence):
            res.insert(0,x)
        return res

def test():
    #构造词典
    normaldict = buildNormalDict.get_dict()

    # 构造分词器
    BMMsegment = BMMSeg(normaldict)

    text = '北京举行新年音乐会'
    gold = ['北京','举行','新年','音乐会']

    print(BMMsegment.seg(text))
    # print("FMM", ''.join(FMMsegment.seg(text)))
    # print("BMM", ''.join(BMMsegment.seg(text)))


    # 测试多句
    data = [text,text]
    golds = [gold, gold]
    print(BMMsegment.seg_data(data))    

    # 测试单条评分
    myscore = score()
    print(gold)
    print(BMMsegment.seg(text))
    myscore.evaluate_line(gold,BMMsegment.seg(text))

    #测试多条评分
    print("\n测试多条评分")
    print(golds)
    print(BMMsegment.seg_data(data))
    myscore.evaluate_data(golds, BMMsegment.seg_data(data))

def test_write():
    data = ['中共中央总书记、国家主席江泽民','中共中央总书记、国家主席江泽民']
    order = ["001","002"]
    normaldict = buildNormalDict.get_dict()
    FMMsegment = BMMSeg(normaldict)
    segres = FMMsegment.seg_data(data)
    print(segres)
    respath = "/mnt/d/Linus/2022Autumn/NLP/dataset/segres.txt"
    writefile.write_sent(segres, respath, order)

def BMM_list_onFulldata():
    #构造词典
    normaldict = buildNormalDict.get_dict()
    # 构造分词器
    segmodel = BMMSeg(normaldict)

    #dummy
    # goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_seq&pos.txt"
    # sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_sent.txt"
    # BMMsegfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/seg_BMM.txt" 

    #BMM 测试整体直接评分
    goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt"
    sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_sent.txt"
    BMMsegfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_seg_BMM.txt" 
    segmodel.eval_on_fulldata(goldfile, sentfile, BMMsegfile)

def BMM_trie_onFulldata():
    #构造词典
    normaldict = buildAwesomeTrieDict.get_dict()
    # 构造分词器
    segmodel = BMMSeg(normaldict)

    #dummy
    # goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_seq&pos.txt"
    # sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_sent.txt"
    # BMMsegfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/seg_BMM.txt" 

    #BMM 测试整体直接评分
    goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt"
    sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_sent.txt"
    BMMseg_res_file = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_Trie_seg_BMM_result.txt" 
    BMMseg_score_file = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_Trie_seg_BMM_score.txt" 
    segmodel.eval_on_fulldata(goldfile, sentfile, BMMseg_res_file, BMMseg_score_file)


if __name__ == "__main__":
    BMM_trie_onFulldata()    
