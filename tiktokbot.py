# Json Response https://m.tiktok.com/share/item/list?id=&type=5&count=48&minCursor=0&maxCursor=0&_signature=Ajk97hAbXtYLdUf7zgjlDAI5Pf
# obj -> body -> itemListData -> itemListData[i] -> itemInfos -> video -> urls[0] gives downloadable url
import requests
import random
import string
import urllib.request
import glob, os
import mimetypes


def clearTMP(delpath):
    r = glob.glob(delpath)
    for i in r:
        os.remove(i)

def sig_generator(stringLength=26):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

# clearTMP('downloaded/*')

count = 10
url = "https://m.tiktok.com/share/item/list?id=&type=5&count=" + str(count) +"&minCursor=0&maxCursor=0&_signature=NMGxyxAeaC89jcve1KWrdDTBsd"
r = requests.get(url, headers={"authority": "m.tiktok.com", "method": "GET", "path": url.split("https://m.tiktok.com")[0], "scheme": "https", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                               "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "cache-control": "max-age=0", "upgrade-insecure-requests": "1",
                               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"})


data = r.json()
i = count - 1

while (i >= 0):
    try:
        r = requests.get(data["body"]["itemListData"][i]["itemInfos"]["video"]["urls"][0], allow_redirects=False)
        content_type = r.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        open('downloaded/' + str(i) + extension, "wb").write(r.content)
        open("downloaded/concat.txt", 'a').write("file " + str(i) + ".mkv" + "\n")
        os.system("ffmpeg -i downloaded/" + str(i) + extension + " -c copy -map 0 downloaded/" + str(i) + ".mkv")
        i -= 1
    except:
        i -= 1

# concat errors
# ffmpeg -f concat -i downloaded/concat.txt -safe 1 -r 30 -fflags +genpts -c:a copy output.mp4