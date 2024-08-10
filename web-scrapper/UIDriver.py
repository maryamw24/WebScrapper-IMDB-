import sys
from tableModel import CustomTableModel
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime
from sortingAlgorithms import *
from sortingThread import SortingThread
from scrappingThread import ScrappingThread
from searchingAlgorithms import *
from scrapping import *
from MovieDL import MovieDL


class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        loadUi("main.ui", self)

        self.setWindowTitle('Cine Picker')
        self.setMinimumSize(1586, 1076)
        
        # Load movies from file
        #MovieDL.loadMovies('scrappingMovies.csv')

        # Columns headings for table
        self.columns = ["Title", "Year", "Certificate", "Duration",
                        "Genres", "Rating", "Description", "Director", "Votes"]

        # Attributes for combobox
        self.algorithmAttributes = {
            "Bubble Sort": ["Title", "Year", "Certificate", "Duration", "Genre", "Rating", "Description", "Director", "Votes"],
            "Selection Sort": ["Title", "Year", "Certificate", "Duration", "Genre", "Rating", "Description", "Director", "Votes"],
            "Insertion Sort": ["Title", "Year", "Certificate", "Duration", "Genre", "Rating", "Description", "Director", "Votes"],
            "Merge Sort": ["Title", "Year", "Certificate", "Duration", "Genre", "Rating", "Description", "Director", "Votes"],
            "Heap Sort": ["Title", "Year", "Certificate", "Duration", "Genre", "Rating", "Description", "Director", "Votes"],
            "Quick Sort": ["Title", "Year", "Certificate", "Duration", "Genre", "Rating", "Description", "Director", "Votes"],
            "Count Sort": ["Year", "Duration", "Votes"],
            "Radix Sort": ["Year", "Duration", "Votes"],
            "Bucket Sort": ["Year", "Duration", "Votes"],
            "Tim Sort": ["Title", "Year", "Certificate", "Duration", "Genre", "Rating", "Description", "Director", "Votes"],
            "Odd Even Sort": ["Title", "Year", "Certificate", "Duration", "Genre", "Rating", "Description", "Director", "Votes"],
            "Shell Sort": ["Title", "Year", "Certificate", "Duration", "Genre", "Rating", "Description", "Director", "Votes"]
        }

        self.image=self.MenuBodyContainer.findChild(QtWidgets.QWidget,'mainImgLbl')
        # Table View
        self.dataView = self.MenuBodyContainer.findChild(
            QtWidgets.QWidget, 'dataView')

        # StackedWidget
        self.sWidget = self.MenuBodyContainer.findChild(
            QtWidgets.QWidget, 'stackedWidget')

        # Time Label
        self.timeLabel = self.sWidget.findChild(QtWidgets.QLabel, 'timeLbl')

        # Bool that check if sorting is in progress
        self.isSorting = False
        self.sortingAttributes = []
        self.isMultilevel = False

        # Counter that counts time for sorting
        self.counter = 0

        # Seperate thread for sorting algorithm
        self.sortingThread = None

        # Seperate thread for scrapping algorithm
        self.scrappedData = []
        self.isScraping = False
        self.resumeScraping = False
        self.currentLink = ""
        self.currentIndex = 0

        # Bool for order of sort
        self.order = True

        # Timer Object
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateCounter)

        # Sorted Array
        self.sortedList = MovieDL.movies.copy()

        # Flag for compound Searching
        self.flag = False

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.home()
        self.homeBtn.clicked.connect(self.home)
        self.scrappingBtn.clicked.connect(self.scrapping)
        self.sortingBtn.clicked.connect(self.sorting)
        self.searchingBtn.clicked.connect(self.searching)

    def home(self):
        pic=QtGui.QPixmap('main.png')
        self.image.setPixmap(pic)
        self.image.show()
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.sWidget.hide()
        self.dataView.hide()

    def scrapping(self):
        self.image.hide()
        self.clearTable()
        self.sWidget.setCurrentIndex(0)
        self.sWidget.show()
        self.resetProgressBar
        startBtn = self.sWidget.findChild(QtWidgets.QWidget, 'startBtn')
        stopBtn = self.sWidget.findChild(QtWidgets.QWidget, 'stopBtn')
        pauseBtn = self.sWidget.findChild(QtWidgets.QWidget, 'pauseBtn')
        resumeBtn = self.sWidget.findChild(QtWidgets.QWidget, 'resumeBtn')
        startBtn.clicked.connect(self.startScrapping)
        resumeBtn.clicked.connect(self.resumeScrapping)
        pauseBtn.clicked.connect(self.pauseScrapping)
        stopBtn.clicked.connect(self.stopScrapping)
        self.dataView.show()

    def updateProgressBar(self):
        value = len(self.scrappedData)//10000
        progressBar = self.sWidget.findChild(QtWidgets.QWidget, 'progeressBar')
        moviesLoaded = self.sWidget.findChild(
            QtWidgets.QWidget, 'moviesLoadedlbl')
        moviesLoaded.setText(str(len(self.scrappedData))+" Movies Scrapped")
        if value<=100:
            progressBar.setValue(value)
        else:
            self.stopScrapping()

    def pauseScrapping(self):
        if self.isScraping and self.scrapingThread.isRunning():
            self.scrapingThread.terminate()
            self.scrapingThread.wait()
            self.isScraping = False

    def stopScrapping(self):
        if self.isScraping and self.scrapingThread.isRunning():
            self.scrapingThread.terminate()
            self.scrapingThread.wait()

        self.isScraping = False
        self.resumeScraping = False
        self.scrappedData.clear()
        self.resetProgressBar()

    def checkScrapping(self):
        genres = getGenres('genre.csv')
        if not self.resumeScraping:
            self.resetProgressBar()
            self.currentIndex = 0
            self.currentLink = genres[self.currentIndex]
            self.isScraping = True
            self.clearTable()
        else:
            self.isScraping = True
            self.currentIndex, self.currentLink = loadProgress("progress.csv")
        self.scrapingThread = None
        self.scrapingThread = ScrappingThread(
            self.currentIndex, self.currentLink)
        self.scrapingThread.scrapingIterationFinished.connect(
            self.handleScrapedData)

    def startScrapping(self):
        self.checkScrapping()
        self.scrapingThread.start()
        self.updateProgressBar()

    def resumeScrapping(self):
        if not self.isScraping:
            self.resumeScraping = True
            self.startScrapping()
        else:
            self.showPopup("Scrapping already in process")

    def resetProgressBar(self):
        progressBar = self.sWidget.findChild(QtWidgets.QWidget, 'progeressBar')
        progressBar.setValue(0)
        moviesLoaded = self.sWidget.findChild(
            QtWidgets.QWidget, 'moviesLoadedlbl')
        moviesLoaded.setText("0 Movies Scrapped")

    def handleScrapedData(self, scrappedData):
        self.scrappedData += scrappedData
        self.updateProgressBar()
        self.clearTable()
        self.loadTable(self.scrappedData)

    def sorting(self):
        self.image.hide()
        self.sWidget.setCurrentIndex(1)
        self.sWidget.show()
        self.dataView.show()
        self.loadTable(MovieDL.movies)
        s = self.sWidget.currentWidget()
        algorithmComboBox = s.findChild(QtWidgets.QComboBox, 'Algorithms')
        attributeComboBox = s.findChild(QtWidgets.QComboBox, 'Attributes')

        def updateAttribute():
            selectedAlgo = algorithmComboBox.currentText()
            attributeComboBox.clear()
            attributeComboBox.addItems(
                self.algorithmAttributes.get(selectedAlgo, []))

        updateAttribute
        algorithmComboBox.currentIndexChanged.connect(updateAttribute)
        multiLevel = s.findChild(QtWidgets.QPushButton, "MultiLevelBtn")
        multiLevel.clicked.connect(
            lambda: self.openDialogueBox(algorithmComboBox.currentText(), attributeComboBox.currentText()))

        sortBtn = s.findChild(QtWidgets.QPushButton, "sortBtn")
        sortBtn.clicked.connect(self.sortData)
        self.resetSortOrder()
        clearBtn = s.findChild(QtWidgets.QPushButton, "clearBtn")
        clearBtn.clicked.connect(self.resetDialogueBox)

    def sortData(self):
        if not self.isSorting:
            self.counter = 0
            self.updateCounter()
            if self.sWidget.findChild(QtWidgets.QRadioButton, 'ascendRBtn').isChecked():
                self.order = True
            if self.sWidget.findChild(QtWidgets.QRadioButton, 'descendRBtn').isChecked():
                self.order = False
            algo = self.sWidget.findChild(
                QtWidgets.QComboBox, 'Algorithms').currentIndex()
            if not self.sortingAttributes.__contains__(self.sWidget.findChild(
                    QtWidgets.QComboBox, 'Attributes').currentText().lower()):
                self.sortingAttributes.append(self.sWidget.findChild(
                    QtWidgets.QComboBox, 'Attributes').currentText().lower())
            attributes = [attribute.lower()
                          for attribute in self.sortingAttributes]
            # print(attributes)
            self.isSorting = True
            self.sortingThread = SortingThread(
                self.sortedList, attributes, self.order, algo)
            self.sortingThread.finished.connect(
                lambda: self.sortingFinished())
            self.sortingThread.start()
            self.timer.start(1000)
        else:
            self.showPopup('Sorting Under Progress!')

    def sortingFinished(self):
        self.isSorting = False
        self.timer.stop()
        self.sortingAttributes.clear()
        self.clearTable()
        self.loadTable(self.sortedList)

    def resetSortOrder(self):
        self.resetDialogueBox()
        self.sWidget.findChild(QtWidgets.QRadioButton,
                               'ascendRBtn').setChecked(True)

    def openDialogueBox(self, algorithm, attribute):
        dlg = QDialog()
        loadUi("MultiLevel.ui", dlg)
        dlg.attributeComboBox = dlg.findChild(
            QtWidgets.QComboBox, 'DialogueAttribute')
        dlg.attributeComboBox.clear()
        dlg.attributeComboBox.addItems(
            self.algorithmAttributes.get(algorithm, []))
        tableWidget = dlg.findChild(QtWidgets.QTableWidget, 'tableWidget')
        if len(self.sortingAttributes) > 1:
            pass
        else:
            self.sortingAttributes.clear()
        if attribute and attribute in self.algorithmAttributes.get(algorithm, []) and not self.sortingAttributes.__contains__(attribute.lower()):
            self.sortingAttributes.append(attribute.lower())

        AddBtn = dlg.findChild(QtWidgets.QPushButton, 'AddBtn')
        DeleteBtn = dlg.findChild(QtWidgets.QPushButton, 'DeleteBtn')
        tableWidget.horizontalHeader().ResizeMode(QHeaderView.Stretch)
        self.loadTableWidget(tableWidget)

        AddBtn.clicked.connect(lambda: self.addButton(dlg, tableWidget))
        DeleteBtn.clicked.connect(lambda: self.deleteButton(dlg, tableWidget))
        dlg.exec_()

    def loadTableWidget(self, tableWidget):
        tableWidget.setRowCount(len(self.sortingAttributes))
        for i, row in enumerate(self.sortingAttributes):
            tableWidget.setItem(i, 0, QTableWidgetItem(str(row).capitalize()))

    def addButton(self, dlg, table):
        comboBox = dlg.findChild(QtWidgets.QComboBox, 'DialogueAttribute')
        if not self.sortingAttributes.__contains__(comboBox.currentText().lower()):
            self.sortingAttributes.append(comboBox.currentText().lower())
            self.loadTableWidget(table)

    def deleteButton(self, dlg, table):
        currentRow = table.currentRow()
        if currentRow >= 0 and len(self.sortingAttributes) > 1:
            deletedAttribute = self.sortingAttributes.pop(currentRow)
            self.loadTableWidget(table)

    def resetDialogueBox(self):
        if self.isSorting and self.sortingThread.isRunning():
            self.sortingThread.terminate()
            self.sortingThread.wait()
            self.sortingAttributes.clear()
            self.isSorting = False
            self.timer.stop()

        self.counter = -1
        self.updateCounter()
        self.sWidget.findChild(QtWidgets.QComboBox,
                               'Algorithms').setCurrentIndex(0)
        self.sWidget.findChild(QtWidgets.QComboBox,
                               'Attributes').setCurrentIndex(0)
        self.sortingAttributes.clear()
        self.sWidget.findChild(QtWidgets.QRadioButton,
                               'ascendRBtn').setChecked(True)
        self.clearTable()
        self.loadTable(self.sortedList)

    def searching(self):
        self.image.hide()
        self.sWidget.setCurrentIndex(2)
        self.hideFilter()
        self.sWidget.show()
        self.dataView.show()
        self.loadTable(MovieDL.movies)
        addAnotherBtn = self.sWidget.findChild(QtWidgets.QWidget, 'addFilter')
        addAnotherBtn.clicked.connect(self.showFilter)
        attributePanel = self.sWidget.findChild(
            QtWidgets.QWidget, 'anotherAttribute')
        cancelBtn = attributePanel.findChild(QtWidgets.QWidget, 'cancelBtn')
        cancelBtn.clicked.connect(self.hideFilter)
        searchBtn = self.sWidget.findChild(QtWidgets.QWidget, 'searchBtn')
        searchBtn.clicked.connect(self.search)

    def search(self):
        if (self.flag == True):
            self.compoundSearching()
        else:
            self.simpleSearch()

    def simpleSearch(self):
        attributes = self.sWidget.findChild(
            QtWidgets.QWidget, 'searchAttribute1')
        attribute = attributes.currentText()
        if attribute != '--Select Attribute--':
            filters = self.sWidget.findChild(
                QtWidgets.QWidget, 'searchFilter1')
            filter = filters.currentText()
            toCheck = self.sWidget.findChild(
                QtWidgets.QWidget, 'toCheckTxt1').text()
            list = linearSearch(
                MovieDL.movies, attribute.lower(), filter, toCheck)
            self.loadTable(list)
            print("Hello")
        else:
            self.showPopup('Select an Attribute')

    def compoundSearching(self):
        # Attribute 1
        attributes1 = self.sWidget.findChild(
            QtWidgets.QWidget, 'searchAttribute1')
        attribute1 = attributes1.currentText()
        if attribute1 != '--Select Attribute--':
            filters1 = self.sWidget.findChild(
                QtWidgets.QWidget, 'searchFilter1')
            filter1 = filters1.currentText()
            toCheck1 = self.sWidget.findChild(
                QtWidgets.QWidget, 'toCheckTxt1').text()
            list1 = linearSearch(
                MovieDL.movies, attribute1.lower(), filter1, toCheck1)
        else:
            self.showPopup('Select Attribute 1')
        # Attribute 2
        attributes2 = self.sWidget.findChild(
            QtWidgets.QWidget, 'searchAttribute2')
        attribute2 = attributes2.currentText()
        if attribute2 != '--Select Attribute--':
            filters2 = self.sWidget.findChild(
                QtWidgets.QWidget, 'searchFilter2')
            filter2 = filters2.currentText()
            toCheck2 = self.sWidget.findChild(
                QtWidgets.QWidget, 'toCheckTxt2').text()
            list2 = linearSearch(
                MovieDL.movies, attribute2.lower(), filter2, toCheck2)
        else:
            self.showPopup('Select Attribute 2')
        # operator
        operators = self.sWidget.findChild(QtWidgets.QWidget, 'operators')
        array = []
        if operators.currentIndex() == 0:
            self.showPopup("Operator not selected")
        if (operators.currentIndex() == 1):
            array = list(set(list1+list2))
        if (operators.currentIndex() == 2):
            array = list(set(list1) & set(list2))
        if operators.currentIndex() == 3:
            array = list(set(list1) - set(list2))
        self.loadTable(array)

    def showPopup(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Error')
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # Hiding widget which contains the information for another attribute
    def hideFilter(self):
        operatorPanel = self.sWidget.findChild(QtWidgets.QWidget, 'operators')
        operatorPanel.hide()
        attributePanel = self.sWidget.findChild(
            QtWidgets.QWidget, 'anotherAttribute')
        attributePanel.hide()
        self.flag = False

    def showFilter(self):
        self.flag = True
        operatorPanel = self.sWidget.findChild(QtWidgets.QWidget, 'operators')
        operatorPanel.show()
        attributePanel = self.sWidget.findChild(
            QtWidgets.QWidget, 'anotherAttribute')
        attributePanel.show()

    def loadTable(self, array):
        data = CustomTableModel(array, self.columns)
        self.dataView.setModel(data)

    def clearTable(self):
        empty = []
        data = CustomTableModel(empty, self.columns)
        self.dataView.setModel(data)

    def updateCounter(self):
        self.counter += 1
        hours = self.counter // 3600
        minutes = (self.counter // 60) % 60
        seconds = self.counter % 60

        counterText = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        self.timeLabel.setText(counterText)

    def populateComboBox(comboBox: QComboBox, items: list):
        comboBox.clear()
        for item in items:
            comboBox.addItem(str(item))
        if len(items) > 0:
            comboBox.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.showMaximized()
    sys.exit(app.exec_())
