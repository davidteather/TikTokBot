import os
import random
import string
import glob
from TikTokApi import TikTokApi

def clearTMP(delpath):
    r = glob.glob(delpath)
    for i in r:
        os.remove(i)

if not os.path.exists("downloaded"):
    os.mkdir('downloaded')

if not os.path.exists("output"):
    os.mkdir("output")

clearTMP('output/output.mp4')

# Vars
count = 30

verifyFp = "verify_" + ''.join(random.choice(string.letters) for num in range(40))
api = TikTokApi.get_instance(custom_verifyFp=verifyFp)
did = str(random.randint(10000, 999999999))

# I recommend using api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True) instead
# of the following line, but I can't guarantee support for the use_test_endpoints parameter into the future
results = api.trending(count=count, custom_did=did)
prevloops = 0
for res in results:
    open('downloaded/' + str(prevloops) +
            ".mp4", "wb").write(api.get_Video_By_TikTok(res, custom_did=did))
    open("downloaded/concat.txt", 'a').write("file " +
                                                str(prevloops) + ".mkv" + "\n")
    os.system("ffmpeg -loglevel panic -i downloaded/" + str(prevloops) +
                ".mp4" + " -c copy -map 0 downloaded/" + str(prevloops) + ".mkv")
    prevloops += 1

os.system("ffmpeg -f concat -i downloaded/concat.txt -safe 1 -r 30 -fflags +genpts -c:a copy downloaded/output.mp4")
os.system('''ffmpeg -loglevel error -r 30 -i resources/bkg.png -i downloaded/output.mp4 -b:v 1M -filter_complex ''' +
          '''"[1:v]scale=''' + "750" +
          ''':''' + "1080" + ''' [ovrl], [0:v][ovrl]overlay=(main_w-overlay_w)/2:((main_h-overlay_h)/2)"''' +
          ''' output/output.mp4''')


clearTMP('downloaded/*')
