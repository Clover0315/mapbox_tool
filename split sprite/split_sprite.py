# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PIL import Image
import os
import json

class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setModal(False)
        Dialog.resize(402, 115)
        self.output = QtWidgets.QPushButton(Dialog)
        self.output.setEnabled(True)
        self.output.setGeometry(QtCore.QRect(210, 10, 191, 51))
        self.output.setObjectName("output")
        self.select = QtWidgets.QPushButton(Dialog)
        self.select.setGeometry(QtCore.QRect(0, 10, 201, 51))
        self.select.setObjectName("select")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 80, 261, 24))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(307, 80, 91, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(0, 70, 401, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(Dialog)
        self.select.clicked.connect(self.selectFiles)#select sprite.png and sprite.json
        self.output.clicked.connect(self.outputFile)#output pieces images
        self.dirPath=None #file direction path,please makesure that it contains both sprite.png and sprite.json

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Split Sprite"))
        self.output.setText(_translate("Dialog", "output"))
        self.select.setText(_translate("Dialog", "select sprite"))
        self.label.setText(_translate("Dialog", "path:"))
    
    #####select sprite.png and sprite.json
    def selectFiles(self):
        dirPath = QFileDialog.getExistingDirectory(self,
                                                    "choose a direction where contains both json and png",
                                                    "C:/")
        self.dirPath=dirPath
        self.label.setText("path:"+dirPath)
        self.progressBar.setValue(0)  # set progressBar


    #####output pieces images
    def outputFile(self):
        if self.dirPath:
            dirPath = self.dirPath
            imgPath = dirPath + '/sprite.png'
            jsonPath = dirPath + '/sprite.json'

            if os.path.exists(imgPath):
                if os.path.exists(jsonPath):
                    load_f = open(jsonPath, 'r', encoding='utf-8')
                    spriteObj = json.load(load_f)

                    img_num=len(spriteObj.keys())#get the num of pieces
                    i=0
                    im = Image.open(imgPath)
                    for key, value in spriteObj.items():
                        fileName=str(key)#get the name of png
                        _width=value['width']#get width of png
                        _height=value['height']#get height of png
                        y=value['y']#get y position of png
                        x=value['x']#get x position of png


                        box = (x, y,x+_width,y+_height)
                        #print(im_crop.size, im_crop.mode)
                        target = Image.new('RGBA', (_width, _height))  # new a image for result
                        target.paste(im.crop(box))
                        target.save( dirPath + '/'+fileName + '.png', quality=100)

                        i+=1
                        self.label.setText(str(i)+':'+fileName)
                        self.progressBar.setValue(i/img_num*100)#set progressBar

                    print('success!you can get the result in:',dirPath)
                    self.label.setText('success!you can get the result in:'+dirPath)

                else:
                    print('cant find sprite.json in ',dirPath)
                    self.label.setText('cant find sprite.json in '+dirPath)
            else:
                print('cant find sprite.png in ', dirPath)
                self.label.setText('cant find sprite.png in '+ dirPath)

        else:
            print('please choose a direction first! ')
            self.label.setText('please choose a direction first! ')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

