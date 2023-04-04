import requests
import json
my_file = open("file.txt", "w") 
def ocr_space_file(filename, overlay=False, api_key='K87340094688957', language='rus'):
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

test = ocr_space_file(filename='C:/test_photo/x1.png', language='rus')
result = json.loads(test)
parsed_results = result.get("ParsedResults")[0]
text_detected = parsed_results.get("ParsedText")
print(text_detected)