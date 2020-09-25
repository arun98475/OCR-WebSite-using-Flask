
from PIL import Image
import pytesseract
import cv2
import os

class TextExtract:
    counter = 0
    def __init__(self,img,prepocessor="thresh"):
        self.image = cv2.imread(img)
        self.prepocessor=prepocessor
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        if self.prepocessor == "thresh":
            gray = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        else :
            gray = cv2.medianBlur(gray, 3)
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        custom_oem_psm_config = r'--psm 6'
        text = pytesseract.image_to_string(Image.open(filename) , config=custom_oem_psm_config)
        os.remove(filename)
        TextExtract.counter+=1
        self.outputFile=f'temp/{img.rsplit("/")[1].rsplit(".")[0]}_editable({self.counter}).txt'
        output_file = open(self.outputFile,"w")
        output_file.write(text)
    def output_file_name(self):
        new_file = self.outputFile.rsplit('/')[1]
        return new_file
    
#TextExtract('sample.jpg')
