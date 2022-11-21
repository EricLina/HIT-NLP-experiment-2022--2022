'''
拟对FMM优化（词典）
'''
import time
from clock import clock
from FMMSeg import FMM_PPTtrie_onFulldata,FMM_list_onFulldata

def PPTTrie_TimeCost():
    start_time = time.time()
    FMM_PPTtrie_onFulldata()
    timecost = time.time() - start_time
    return timecost

def List_TimeCost():
    start_time = time.time()
    FMM_list_onFulldata()
    timecost = time.time() - start_time
    return timecost

if __name__ == "__main__":
    print(PPTTrie_TimeCost())
    # print(List_TimeCost())

