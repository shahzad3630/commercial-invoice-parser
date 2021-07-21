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
