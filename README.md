# commercial-invoice-parser

The commercial-invoice-parser parses a commercial invoice document either in pdf or image format to give invoice number, date, amount and its issuer.

It uses pytesseract to extract the text from the document and produces the values and names after parsing.

This package works on <b>english</b> language invoices


## software and modules installation

<i>tesseract installation</i>
sudo apt-get install tesseract-ocr
pip install pytesseract

<i>wand and imagewick installation</i>
pip install Wand
sudo apt-get install libmagickwand-dev
sudo apt-get install build-essential checkinstall && sudo apt-get build-dep imagemagick -y
sudo wget http://www.imagemagick.org/download/ImageMagick.tar.gz
tar -xzvf ImageMagick.tar.gz

cd ImageMagick-[VERSION]
./configure
make clean
make
sudo checkinstall
sudo ldconfig /usr/local/lib
cd ..

<i>ghostscript installation</i>
sudo apt install ghostscript
