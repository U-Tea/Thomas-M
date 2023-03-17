import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
import os
from PyQt5.QtCore import Qt
import functions
from datetime import datetime
from PyQt5 import QtGui


class FileDialogs(QWidget):
    def __init__(self):
        super().__init__()

        # create three file buttons and their corresponding text boxes
        self.button1 = QPushButton("Select Translated File")
        self.textbox1 = QLineEdit()
        self.button2 = QPushButton("Select Original File")
        self.textbox2 = QLineEdit()
        self.button3 = QPushButton("Select Certificate File")
        self.textbox3 = QLineEdit()
        self.button4 = QPushButton("Name")
        self.textbox4 = QLineEdit()

        # create a button to print all file paths
        self.printButton = QPushButton("Combine")
        self.printButton.clicked.connect(self.printFilePaths)
        self.printButton.setEnabled(False)

        
        

        # create a vertical layout for the window
        vbox = QVBoxLayout()

        # create a horizontal layout for the first file button and its text box
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.button1)
        hbox1.addWidget(self.textbox1)
        self.button1.setFixedSize(130, 30)

        # create a horizontal layout for the second file button and its text box
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.button2)
        self.button2.setFixedSize(130, 30)
        hbox2.addWidget(self.textbox2)

        # create a horizontal layout for the third file button and its text box
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.button3)
        hbox3.addWidget(self.textbox3)
        self.button3.setFixedSize(130, 30)

        #provide base path for template file
        if os.path.exists("path.txt"):
            with open("path.txt", 'r') as nm:
                path = nm.read();
                self.textbox3.setText(os.path.basename(path));
                self.textbox3.setToolTip(path)

        #add textbox for name
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.button4)
        hbox4.addWidget(self.textbox4)
        self.button4.setFixedSize(130, 30)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.printButton);

        self.printButton.setFixedSize(260, 30)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.printButton.setFont(font)

        #add Name if file exists
        if os.path.exists("name.txt"):
            with open("name.txt", 'r') as nm:
                name = nm.read();
                self.textbox4.setText(name);
        

        # add the three horizontal layouts and the print button to the vertical layout
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        
        hbox5.setAlignment(Qt.AlignCenter)
        vbox.setAlignment(Qt.AlignCenter)
        

        # set the vertical layout as the main layout for the window
        self.setLayout(vbox)


        # connect the three file buttons to their corresponding file dialogs
        self.button1.clicked.connect(lambda: self.showFileDialog(self.textbox1, "Word Documents (*.docx)"));
        self.button2.clicked.connect(lambda: self.showFileDialog(self.textbox2, "Pdf Documents (*.pdf)"));
        self.button3.clicked.connect(lambda: self.showFileDialog(self.textbox3, "Word Documents (*.docx)"));

        #set geometry of the window
        self.resize(500, 200)

    def showFileDialog(self, textbox, fileType):
        # show a file dialog and set the selected file name as the text of the corresponding text box
        filepath, _ = QFileDialog.getOpenFileName(self, "Open file", "", fileType)
        filename = os.path.basename(filepath)
        textbox.setText(filename)

        # set the selected file path as the tooltip for the corresponding text box
        textbox.setToolTip(filepath)

        if not filepath:
            textbox.clear()

        # enable the print button if all three text boxes have a file name
        if self.textbox1.text() and self.textbox2.text() and self.textbox3.text():
            self.printButton.setEnabled(True)
        else:
            self.printButton.setEnabled(False)

    def printFilePaths(self):
        filenameText = "Original File Name"
        dateText = "{{date}}"
        nameText = "{{name}}"
        translatedFile_path = self.textbox1.toolTip()
        originalFile_path = self.textbox2.toolTip()
        certificateFile_path = self.textbox3.toolTip()
        originalFile_Name = self.textbox2.text()
        name_in_box = self.textbox4.text()
        new_certificateFile_path = os.path.dirname(originalFile_path) +"/"+ self.textbox3.text();
        

        if os.path.exists("name.txt"):
            with open("name.txt", 'r') as nm:
                name = nm.read();
            if name_in_box != name:
                with open("name.txt", 'w') as f:
                    f.write(name_in_box)
        else:
            with open("name.txt", 'w') as f:
                    f.write(name_in_box)
            
        """checking for file path and saving if not present"""
        if os.path.exists("path.txt"):
            with open("path.txt", 'r') as nm:
                certificateFile_path_in_txt = nm.read();
            if certificateFile_path != certificateFile_path_in_txt:
                with open("path.txt", 'w') as f:
                    f.write(certificateFile_path)
        else:
            with open("path.txt", 'w') as f:
                    f.write(certificateFile_path)

                

        functions.copy_file(certificateFile_path, new_certificateFile_path);

        self.textbox1.clear()
        self.textbox1.setToolTip('')

        self.textbox3.clear()
        self.textbox3.setToolTip('')
        self.printButton.setEnabled(False)


        functions.replace_text_in_docx(new_certificateFile_path, filenameText, os.path.splitext(os.path.basename(originalFile_path))[0]);
        functions.replace_text_in_docx(new_certificateFile_path, dateText, datetime.today().strftime('%B %d, %Y'));
        functions.replace_text_in_docx(new_certificateFile_path, nameText, name_in_box);

        """test"""

        functions.word_to_pdf(translatedFile_path);
        functions.word_to_pdf(certificateFile_path);

        certificatePdf_path = os.path.splitext(new_certificateFile_path)[0] + '.pdf'
        translatedPdf_path = os.path.splitext(translatedFile_path)[0] + '.pdf'

        functions.combine_pdfs(translatedPdf_path, originalFile_path, certificatePdf_path);

        functions.delete_files(certificatePdf_path)
        functions.delete_files(translatedPdf_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileDialogs = FileDialogs()
    fileDialogs.show()
    sys.exit(app.exec_())
