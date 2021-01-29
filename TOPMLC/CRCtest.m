% %���ı���ʽ��ȡ�ļ���ȫ���ַ�
% f=fopen('CRT example.top','rt');
% text=fread(f,'*char');  %����1�е��ַ���
% fclose(f);
% %ȥ������CRC��
% text(9207:9212)=[];
clc;clear
load CRCtest
%���ַ���ascii��
asc=abs(text);  %double����
%ת���ɶ�����
bin=de2bi(asc,16,'left-msb');  %ÿһ��Ϊ1���ַ��Ķ�������,16λ��double���ͣ����λ�����
%ת����һ��������
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
    out=generate(H(i,1),rebin); %����1��
    [m2,~]=size(out);
    index=m2-(length(p)-1)+1;
    crc=out(index:m2);
    decrc=bi2de(crc');
    CRC(i,1)=decrc;
end
find(CRC==19634)
%û�ж�Ӧ�Ľ��

%�ı��ʼֵΪȫ1�����²���
clc;clear
load CRCtest
%���ַ���ascii��
asc=abs(text);  %double����
%ת���ɶ�����
bin=de2bi(asc,16,'left-msb');  %ÿһ��Ϊ1���ַ��Ķ�������,16λ��double���ͣ����λ�����
%ת����һ��������
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
    out=generate(H(i,1),rebin); %����1��
    [m2,~]=size(out);
    index=m2-(16-1)+1;
    crc=out(index:m2);
    decrc=bi2de(crc');
    CRC(i,1)=decrc;
end
find(CRC==19634)
%16λCRC�����ֳ�ʼֵ��û�н��
%15λCRC����ʼֵȫ1���н��p=1714([1 0 0 0 1 1 0 1 0 1 1 0 0 0 1 1])��7749([1 0 1 1 1
%1 0 0 1 0 0 0 1 0 0 1])

%����һ���ĵ�����
clc;clear
% %���ı���ʽ��ȡ�ļ���ȫ���ַ�
% f=fopen('IMRT example.top','rt');
% text=fread(f,'*char');  %����1�е��ַ���
% fclose(f);
% %ȥ������CRC��
% text(17501:17506)=[];

%���ַ���ascii��
asc=abs(text);  %double����
%ת���ɶ�����
bin=de2bi(asc,16,'left-msb');  %ÿһ��Ϊ1���ַ��Ķ�������,16λ��double���ͣ����λ�����
%ת����һ��������
rebin=reshape(bin',[],1);

zero=zeros(1,15);
one=ones(1,15);
p=[1 0 0 0 1 1 0 1 0 1 1 0 0 0 1 1];
% p=[1 0 1 1 1 1 0 0 1 0 0 0 1 0 0 1];
h=crc.generator('Polynomial',p,'InitialState',one,'FinalXOR',zero);
out=generate(h,rebin); %����1��
[m2,~]=size(out);
index=m2-(16-1)+1;
crc=out(index:m2);
decrc=bi2de(crc');
%IMRT�ļ�CRC�벻ƥ��
%�ƽ�ʧ��




                                                            
                                                                


