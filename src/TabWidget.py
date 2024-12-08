'''
TabWidget Class
Contains specification of the TabWidget class for the main window of the program.
'''
from PyQt5 import QtWidgets, QtCore, QtGui #Needed imports
class TabBar(QtWidgets.QTabBar): #used within the TabWidget class.  This is the tabs on the side
    def tabSizeHint(self, index): #used for formatting
        s = QtWidgets.QTabBar.tabSizeHint(self, index) #get the size of this tab
        s.transpose() #rotate the tab
        s = QtCore.QSize(150, 30) #THIS IS THE REAL SIZE OF THE TABS
        return s #return it

    #how do we change the colors of the tabs?
    
    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            

            # Draw tab shape
            painter.drawRoundedRect(opt.rect, 5, 5)
            
            # Save the current painter state
            painter.save()
            
            # Handle text positioning and rotation
            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            
            # Draw the text
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt)
            painter.restore()

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)
        
        # Style the tab widget container
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                background: white;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
        """)
