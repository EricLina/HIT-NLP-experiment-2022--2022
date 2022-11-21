from dict import Dict
from Score import score
from fileProcess import read_gold, read_sent, writefile,DEFAULT_ENCODE
from clock import clock
from tqdm import tqdm
import re

class BaseSeg():
    def __init__(self, dict:Dict):
        self.dict = dict
        self.spec_num = '薍'

    def seg(self, sentence: str):
        pass

    @clock
    def seg_data(self, sentences: list):
        res = []
        bar = tqdm(sentences)

        for s in tqdm(sentences):
            sub_string , filted_contents = self.pre_process(s)
            seg_result = self.seg(sub_string)
            s = self.back_process(seg_result, filted_contents)
            res.append(s)

        # for i, s in enumerate(sentences) :
        #     if(i % 100 == 0):
        #         print("正在处理第 %d 条数据/共 %d 条"%(i,totol))
        #     res.append(self.seg(s))
        return res

    def evaluate_data(self, predict_data: list, golds: list, isTesting:bool = False):
        '''
        对一批数据进行分词，并打印最终评测分数
        @para:
            sentences: 待分词数据，list格式，list[i]为一条字符串
            golds： 参考数据，list格式，list[i]为分好的结果，每一条结果都是类似['中共中央', '总书记', '、', '国家', '主席', '江', '泽民']的格式
            isTesting: 是否需要打印数据对
        @ return:
            None
        '''
        myscore = score()
        if (isTesting):
            for x,y in zip (golds, predict_data):
                print(x,y)
        return myscore.evaluate_data(golds, predict_data)


    def eval_on_fulldata(self, gold_file , sent_file, 
                            seg_res_path:str ,
                            seg_score_path:str ):
        ''''
        gold_file : str /list , str就从文件中读转为list，若直接为list就能直接用
        '''

        if(isinstance(gold_file,str)):
            gold_file = read_gold(gold_file)
            gold = gold_file.get_data()
        else:
            gold = gold_file

        if(isinstance(sent_file, str)):
            sent_file = read_sent(sent_file)
            sent = sent_file.get_data()
        else :
            sent = sent_file
        # sent_order = sent_file.get_order()


        print("\n正在分词中....")
        predicted_labels = self.seg_data(sent)
        print("分词结束")


        # writefile.write_sent(predicted_labels, savepath, sent_order)
        writefile.write_sent(predicted_labels, seg_res_path, order=None)

        precision, recall, f1 = self.evaluate_data(predicted_labels, gold)
        with open(seg_score_path,'w',encoding = DEFAULT_ENCODE) as f:
            f.write('Precision: %f \n'%(precision))
            f.write("Recall: %f \n"%(recall))
            f.write("F MEASURE: %f"%(f1))
        f.close()

    def pre_process(self,sent_sentence:str):
        """
        对输入的句子进行后处理，具体为过滤日期，人名等，将其替换为一个特定字符。
        return： 替换后的字符串 ， 过滤的内容列表
        """
        pattern = re.compile(r"\d{8}(?:-|\/|.)\d{2}(?:-|\/|.)\d{3}(?:-|\/|.)\d{3}")
        find_result = pattern.findall(sent_sentence)
        sub_sentence = re.sub(pattern, repl=self.spec_num ,string = sent_sentence, count = 0)
        return sub_sentence, find_result

    def back_process(self, sub_sentence_list:list, find_result:list):
        result = []
        n = len(find_result)
        if(n == 0): return sub_sentence_list

        i = 0
        for item in sub_sentence_list:
            if  item == self.spec_num:
                item = find_result[i]
                i += 1
            result.append(item)
        return result

def test_back_process():
    s = BaseSeg(None)
    sentence = "震撼世界的报告（附图片１张）"
    substring, filed_list = s.pre_process(sentence)
    print(substring, filed_list)

    segreult = ["薍","震撼","世界","的","报告","(","附图片1张",")"]
    res = s.back_process(segreult, filed_list) 
    print(res)

if __name__ == "__main__":
    test_back_process()

        