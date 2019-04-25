# coding: utf-8
 
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
 
# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('stopwords.txt',encoding='gbk').readlines()]
    return stopwords

# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    #print("正在分词")
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

# 给出文档路径
filename = "ciyun.txt"
outfilename = "out.txt"
inputs = open(filename, 'r', encoding='gbk')
outputs = open(outfilename, 'w', encoding='gbk')

str=''
# 将输出结果写入ou.txt中
for line in inputs:
	line_seg = seg_depart(line)
	outputs.write(line_seg + '\n')
	str+=line_seg
	str+=" "
	#print("-------------------正在分词和去停用词-----------")
outputs.close()
inputs.close()
print("删除停用词和分词成功！！！")
 
cloud = WordCloud(
 #设置字体，不指定可能会出现中文乱码
 font_path="msyh.ttf",
 #font_path=path.join(e,'xxx.ttc'),
 #设置背景色
 background_color='white',
 #词云形状
 #mask=color_mask,
 #允许最大词汇
 max_words=2000,
 #最大号字体
 max_font_size=40
 )
 
wc = cloud.generate(str)
wc.to_file("ciyun.jpg") 
plt.imshow(wc)
plt.axis("off")
plt.show()