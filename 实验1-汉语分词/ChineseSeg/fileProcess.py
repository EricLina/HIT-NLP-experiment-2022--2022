'''
用于读写文件、预处理文本格式
'''
from cgitb import reset
import os
from unittest import result
import numpy as np

encode = {
    "Windows":'utf-8',
    "Linux":'gbk',
    "Raw":'gb2312',
    "Convert":"utf-8",
}
DEFAULT_ENCODE=encode["Linux"]
RAW_ENCODE=encode["Raw"]

class readfile():
    def __init__(self, file:str = "") -> None:
        self.data = []
        self.load_file(file)
        print("加载成功")
        print("前5条数据：",self.data[:5])
    
    def get_data(self):
        return self.data

    def load_file(self, file:str):
        if not os.path.exists(file):
            return []
        result = []
        with open(file, 'r', encoding=DEFAULT_ENCODE) as f :
            for line in f :
                if(line == []): 
                    continue
                line = line.strip()
                line = self.processLine(line)
                result.append(line)
        self.data = result
    
    def processLine(self, line):
        return line

class read_gold(readfile):
    def __init__(self, file: str = "", is_remove_wrong_char = True) -> None:
        print("加载参考数据中....")
        self.is_remove_wrong_char = is_remove_wrong_char
        super().__init__(file)

    def processLine(self, line):
        if (self.is_remove_wrong_char):
            line = line.replace('[','') # 处理左括号多余问题
        line = line.strip().split()
        # line = line[1:] # 忽略第一个 ：199801-01-001-001 
        line = [x.split('/')[0] for x in line]
        return line
    
def convert_to_raw(src_gold_file ,target_file):
    data =  read_gold(src_gold_file, is_remove_wrong_char = True).get_data()
    print(data[0])
    with open(target_file, 'w', encoding = DEFAULT_ENCODE) as f:
        for i, line in enumerate(data):
            f.write("".join(line))
            f.write('\n')

    pass
    

class read_sent(readfile):
    def __init__(self, file: str = "") -> None:
        print("加载待分词数据中....")
        self.order=[]
        self.count = 0
        super().__init__(file)
    
    def processLine(self, line):
        # 19980101-01-001-001迈向充满希望的新世纪——一九九八年新年讲话（附图片１张）
        # 19980101-01-001-001 共19个字符，去除
        self.order.append(line[:19])
        self.count += 1
        # line = line[19:] #ps：不合理的地方，直接用[:19]（耍小聪明啊）
        return line

    def get_order(self):
        assert self.count == len(self.order)
        return self.order


class writefile():
    def __init__(self) -> None:
        pass

    def write_sent(seg_res: list, respath:str, order: list = None):
        '''
        将分词结果写回文件保存
        @para: 
            seg_res: 分词结果，list格式，
                eg.[['中共中央', '总书记', '、', '国家', '主席', '江', '泽民'], ['中共中央', '总书记', '、', '国家', '主席', '江', '泽民']]
            respath: 结果文件路径
            order: 每一条记录的编号，list 格式
        '''
        if(order != None):
            assert len(seg_res) == len(order)
            with open(respath, 'w', encoding = DEFAULT_ENCODE) as f:
                for i, line in enumerate(seg_res):
                    if len(line) > 0:
                        f.write(order[i]+'/ ')
                        f.write("/ ".join(line))
                    f.write('\n')
            f.close()

        else :
            with open(respath, 'w', encoding = DEFAULT_ENCODE) as f:
                for i, line in enumerate(seg_res):
                    f.write("/ ".join(line))
                    f.write('\n')
            f.close()


class dataset():
    def __init__(self,sent_file, gold_file = None, split = True, test_radio = 0.3):
        if(isinstance(sent_file, str)):
            self.sent_data = self.__load_sent_data(sent_file)
            self.len = len(self.sent_data)
        elif(isinstance(sent_file, list)):
            self.sent_data = self.__load_sent_datasets(sent_file)
            self.len = len(self.sent_data)
            if (gold_file != None):
                self.gold_data = self.__load_gold_dataset(gold_file)
                assert (len(self.sent_data) == len(self.gold_data))
                self.split = split
                if(self.split):
                    self.test_radio =  test_radio
                    self._split()
        else:
            raise(FileNotFoundError)
        
        
        print("初始化成功，共%d条数据", self.len)




    def __getitem__(self, index):
        if(index < self.len):
            return self.sent_data[index]
        else :
            raise Exception('Index should be less than %d',index)

    def __len__ (self):
        return self.len

    def __load_sent_data(self, file):
        if not os.path.exists(file):
            return []
        result = []
        with open(file, 'r', encoding = DEFAULT_ENCODE) as f:
            for line in f:
                if(len(line) == 0) :
                    continue 
                line = line.strip()
                result.append(line)
        return result
    
    def __load_gold_data(self, file):
        return read_gold(file).get_data()
    
    def __load_gold_dataset(self, files:list):
        All_data = []
        for file in files:
            result = self.__load_gold_data(file)
            All_data.extend(result)

        print("ALl sentence number: ",len(All_data))
        return All_data
        pass
    
    def __load_sent_datasets(self, files:list):
        All_data = []
        for file in files:
            result = self.__load_sent_data(file)
            All_data.extend(result)

        print("ALl sentence number: ",len(All_data))
        return All_data
    
    def _split(self):
        shuffle_indexes = np.random.permutation(self.len)
        # #比例分割
        # test_ratio = 0.3
        print("划分比例：",self.test_radio)
        #测试集的大小
        test_size = int(self.test_radio * self.len)
        #测试集的索引
        test_indexes = shuffle_indexes[:test_size]
        #训练集的索引
        train_indexes = shuffle_indexes[test_size:]
        
        X = np.array(self.sent_data)
        Y = np.array(self.gold_data, dtype=list)
        self.x_test = X[test_indexes].tolist()
        self.x_train = X[train_indexes].tolist()
        self.y_test = Y[test_indexes].tolist()
        self.y_train = Y[train_indexes].tolist()


        print("测试集大小:",test_size)
        print("训练集大小:",self.len - test_size)


        pass
        
def get_3_dataset(radio = 0.3):
    gold_file_1 = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt"
    sent_file_1 = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_sent.txt"
    gold_file_2 ="/mnt/d/Linus/2022Autumn/NLP/dataset/2022训练数据第二批199802原版/199802.txt"
    sent_file_2 = "/mnt/d/Linus/2022Autumn/NLP/dataset/2022训练数据第二批199802原版/199802_sent.txt"
    gold_file_3 = "/mnt/d/Linus/2022Autumn/NLP/dataset/2022训练数据第二批199803原版/199803.txt"
    sent_file_3 = "/mnt/d/Linus/2022Autumn/NLP/dataset/2022训练数据第二批199803原版/199803_sent.txt"
    golds = [gold_file_1, gold_file_2, gold_file_3]
    sents = [sent_file_1, sent_file_2, sent_file_3]
    Thedataset = dataset(sent_file= sents, gold_file= golds, split= True, test_radio= radio)

    return Thedataset

if __name__ == "__main__":

    # gold_file = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_seq&pos.txt"
    # gold_file = read_gold(gold_file)


    # sent_file = "/mnt/d/Linus/2022Autumn/NLP/dataset/dummy_sent.txt"
    # sent_file = read_sent(sent_file)

    gold_file_1 = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt"
    sent_file_1 = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_sent.txt"
    gold_file_2 ="/mnt/d/Linus/2022Autumn/NLP/dataset/2022训练数据第二批199802原版/199802.txt"
    sent_file_2 = "/mnt/d/Linus/2022Autumn/NLP/dataset/2022训练数据第二批199802原版/199802_sent.txt"
    gold_file_3 = "/mnt/d/Linus/2022Autumn/NLP/dataset/2022训练数据第二批199803原版/199803.txt"
    sent_file_3 = "/mnt/d/Linus/2022Autumn/NLP/dataset/2022训练数据第二批199803原版/199803_sent.txt"
    # convert_to_raw(gold_file_3, target_file_3)








