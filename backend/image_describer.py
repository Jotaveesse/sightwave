import os
import requests
import json
import base64

AZURE_URL = os.environ["AZURE_URL"]
AZURE_KEY = os.environ["AZURE_KEY"]

def get_image_description(image_url=None, image_base64=None):
    api_url = AZURE_URL + "computervision/imageanalysis:analyze"
    params = {
        'api-version':'2023-04-01-preview',
        'features': 'caption,tags,denseCaptions'
    }
    
    if image_url:
        data = json.dumps({'url': image_url})
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': AZURE_KEY
        }

    elif image_base64:
        data = base64.b64decode(image_base64.split(',')[1])
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': AZURE_KEY
        }
    else:
        return None

    response = requests.post(api_url, headers=headers, params=params, data=data)
    response.raise_for_status()
    analysis = response.json()

    return analysis