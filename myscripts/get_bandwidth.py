import os
import random
#import numpy as np
import time
import sys
#from prettytable import PrettyTable
#import datetime
import math

#该实验用于得到1-1024k的请求与大小的关系
final_bandwidth={}
print("start testing")

testcase = [1024]

fd1 = open("/users/hys/iosize-bandwidth.txt", "a")
#fd1.write("iosize bandwidth\n")    
#for iosize in range(3,4):
#for iosize in testcase:
for iosize in range(1,1025):
    #修改配置配置文件
    if True:
    #if iosize%4!=0:
        run_cmd = "/users/hys/env/fio/bin/fio -filename=/users/hys/cephrbd/test -direct=1 -iodepth 10 -thread -rw=randwrite -ioengine=libaio -bs=%dk -size=%dk -numjobs=10 -runtime=15 -group_reporting -name=rand_100write_4k"%(iosize,100*iosize)
        #print(run_cmd)
        bw = 0.0
        bw_total = 0.0
        for i in range(2):
            with os.popen(run_cmd, "r") as p:
                r = p.readlines()
                find=0
                for line in r:
                    #print(line[2:7])
                    if line[2:7] == "WRITE":
                        find=1
                    if find == 1:
                        #print(line)
                        i = line.find('=')
                        j = line.find('/',i+1)
                        #print(line[i+1:j])
                        bw = float(line[i+1:j-3])
                        if line[j-3:j]=="KiB":
                            bw = bw/1024
                        #print(bw)
                        break
            bw_total = bw_total+bw
            time.sleep(3)
        bw = bw_total/2
        fd1.write(str(iosize)+" "+str(bw)+"\n")
        fd1.flush()
        time.sleep(10)    

fd1.close()
