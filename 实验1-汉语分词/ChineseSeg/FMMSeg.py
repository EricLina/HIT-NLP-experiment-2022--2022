'''
Forward Maximum Match

'''
from BaseSeg import BaseSeg
from Score import score
from dict import Dict, AwesomeTrie
from fileProcess import read_gold, read_sent, writefile
from builddict import buildNormalDict,buildAwesomeTrieDict,buildPPTTrieDict
from fileProcess import get_3_dataset
from builddict import builddict

count = 0
allchars =  0
sentencecount = 0
class FMMSeg(BaseSeg):
    '''
    正向最大匹配分词（从左到右）
    '''
    def __init__(self, dict:Dict ):
        super().__init__(dict)

    
    def FMM_seg(self, sentence: str):
        word_startidx = 0
        end_index = len(sentence)
        global allchars, sentencecount, count
        allchars += end_index
        sentencecount += 1
        while(word_startidx < end_index):
            word = ''
            for word_endidx in range(word_startidx + self.dict.max_word_len, word_startidx, -1):
                # print(self.dict.max_word_len)
                word = sentence[word_startidx : word_endidx]

                count += 1
                if(self.dict.search(word)):
                    #  a matched word found in dict
                    word_startidx = word_endidx - 1
                    break
            word_startidx = word_startidx + 1
            yield word

    
    def seg(self, sentence: str):
        res = []
        for x in self.FMM_seg(sentence):
            res.append(x)
        return res


def test():
    #构造词典
    normaldict = buildAwesomeTrieDict.get_dict()

    # 构造分词器
    FMMsegment = FMMSeg(normaldict)

    text = '中共中央总书记、国家主席江泽民'
    gold = ['中共中央总', '书记', '、', '国家', '主席', '江', '泽民']

    print(FMMsegment.seg(text))


    # 测试多句
    data = ['中共中央总书记、国家主席江泽民','中共中央总书记、国家主席江泽民']
    golds = [['中共中央', '总书记', '、', '国家', '主席', '江', '泽民'],['中共中央', '总书记', '、', '国家', '主席', '江', '泽民',]]
    print(FMMsegment.seg_data(data)) 

    # 测试单条评分
    myscore = score()
    print(gold)
    print(FMMsegment.seg(text))
    myscore.evaluate_line(gold,FMMsegment.seg(text))

    #测试多条评分
    print("\n测试多条评分")
    print(golds)
    print(FMMsegment.seg_data(data))
    myscore.evaluate_data(golds, FMMsegment.seg_data(data))

def test_write():
    data = ['中共中央总书记、国家主席江泽民','中共中央总书记、国家主席江泽民']
    order = ["001","002"]
    normaldict = buildNormalDict.get_dict()
    FMMsegment = FMMSeg(normaldict)
    segres = FMMsegment.seg_data(data)
    print(segres)
    respath = "/mnt/d/Linus/2022Autumn/NLP/dataset/segres.txt"
    writefile.write_sent(segres, respath, order)

def FMM_list_onFulldata():
    #构造词典
    normaldict = buildNormalDict.get_dict()

    # 构造分词器
    segmodel = FMMSeg(normaldict)


    #dummy
    # goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_seq&pos.txt"
    # sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_sent.txt"
    # FMMsegfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/seg_FMM.txt" 

    #FMM 测试整体直接评分
    goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt"
    sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_sent.txt"
    FMMseg_res_file = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_List_seg_FMM_result.txt" 
    FMMseg_score_file = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_List_seg_FMM_score.txt" 
    segmodel.eval_on_fulldata(goldfile, sentfile, FMMseg_res_file, FMMseg_score_file)


def FMM_trie_onFulldata():
    #构造词典
    normaldict = buildAwesomeTrieDict.get_dict()

    # 构造分词器
    segmodel = FMMSeg(normaldict)


    #dummy
    # goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_seq&pos.txt"
    # sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_sent.txt"
    # FMMsegfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/seg_FMM.txt" 

    #FMM 测试整体直接评分
    goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt"
    sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_sent.txt"
    FMMseg_res_file = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_Trie_seg_FMM_result.txt" 
    FMMseg_score_file = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_Trie_seg_FMM_score.txt" 
    segmodel.eval_on_fulldata(goldfile, sentfile, FMMseg_res_file, FMMseg_score_file)


def FMM_PPTtrie_onFulldata():
    #构造词典
    PPTtrieldict = buildPPTTrieDict.get_dict()

    # 构造分词器
    segmodel = FMMSeg(PPTtrieldict)


    #dummy
    # goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_seq&pos.txt"
    # sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_sent.txt"
    # FMMsegfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/seg_FMM.txt" 

    # #FMM 测试整体直接评分
    goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt"
    sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_sent.txt"
    FMMsegfile_result = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_PPTTrie_seg_FMM_result.txt" 
    FMMsegfile_score = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_PPTTrie_seg_FMM_score.txt" 
    segmodel.eval_on_fulldata(goldfile, sentfile, FMMsegfile_result,FMMsegfile_score)


def FMM_on_3_dataset(split_test_radio = 0.3):

    Dataset = get_3_dataset(radio= split_test_radio)
    
    #构造词典
    Full3_awesomeTriedict = AwesomeTrie()
    for x in Dataset.y_train:
        Full3_awesomeTriedict.insert(x)


    # 构造分词器
    segmodel = FMMSeg(Full3_awesomeTriedict)
 
    # 封闭测试
    result_path_train = "/mnt/d/Linus/2022Autumn/NLP/dataset/full3_FMM_train_reult_"+str(split_test_radio*10)+ ".txt"
    score_path_train = "/mnt/d/Linus/2022Autumn/NLP/dataset/full3_FMM_train_score_"+str(split_test_radio*10)+ ".txt"
    segmodel.eval_on_fulldata(Dataset.y_train, Dataset.x_train,result_path_train, score_path_train)
    # 测试集测试
    result_path_test = "/mnt/d/Linus/2022Autumn/NLP/dataset/full3_FMM_test_reult_"+str(split_test_radio*10)+ ".txt"
    score_path_test = "/mnt/d/Linus/2022Autumn/NLP/dataset/full3_FMM_test_score_"+str(split_test_radio*10)+ ".txt"
    segmodel.eval_on_fulldata(Dataset.y_test, Dataset.x_test,result_path_test, score_path_test)



if __name__ == "__main__":
    # FMM_trie_onFulldata()
    # print("dict 查询次数 ", count)
    # print("总字符数：", allchars)
    # print("总句子数：",sentencecount)
    # print("句子平均长度", allchars/ sentencecount)
    # print("一句平均查询字典次数：", count / sentencecount)

    # goldfile = '/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt'
    # predictfile = '/mnt/d/Linus/2022Autumn/NLP/dataset/Final_seg_FMM.txt'
    # score().evalutate_file(goldfile, predictfile)

    # test()
    # FMM_PPTtrie_onFulldata()  
    # 
    # FMM_list_onFulldata()  

    for x in [0.3, 0.2, 0.1]:
        FMM_on_3_dataset(x)
