from PyQt5.QtCore import Qt, QAbstractTableModel


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, columns, parent=None):
        super().__init__(parent)
        self.data = data
        self.columns = columns

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.columns)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            movie = self.data[index.row()]
            if index.column() == 0:
                return movie.title
            elif index.column() == 1:
                return str(movie.year)
            elif index.column() == 2:
                return movie.certificate
            elif index.column() == 3:
                return str(movie.duration)
            elif index.column() == 4:
                return movie.genre
            elif index.column() == 5:
                return str(movie.rating)
            elif index.column() == 6:
                return movie.description
            elif index.column() == 7:
                return movie.director
            elif index.column() == 8:
                return str(movie.votes)
            # Add more columns as needed, following the pattern
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # Set column headers
            return self.columns[section]
        return None

    def setData(self, data):
        # Set new data to the model
        self.beginResetModel()
        self.data = data
        self.endResetModel()
