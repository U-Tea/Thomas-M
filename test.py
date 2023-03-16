import functions
import os

file1_path = "C:/Users/U-Tea/Documents/Upwork/Thomas M/Diplome-dhematologie-Original.pdf"
file2_path = "C:/Users/U-Tea/Documents/Upwork/Thomas M/English (Canada)_Diplome-dhematologie-Original.pdf"

wordfile_path = "C:/Users/U-Tea/Documents/Upwork/Thomas M/English (Canada)_Diplome-dhematologie-Original.docx"

replacement_file = "C:/Users/U-Tea/Documents/Upwork/Thomas M/MCC_Certificate of Accuracy_TEP - EN-CA template_TEP.docx"
replaceable_text = "Original File Name"
replacement_text = os.path.splitext(os.path.basename(file1_path))[0]
functions.replace_text_in_docx(replacement_file, replaceable_text, replacement_text)
