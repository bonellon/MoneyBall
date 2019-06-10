from aylienapiclient import textapi

client = textapi.Client("eb565fb5", "710c5f1c0299fdc37629c4fcb1ff2eb5")

def getRatings(url):
    json = client.Elsa({'url':url})
    return json