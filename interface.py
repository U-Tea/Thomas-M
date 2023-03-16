import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLineEdit, QVBoxLayout, QHBoxLayout
import os
import functions


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

        # create a horizontal layout for the second file button and its text box
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.button2)
        hbox2.addWidget(self.textbox2)

        # create a horizontal layout for the third file button and its text box
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.button3)
        hbox3.addWidget(self.textbox3)

        # add the three horizontal layouts and the print button to the vertical layout
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.printButton)

        # set the vertical layout as the main layout for the window
        self.setLayout(vbox)

        # connect the three file buttons to their corresponding file dialogs
        self.button1.clicked.connect(lambda: self.showFileDialog(self.textbox1, "Word Documents (*.docx)"));
        self.button2.clicked.connect(lambda: self.showFileDialog(self.textbox2, "Pdf Documents (*.pdf)"));
        self.button3.clicked.connect(lambda: self.showFileDialog(self.textbox3, "Word Documents (*.docx)"));

        #set geometry of the window
        self.setGeometry(100, 100, 500, 200)

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
        old_text = "Original File Name"
        translatedFile_path = self.textbox1.toolTip()
        originalFile_path = self.textbox2.toolTip()
        certificateFile_path = self.textbox3.toolTip()
        originalFile_Name = self.textbox2.text()

        self.textbox1.clear()
        self.textbox1.setToolTip('')
        self.textbox2.clear()
        self.textbox2.setToolTip('')
        self.textbox3.clear()
        self.textbox3.setToolTip('')
        self.printButton.setEnabled(False)

        functions.replace_text_in_docx(certificateFile_path, old_text, originalFile_Name);
        functions.word_to_pdf(translatedFile_path);
        functions.word_to_pdf(certificateFile_path);

        certificatePdf_path = os.path.splitext(certificateFile_path)[0] + '.pdf'
        translatedPdf_path = os.path.splitext(translatedFile_path)[0] + '.pdf'

        functions.combine_pdfs(translatedPdf_path, originalFile_path, certificatePdf_path);


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileDialogs = FileDialogs()
    fileDialogs.show()
    sys.exit(app.exec_())
