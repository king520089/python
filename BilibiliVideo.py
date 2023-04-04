import requests, re, json, time
from lxml import etree

url = input("请输入视频网址：")


def TimeCount(func):
    def inner():
        start = time.time()
        func()
        end = time.time()
        print("爬取视频总共花了%d秒" % (end - start))

    return inner


@TimeCount
def spiderMovie():
    def getWebUrl(URL):
        url = URL
        global headers
        headers = {
            "referer": url,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63"}
        response = requests.get(url=url, headers=headers).text
        tree = etree.HTML(response)
        web_information = tree.xpath('/html/head/script[3]/text()')[0]
        message_text = re.sub(pattern=r'window.__playinfo__=', repl="", string=web_information, flags=re.S)
        return message_text

    def getVideo(video):
        VideoUrl = json.loads(video)['data']['dash']['video'][0]['baseUrl']
        Video = requests.get(url=VideoUrl, headers=headers).content
        return Video

    def getAudio(audio):
        AudioUrl = json.loads(audio)['data']['dash']['audio'][0]['baseUrl']
        Audio = requests.get(url=AudioUrl, headers=headers).content
        return Audio

    def VideoDownloads(*args):
        with open('D:\视频\舞蹈.mp4', mode='wb') as file:
            file.write(args[0])
        with open('D:\视频\音乐.mp3', mode='wb') as files:
            files.write(args[1])

    film = getWebUrl(url)
    movie = getVideo(film)
    music = getAudio(film)
    VideoDownloads(movie, music)


spiderMovie()