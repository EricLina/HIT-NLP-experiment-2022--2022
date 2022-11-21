import json
from fileProcess import DEFAULT_ENCODE

class Dict():
    def __init__(self) -> None:
        self.max_word_len = 0
        self.totol_wordnum = 0
        

    def search(self, word: str):
        pass 

    def insert(self, word: str):
        pass 

    def showdict(self):
        pass

    def write_dict(self, dictfile:str):
        print("词典已经写入 %s 中"%dictfile)
        pass

    def read_dict(self, dictfile:str):
        print("词典从 %s 加载成功"%dictfile)
        self.showdict()
        

'''
构造基于List的词典
'''
class NormalDict(Dict):

    def __init__(self) -> None:
        super().__init__()
        self.dict = []
        self.max_word_len = 0
        print("正在创建基于List的字典....")

    def search(self, word: str):
        for inner_word in self.dict:
            if(word == inner_word):
                return True
        return False
    def insert(self, word :str):
        print("插入 ",word)
        if(self.search(word)):
            # print(word," 已存在")
            return 
        self.dict.append(word)
        self.max_word_len = max(len(word), self.max_word_len)
        self.totol_wordnum += 1
    
    def showdict(self):
        print("*"*10)
        print("词典信息如下：")
        print("本词典基于List实现")
        print("共收录 %d 个词"%self.totol_wordnum)
        print("最大词长  :%d"%self.max_word_len)
        print("前10条词如下： ",self.dict[:10])
        print("*"*10,'\n')

    def write_dict(self, dictfile:str = 'dict_normal.txt'):
        with open(dictfile, 'w', encoding= DEFAULT_ENCODE) as f:
            for x in self.dict:
                f.write(str(x))
                f.write('\n')
        f.close()
        return super().write_dict(dictfile)
        

    def read_dict(self, dictfile:str = 'dict_normal.txt'):
        self.dict = []
        self.max_word_len = 0
        self.totol_wordnum = 0
        with open(dictfile, 'r', encoding=DEFAULT_ENCODE) as f:
            for line in f :
                self.dict.append(line.rstrip('\n'))
                self.max_word_len = max(self.max_word_len, len(line))
                self.totol_wordnum += 1
        f.close()
        return super().read_dict(dictfile)
        
        

'''
前缀树Node
'''
class TrieNode():
    def __init__(self, char, terminal, children) -> None:
        self.char = char
        self.terminal = terminal
        self.children = children

    def is_terminal(self):
        return self.terminal
    
    def set_terminal(self, terminal):
        self.terminal = terminal

    def get_char(self):
        return self.char
    
    def set_char(self, char):
        self.char = char 
    
    def get_children(self):
        return self.children
    
    def get_child(self, char):
        for child in self.children:
            if (char == child.get_char()):
                return child
        return None
    
    def get_child_if_not_exist_then_create(self, char):
        child = self.get_child(char)
        new = 0
        if not child:
            new = 1
            child = TrieNode(char,False,[])
            self.add_child(child)
        return child, new
    
    def add_child(self,child):
        self.children.append(child)
    


'''
前缀树(魔改PPT上的代码，将{}换[]并在每一次查找child时直接for循环查找)
'''
class PPTTrie(Dict):

    def __init__(self) -> None:
        super().__init__()
        self.ROOT_NODE = TrieNode('', False, [])
        self.totol_node_num = 0

    def search(self, word):
        if(len(word) < 1):
            return False
        node = self.ROOT_NODE
        for i in word:
            child = node.get_child(i)
            if not child :
                return False
            else:
                node = child
        return node.is_terminal()
    
    def insert(self, word: str):
        if (len(word) < 1):
            return
        self.max_word_len = max(self.max_word_len, len(word))
        node = self.ROOT_NODE

        for i in word:
            child,new = node.get_child_if_not_exist_then_create(i)
            self.totol_node_num += new
            node = child
        
        node.set_terminal(True)
    
    def showdict(self):
        print("基于PPT上的前缀树的词典：")
        print("共有 %d 个Node",self.totol_node_num)
        print("最大词的长度 :%d",self.max_word_len)
    


'''
构造前缀字典树得到词典
'''
class AwesomeTrie(Dict):
    '''
    基于Python内置词典的前缀树，建树与查找速度飞快
    '''
    def __init__(self):
        super().__init__()
        self.root = {}
        self.max_word_len = 0
        self.end_token = '[END]'
        self.freq_token = '[FREQ]'
        self.totol_word_freq = 0
        print("正在创建基于Trie的词典...")
        

    def insert(self, word: str, freq: int = 1, tag: str = None ):
        self.max_word_len = max(len(word), self.max_word_len)
        node = self.root
        is_in = True
        for char in word:
            if(node.get(char) == None):
                node[char] = {}
                is_in = False
            node = node.get(char)
            # node = node.setdefault(char, {}) #向下寻找下一个字符对应的节点，若没有，则新建一个
        
        node[self.end_token] = self.end_token
        if self.freq_token in node.keys():
            node[self.freq_token] += freq
        else:
            node[self.freq_token] = freq
        self.totol_word_freq += freq
        if not is_in :
            self.totol_wordnum += 1

    def search(self, word: str):
        '''
        寻找word是否在TrieDict中(此word必须对应叶节点)
        若存在则返回对应的Node，否则返回None
        '''
        node = self.root
        for char in word:
            if(char not in node.keys()):
                return None
            node = node[char]
        
        if self.end_token in node.keys():
            return node
        else :
            return None

    def get_freq(self, word:str):
        node = self.search(word)
        if node != None:
            return node.get(self.freq_token, 1) #当dict不存在key = self.freq_token, 缺省值返回1
        else :
            return 0
    
    def yieldDict(self, mydict:dict, path:str):
        for key,value in mydict.items():
            path += key
            if(isinstance(value,dict)):
                yield from self.yieldDict(value,path)
            if(key == '[END]'):
                rt = (path[:-len(key)],mydict['[FREQ]'])
                yield rt
            path = path[:-len(key)]
        

    def dfs_on_dict(self):
        '''
        深度优先打印所有END节点与其FREQ
        AAB 2
        AAC 1
        A 1
        '''
        for item in self.yieldDict(self.root,""):
            print(item)

    def showdict(self):
        print("*"*10)
        print("词典信息如下：")
        print("\t本词典基于前缀树实现")
        print("\t共收录 %d 个词"%self.totol_wordnum)
        print("\t最大词长 %d :"%self.max_word_len)
        print("词典如下: (词、词频)")
        self.dfs_on_dict()
        print("*"*10,'\n')

    def write_dict(self, dictfile:str = "dict_trie.txt"):
        '''
        由于前缀树的构造时间很短（不到2s），所以保存词典的操作没什么必要，直接构建即可
        '''
        with open (dictfile , 'w') as f:
            for line in self.yieldDict(self.root,""):
                f.write(str(line[0])+' '+str(line[1]))
                f.write('\n')
        f.close()
        return super().write_dict(dictfile)

    def read_dict(self, dictfile:str = "dict_trie.txt"):
        with open(dictfile, 'r') as f :
            self.root = json.load(f)
        return super().read_dict()


def yieldDict(dict:dict, path:str):
    for key,value in dict:
        path += key
        if(isinstance(value,dict)):
            yieldDict(value,path)
        if(key == '[END]'):
            yield [path,dict['FREQ']]
        path = path[:-len(key)]



if __name__ == "__main__":

    # List
    # dict = NormalDict()
    # words = ["我","爱","中国","中国人民"]
    # for word in words:
    #     dict.insert(word)
    # print(dict.search("我"))
    # print(dict.search("中国人民"))
    # print(dict.search("中国"))
    # print(dict.search("美国"))
    # dict.showdict()

    # Trie
    t = AwesomeTrie()
    t.insert('AAB')
    t.insert('AAC')
    t.insert('AAB')
    print(t.root)
    a = t.search('AAB')
    t.insert('A')

    print("--"*10)
    print(t.get_freq('AAC'))
    print(a)

    t.showdict()

