from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return 3 #only 3 as I am doing one button and then 2 info rn.  len(self._data[0])
# pw_page = QWidget(self)
# pw_page.table = QTableView()
# #read CSV file
# with open( 'passwords.csv', 'r' ) as file:
    # reader = csv.reader( file )
    # data = list( reader )
# button_list = []
# pw_page.model = TableModel.TableModel( data )
# pw_page.proxy_model = QSortFilterProxyModel()
# pw_page.proxy_model.setFilterKeyColumn(-1) # Search all columns.
# pw_page.proxy_model.setSourceModel(pw_page.model)

# # pw_page.proxy_model.sort(0, Qt.AscendingOrder) #see how to sort by timestamp

# pw_page.table.setModel(pw_page.proxy_model)

# pw_page.searchbar = QLineEdit()

# # You can choose the type of search by connecting to a different slot here.
# # see https://doc.qt.io/qt-5/qsortfilterproxymodel.html#public-slots
# pw_page.searchbar.textChanged.connect(pw_page.proxy_model.setFilterFixedString)

# layout = QVBoxLayout()

# layout.addWidget(pw_page.searchbar)
# layout.addWidget(pw_page.table)

# container = QWidget()
# container.setLayout(layout)
# return container