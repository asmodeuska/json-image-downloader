import sys, json, os, requests
from datetime import datetime
from validator_collection import checkers
#downloads images from the given url. Works only on the first element of the json array. 

if(len(sys.argv) < 3):
    print("Usage: python3 main.py <path to json file> <keys which you want to download>")
    exit(1)

f = open(sys.argv[1], 'r')
data = json.load(f)
toDownload = []

for i in range(2, len(sys.argv)):
    if sys.argv[i] in data[0]:
        toDownload = [item.get(sys.argv[i]) for item in data]

if(len(toDownload) == 0):
    print("No keys found")
    exit(1)

if (os.path.isdir(os.getcwd()+"\\downloads") == False):
    os.mkdir(os.getcwd()+"\\downloads")
folderName = os.getcwd()+'\\downloads\\'+datetime.utcnow().strftime("%Y_%m_%d-%I_%M_%S_%p")+'\\'
os.makedirs(folderName)
print("Found " + str(len(toDownload)) + " keys")
validKeys=0
for i in toDownload:
    if (checkers.is_url(i)):
        try:
            r = requests.get(i)
            r.raise_for_status()
            validKeys+=1
            with open(folderName + i.rsplit('/',1)[-1], 'wb') as outfile:
                outfile.write(r.content)
                print("Downloaded " + i)
        except requests.exceptions.RequestException as e:
            print("Error: " + str(e) + " for " + i)
print("Downloaded " + str(validKeys) + " valid urls from " + str(len(toDownload)) + " keys")
