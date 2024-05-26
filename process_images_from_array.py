import base64
import matplotlib as plt 
from base64 import b64decode
import numpy as np
from PIL import Image
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage


def encode_image_file(image_file):
    ''' Encode uploaded image file '''
    return base64.b64encode(image_file.read()).decode('utf-8')

def image_captioning(img_base64,prompt):
    ''' Image summary '''
    chat = ChatOpenAI(model="gpt-4o",
                      max_tokens=4000)

    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text":prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        },
                    },
                ]
            )
        ]
    )
    return msg.content

# Read images, encode to base64 strings, and get image summaries
def read_images(base64_images, prompt):
    image_summaries = []

    # Check if base64_images is a single image or a list of images
    if isinstance(base64_images, str):
        # If it's a single image, process it directly
        img_capt = image_captioning(base64_images, prompt)
        image_summaries.append(img_capt)
    else:
        # If it's a list of images, process each image
        for base64_image in base64_images:
            img_capt = image_captioning(base64_image, prompt)
            image_summaries.append(img_capt)
    
    return image_summaries

def text_prompt():
    prompt ="""
You are given a page, which might contain graphs, tables and images.
This page is the part of the larger document.
Describe just the text of the page in details, leave the unique reference to the graphs, tables and images, if these present. 
Don not hallucinate, provide only the text output, ignore the graphs, tables and images content other than their reference.
""" 
    return prompt

def graphs_and_tables_prompt():
    prompt ="""
You are given a page, which might contain graphs, tables and images.
This page is the part of the larger document.
Describe just the graphs and tables in details. 
Be very specific about the values, group the data together in the recieved output.
Don not hallucinate, provide only the graphs and tables output, ignore the page content other than graphs' and tables' descriptions.
""" 
    return prompt

def generate_piechart(text):
    prompt=f"""
You are given the description of either table or the graph:{text}
You should write a code to draw a pie chart based on this data using matplotlib.
The drawn piechart should be saved as jpg file, it should contain barchart in the name.
Add plt.show() at the end of the script as well.
The output should contain just python code, dont put there anything like '''python. 
"""
    chat = ChatOpenAI(model="gpt-4o",
                        max_tokens=4000
                        )

    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text":prompt},
                ]
            )
        ]
    )
    return msg.content

def generate_barchart(text):
    prompt=f"""
You are given the description of either table or the graph:{text}
You should write a code to draw a bar chart based on this data using matplotlib.
The drawn barchart should be saved as jpg file, it should contain barchart in the name.
Add plt.show() at the end of the script as well.
The output should contain just python code, dont put there anything like '''python. 
"""
    chat = ChatOpenAI(model="gpt-4o",
                        max_tokens=4000
                        )

    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text":prompt},
                ]
            )
        ]
    )
    return msg.content




