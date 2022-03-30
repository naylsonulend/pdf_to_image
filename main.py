import os
from pathlib import Path
import fitz
from PyPDF2 import PdfFileWriter, PdfFileReader
import img2pdf


def convert_file(before_dir, after_dir, file_name):
    file_name = file_name.replace("/", "")
    input_pdf = Path(f"{before_dir}/{file_name}")
    output_path = Path(f"{after_dir}/{file_name}")
    output_pdf = open(output_path, "wb")

    pdf_reader = PdfFileReader(open(input_pdf, 'rb'))
    pdf_writer = PdfFileWriter()

    last_page = pdf_reader.numPages-1

    for pageNum in range(last_page):
        pageObj = pdf_reader.getPage(pageNum)
        pdf_writer.addPage(pageObj)

    doc = fitz.open(input_pdf)
    page = doc[last_page]
    image_path = f"{after_dir}/temp/image"
    zoom = 1.5
    mat = fitz.Matrix(zoom, zoom)
    image = page.get_pixmap(matrix=mat, dpi=100)
    image.save(image_path)

    pdf_path = f"{after_dir}/temp/{page.number}-temp.pdf"

    pdf_bytes = img2pdf.convert(image_path)
    file_temp = open(pdf_path, "wb")
    file_temp.write(pdf_bytes)
    file_temp.close()

    pdf_reader = PdfFileReader(open(pdf_path, "rb"))
    new_page = pdf_reader.getPage(0)
    pdf_writer.addPage(new_page)

    temp_files.append(pdf_path)

    pdf_writer.write(output_pdf)
    output_pdf.close()
    os.remove(image_path)


def main():
    current_dir = os.getcwd()

    try:
        before_dir = os.mkdir(current_dir+"/PDF_ANTES")
    except:
        before_dir = current_dir+"/PDF_ANTES"

    try:
        after_dir = os.mkdir(current_dir+"/PDF_DEPOIS")
    except:
        after_dir = current_dir+"/PDF_DEPOIS"

    try:
        os.mkdir(after_dir+"/temp/")
    except:
        ...

    dir_list = os.listdir(current_dir+"/PDF_ANTES")

    for file_name in dir_list:
        print("Convertendo... "+file_name)
        convert_file(before_dir, after_dir, file_name)


temp_files = []
main()

for t_path in temp_files:
    try:
        os.remove(t_path)
    except:
        ...
