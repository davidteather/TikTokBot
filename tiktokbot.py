import requests
import random
import string
import glob
import math
import os
from TikTokApi import TikTokApi


# Creates new folders
if not os.path.isdir('output'):
    os.mkdir('output')

if not os.path.isdir('downloaded'):
    os.mkdir('downloaded')


# Functions to use later
def getLength(pathtofile):
    secsval = os.popen('''ffprobe -i ''' + pathtofile +
                       ''' -show_entries format=duration -v quiet -of csv="p=0"''').read()
    secsval.replace("\n", "")
    secs = float(secsval)
    return secs

def getSize(pathtofile):
    size = os.popen(
        "ffprobe -v error -select_streams v:0 -show_entries stream=width,height -v quiet -of csv=s=x:p=0 " + pathtofile).read()
    return int(size.split("x")[0]), int(size.split("x")[1])


def calculateScale(pathtofile):
    width, height = getSize(pathtofile)

    ratio = width / height
    if height > 1080:
        # Too tall
        shorten = height - 1080
        delength = shorten * ratio

        return width - delength, height - shorten

    elif height < 1080:
        if height < width:
            # Needs to extend up and use top as a limit
            shorten = 1080 - height
            delength = shorten * ratio

            return width + delength, height + shorten
        else:
            return ((width * 1080) / height), 1080


def clearTMP(delpath):
    r = glob.glob(delpath)
    for i in r:
        os.remove(i)


clearTMP("downloaded/*")
clearTMP('output/output.mp4')


#
# Start interface
#
print("Pick a video length (1-3)")
print("1. 2-3 minutes")
print("2. 5-7 minutes")
print("3. 10-12 minutes")

inp = input()

selections = {
    "1": 180,
    "2": 420,
    "3": 720
}

maxLength = selections.get(inp)
if maxLength == None:
    maxLength = 420

print("Select a video type")
print("1. Trending")
print("2. Hashtag")
print("3. User")
print("4. Sound")

selection = input()

if selection == "1":
    videoType = 1
elif selection == "2":
    videoType = 2
    print("Type in the hashtag without the #")
    print("You can add more hashtags by adding && between them ex: funny&&xmas")
    hashtags = input().split("&&")
elif selection == "3":
    videoType = 3
    print("Type in the user without the @")
    print("You can add more users by adding && between them ex: thecardguy&&spencerx")
    users = input().split("&&")
elif selection == "4":
    videoType = 4
    print("Type in the sound id or full url")
    print("You can add more sounds by adding && between them ex: 6729653061406474242&&https://www.tiktok.com/music/Wobble-224409322976509952?lang=en")
    sounds = input().split("&&")


# The count of the videos to retrieve per specified thing.
# If you're doing a lot of tags or users you might want to decrease count for a quicker runtime
count = 100
verifyFp = "verify_" + ''.join(random.choice(string.ascii_letters) for num in range(40))

# I recommend using api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True) instead
# of the following line, but I can't guarantee support for the use_test_endpoints parameter into the future
api = TikTokApi.get_instance(custom_verifyFp=verifyFp)
did = ''.join(random.choice(string.digits) for num in range(19))

if videoType == 1:
    results = api.trending(count=count, custom_did=did)
else:
    results = []
    if videoType == 2:
        for x in hashtags:
            res = api.byHashtag(x, count=count, custom_did=did)
            for y in res:
                results.append(y)
    elif videoType == 3:
        for x in users:
            res = api.byUsername(username=x, count=count, custom_did=did)
            for y in res:
                results.append(y)
    elif videoType == 4:
        for x in sounds:
            x = x.split("ps://www.tiktok.com/music/")[1].split("?")[0]
            x = x.split("-")[len(x.split("-"))-1]
            res = api.bySound(x, count=count, custom_did=did)
            for y in res:
                results.append(y)

random.shuffle(results)
currentLength = 0

for x in range(len(results)):
    if currentLength < maxLength:
        try:
            b = api.get_Video_By_TikTok(results[x], custom_did=did)
        except:
            b = api.get_Video_By_DownloadURL(
                results[x]['itemInfos']['video']['urls'][0], custom_did=did)
        open('downloaded/' + str(x) +
             ".mp4", "wb").write(b)

        vidLength = getLength('downloaded/' + str(x) + ".mp4")

        if currentLength + vidLength < maxLength:
            open("downloaded/concat.txt", 'a').write("file " +
                                                     str(x) + "bkg.mp4" + "\n")

            currentLength += vidLength
            print(currentLength)

            p1, p2 = calculateScale("downloaded/" + str(x) + ".mp4")

            os.system('''ffmpeg -loglevel error -r 30 -i resources/bkg.png -i downloaded/''' + str(x) + ".mp4" + ''' -b:v 1M -filter_complex ''' +
                      '''"[1:v]scale=''' + str(math.floor(p1)) + ''':''' + str(math.floor(p2)) + ''' [ovrl], [0:v][ovrl]overlay=(main_w-overlay_w)/2:((main_h-overlay_h)/2)"''' +
                      ''' downloaded/''' + str(x) + '''bkg.mp4''')
        else:
            break
    else:
        break

os.system("ffmpeg -f concat -i downloaded/concat.txt -safe 1 -r 30 -fflags +genpts -c:a copy output/output.mp4")


clearTMP('downloaded/*')
