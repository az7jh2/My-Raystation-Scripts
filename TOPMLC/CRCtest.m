% %以文本格式读取文件的全部字符
% f=fopen('CRT example.top','rt');
% text=fread(f,'*char');  %多行1列的字符串
% fclose(f);
% %去除最后的CRC码
% text(9207:9212)=[];
clc;clear
load CRCtest
%求字符的ascii码
asc=abs(text);  %double类型
%转换成二进制
bin=de2bi(asc,16,'left-msb');  %每一行为1个字符的二进制码,16位，double类型，最高位在左边
%转换成一个列向量
rebin=reshape(bin',[],1);

%CRC16, x^16+x^15+x^2+1
%p=[1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1];
% zero=zeros(1,15);
% H=[];
% for a1=0:1
%     for a2=0:1
%         for a3=0:1
%             for a4=0:1
%                 for a5=0:1
%                     for a6=0:1
%                         for a7=0:1
%                             for a8=0:1
%                                 for a9=0:1
%                                     for a10=0:1
%                                         for a11=0:1
%                                             for a12=0:1
%                                                 for a13=0:1
%                                                     for a14=0:1
%                                                         p=[1 a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 a11 a12 a13 a14 1];
%                                                         h=crc.generator('Polynomial',p,'InitialState',zero,'FinalXOR',zero);
%                                                         H=[H;h];
%                                                     end
%                                                 end
%                                             end
%                                         end
%                                     end
%                                 end
%                             end
%                         end
%                     end
%                 end
%             end
%         end
%     end
% end
load PolySet
L=length(H);
CRC=zeros(L,1);
for i=1:L
    out=generate(H(i,1),rebin); %多行1列
    [m2,~]=size(out);
    index=m2-(length(p)-1)+1;
    crc=out(index:m2);
    decrc=bi2de(crc');
    CRC(i,1)=decrc;
end
find(CRC==19634)
%没有对应的结果

%改变初始值为全1，重新测试
clc;clear
load CRCtest
%求字符的ascii码
asc=abs(text);  %double类型
%转换成二进制
bin=de2bi(asc,16,'left-msb');  %每一行为1个字符的二进制码,16位，double类型，最高位在左边
%转换成一个列向量
rebin=reshape(bin',[],1);

load PolySet15
L=length(H);
CRC=zeros(L,1);
one=ones(1,15);
for i=1:L
    H(i,1).InitialState=one;
end
% for i=1:L
%     H(i,1).FinalXOR=one;
% end
for i=1:L
    out=generate(H(i,1),rebin); %多行1列
    [m2,~]=size(out);
    index=m2-(16-1)+1;
    crc=out(index:m2);
    decrc=bi2de(crc');
    CRC(i,1)=decrc;
end
find(CRC==19634)
%16位CRC，两种初始值均没有结果
%15位CRC，初始值全1，有结果p=1714([1 0 0 0 1 1 0 1 0 1 1 0 0 0 1 1])和7749([1 0 1 1 1
%1 0 0 1 0 0 0 1 0 0 1])

%以另一个文档测试
clc;clear
% %以文本格式读取文件的全部字符
% f=fopen('IMRT example.top','rt');
% text=fread(f,'*char');  %多行1列的字符串
% fclose(f);
% %去除最后的CRC码
% text(17501:17506)=[];

%求字符的ascii码
asc=abs(text);  %double类型
%转换成二进制
bin=de2bi(asc,16,'left-msb');  %每一行为1个字符的二进制码,16位，double类型，最高位在左边
%转换成一个列向量
rebin=reshape(bin',[],1);

zero=zeros(1,15);
one=ones(1,15);
p=[1 0 0 0 1 1 0 1 0 1 1 0 0 0 1 1];
% p=[1 0 1 1 1 1 0 0 1 0 0 0 1 0 0 1];
h=crc.generator('Polynomial',p,'InitialState',one,'FinalXOR',zero);
out=generate(h,rebin); %多行1列
[m2,~]=size(out);
index=m2-(16-1)+1;
crc=out(index:m2);
decrc=bi2de(crc');
%IMRT文件CRC码不匹配
%破解失败




                                                            
                                                                


