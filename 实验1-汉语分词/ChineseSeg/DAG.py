from BaseSeg import BaseSeg
from fileProcess import get_3_dataset
from builddict import builddict
import math
import os 


class DAGSeg(BaseSeg):
    def __init__(self,dictfile:str) -> None:
        self.lfreq, self.ltotal =  self.__gen_pfdict(filename = dictfile)
        super().__init__(None)

    def __gen_pfdict(self, filename:str):
        '''
        从词典中构建一个前缀词典（若前缀不在词典中，将其词频设置为0，便于DAG的构建
        '''
        lfreq = {}
        ltotal = 0
        with open(filename) as f:
            for line in f:
                word, freq = line.split()
                freq = int(freq)
                lfreq[word] = freq
                ltotal += freq
                for ch in range(len(word)):
                    wfrag = word[: ch +1 ]
                    if wfrag not in lfreq:
                        lfreq[wfrag] = 0                        
        return lfreq, ltotal

    def get_DAG(self, sentence:str):
        '''
        得到DAG表，其中DAG[i]代表以sentence[i]开头的单词区间末尾所构成的列表
        如 "去北京大学玩" --> DAG[1] = [1,2,4], 代表[北京,北京大学]
            {0: [0], 1: [1, 2, 4], 2: [2], 3: [3, 4], 4: [4], 5: [5]}
        '''
        DAG = {}
        N = len(sentence)
        for k in range(N):
            tmlist = []
            i = k 
            frag = sentence[k]
            while i < N and frag in self.lfreq:
                if self.lfreq[frag] > 0:
                    tmlist.append(i)
                i+=1
                frag = sentence[k:i+1]
            if not tmlist:
                tmlist.append(k)
            DAG[k] = tmlist
        # print(DAG)
        return DAG
    
    def calc(self, sentence:str):
        '''
        从后往前利用DAG+动态规划，计算切分的概率
        '''
        DAG = self.get_DAG(sentence)
        route = {}

        N = len(sentence)
        route[N] = (0,0)
        logtotal = math.log(self.ltotal) #取对数 防止下溢问题
        for idx in range(N-1, -1, -1): #倒序遍历每个字（sentence[idx]）
            route[idx] = (float('-INF'),0)
            
            for x in DAG[idx]: #计算子句sentence[idx: N-1]的概率得分，并保存最大值与其对应的末尾位置
                char_freq = self.lfreq.get(sentence[idx : x+1]) or 1
                logfreq = math.log(char_freq) - logtotal # log(char_freq/total) = log(char_freq) - log(freq_total)
                # print(logfreq)
                accumulate_freq = logfreq  + route[x+1][0]

                if(accumulate_freq > route[idx][0]):
                    route[idx] = (accumulate_freq, x)

        # print(route)
        return route
    
    def DAG_seg(self, sentence:str):
        route = self.calc(sentence=sentence)
        N = len(sentence)
        wordbegin = 0
        while wordbegin < N:
            wordend = route[wordbegin][1]
            yield sentence[wordbegin : wordend+1]
            wordbegin = wordend+1
    
    def seg(self, sentence:str):
        res = []
        for x in self.DAG_seg(sentence):
            res.append(x)
        # print(res)
        return res

def DAG_on_full_dataset():
    dictfile = '/mnt/d/Linus/2022Autumn/NLP/dict/awesomeTrie.dic'
    segmodel = DAGSeg(dictfile)
    goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt"
    sentfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_sent.txt"
    DAG_segfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_seg_DAG_result.txt" 
    DAG_seg_score_file =  "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_seg_DAG_score.txt" 
    segmodel.eval_on_fulldata(goldfile, sentfile, DAG_segfile, DAG_seg_score_file)

def DAG_on_3_dataset(split_test_radio = 0.3, recreate = False):

    Dataset = get_3_dataset(radio= split_test_radio)
    dict_savepath = '/mnt/d/Linus/2022Autumn/NLP/dict/Full3_awesomeTrie_'+str(split_test_radio*10)+ '.dic'
    if(not os.path.exists(dict_savepath) or recreate):
        Full3_awesomeTriedict = builddict(1)
        Full3_awesomeTriedict.build_dict(Dataset.y_train)
        Full3_awesomeTriedict.save_dict(dict_savepath)
    # dict_savepath = '/mnt/d/Linus/2022Autumn/NLP/dict/Full3_awesomeTrie.dic'
    
    segmodel = DAGSeg(dict_savepath)   
    # 封闭测试
    result_path_train = "/mnt/d/Linus/2022Autumn/NLP/dataset/full3_DAG_train_reult_"+str(split_test_radio*10)+ ".txt"
    score_path_train = "/mnt/d/Linus/2022Autumn/NLP/dataset/full3_DAG_train_score_"+str(split_test_radio*10)+ ".txt"
    segmodel.eval_on_fulldata(Dataset.y_train, Dataset.x_train,result_path_train, score_path_train)
    # 测试集测试
    result_path_test = "/mnt/d/Linus/2022Autumn/NLP/dataset/full3_DAG_test_reult_"+str(split_test_radio*10)+ ".txt"
    score_path_test = "/mnt/d/Linus/2022Autumn/NLP/dataset/full3_DAG_test_score_"+str(split_test_radio*10)+ ".txt"
    segmodel.eval_on_fulldata(Dataset.y_test, Dataset.x_test,result_path_test, score_path_test)



def test_DAG():
    dictfile = '/mnt/d/Linus/2022Autumn/NLP/dict/awesomeTrie.dic'
    dag = DAGSeg(dictfile)
    # print(dag.lfreq)
    print(dag.lfreq["同胞"])
    # print(dag.lfreq["胞"])
    # print(dag.lfreq["披盖"])

    sentence = "同胞们、朋友们、女士们、先生们："
    dag.get_DAG(sentence)

    dag.calc(sentence)
    # testMax()

    print(dag.seg(sentence))
    


if __name__ == "__main__":

    for x in [0.3,0.2,0.1]:
        DAG_on_3_dataset(x, recreate= True)

