#
# Ted Shaowang 2017/08/18
#
# 将 crawler.py 输出的文本进行拆分
#

import jieba
import codecs


# 将每个公众号的信息拆分成一个list，每个元素分别是每天的推送
def partition(filename):
  file = codecs.open(filename, 'r', encoding='utf8').readlines()
  resultList = []
  thisArticle = []
  titleList = []
  dateList = []

  # 单独处理第一篇文章，后面的用循环处理
  titleList.append(file[1])
  dateList.append(file[2])

  i = 4
  while i < len(file):
    file[i] = file[i].replace(u'\xa0', '')
    file[i] = file[i].replace(u'\n', '')
    if file[i] == "--------------------------------" and i + 3 < len(file):
      i += 3
      titleList.append(file[i])
      i += 1
      dateList.append(file[i])
      resultList.append(''.join(thisArticle))
      thisArticle = []
    else:
      thisArticle.append(file[i])
    i += 1

  return [resultList, titleList, dateList]


# 对每篇文章进行分词处理
def cut(filename):
  [resultList, titleList, dateList] = partition(filename)

  for line in resultList:
    segResultList = jieba.cut(line, cut_all=False)
    print(', '.join(segResultList))


def main():
  filename = input()
  cut(filename=filename)


if __name__ == '__main__':
  main()
