import requests
import re
import json
import os
import base64

def make_get_request(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Get request failed with status code: {response.status_code}")
            print(response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

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

def clean_query(query):
    lower_query = query.lower()
    index = lower_query.find("feat")
    if index != -1:
        query = query[:index]
    
    query = query[:64] # limits the string to a max of 64 characters
    query = re.sub(r'[^\w\s]', ' ', query) # removes special characters
    return query