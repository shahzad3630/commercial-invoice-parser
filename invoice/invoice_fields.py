import os, re
import numpy as np
import io
from PIL import Image
import traceback


def has_digit(string):
    # check whether string has digit
    
    for i in range(len(string)):
        if string[i].isdigit():
            return True
    return False


# ************************************************

class Invoice_Number():
    
    def __init__(self):
        self.no_pattern="invoice[ ]*(number|no[ ]*\.?)?[ ]*:?[ ]*([A-Za-z0-9]+(\-[A-Za-z0-9]+)*)"
        
        
    def parse_invoice_no(self, line):
        txt_low=line.lower()
        match=re.search(self.no_pattern, txt_low)
        
        if match:
            substr=match.group(2).upper()
            
            if substr=="NUMBER" or substr=="NO":
                return (-1,-1)

            if not has_digit(substr):
                return (-1,-1)

            return (1,substr)   # (status, invoice_no)

        return (-1,-1)        
        

    def get_invoice_no_from_page_text(self, page_txt):
        for line in page_txt.split("\n"):
            line=line.strip()

            if len(line)==0:
                continue

            (status,num)=self.parse_invoice_no(line)
            if status!=-1:
                return num

        return []

    
    def get_invoice_no_from_pages(self, pages_text_list):
        # parse each page text and return invoice no.
        #
        # INPUT :
        #        pages_text_list : pytesseract per page text list
        # OUTPUT:
        #        invoice number ; if detected else empty list
        
        
        for page in pages_text_list:
            res=self.get_invoice_no_from_page_text(page)
            if len(res)==0:
                continue
            else:
                return res
            
        return []


class Invoice_Date():
    
    def __init__(self):
        date_base="(date|date[ ]*of[ ]*issue|date[ ]*printed)?[ ]*:?[ ]*"
        month_re_1="(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
        month_re_2="(january|february|march|april|may|june|july|august|september|october|november|december)"

        p1=date_base+"([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9])"
        p2=date_base+"([0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9])"
        p3=date_base+"([0-9][0-9]\-[0-9][0-9]\-[0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9])"

        p4=date_base+"(({}|{})[ ]*\.?[ ]*[0-9]+[a-z]*[ ]*,[ ]*[0-9][0-9][0-9][0-9])".format(month_re_1,month_re_2)

        self.date_pattern_ll=[p1,p2,p3,p4]        
                
        
    def parse_invoice_date(self, line):
        txt_low=line.lower()
        for pattern in self.date_pattern_ll:
            match=re.search(pattern,txt_low)
            if match:
                substr=match.group(2).upper()        
                return (1,substr)   # (status, invoice_date)

        return (-1,-1)
        
        
    def get_invoice_date_from_page_text(self, page_txt):
        result=[]
        for line in page_txt.split("\n"):
            line=line.strip()
            if len(line)==0:
                continue

            (status,num)=self.parse_invoice_date(line)
            if status!=-1:
                return num

        return []
        
        
    def get_invoice_date_from_pages(self, pages_text_list):
        result=[]
        for page in pages_text_list:
            res=self.get_invoice_date_from_page_text(page)
            if len(res)==0:
                continue
            else:
                return res

        return []


class Invoice_Amt():
    
    def __init__(self):
        base="(([0-9],|[0-9][0-9],)?([0-9][0-9],|([0-9][0-9][0-9],))?[0-9][0-9][0-9]\.[0-9][0-9]?[0-9]?)"
        pre="($|£|€|usd|inr|)?[ ]*"
        pattern=pre+base
        
        self.amt_pattern_ll=[pattern]        
        
        
    def parse_amount(self, line):
        candidate=[]

        txt_low=line.lower()
        if " kg" in txt_low:  # line has weight not amt
            return (-1,0)
        
        for pattern in self.amt_pattern_ll:
            match_all=re.findall(pattern, txt_low)
            for match in match_all:
                substr=match[1]  
                candidate.append(substr)    

        if len(candidate)!=0:
            return (1,candidate)   # (status, amount candidate)

        return (-1,0)


    def get_invoice_amt_from_page_text(self, page_txt):
        result=[]
        for line in page_txt.split("\n"):
            line=line.strip()
            if len(line)==0:
                continue

            (status,candidate)=self.parse_amount(line)
            if status!=-1:
                result+=candidate

        return result


    def select_amt_from_candidate(self, candidates):
        if len(candidates)==0:
            return (-1,-1)

        can_ll=[]
        for ss in candidates:
            try:
                num=ss.rpartition(".")[0].replace(",","")
                dec="."+ss.rpartition(".")[-1].replace(",","")
                num=float(num)
                dec=float(dec)
                num=num+dec
                can_ll.append(num)
            except:
                traceback.print_exc()
                pass

        can_ll=sorted(can_ll, reverse=True)
        
        if len(can_ll)==0:
            # if parsing error in try blk and no valid candidate
            return (-2,-1)

        return (1,can_ll[0])

    
    def get_invoice_amount_from_pages(self, pages_text_list):
        candidates=[]
        for page in pages_text_list:
            res=self.get_invoice_amt_from_page_text(page)
            if len(res)==0:
                continue
            else:
                candidates+=res

        candidates=np.unique(candidates).tolist()
        (status, amount)=self.select_amt_from_candidate(candidates)
        
        if status!=1:
            return []
        
        return amount
    

class Invoice_Issuer():
    
    def __init__(self):
        pass
    
    
    def get_invoice_issuer_from_page_text(self, page_txt):
        for line in page_txt.split("\n"):
            line=line.strip()
            if len(line)<=2:
                continue

            return line

        return []

    
    def get_invoice_issuer_from_pages(self, pages_text_list):
        for page in pages_text_list:
            inv_issuer=self.get_invoice_issuer_from_page_text(page)
            return inv_issuer

        return []

