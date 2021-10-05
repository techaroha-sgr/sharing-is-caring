import pytesseract
import pandas as pd
from pdf2image import convert_from_path
from pytesseract import Output
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

custom_oem_psm_config = r'--oem 1 --psm 6 -l eng'

pdf_filepath='YOUR_FILENAME.pdf'

pages = convert_from_path(pdf_filepath, dpi=300)
output_dir = os.path.dirname(pdf_filepath)

counter = 0

# SAVE IMAGE PAGES
for page in pages:

    out_filepath = os.path.join("page_" + str(counter) + ".jpg")
    page.save(out_filepath, 'JPEG')
    counter = counter + 1  # Increment the counter to update filename
    continue


# RAW IMAGE PROCESSING CV2
image_file = "page_0.jpg"
img = cv2.imread(image_file)

d = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# DISPLAY AND SAVE IMAGE
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("page_0_cv2_map.png",img);

# SAVE TESSERACT OCR EXTRACTED DATA WITH COORDINATES
tsv_image = 'tessdata_output.tsv'
tsv_data = pytesseract.image_to_data(image_file, config=custom_oem_psm_config, lang='eng')

with open(tsv_image, 'wt', encoding='utf-8') as file:
    file.write(tsv_data)

# END ------- 
