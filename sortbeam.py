# -*- coding: utf-8 -*-
#对当前计划的当前射野集重命名并排序
from connect import *
from operator import itemgetter
from string import zfill
from collections import Counter

#patient获取为当前患者
patient=get_current('Patient')
#获取当前计划
plan=get_current("Plan")
#获取当前射野集
beam_set=get_current("BeamSet")

#获取射野名称、机架角度、序号,以列表形式保存
#依次为序号（射野唯一标识）、名称、机架角度、射野排序号码、
beam=[]
i=0
while 1:
    try:
        beam.append([i,beam_set.Beams[i].Name,beam_set.Beams[i].GantryAngle,beam_set.Beams[i].Number])
        i+=1
    except ValueError:
        break

#判断机架角度，180-360之间的度数改为负数
n=range(len(beam))
for i in n:
    if 180<=beam[i][2]<360:
        beam[i][2]-=360

#排序,先按机架角度排序，相同的机架角度按序号排序
beam=sorted(beam,key=itemgetter(2,0))

#考虑到Varian分野问题查找有重复的机架角度
re=Counter([beam[i][2] for i in n])
#有重复的机架角度
regan=[x for x in re.keys() if re[x]>1]
#对排序好的beam重命名
num=1
i=0
while i<len(beam):
    if beam[i][2] in regan: #有重复
        rr=re[beam[i][2]]  #重复次数
        for j in range(rr):
            beam[i][3]=i+1
            beam[i][1]='B'+str(num)+'_G'+zfill(str(int(beam_set.Beams[beam[i][0]].GantryAngle)),3)+chr(97+j)
            i+=1
        num+=1
    else:
        beam[i][3]=i+1
        beam[i][1]='B'+str(num)+'_G'+zfill(str(int(beam_set.Beams[beam[i][0]].GantryAngle)),3)
        i+=1
        num+=1
#输出至计划系统,机架角度为3位数
for i in n:
    beam_set.Beams[beam[i][0]].Number=beam[i][3]
    beam_set.Beams[beam[i][0]].Name=beam[i][1]