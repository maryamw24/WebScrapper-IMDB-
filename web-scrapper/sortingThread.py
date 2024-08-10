from PyQt5.QtCore import QThread
from sortingAlgorithms import *


class SortingThread(QThread):
    def __init__(self, array, attribute, order, algorithm):
        super().__init__()
        self.array = array
        self.attribute = attribute
        self.order = order
        self.algorithm = algorithm

    def run(self):
        if self.algorithm == 1:
            # bubble
            bubbleSort(self.array, self.attribute, self.order)

        if self.algorithm == 2:
            # selection
            selectionSort(self.array, self.attribute, self.order)

        if self.algorithm == 3:
            # merge
            mergeSort(self.array, self.attribute, self.order)

        if self.algorithm == 4:
            # heap
            heapSort(self.array, self.attribute, self.order)

        if self.algorithm == 5:
            # insertion
            insertionSort(self.array, self.attribute, self.order)

        if self.algorithm == 6:
            # quick
            quickSort(self.array, self.attribute, self.order)

        if self.algorithm == 7:
            # radix
            radixSort(self.array, self.attribute, self.order)

        if self.algorithm == 8:
            # count
            countSort(self.array, self.attribute, self.order)

        if self.algorithm == 9:
            # bucket
            bucketSort(self.array, self.attribute, self.order)

        if self.algorithm == 10:
            # tim
            timSort(self.array, self.attribute, self.order)
    
        if self.algorithm == 11:
            # oddeven
            oddEvenSort(self.array, self.attribute, self.order)
            
        if self.algorithm == 12:
            # oddeven
            shellSort(self.array, self.attribute, self.order)
        self.finished.emit()
