#To get the output of moviepy process you have to create inherited class and override it's callback function
#improve downloading progressbar
#run proof tests-turn of internet while downloading
from PyQt5 import QtWidgets as q
import loading
open=True
class loadWindow(q.QMainWindow,loading.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progressBar.setValue(0)
        self.show()
    def closeEvent(self,event):
        event.ignore()
def run():
    global assistants,open
    import assistants
    open=False
app=q.QApplication([])
w=loadWindow()
import os,time,threading
threadx=threading.Thread(target=run)
threadx.start()
p=None
while open:
    time.sleep(0.05)
    x=os.getenv('love')
    if x!=p:
        p=x
        w.progressBar.setValue(int(x)*10)
    app.processEvents()
w=assistants.mw()
w.show()
app.setPalette(assistants.darkPalette)
app.setStyle('Fusion')
app.exec()
