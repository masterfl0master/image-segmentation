#!/usr/bin/env python
import cv

from PyQt4 import QtCore, QtGui
import kmeans
import meanshift
import cv


class RenderArea(QtGui.QWidget):
    def __init__(self, path, parent=None):
        super(RenderArea, self).__init__(parent)

        self.setBackgroundRole(QtGui.QPalette.Base)

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(100, 100)

class Window(QtGui.QWidget):

    def __init__(self):
        super(Window, self).__init__()

        browseButton = self.createButton("&Browse...", self.browse)
        browseButton2 = self.createButton("&Show Output...", self.browse2)
        segmentButton = self.createButton("&Segment...", self.segment)
        directoryLabel = QtGui.QLabel("Input Image:")
        outputImageLabel = QtGui.QLabel("Output Image:")
        self.algorithmComboBox = QtGui.QComboBox()
        self.algorithmComboBox.addItem("K-means")
        self.algorithmComboBox.addItem("Mean Shift")

        algorithm = QtGui.QLabel("&Algorithm:")
        algorithm.setBuddy(self.algorithmComboBox)

        self.featureComboBox = QtGui.QComboBox()
        self.featureComboBox.addItem("Intensity")
        self.featureComboBox.addItem("Intensity and pixel coordinates")
        self.featureComboBox.addItem("RGB color")
        self.featureComboBox.addItem("YUV color")
        self.featureComboBox.addItem("Leung-Malik")
        self.featureComboBox.addItem("Invariant LM")
        self.featureComboBox.addItem("PCA")
        feature = QtGui.QLabel("&Feature:")
        feature.setBuddy(self.featureComboBox)
        self.userpath = QtGui.QLineEdit("../test images/single object/189080.jpg")
        self.userpath2 = QtGui.QLineEdit()
        self.kText = QtGui.QLineEdit("3")

        self.kLabel = QtGui.QLabel("&K:")
        self.kLabel.setBuddy(self.kText)

        self.iterationsText = QtGui.QLineEdit("200")
        self.epsilonText = QtGui.QLineEdit("0.01")

        self.iterationsLabel = QtGui.QLabel("&Number Of Iterations:")
        self.iterationsLabel.setBuddy(self.iterationsText)

        self.epsilonLabel = QtGui.QLabel("&Epsilon:")
        self.epsilonLabel.setBuddy(self.epsilonText)

        self.featureComboBox.activated.connect(self.featureChanged)
        self.algorithmComboBox.activated.connect(self.algorithmChanged)


        topLayout = QtGui.QGridLayout()

        self.mainLayout = QtGui.QGridLayout()
        self.mainLayout.addLayout(topLayout, 0, 0, 1, 4)
        self.mainLayout.addWidget(algorithm, 1, 0)
        self.mainLayout.addWidget(self.algorithmComboBox, 1, 1, 1, 3)
        self.mainLayout.addWidget(feature, 2, 0)
        self.mainLayout.addWidget(self.featureComboBox, 2, 1)
        self.mainLayout.addWidget(self.kLabel, 4, 0)
        self.mainLayout.addWidget(self.kText, 4, 1, 1, 3)
        self.mainLayout.addWidget(self.iterationsLabel, 5, 0)
        self.mainLayout.addWidget(self.iterationsText, 5, 1, 1, 3)
        self.mainLayout.addWidget(browseButton, 3, 2)
        self.mainLayout.addWidget(directoryLabel, 3, 0)
        self.mainLayout.addWidget(self.userpath, 3, 1)
        self.mainLayout.addWidget(self.epsilonText, 6, 1)
        self.mainLayout.addWidget(self.epsilonLabel, 6, 0)
        self.mainLayout.addWidget(segmentButton, 7, 1)
        self.mainLayout.addWidget(outputImageLabel, 8, 0)
        self.mainLayout.addWidget(self.userpath2, 8, 1)
        self.mainLayout.addWidget(browseButton2, 8, 2)
        self.setLayout(self.mainLayout)

        self.featureChanged()
        self.algorithmChanged()

        self.setWindowTitle("Segmentation")


    def browse(self):
        filePath = QtGui.QFileDialog.getOpenFileName(self, "Find Files",
                QtCore.QDir.currentPath())
        self.userpath.setText(filePath)

    def segment(self):
    	algorithm = self.algorithmComboBox.currentText()
        imgPath = str(self.userpath.text())
        index = self.featureComboBox.currentIndex()
        features = ["INTENSITY","INTENSITY+LOC","RGB","YUV","LM",
                "ILM","PCA"]
        if algorithm == "K-means":
            k = int(self.kText.text())
            iterations = int(self.iterationsText.text())
            epsilon = float(self.epsilonText.text())
            print imgPath,index,k,iterations,epsilon
            org = cv.LoadImageM(imgPath)
            im = kmeans.kmeans(imgPath,features[index],k,iterations,epsilon)
            cv.ShowImage("original",org)
            cv.ShowImage("segmented",im)
        elif algorithm == "Mean Shift":
            if index == 4:
                QtGui.QMessageBox.information(self, 'Error',
                        'LM is not supported in mean shift')
                return
            print imgPath,features[index]
            org = cv.LoadImageM(imgPath)
            im = meanshift.meanshift(imgPath,features[index])
            cv.ShowImage("original",org)
            cv.ShowImage("segmented",im)


    def browse2(self):
        filePath = QtGui.QFileDialog.getOpenFileName(self, "Find Files",
                QtCore.QDir.currentPath())
        self.userpath2.setText(filePath)
        img = cv.LoadImageM(str(filePath))
        cv.NamedWindow("Output", 1) ;
        cv.ShowImage( "Output", img );

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Preferred)
        return comboBox

    def featureChanged(self):
        feature = self.featureComboBox.currentText()

    def algorithmChanged(self):
        algorithm = self.algorithmComboBox.currentText()
        if algorithm == "Mean Shift":
          self.kText.hide()
          self.kLabel.hide()
          self.iterationsText.hide()
          self.iterationsLabel.hide()
          self.epsilonLabel.hide()
          self.epsilonText.hide()
        elif algorithm == "K-means":
          self.kText.show()
          self.kLabel.show()
          self.iterationsText.show()
          self.iterationsLabel.show()
          self.epsilonLabel.show()
          self.epsilonText.show()

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
