import urllib, json

class GiphyApi:

    def __init__(self, api_token = "dc6zaTOxFJmzC"):
        self.api_token = api_token

    def randomize_image(self, tags):
        request_url = "http://api.giphy.com/v1/gifs/random?api_key=%s&tag=%s" % (self.api_token, tags)
        giphy_data = json.loads(urllib.urlopen(request_url).read())
        return giphy_data['data']['image_url']
