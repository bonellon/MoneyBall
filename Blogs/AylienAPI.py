from aylienapiclient import textapi
from urllib.error import URLError
from aylienapiclient.errors import HttpError

#account bonellon@tcd.ie
#client = textapi.Client("eb565fb5", "710c5f1c0299fdc37629c4fcb1ff2eb5")

#account nbonelloghio@hotmail.com
client = textapi.Client("36913d8f", "ca86dde91123ded2fb1f7e6372ccaa84")


def getRatings(url):
    #try:
    print(client.RateLimits())
    json = client.Elsa({'url':url})
    return json
    #except HttpError as err:
     #   print("AylienAPI Error: "+str(err))
      #  return None
    #except URLError as err:
     #   print("AylienAPI: No active internet connection...")
      #  print(err)
       # return None
