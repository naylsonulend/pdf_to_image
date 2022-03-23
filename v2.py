import os
from pathlib import Path
import fitz
from PyPDF2 import PdfFileWriter, PdfFileReader
import img2pdf


def convert_file(before_dir, after_dir, file_name):
    file_name = file_name.replace("/", "")
    input_pdf = Path(f"{before_dir}/{file_name}")
    output_pdf = Path(f"{after_dir}/{file_name}".replace(" ", "_"))

    pdf_writer = PdfFileWriter()

    doc = fitz.open(input_pdf)
    for page in doc:
        image_path = f"{after_dir}/temp"
        zoom = 3
        mat = fitz.Matrix(zoom, zoom)
        image = page.get_pixmap(matrix=mat)
        image.save(image_path)

        pdf_path = f"{after_dir}/{page.number}-temp.pdf"

        pdf_bytes = img2pdf.convert(image_path)
        file_temp = open(pdf_path, "wb")
        file_temp.write(pdf_bytes)
        file_temp.close()
        os.remove(image_path)

        pdf_reader = PdfFileReader(open(pdf_path, "rb"))
        new_page = pdf_reader.getPage(0)
        pdf_writer.addPage(new_page)

        os.remove(pdf_path)

    pdf_writer.write(open(output_pdf, "wb"))


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

    dir_list = os.listdir(current_dir+"/PDF_ANTES")

    for file_name in dir_list:
        print("Convertendo... "+file_name)
        convert_file(before_dir, after_dir, file_name)


main()
