from bs4 import BeautifulSoup
import urllib.request as request
import urllib.error
from flask import Flask
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
import os
import platform
from PIL import Image


app = Flask(__name__)
api = Api(app)

# API that pings pond5 website. Returns "Pong" if successful
class Ping(Resource):
    def get(self):
        URL = "www.pond5.com"
        ping = os.system(" ping -c 1 " + URL)
        # Success
        if ping==0:
            return "Pong"
        # Failure
        else:
            return "Unable to ping"

# API that returns information about the system running in JSON format
class System(Resource):
    def get(self):
        data = {'system': platform.uname().system,
                'release': platform.release(),
                'version': platform.uname().version,
                'architecture': platform.architecture(),
                'machine': platform.machine()}
        return jsonify(data)

# API that returns preview information about a media picture from pond5.com
class Media_info(Resource):
    # media_id is the numbered code of the specific photo resource
    def get(self, media_id):
        URL = "https://www.pond5.com/photo/" + str(media_id)

        try:
            response = request.urlopen(URL)
        except urllib.error.URLError as e:
            return e.reason

        # Parse webpage and identify the image
        soup = BeautifulSoup(response, 'html.parser')
        icon = soup.find('img')

        # Save name and source
        img_src = icon['src']
        img_name = icon['alt']

        # Open image source and get dimensions and size
        img_data = request.urlopen(icon['src'])
        im = Image.open(img_data)
        img_dimensions = {'width': im.size[0], 'height': im.size[1]}
        img_size = img_data.info()["Content-Length"]

        # Gather information to JSON object
        data = {'name': img_name,
                'source': img_src,
                'dimensions':img_dimensions,
                'size': img_size}

        return jsonify(data)

# Define routes
api.add_resource(Ping, '/ping')
api.add_resource(System, '/system')
api.add_resource(Media_info, '/mediainfo/<media_id>')

# Basic homepage information
@app.route("/")
def home():
    html = "<h3>Welcome!</h3><br><p>Navigate to /ping to ping Pond5 site.</p><br>\
    <p>Navigate to /system to display system information.</p><br>\
    <p>Navigate to /mediainfo/media_id to get preview information of an image\
    where media_id is the resource id number.</p>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
