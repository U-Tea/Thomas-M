"""all the functions"""
import os
import sys
import canvas
from docx import Document
from docx2pdf import convert
from PyPDF2 import PdfMerger, PdfReader

"""combine pdf"""
def combine_pdfs(file1, file2, file3):
    # Create a merger object
    merger = PdfMerger()

    # Open the two PDF files and add them to the merger object
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2, open(file3, 'rb') as f3:
        pdf1 = PdfReader(f1)
        pdf2 = PdfReader(f2)
        pdf3 = PdfReader(f3)
        merger.append(pdf1)
        merger.append(pdf2)
        merger.append(pdf3)

    # Create a file name for the combined PDF file
    file1_name = os.path.splitext(os.path.basename(file1))[0]
    output_name = f'{file1_name}.pdf'

    # Write the combined PDF file to disk
    with open(output_name, 'wb') as f:
        merger.write(f)

    return output_name





'''function to create pdf from word file'''




def word_to_pdf(input_file):
    # Convert the Word file to PDF using docx2pdf
    output_file = os.path.splitext(input_file)[0] + '.pdf'
    convert(input_file, output_file)

    # Remove the page numbers added by docx2pdf using reportlab
    with open(output_file, 'rb') as f:
        data = f.read()

    with open(output_file, 'wb') as f:
        canvas_obj = canvas.Canvas(f)
        canvas_obj.setFont("Helvetica", 9)
        page_width, page_height = canvas_obj._pagesize
        for page in canvas_obj.splitTextByLength(data, max_len=page_width*page_height):
            canvas_obj.showPage()
            canvas_obj.drawString(0, 0, page.decode("utf-8"))

    return output_file



"""replace text"""


def replace_text_in_docx(docx_path, replaceable_text, replacement_text):
    doc = Document(docx_path)
    for p in doc.paragraphs:
        if replaceable_text in p.text:
            inline = p.runs
            for i in range(len(inline)):
                if replaceable_text in inline[i].text:
                    text = inline[i].text.replace(replaceable_text, replacement_text)
                    inline[i].text = text
    doc.save(docx_path)
