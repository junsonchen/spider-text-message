
# encoding=utf8
import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

DEBUG = False

#外部传进url
def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    sourceUrl = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']
    description = urlInfo['description']

    html = tools.getHtml(sourceUrl)
    if not DEBUG:
        if html == None:
            basePaser.updateUrl(sourceUrl, Constance.EXCEPTION)
            return

        regex = '[\u4e00-\u9fa5]+'
        chineseWord = tools.getInfo(html, regex)
        if not chineseWord:
            basePaser.updateUrl(sourceUrl, Constance.DONE)
            return

        # 取当前页面的全部url
        urls = tools.getUrls(html)

        # 过滤掉外链接 添加到数据库
        fitUrl = tools.fitUrl(urls, ['news.cn', 'xinhuanet.com'])
        for url in fitUrl:
            # log.debug('url = ' + url)
            basePaser.addUrl(url, websiteId, depth + 1)


    # 取当前页的文章信息
    # 标题
    regexs = '<h1.*?>(.*?)</h1>'
    title = tools.getInfo(html, regexs)
    title = title and title[0] or ''
    title = tools.delHtmlTag(title)
    # 内容
    regexs = ['<div id="content">(.*?)<div class="clear"></div>',
              '<div class="article">(.*?)<!--文章操作-->',
              '<div id="videoArea">(.*?)<!--文章操作-->',
              '<div class="content">(.*?)<div id="articleEdit">'
             ]

    content = tools.getInfo(html, regexs)
    content = content and content[0] or ''
    content = tools.delHtmlTag(content)

    log.debug('''
                depth     = %d
                sourceUrl = %s
                title     = %s
                content   =  %s
             '''%(depth, sourceUrl, title, content))

    if not DEBUG:
        if content and title:
            basePaser.addTextInfo(websiteId, sourceUrl, title, content)

        # 更新sourceUrl为done
        basePaser.updateUrl(sourceUrl, Constance.DONE)

if __name__ == '__main__':
    DEBUG = True
    url = 'http://news.xinhuanet.com/newmedia/2015-08/04/c_134478273.htm'
    haha = {'url': url, 'website_id': '582ea577350b654b67dc8ac8', 'depth': 1, 'description': ''}
    parseUrl(haha)