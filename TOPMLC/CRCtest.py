# -*- coding: utf-8 -*-
#CRC测试
import crcmod
#读入文件,第二个参数默认为r，文本格式读入
#f=open('e:/Script/TOP MLC/CRT example.top')
f=open('e:/Script/TOP MLC/IMRT example.top')
#读取所有内容,汉子需要转码
try:
    text=f.read().decode('gb2312')
finally:
    f.close()
#len 9212,unicode类型

codetext=text.encode('utf-8')
#len 9218,str类型

#去除最后的空格
msg=codetext[:-1]

#去除CRC数值
msg=codetext[:-6]

#去除CRC数值及前一个空格
msg=codetext[:-7]

#去除整行CRC=
msg=codetext[:-12]

#去除整行CRC=及前一个回车
msg=codetext[:-13]

#去除Note以后
msg=codetext[:-78]

#遍历所有组合,0x10000-0x1FFFF,65536-131071
p=range(0b10000000000000001,0b11111111111111111,2)
result=[]
for i in p:
    crc16_func = crcmod.mkCrcFun(i, initCrc=0xFFFF, xorOut=0)
    crc_value=crc16_func(msg)
    if crc_value==0:
        result.append(i)
#初始值为全0或全1，均找不到匹配的结果