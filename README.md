# commercial-invoice-parser

The commercial-invoice-parser parses a commercial invoice document either in pdf or image format to give invoice number, date, amount and its issuer.

It uses pytesseract to extract the text from the document and produces the values and names after parsing.

This package works on <b>english</b> language invoices


## software and modules installation

<b>tesseract installation</b><br>
sudo apt-get install tesseract-ocr<br>
pip install pytesseract<br>

<b>wand and imagewick installation</b><br>
pip install Wand<br>
sudo apt-get install libmagickwand-dev<br>

sudo apt-get install build-essential checkinstall && sudo apt-get build-dep imagemagick -y<br>
sudo wget http://www.imagemagick.org/download/ImageMagick.tar.gz<br>
tar -xzvf ImageMagick.tar.gz<br>

cd ImageMagick-[VERSION]<br>
./configure<br>
make clean<br>
make<br>
sudo checkinstall<br>
sudo ldconfig /usr/local/lib<br>
cd ..

<b>ghostscript installation</b><br>
sudo apt install ghostscript<br>

## Text extraction

Tesseract is an OCR engine, which on accepting image and pdf files, extracts the text and returns string of 
alpha-numeric characters along with other characters present in the given language.

This project takes an image or pdf that is an invoice. The system takes the input and extracts text. After processing, 
required fields are returned as output like invoice date, amount etc.

Below is an invoice that is to be parsed.
<br>
<hr/>

![download (1)](https://user-images.githubusercontent.com/87579053/138683429-56557ac6-e8f1-4449-859c-ffc704cc0c45.png)

<hr/>

The above invoice has encircled marks. These have been marked to assist others to what fields are to be looked for and for
demonstration purpose only. These features are to be extracted and parsed from the invoices after passing them to the system

