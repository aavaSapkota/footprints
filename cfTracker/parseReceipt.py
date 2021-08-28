import csv
from google.cloud import vision
import io

FOODS = set()

with open('../data/aliases.csv', mode='r') as f:
    csvFile = csv.reader(f)
    for lines in csvFile:
        FOODS.update(lines)

def is_registered(name):
    return name in FOODS

#FOODS.add("OCN SPRY JCE")

def parse_receipt(img_bytes):
    client = vision.ImageAnnotatorClient()

    # with io.open(receipt_path, 'rb') as image_file:
    #   content = image_file.read()

    vision_img = vision.Image(content=img_bytes)
    response = client.text_detection(image=vision_img)

    detected_text = response.text_annotations
    store_name = detected_text[1].description.strip()

    parsed_text = []
    IGNORE_CODES = ["FB"]
    CLEAR_CODES = ["TR#", "ST#"]
    STOP_CODES = ["SUBTOTAL"]

    # filter text
    for text in detected_text:
        descp = text.description.strip()
        
        if descp in CLEAR_CODES: 
            parsed_text = []
            continue
        if descp in IGNORE_CODES: continue
        if descp.upper() in STOP_CODES: break
        if len(descp) <= 1: continue
        if is_num(descp) or is_num(descp.replace("O","0")): continue
        
        node = {}
        node["text"] = text.description
        node["bounds"] = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        parsed_text.append(node)


    # get product names
    products = {}
    LEN = len(parsed_text)

    # todo: make this not o(n^2)
    for ind in range(LEN):
        if "taken" in parsed_text[ind]: continue
        curr = parsed_text[ind]
        y_bnd = parsed_text[ind]["bounds"][0][1]
        phrase = parsed_text[ind]["text"]
        
        for j in range(ind+1,LEN):
            if parsed_text[j]["bounds"][0][1] - y_bnd < 5:
                phrase += " " + parsed_text[j]["text"]
                parsed_text[j]["taken"] = True
            else: break
        phrase = phrase.strip()
        if is_registered(phrase):
            if phrase in products:
                products[phrase] += 1
            else:
                products[phrase] = 1

    return {
        "items": products,
        "store": store_name
    }


'''
items: {
    "name": quantity,
    "thing": 1,
    "ting": 2,
}
'''
