#
# Ted Shaowang 2017/08/18
#
# For articles in a particular account given by crawler.py,
# do Chinese text segmentation and text classification
# using K-means clustering.
# 将 crawler.py 输出每个公众号的文章进行分词并对文章聚类
#

import codecs
import jieba.analyse
import numpy as np
from sklearn.cluster import KMeans


# 将每个公众号的信息拆分成一个list，每个元素分别是每天的推送
def partition(filename):
  file = codecs.open(filename, 'r', encoding='utf8').readlines()
  resultList = []
  thisArticle = []
  titleList = []
  dateList = []

  # 单独处理第一篇文章，后面的用循环处理
  # Process first article individually
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


# Do Chinese text segmentation and text classification using K-means clustering
# 对一个公众号的每篇文章进行分词处理，并用 K-Means 聚类
def cluster(filename, n_clusters):
  jieba.analyse.set_stop_words("./stopwords-utf8.txt")
  [resultList, titleList, dateList] = partition(filename)
  tags = []

  for i in range(len(resultList)):
    thisArticleWeights = []
    line = resultList[i]
    thisArticleTags = jieba.analyse.extract_tags(line, topK=20, withWeight=True, allowPOS=())
    for tag in thisArticleTags:
      thisArticleWeights.append(tag[1])  # Keep weights only

    if len(thisArticleWeights) == 20:
      tags.append(thisArticleWeights)
    else:
      tags.append(np.zeros(20, float))

    # To print tags and weights for each article respectively
    # print(title + date)
    # for tag in thisArticleTags:
    #   print("tag: %s\t\t weight: %f" % (tag[0], tag[1]))
    # print()
    # print("--------------------------------")
    # print()

  x = np.array(tags, float)
  kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(x)
  print("Cluster index, Title of article")
  for i in range(len(kmeans.labels_)):
    print("%d, %s" % (kmeans.labels_[i], titleList[i].replace('\n', '')))


def main():
  filename = input()
  cluster(filename=filename, n_clusters=3)  # number of clusters to form


if __name__ == '__main__':
  main()
