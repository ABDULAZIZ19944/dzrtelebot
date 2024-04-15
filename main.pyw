import sys, time


from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIcon

from CheckerThread import CheckerThread as CheckerThread
import base64
from products import products

class MyApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("بوت دزرت")
        self.setFixedSize(330, 412)
        self.window_width, self.window_height = 330, 470
        self.setMinimumSize(self.window_width, self.window_height)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)
        self.setWindowIcon(QIcon('icon.png'))
        
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.receiverIdLB = QLabel("اي دي المستقبل", self)
        self.receiverIdLE = QLineEdit(self)
        self.layout.addWidget(self.receiverIdLB, 0, 0)
        self.layout.addWidget(self.receiverIdLE, 0, 1)

        self.refreshRateLB = QLabel("معدل التحديث", self)
        self.refreshRateSB = QSpinBox(self)
        self.refreshRateSB.setMinimum(1)
        self.refreshRateSB.setMaximum(99999999)
        self.refreshRateSB.setValue(3)
        self.layout.addWidget(self.refreshRateLB, 1, 0)
        self.layout.addWidget(self.refreshRateSB, 1, 1)

        self.botTokenLB = QLabel("توكن التلجرام", self)
        self.botTokenLE = QLineEdit(self)
        self.layout.addWidget(self.botTokenLB, 2, 0)
        self.layout.addWidget(self.botTokenLE, 2, 1)

        self.botTokenLB = QLabel("توكن التلجرام", self)
        self.botTokenLE = QLineEdit(self)
        self.layout.addWidget(self.botTokenLB, 2, 0)
        self.layout.addWidget(self.botTokenLE, 2, 1)
        

        self.productsLW = QListWidget()
        self.layout.addWidget(self.productsLW, 3, 0, 1, 0)
        self.productsLW.itemDoubleClicked.connect(self.onProductDoubleClick)

        items = list(products.keys())
        for item in items:
            listItem = QListWidgetItem(item)
            listItem.setFlags(listItem.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            listItem.setFlags(listItem.flags() & ~Qt.ItemFlag.ItemIsSelectable)

            listItem.setCheckState(Qt.CheckState.Unchecked)
            self.productsLW.addItem(listItem)
        
        self.saveBT = QPushButton("حفظ الاعدادات", self)
        self.saveBT.clicked.connect(self.saveBTClicked)
        self.layout.addWidget(self.saveBT, 4, 0, 1, 0)

        self.startBT = QPushButton("تشغيل", self)
        self.startBT.clicked.connect(self.startBTClicked)
        self.layout.addWidget(self.startBT, 5, 0, 1, 0)

        self.statusForcedLB = QLabel("الحالة", self)
        self.statusLB = QLabel("بانتظار التشغيل", self)
        self.layout.addWidget(self.statusForcedLB, 6, 0)
        self.layout.addWidget(self.statusLB, 6, 1)

        self.creditsLB = QLabel(base64.b64decode("2LHZgtmFINin2YTYp9i12K/Yp9ixIDogMS4yPGJyPtiq2YUg2KfZhti02KfYptipINio2YjYp9iz2LfYqSA6IDxhIGhyZWY9Imh0dHBzOi8vd3d3LmRsYWJpYi5jb20iPtiv2YrZgdmK2K8g2KzZitmF2Yo8L2E+").decode('utf-8'), self)
        self.creditsLB.setTextFormat(Qt.TextFormat.RichText)
        self.creditsLB.setOpenExternalLinks(True)
        self.layout.addWidget(self.creditsLB, 7, 0, 1, 0)
        
        #load settings
        self.loadSettings()
        


    def onProductDoubleClick(self):
        item = self.productsLW.currentItem()
        if item is not None:
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)
                
    def tftolistwidget(self, check_string : str, listwidget : QListWidget):
        for index in range(listwidget.count()):
            item = listwidget.item(index)
            if index < len(check_string) and check_string[index] == "t":
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            
            
    def listwidgettotf(self, listwidget) -> str:
        check_string = ""
        for index in range(listwidget.count()):
            item = listwidget.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                check_string += "t" #true
            else:
                check_string += "f" # false
        return check_string

    def loadSettings(self):
        settings = QSettings("dLabib", "dzrt Bot")
        if settings.value("rec_id") is None:
            settings.setValue("rec_id", "")
        self.receiverIdLE.setText(settings.value("rec_id"))
        
        if settings.value("refresh_rate") is None:
            settings.setValue("refresh_rate", 3)
        self.refreshRateSB.setValue(settings.value("refresh_rate"))
        
        if settings.value("bot_token") is None:
            settings.setValue("bot_token", "")
        self.botTokenLE.setText(settings.value("bot_token"))
        
        if settings.value("selected_items") is None:
            settings.setValue("selected_items", "f" * len(products))
        self.tftolistwidget(settings.value("selected_items"), self.productsLW)
        
        if len(app.arguments()) > 1 and app.arguments()[1] == "s":
            self.startBTClicked()
        
    def get_checked_items_values(self):
        checked_values = []
        for index in range(self.productsLW.count()):
            item = self.productsLW.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                checked_values.append(products.get(item.text()))
        return checked_values


    def saveBTClicked(self):
    
        settings = QSettings("dLabib", "dzrt Bot")
        settings.setValue("rec_id", self.receiverIdLE.text())
        settings.setValue("refresh_rate", self.refreshRateSB.value())
        settings.setValue("bot_token", self.botTokenLE.text())
        settings.setValue("selected_items", self.listwidgettotf(self.productsLW))

    def startBTClicked(self):
        if self.startBT.text() == "تشغيل":
            self.startBT.setText("جاري العمل ... اضغط للالغاء")
            self.operationThread = CheckerThread(self)
            self.operationThread.rec_id = self.receiverIdLE.text()
            self.operationThread.refresh_rate = self.refreshRateSB.value()
            self.operationThread.bot_token = self.botTokenLE.text()
            self.operationThread.links = self.get_checked_items_values()
            

            self.operationThread.startSignal.connect(self.onOperationStarted)
            self.operationThread.stopSignal.connect(self.onOperationStopped)
            self.operationThread.checkingSignal.connect(self.onOperationWorking)
            self.operationThread.idleSignal.connect(self.onOperationIdle)
            self.operationThread.start()

        else:
            self.operationThread.stop()
            self.startBT.setText("... تم طلب الغاء العملية")

    def changeStatus(self, newstatus : str):
            self.statusLB.setText(newstatus)
        
        
        
    def onOperationStarted(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        self.show()
        self.changeStatus("جاري التجهيز للبدأ")
            
    def onOperationStopped(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowCloseButtonHint)
        self.show() 
        self.changeStatus("توقف")
        self.startBT.setText("تشغيل")

    def onOperationWorking(self):
        self.changeStatus("جاري التحقق")

    def onOperationIdle(self):
        self.changeStatus("راحة")

# start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(
        """
        QWidget {
            font-size: 16px;
        }
    """
    )

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing Window...")
