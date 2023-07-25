import requests
import json
import re
import base64
import os

ASTICA_URL = 'https://vision.astica.ai/describe'

with open('keys.json') as file:
    keys = json.load(file)
    
def make_post_request(endpoint, payload, timeout=30):
    try:
        response = requests.post(endpoint, data=json.dumps(payload), timeout=timeout, headers={ 'Content-Type': 'application/json', })
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Post request failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# retrieves the file and transforms to base64
def path_to_base64(image_path):
    with open(image_path, 'rb') as file:
        image_data = file.read()
    
    image_extension = os.path.splitext(image_path)[1]
    image_base64 = f"data:image/{image_extension[1:]};base64,{base64.b64encode(image_data).decode('utf-8')}"

    return image_base64

def is_url(input_string):
    url_pattern = r"^(http|https|ftp)://.*"  # matches http, https, and ftp protocols
    return bool(re.match(url_pattern, input_string))

def get_image_description(image_path):
    # accepts url or file path (JPG AND PNG ONLY) (USING FILE PATH COSTS MORE)
    if is_url(image_path):
        image = image_path
    else:
        image = path_to_base64(image_path)
    
    astica_params = {
        'tkn': keys['astica_key'],
        'modelVersion': '1.0_full', # '1.0_full', '2.0_full', or '2.1_full'
        'visionParams': 'description', # defines the parameters to be detected, some can cost a lot, so be careful
        'input': image,
    }

    response = make_post_request(ASTICA_URL, astica_params)

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