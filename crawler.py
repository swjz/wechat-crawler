import re
import codecs
import requests


def findURIList(filename='list.html'):
  file = codecs.open(filename, 'r', encoding='utf8')
  result = []
  try:
    for line in file:
      match = re.compile(r'(?<=hrefs=["])http://mp.weixin.qq.com/s.*?(?=["])')
      lineResult = re.findall(match, line)
      for thisResult in lineResult:
        result.append(thisResult)
  finally:
    file.close()

  return result


def crawler(filename='list.html'):
  count = 0
  result = findURIList(filename)
  for line in result:
    count += 1
    if count < 3:
      headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
      }
      response = requests.get(line, headers=headers)
      print(response.text)


def main():
  crawler()


if __name__ == '__main__':
  main()
