from aylienapiclient import textapi

#account bonellon@tcd.ie
#client = textapi.Client("eb565fb5", "710c5f1c0299fdc37629c4fcb1ff2eb5")

#account nbonelloghio@hotmail.com
#client = textapi.Client("36913d8f", "ca86dde91123ded2fb1f7e6372ccaa84")

#account nicbonelloghio@gmail.com
client = textapi.Client("4e9cf96f", "4ff17796824f5c22ab61c3eb7b3ff6a7")

def getRatings(url):
    print(client.RateLimits())
    json = client.Elsa({'url':url})
    return json
