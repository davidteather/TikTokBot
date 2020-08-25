import os
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
api = TikTokApi()

results = api.trending(count=count)
prevloops = 0
for res in results:
    open('downloaded/' + str(prevloops) +
            ".mp4", "wb").write(api.get_Video_By_TikTok(res))
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
