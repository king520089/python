import requests, re, tqdm
from lxml import etree

url = input("请输入视频网址:")


def getVideoUrl(url):
    url = url
    global headers
    headers = {"Referer": "https://www.acfun.cn/",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63"
               }
    response = requests.get(url=url, headers=headers).text
    tree = etree.HTML(response)
    message = tree.xpath('//body/script[7]/text()')[0]
    videoUrl = re.findall(pattern=r'\\"backupUrl\\":\[\\\"(.*?)\\\"\]\,\\"m3u8Slice\\"', string=message, flags=re.S)[1]
    return videoUrl


def getVideo(param):
    m3u8Text = requests.get(url=param, headers=headers).text
    firstTs = re.sub(pattern=r'#EXTM3U\n#EXT-X-VERSION:\d*\n#EXT-X-TARGETDURATION:\d*\n#EXT-X-MEDIA-SEQUENCE:\d*',
                     repl="", string=m3u8Text, flags=re.S)
    secondTs = re.sub(pattern=r'#EXTINF:\d*\.\d*\,', repl="", string=firstTs, flags=re.S)
    lastTs = re.sub(pattern=r'#EXT-X-ENDLIST', repl="", string=secondTs, flags=re.S).split()
    for item in tqdm.tqdm(lastTs):
        motionUrl = "https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/" + item
        video = requests.get(url=motionUrl, headers=headers).content
        with open("D:\视频\【大温温温温】穿个黑色连裤袜录舞！可以和我交往吗！.mp4", mode='ab') as file:
            file.write(video)


param = getVideoUrl(url)
getVideo(param)
