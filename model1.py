from transformers import pipeline
from openai import OpenAI

# Function to generate text from image
def img2text(imgUrl):
    img_to_text_pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    text = img_to_text_pipe(imgUrl)[0]["generated_text"]
    return text

# New image classification pipeline
def classifyImage(imgUrl):
    img_classify_pipe = pipeline("image-classification", model="google/vit-base-patch16-224")
    #pipe = pipeline("image-classification", model="google/vit-base-patch16-224")
    classification = img_classify_pipe(imgUrl)
    return classification

# Function to generate a short story based on a scenario
def textGeneration(msg):
    """msg should be a dict of the form - {"role": "user","content": scenario}"""

    client = OpenAI()
    
    msg_list = [{"role": "system", "content": "You are an expert social media content creator. Using engaging visuals and captions, you generate an Instagram post description in less than 100 words based on the given scenario."}]
    msg_list.append(msg)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        max_completion_tokens=200,
        messages=msg_list
    )
    
    out_message = response.choices[0].message.content
    return (out_message)

# Function to run all three models (image to text, image classification, and text generation)
def runModels(url):
    # Generate caption from image
    scenario = img2text(url)
    
    # Classify the image
    classification = classifyImage(url)
    
    # Generate Instagram post text based on scenario
    message = {"role": "user", "content": scenario}
    story = textGeneration(message)
    
    # Return the caption, story, and classification result
    return (scenario, story, classification)
