from glom import glom
import base64
import requests

def image_to_base64(image):
    return base64.b64encode(image).decode()

def fetch_image(url):
    return requests.get(url).content

def transform(results):
    return [
        {
            "id": glom(r, "id.videoId"),
            "image": image_to_base64(fetch_image(glom(r, "snippet.thumbnails.medium.url"))),
            "title": glom(r, "snippet.title"),
            "description": glom(r, "snippet.description")
        }
        for r in results
    ]