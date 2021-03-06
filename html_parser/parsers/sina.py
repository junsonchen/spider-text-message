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

    # 使用urlopen网页有时乱码 用get请求 然后设置编码解决了问题
    html = tools.getHtmlByGet(sourceUrl)

    if not DEBUG:
        if html == None:
            if sourceUrl == Constance.SINA:
                basePaser.updateUrl(sourceUrl, Constance.TODO)
            else:
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
        fitUrl = tools.fitUrl(urls, "sina.com.cn")
        for url in fitUrl:
            # log.debug('url = ' + url)
            basePaser.addUrl(url, websiteId, depth + 1)

    # 取当前页的文章信息
    # 标题
    regexs = '<h1.*?>(.*?)</h1>'
    title = tools.getInfo(html, regexs)
    title = title and title[0] or ''
    title = tools.delHtmlTag(title)

    if title == '加载中...':
        # 更新sourceUrl为done
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return


    # 内容
    regexs = ['id="artibody".*?>(.*?)<!-- 吸顶导航结束定位标记 -->',
              'id="artibody".*?>(.*?)<div id="left_hzh_ad">',
              '<!-- 正文内容 begin -->(.*?)<!-- 正文内容 end -->',
              'id="articleContent".*?>(.*?)<div class="spacer"></div>'
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
    print(html)
    if not DEBUG:
        if content and title:
            basePaser.addTextInfo(websiteId, sourceUrl, title, content)

        # 更新sourceUrl为done
        basePaser.updateUrl(sourceUrl, Constance.DONE)

if __name__ == '__main__':
    print('main')
    DEBUG = True
    url = 'http://sina.com.cn/m/xiaojunsong'
    haha = {'url': url, 'website_id': '582ea577350b654b67dc8ac8', 'depth': 1, 'description': ''}
    parseUrl(haha)