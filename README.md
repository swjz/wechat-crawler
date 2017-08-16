# A Crawler for WeChat Official Accounts

Crawls ALL articles from one particular account; TBS Studio may be needed to get the full list of articles (html file).

Currently only plain text supported.

Usage:
`echo 'html filename' | python3 crawler.py > 'output text filename'`

Example:
`echo lalala.html | python3 crawler.py > lalala.txt`

# 微信公众号文章爬虫

可爬取某一公众号所有文章，需要通过 TBS Studio 得到文章列表页 html 方可爬取。目前仅支持纯文本爬取。

用法:
`echo 'html filename' | python3 crawler.py > 'output text filename'`

示例:
`echo lalala.html | python3 crawler.py > lalala.txt`
