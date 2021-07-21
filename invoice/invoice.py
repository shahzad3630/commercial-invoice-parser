import os, re
import numpy as np
import io
from PIL import Image
import traceback
from tqdm.notebook import tqdm

import os, re
import numpy as np
import io
from PIL import Image
import traceback

import gc
import pytesseract
from wand.image import Image as wi
from .invoice_fields import *

# ************************************************


def extract_text_from_image(doc_path):
    # extract text from the file
    #
    # INPUT: 
    #        doc_path : path of invoice document
    # OUTPUT:
    #       list of texts
    
    pdf=wi(filename=doc_path, resolution=300)
    pdf_img=pdf.convert('jpg')
    img_blob_list=[]
    text_list=[]

    for img in pdf_img.sequence:
        page=wi(image=img)
        img_blob_list.append(page.make_blob('jpg'))

    for blob in img_blob_list:
        im=Image.open(io.BytesIO(blob))
        text=pytesseract.image_to_string(im,lang='eng').strip()
        
        if len(text)==0:
            continue
        text_list.append(text)
        
    return text_list

#  *************************************************

class Invoice(Invoice_Number, Invoice_Date, Invoice_Amt, Invoice_Issuer):
    # class to get invoice fileds from invoice document
    #       whether pdf or image.
    # Get API will give corresponding field it calls for.
    # It will return the required field or return empty list,
    #       if no valid field is detected.
    
    def __init__(self, doc_path):
        # doc_path: invoice pdf or image
        
        Invoice_Number.__init__(self)
        Invoice_Date.__init__(self)
        Invoice_Amt.__init__(self)
        Invoice_Issuer.__init__(self)
        
        self.doc_path=doc_path
        print("pytesseract text extraction operation going ...")
        self.pages_text_list=extract_text_from_image(doc_path)
        print("text extraction Done")
        
        
    def get_invoice_no(self):
        return self.get_invoice_no_from_pages(self.pages_text_list)
    
    
    def get_invoice_date(self):
        return self.get_invoice_date_from_pages(self.pages_text_list)
        
        
    def get_invoice_amount(self):
        return self.get_invoice_amount_from_pages(self.pages_text_list)
    
    
    def get_invoice_issuer(self):
        return self.get_invoice_issuer_from_pages(self.pages_text_list)
    
    
