from .package import requester as req
from dotenv import load_dotenv
import json
import re
import os

load_dotenv()

ASTICA_KEY = os.getenv("ASTICA_KEY")
ASTICA_URL = os.getenv("ASTICA_URL")
    
def is_url(input_string):
    url_pattern = r"^(http|https|ftp)://.*"  # matches http, https, and ftp protocols
    return bool(re.match(url_pattern, input_string))

def get_image_description(image_path):
    # accepts url or file path (JPG AND PNG ONLY) (USING FILE PATH COSTS MORE)
    if is_url(image_path):
        image = image_path
    else:
        image = req.path_to_base64(image_path)
    
    astica_params = {
        'tkn':  ASTICA_KEY,
        'modelVersion': '1.0_full', # '1.0_full', '2.0_full', or '2.1_full'
        'visionParams': 'description', # defines the parameters to be detected, some can cost a lot, so be careful
        'input': image,
    }

    response = req.make_post_request(ASTICA_URL, astica_params)

    if response == None:
        return None

    # prints whole response
    print(json.dumps(response, indent=4))

    # Handle asticaAPI response
    if 'status' in response:
        # Output Error if exists
        if response['status'] == 'error':
            print('Output:\n', response['error'])
            return (None, None)
        # Output Success if exists
        if response['status'] == 'success':
            '''if 'caption_GPTS' in response and response['caption_GPTS'] != '':
                print('GPT Caption:', response['caption_GPTS'])
            if 'caption' in response and response['caption']['text'] != '':
                print('Caption:', response['caption']['text'])
            if 'caption_tags' in response and response['caption']['text'] != '':
                print('Tags:', response['caption_tags'])
            if 'CaptionDetailed' in response and response['CaptionDetailed']['text'] != '':
                print('CaptionDetailed:', response['CaptionDetailed']['text'])
            if 'objects' in response:
                print('Objects:', response['objects'])'''
            
            return (response['caption']['text'], response['caption_tags'])
    else:
        print('Invalid response')
        return (None, None)