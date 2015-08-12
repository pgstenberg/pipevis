import urllib, json, random

class GiphyApi:

    def __init__(self, tags, api_token = "dc6zaTOxFJmzC"):
        self.api_token = api_token
        self.tags = tags

    def randomize_image(self, tag_collection):
        randomized_tag = random.choice(self.tags[tag_collection])
        request_url = "http://api.giphy.com/v1/gifs/random?api_key=%s&tag=%s" % (self.api_token, randomized_tag)
        giphy_data = json.loads(urllib.urlopen(request_url).read())
        return giphy_data['data']['image_url']
