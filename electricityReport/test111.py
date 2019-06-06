#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing import Process
import time,random
import os



def piao(name):
    print(os.getppid(),os.getpid())
    print('%s is piaoing' %name)
    time.sleep(5)
    print('%s is piao end' %name)



def doSome():
    for i in range(24):
        if i == 23:
            return





if __name__ == '__main__':
    p1=Process(target=piao,kwargs={'name':'alex',})
    p2=Process(target=piao,args=('wupeiqi',))
    p3=Process(target=piao,kwargs={'name':'yuanhao',})
    p1.start()
    p2.start()
    p3.start()
    print('主进程',os.getpid())