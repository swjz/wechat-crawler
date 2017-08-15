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
  count = 0
  titleList = []
  dateList = []
  userList = []
  articleList = []
  result = findURIList(filename)
  for page in result:
    count += 1
    if count < 2:
      headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
      }
      response = requests.get(page, headers=headers)

      titleMatch = re.compile(r'(?<=<title>).*?(?=</title>)')
      title = re.search(titleMatch, response.text).group()
      titleList.append(title)

      dateMatch = re.compile(r'(?<=<em id="post-date" class="rich_media_meta rich_media_meta_text">).*?(?=</em>)')
      date = re.search(dateMatch, response.text).group()
      dateList.append(date)

      userMatch = re.compile(r'(?<=id="post-user">).*?(?=</a>)')
      user = re.search(userMatch, response.text).group()
      userList.append(user)

      articleMatch = re.compile(r'(?<=id="js_content">).*?(?=</div>)', re.DOTALL)
      rawArticle = re.search(articleMatch, response.text).group()
      htmlArticle = etree.HTML(rawArticle)
      article = htmlArticle.xpath('//p//span')


      articleList.append(article)


      print(title + " " + date + " " + user)
      print()
      for line in article:
        print(line.text)
      print()
      print("--------------------------------")
      print()
      print()

def main():
  crawler()


if __name__ == '__main__':
  main()
