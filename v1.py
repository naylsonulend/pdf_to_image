import os
from pdf2image import convert_from_path
from pathlib import Path


def convert_file(before_dir, after_dir, file_name):
    file_name = file_name.replace("/", "")
    input_pdf = Path(f"{before_dir}/{file_name}")
    images = convert_from_path(input_pdf)

    output_path = Path(f"{after_dir}/{file_name}")
    output_pdf = images[0].convert("RGB")
    output_pdf.save(output_path, save_all=True, append_images=images[1:])


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
