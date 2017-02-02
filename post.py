def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.myFirstMD
    return db

if __name__ == '__main__':    #only execute this in the main thread

    HOST = 'http://weixin.sogou.com/'

    key_word = "咪蒙"
    entry = HOST + "weixin?type=2&query=" + key_word + "&page={}"

    import requests as req
    import re

    rInfo = '<h\d[\s\S]*?href="([\s\S]*?)".*?>([\s\S]*?)<\/a>[\s\S]*?<\/h\d>\s*<p[\s\S]*?>([\s\S]*?)<\/p>'

    html = req.get(entry.format(1))  # 第一页
    infos = re.findall(rInfo, html.text)

    def remove_tags(s):
        return re.sub('<.*?>', '', s)

    from html import unescape
    from urllib.parse import urlencode

    def weixin_params(link):
        ## link是临时链接的url
        html = req.get(link)
        rParams = 'var (biz =.*?".*?");\s*var (sn =.*?".*?");\s*var (mid =.*?".*?");\s*var (idx =.*?".*?");'
        params = re.findall(rParams, html.text)

        #initialization
        db = get_db()

        ## 文章内容就在html.txt中，用正则表达式找出来
        r_post_doby = '"rich_media">([\w\W]+)</div>'
        post_body = re.findall(r_post_doby, html.text)

        if len(params) == 0:
            return None
        p = {i.split('=')[0].strip(): i.split('=', 1)[1].strip('|" ') for i in params[0]}

        #Store the post in MongoDB
        posts = db.posts
        post_item = {
            "content" : post_body[0]
        }
        posts.insert(post_item)
        #
        # ## 把文章内容保存到html文件, 文件名:mid
        # f_name = p['mid'] + ".html"
        #
        # import pprint
        # pprint.pprint(posts.find_one())
        #
        # with open(f_name, 'w+', encoding='utf8') as f:
        #    f.write(post_body[0])

#        return p
#
    for (link, title, abstract) in infos:
        title = unescape(remove_tags(title))
        abstract = unescape(remove_tags(abstract))

        link = link.replace('amp;', '')
        params = weixin_params(link)

        print(link, title, abstract)
        if params is not None:
            link = "http://mp.weixin.qq.com/s?" + urlencode(params)
            print("fixed url: ", link, title, abstract)