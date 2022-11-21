from dict import AwesomeTrie, PPTTrie, NormalDict
from dict import Dict
from clock import clock
from fileProcess import DEFAULT_ENCODE
import os

dictType = {
    1 : AwesomeTrie,
    2 : NormalDict, 
    3 : NormalDict,
    4 : PPTTrie
}


class builddict():
    def __init__(self,Type:int = 1, file:str = None):
        '''
        dictType: 
            1: Trie
            2: NormalDict
        file: 分词结果文件路径
        '''
        self.dict = dictType[Type]()
        if(file != None):
            self.build_dict(file)

    def build_dict(self, segfile:str):
        '''
        从已经分词好的文件中获取词典，并保存词典文件
        @para: 
            segfile: 标准分词结果文件
        '''
        if not os.path.exists(segfile):
            print('%s not exists!', segfile)
            return
        
        with open(segfile, 'r', encoding=DEFAULT_ENCODE ) as f :
            for line in f:
                line = line.strip().split()
                # line = line[1:] #这里是为了去除头部的 19981001-08-03
                line = [x.split('/')[0] for x in line]
                for x in line:
                    self.dict.insert(x)
        f.close()
    
    def build_dict(self, seglist:list):
        if len(seglist) == 0:
            print('%s empty!', seglist)
            return
        for line in seglist:
            # line = line.strip().split()
            # # line = line[1:] #这里是为了去除头部的 19981001-08-03
            # line = [x.split('/')[0] for x in line]
            for x in line:
                self.dict.insert(x)



    def save_dict(self, dict_file:str):
        '''
        @para:
            dict_file: 得到的词典保存路径
        '''
        self.dict.write_dict(dict_file)
    

    def load_dict(self, dict_file:str):
        '''
        @para:
            dict_file: 词典保存路径
        '''
        self.dict.read_dict(dict_file)

    
    def get_dict(self):
        return self.dict

class buildNormalDict(builddict):
    def __init__(self, Type: int = 1, file: str = None):
        super().__init__(2, file)
    
    def get_dict():
        normaldict = builddict(2)
        normaldict.load_dict("dict/normal.dic")
        return normaldict.dict

class buildAwesomeTrieDict(builddict):
    def __init__(self, Type: int = 1, file: str = None):
        super().__init__(1, file)
    
    def get_dict():
        triedict = builddict(1)
        triedict.build_dict("dataset/199801_seg&pos.txt")
        return triedict.dict




class buildCustomTrieDict(builddict):
    def __init__(self, Type: int = 3, file: str = None):
        super().__init__(3, file)
    
    def get_dict():
        triedict = builddict(3)
        triedict.build_dict("dataset/199801_seg&pos.txt")
        return triedict.dict


class buildPPTTrieDict(builddict):
    def __init__(self, Type: int = 4, file: str = None):
        super().__init__(4, file)
    
    def get_dict():
        triedict = builddict(4)
        triedict.build_dict("dataset/199801_seg&pos.txt")
        return triedict.dict



def NormalDict_build_save():
    normaldict = builddict(2)
    normaldict.build_dict("dataset/199801_seg&pos.txt")
    normaldict.save_dict("dict/normal.dic")

def AwesomeTrieDict_build_save():
    awesomeTriedict = builddict(1)
    awesomeTriedict.build_dict("dataset/199801_seg&pos.txt")
    awesomeTriedict.save_dict('dict/awesomeTrie.dic')

@clock
def search(dict,content):
    dict.search(content)

@clock
def test_NormalDict_load():
    normaldict = buildNormalDict.get_dict()
    print(normaldict.__class__)
    search(normaldict,"如泣如诉")

    
@clock
def test_PPTTrie_build():
    PPTTrie = buildPPTTrieDict.get_dict()
    PPTTrie.showdict()
    search(PPTTrie,"如泣如诉")



@clock
def test_build_Trie():
    triedict = buildAwesomeTrieDict.get_dict()
    print(triedict.__class__)
    triedict.showdict()
    search(triedict,"如泣如诉")

def test_build_CustomerTrie():
    custrie = buildCustomTrieDict.get_dict()
    print(custrie.__class__)
    search(custrie,"如泣如诉")


if __name__ == "__main__":
    # thisdict = builddict(1)
    # thisdict.load_dict("dataset/dummy_seq&pos.txt")
    # dic = thisdict.get_dict()
    # dic.showdict()

    # thatdict = builddict(2)
    # # thatdict.load_dict("dataset/dummy_seq&pos.txt")
    # thatdict.build_dict("dataset/199801_seg&pos.txt")
    # dic = thatdict.get_dict()
    # dic.showdict()

    #测试List完整词典读写
    # NormalDict_build_save() # 耗时将近 15 min
    # test_NormalDict_load()  # 耗时很短，不到 1 s

    # #测试Trie完整词典读写
    # test_build_Trie() # 耗时 1.532167911529541 s
    #                   # 在使用自己的字典时，耗时21.98s
    AwesomeTrieDict_build_save()
    
    # 测试PPT Trie的完整词典建立与查找
    # 建立时间较长，需要38.3s
    # 查找时间很快，只需5.3 e-5 s
    # test_PPTTrie_build()
    
    
    
    