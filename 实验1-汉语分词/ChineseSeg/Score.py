import re
from fileProcess import read_gold



class score():
    def __init__(self) -> None:
        pass
    
    def get_position(self, seglist: list):
        '''
        @parameter: 
         seglist: 分词结果 
        @return : 
         返回分词结果每一个单词的首尾位置
        '''
        seg_arr =[]
        pos = 0
        for word in seglist:
            curlen = len(word)
            seg_arr.append(tuple([pos, pos + curlen]))  
            pos += curlen
        return seg_arr
            

    def evaluate_line(self, gold:list, predict_label:list):
        '''
        对一条数据进行评分，返回precision, recall, f1
        @para：
            gold: 一条参考结果
            predict_label: 一条分词结果
        @return：
            precision, recall, f1
        '''
        pred_num = len(predict_label)
        gold_num = len(gold)

        gold_arr = self.get_position(gold)
        pred_arr = self.get_position(predict_label)

        pred_cap_gold_num = 0
        for tp in pred_arr:
            if (tp in gold_arr):
                pred_cap_gold_num += 1
        

        precision = pred_cap_gold_num / pred_num
        recall = pred_cap_gold_num / gold_num
        f1 = 2. * precision * recall / (precision + recall)
        print('Recall: %f'%(recall))
        print('Precision: %f'%(precision))
        print('F MEASURE: %f'%(f1))
        return precision, recall, f1

    def evaluate_data(self, golddata:list, predictdata:list):
        '''
        对一批数据进行评分，返回precision, recall, f1
        @para：
            golddata： 参考结果（需要转化为list，每一个元素为一条list数据）
            predictdata: 模型分词结果（格式需要与上一致）
        @return：
            precision, recall, f1
        '''
        
        dismatch_num = 0

        all_pred_num = 0
        all_gold_num = 0
        pred_cap_gold_num = 0
        # 参考与预测结果必须一对一
        assert len(golddata) == len(predictdata)
        print("测试集数据共%d条"%len(golddata))
        #并行遍历
        for gold,predict_label in zip(golddata, predictdata):
            pred_num = len(predict_label)
            all_pred_num += pred_num
            gold_num = len(gold)
            all_gold_num += gold_num

            # 统计不相等
            predictstr = ''.join(x for x in predict_label)
            goldstr = ''.join(x for x in gold)
            goldstr = goldstr.replace('[','')
            if(len(predictstr) != len(goldstr)):
                print(dismatch_num)
                print(predictstr)
                print(goldstr)
                print('.'*15)
                dismatch_num += 1

            gold_arr = self.get_position(gold)
            pred_arr = self.get_position(predict_label)

            cap_num = 0
            for tp in pred_arr:
                if (tp in gold_arr):
                    cap_num += 1
                    pred_cap_gold_num += 1

        #计算结果
        precision = pred_cap_gold_num / all_pred_num
        recall = pred_cap_gold_num / all_gold_num
        f1 = 2. * precision * recall / (precision + recall)

        print('Recall: %f'%(recall))
        print('Precision: %f'%(precision))
        print('F MEASURE: %f'%(f1))

        print("不相等的句子条数:",dismatch_num)

        return precision, recall, f1       


    def bad_evaluate(self, gold, predict_label):
        # 使用Set进行去重，然后看共现
        # 参考： https://blog.csdn.net/u012297539/article/details/111864251 （明显是错误的）
        A = set(gold)
        B = set(predict_label)
        A_cap_B = A & B

        A_size = len(A)
        B_size = len(B)
        A_cap_B_size = len(A_cap_B)

        precision = A_cap_B_size / A_size  # 预测为正 且 正确 / 预测所有为正的结果
        recall = A_cap_B_size / B_size      # 
        f1 = 2 * precision * recall / (precision + recall)
        return precision, recall, f1

    def evalutate_file(self, gold_file:str, predictfile:str):
        goldsdata = read_gold(gold_file).get_data()
        predictdata = read_gold(predictfile).get_data()
        FMM_score = score().evaluate_data(goldsdata, predictdata)



def Debug_fmm():
    segfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/Final_Trie_seg_FMM.txt"
    goldfile = "/mnt/d/Linus/2022Autumn/NLP/dataset/199801_seg&pos.txt"
    score0 = score()
    score0.evalutate_file(goldfile,segfile)

if __name__ == "__main__":
    # goldseg = "19980101-01-001-002/m  中共中央/nt  总书记/n  、/w  国家/n  主席/n  江/nr  泽民/nr  "
    # goldseg = read_gold().processLine(goldseg)
    # print(goldseg)
    # modelseg = ['中共中央', '总书记', '、', '国家', '主席', '江', '泽民',]
    # print(modelseg)
    
    # Res = score()
    # # print(Res.get_position(modelseg))
    # precision, recall, f1 = Res.evaluate_line(goldseg, modelseg)
    # precision, recall, f1 = Res.evaluate_data([goldseg], [modelseg])
    Debug_fmm()

