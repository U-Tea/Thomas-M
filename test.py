import os

file2  = "C:/Users/U-Tea/Documents/Upwork/Thomas M/MCC_Certificate of Accuracy_TEP - EN-CA template_TEP.docx"
file2_name = os.path.splitext(os.path.basename(file2))[0]
directory = os.path.dirname(file2)
output_name = f'{directory}/{file2_name} Final.pdf'

with open(output_name, 'wb') as f:
    print(output_name)

print(file2_name, directory, output_name);