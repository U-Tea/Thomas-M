import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLineEdit, QVBoxLayout, QHBoxLayout
import os

class FileDialogs(QWidget):
    def __init__(self):
        super().__init__()

        # create three file buttons and their corresponding text boxes
        self.button1 = QPushButton("Open File 1")
        self.textbox1 = QLineEdit()
        self.button2 = QPushButton("Open File 2")
        self.textbox2 = QLineEdit()
        self.button3 = QPushButton("Open File 3")
        self.textbox3 = QLineEdit()

        # create a button to print all file paths
        self.printButton = QPushButton("Print File Paths")
        self.printButton.clicked.connect(self.printFilePaths)

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
        self.button1.clicked.connect(lambda: self.showFileDialog(self.textbox1))
        self.button2.clicked.connect(lambda: self.showFileDialog(self.textbox2))
        self.button3.clicked.connect(lambda: self.showFileDialog(self.textbox3))

    def showFileDialog(self, textbox):
        # show a file dialog and set the selected file name as the text of the corresponding text box
        filepath, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;Text Files (*.txt)")
        filename = os.path.basename(filepath)
        textbox.setText(filename)

        # set the selected file path as the tooltip for the corresponding text box
        textbox.setToolTip(filepath)

    def printFilePaths(self):
        # print the file paths of all three files
        file1_path = self.textbox1.toolTip()
        file2_path = self.textbox2.toolTip()
        file3_path = self.textbox3.toolTip()
        print("File 1 path:", file1_path)
        print("File 2 path:", file2_path)
        print("File 3 path:", file3_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileDialogs = FileDialogs()
    fileDialogs.show()
    sys.exit(app.exec_())
