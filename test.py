import requests

def test():
    # API endpoint and subscription key
    endpoint = "https://sightwave.cognitiveservices.azure.com/"
    subscription_key = "dee7616b650d4c9fa8c14eff0b06c27b"

    # Construct the API URL
    api_url = endpoint + "vision/v3.2/analyze"

    # Image URL or binary data
    image_url = "https://as1.ftcdn.net/v2/jpg/05/61/99/50/1000_F_561995097_a0dHcJrC2lCdOj6CBp6xBeGYv0hCsMyM.jpg"

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    # Request body
    data = {
        "url": image_url,
    }

    params = {
        "visualFeatures": "Description",  # Include desired visual features
    }

    # Send POST request
    response = requests.post(api_url, headers=headers, params=params, json=data)

    # Parse and handle response
    result = response.json()
    print(result)
    description = result["description"]["captions"][0]["text"]
    print("Image Description:", description)
    raise Exception("") 

