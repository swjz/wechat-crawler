#
# Ted Shaowang 2017/08/16
#
# A crawler for WeChat Official Accounts
# 微信公众号文章爬虫
#
# Crawls ALL articles from one particular account
# TBS Studio may be needed to get the full list of articles (html file)
# 可爬取某一公众号所有文章，需要通过 TBS Studio 得到文章列表页 html 方可爬取
#
# Currently only plain text supported
# 目前仅支持纯文本爬取
#
# Usage:
# echo 'html filename' | python3 crawler.py > 'output text filename'
#
# Example:
# echo FSTQuant.html | python3 crawler.py > FSTQuant.txt
#


import re
import codecs
import requests
from lxml import etree


def findURIList(filename='list.html'):
  file = codecs.open(filename, 'r', encoding='utf8')
  resultList = []
  try:
    for line in file:
      match = re.compile(r'(?<=hrefs=["])http://mp.weixin.qq.com/s.*?(?=["])')
      lineResult = re.findall(match, line)
      for thisResult in lineResult:
        resultList.append(thisResult)
  finally:
    file.close()
    resultListUnique = list(set(resultList))
    resultListUnique.sort(key=resultList.index)

  return resultListUnique


def crawler(filename='list.html'):
  titleList = []
  dateList = []
  userList = []
  articleList = []
  result = findURIList(filename)
  for i in range(len(result)):
    # 方便从中间开始爬
    startPoint = 0
    if i+startPoint>=len(result)-1:
      break
    page = result[i+startPoint]

    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }
    response = requests.get(page, headers=headers)

    titleMatch = re.compile(r'(?<=<title>).*?(?=</title>)')
    title = re.search(titleMatch, response.text).group()
    titleList.append(title)

    dateMatch = re.compile(r'(?<=<em id="post-date" class="rich_media_meta rich_media_meta_text">).*?(?=</em>)')
    # 如果内容被作者删除或违规删除，date 将返回 None
    date = re.search(dateMatch, response.text)
    if date:
      date = date.group()
    else:
      continue
    dateList.append(date)

    userMatch = re.compile(r'(?<=id="post-user">).*?(?=</a>)')
    user = re.search(userMatch, response.text).group()
    userList.append(user)

    articleMatch = re.compile(r'(?<=id="js_content">).*?(?=</div>)', re.DOTALL)
    rawArticle = re.search(articleMatch, response.text).group()
    htmlArticle = etree.HTML(rawArticle)
    article = htmlArticle.xpath('//p//span | //p//strong | //p')

    articleList.append(article)

    print("Article No. " + str(i+startPoint))
    print(title)
    print(date + " " + user)
    print()
    for line in article:
      print(line.text)
    print()
    print("--------------------------------")
    print()


def main():
  filename = input()
  crawler(filename=filename)


if __name__ == '__main__':
  main()
