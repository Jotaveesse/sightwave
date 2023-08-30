import azure.ai.vision as sdk
import os
from dotenv import load_dotenv
import base64

load_dotenv()

AZURE_URL = os.environ["AZURE_URL"]
AZURE_KEY = os.getenv("AZURE_KEY")

def get_image_description(image_url= None, image_base64=None):
    service_options = sdk.VisionServiceOptions(AZURE_URL, AZURE_KEY)
    if image_url:
        vision_source = sdk.VisionSource(url=image_url)

    elif image_base64:
        file_path = store_base64_image(image_base64.split(',')[1], "img", "tmp")
        vision_source = sdk.VisionSource(filename=file_path)

    else:
        return None

    analysis_options = sdk.ImageAnalysisOptions()

    analysis_options.features = (
        sdk.ImageAnalysisFeature.CAPTION |
        sdk.ImageAnalysisFeature.DENSE_CAPTIONS |
        sdk.ImageAnalysisFeature.TAGS
    )

    image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

    result = image_analyzer.analyze() 

    if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
        
        # if result.caption is not None:
        #     print(" Caption:")
        #     print("   '{}', Confidence {:.4f}".format(result.caption.content, result.caption.confidence))

        # if result.dense_captions is not None:
        #     print(" Dense Captions:")
        #     for caption in result.dense_captions:
        #         print("   '{}', {}, Confidence: {:.4f}".format(caption.content, caption.bounding_box, caption.confidence))

        # if result.tags is not None:
        #     print(" Tags:")
        #     for tag in result.tags:
        #         print("   '{}', Confidence {:.4f}".format(tag.name, tag.confidence))

        return result

    else:

        error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
        print(" Analysis failed.")
        print("   Error reason: {}".format(error_details.reason))
        print("   Error code: {}".format(error_details.error_code))
        print("   Error message: {}".format(error_details.message))

        return None

def store_base64_image(base64_string, file_name, directory):
    # Decode the base64 string
    image_data = base64.b64decode(base64_string)
    
    # Create the file path
    file_path = os.path.join(directory, file_name)
    
    # Write the image data to the file
    with open(file_path, 'wb') as f:
        f.write(image_data)
    
    return file_path