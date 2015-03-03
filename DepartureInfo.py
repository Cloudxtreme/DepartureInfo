__author__ = 'Reuben'
__version__ = '.921'
import sys
if 'twisted.internet.reactor' in sys.modules:
    del sys.modules['twisted.internet.reactor'] #This is to be used when creating the EXE with pyinstaller.
import qt4reactor
qt4reactor.install()
from twisted.internet import protocol, reactor
from PyQt4 import QtCore, QtGui
from departurewindow import Ui_MainWindow
from popup import Ui_Popup
import threading
import time
import requests
from sqlalchemy import *
from sqlalchemy.sql import select
client = [] #this is needed to access the server out of the protocol instance
sqlerror = None
servererror = None
#This is to connect to the database
class Connection(object):
    def __init__(self):
        #self.aiport = aiport
        #self.atis = atis
        try:
            self.username = 'USERNAME' #USE YOUR OWN CREDENTIALS
            self.password = 'PASSWORD'
            self.tablename = 'TABLENAME'
            self.meta = MetaData()
            self.engine = create_engine('mysql://%s:%s@HOSTNAME/DATABASE' % (
                self.username, self.password), pool_timeout=5) #USE YOUR OWN CREDENTIALS
            self.atis = Table(self.tablename, self.meta, autoload=True, autoload_with=self.engine)
            self.conn = self.engine.connect()
        except Exception, error:
            global sqlerror
            sqlerror = 1


    @property
    def getAirports(self):
        airports = []
        conn = self.engine.connect()
        s = select([self.atis])
        result = conn.execute(s)
        for row in result:
            airports.append(row[self.atis.c.aiport])
        return airports
#Twisted Client Stuff
class Client(protocol.Protocol):
    def connectionMade(self):
        self.factory.connections.append(self.transport)
        client.append(self.transport)
    def dataReceived(self, data):

        if data.strip().lower() == 'atis':
            MainApp.atisAirportChanged()
            Popup.show()
        else:
            return
    def connectionLost(self, reason):
        try:
            reactor.stop()
        except Exception:
            pass
    def sendData(self, data):
        conn = client[0]
        conn.write(data)
class ClientFactory(protocol.ReconnectingClientFactory):
    connections = []
    def startedConnecting(self, connector):
        MainApp.statusBar.showMessage('Connecting to Server...')

    def buildProtocol(self, addr):
        p = Client()
        p.factory = self
        MainApp.statusBar.showMessage('Connected to Server. IDS should function.')
        if sqlerror:
            MainApp.statusBar.showMessage('Database down. Contact admin.')
        self.resetDelay()
        return p

    def clientConnectionLost(self, connector, unused_reason):
        MainApp.statusBar.showMessage('Not connected to server. IDS will not work.')
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, unused_reason)
        global servererror
        servererror = 1
    def clientConnectionFailed(self, connector, reason):
        MainApp.statusBar.showMessage('Not connected to server. IDS will not work.')
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        global servererror
        servererror = 1

class PopupWindow(QtGui.QWidget, Ui_Popup):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.updatePushButton.clicked.connect(self.close)


class ProgramWindow(QtGui.QMainWindow, Ui_MainWindow, Connection, Client):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        try:
            Connection.__init__(self)
        except:
            pass

        #self.reactor = reactor
        self.setupUi(self)
        #Departure Tab
        self.runwayComboBox.addItems(self.getDepartureRunways)
        self.runwayComboBox.setCurrentIndex(-1)
        self.runwayComboBox.highlighted.connect(self.runwayComboBox.setCurrentIndex)
        self.runwayComboBox.highlighted.connect(self.runwayChanged)

        self.departureComboBox.addItems(self.getdepartures)
        self.departureComboBox.setCurrentIndex(-1)
        self.departureComboBox.highlighted.connect(self.departureComboBox.setCurrentIndex)
        self.departureComboBox.highlighted.connect(self.departureChanged)

        #IDS 1 tab ATIS
        try:

            self.idAirportList.addItems(self.getAirports)
            self.idAirportList.setCurrentIndex(-1)
            self.idAirportList.highlighted.connect(self.idAirportList.setCurrentIndex)
            self.idAirportList.activated.connect(self.atisAirportChanged)
            self.idAtisCodeEdit.setMaxLength(1)
            self.idAtisCodeEdit.textEdited.connect(self.setAtis)
        except:
            pass
        #IDS 1 tab Metar
        try:
            self.idAirportList.highlighted.connect(self.getMetar)
        except:
            pass
        #Stay on top button
        self.stayOnTopButton.clicked.connect(self.stayOnTop)


        #Approach Tab
        self.approachFlowComboBox.addItems(self.getApproachFlows)
        self.approachFlowComboBox.setCurrentIndex(-1)
        self.approachFlowComboBox.highlighted.connect(self.approachFlowComboBox.setCurrentIndex)
        self.approachFlowComboBox.highlighted.connect(self.approachFlowChanged)

        #Exit Button
        self.exitButton.clicked.connect(self.close)
        #Connect to Database

    #functions for the Departure Tab
    def runwayChanged(self):
        self.runwayComboBox.highlighted.connect(self.runwayComboBox.setCurrentIndex)
        constant = 0
        f = open("AppData/NavData/NavData.txt")
        if self.departureComboBox.currentText() == '':
            pass
        else:
            for line in f:
                if self.runwayComboBox.currentText() == line[
                                                        0:9].strip() and self.departureComboBox.currentText() == line[
                                                                                                                 9:19].strip():
                    self.departureNameBrowser.setText(line[24:49].strip())
                    self.departureHeadingBrowser.setText(line[127:149].strip())
                    self.departureFlowBrowser.setText(line[194:209].strip())
                    self.correspondingDepartureBrowser.setText(line[233:].strip())
                    self.departureFirstFixBrowser.setText(line[159:189].strip())
                    self.departureTransitionsBrowser.setText(line[61:119].strip())
                    constant = 1
                else:
                    pass

        f.close()

    @property
    def getDepartureRunways(self):
        f = open("AppData/NavData/NavData.txt")
        runways = []
        for line in f:
            if line[0] == '#':
                pass
            elif line[0:9].strip() in runways:
                pass
            else:
                runways.append(line[0:9].strip())
        f.close()
        return runways

    @property
    def getdepartures(self):
        f = open("AppData/NavData/NavData.txt")
        departures = []
        for line in f:
            if line[0] == '#':
                pass
            elif line.strip() == '':
                pass
            elif line[9:19].strip() in departures:
                pass
            else:
                departures.append(line[9:19].strip())
        f.close
        return departures


    def departureChanged(self):
        self.departureComboBox.highlighted.connect(self.departureComboBox.setCurrentIndex)
        constant = 0
        f = open("AppData/NavData/NavData.txt")
        if self.runwayComboBox.currentText() == '':
            pass
        else:
            for line in f:
                if self.runwayComboBox.currentText() == line[
                                                        0:9].strip() and self.departureComboBox.currentText() == line[
                                                                                                                 9:19].strip():
                    self.departureNameBrowser.setText(line[24:49].strip())
                    self.departureHeadingBrowser.setText(line[127:149].strip())
                    self.departureFlowBrowser.setText(line[194:209].strip())
                    self.correspondingDepartureBrowser.setText(line[233:].strip())
                    self.departureFirstFixBrowser.setText(line[159:189].strip())
                    self.departureTransitionsBrowser.setText(line[61:119].strip())
                    constant = 1
                else:
                    pass
                if constant == 0:
                    pass
                    #self.depInfoBrowser.setText('')
                else:
                    pass
        f.close()

    #methods for approach tab

    @property
    def getApproachFlows(self):
        f = open('AppData/Pictures/Pictures.txt')
        flows = []
        for line in f:
            if line[0] == '#':
                pass
            else:
                flows.append(line[:19].strip())
        f.close()
        return flows


    def approachFlowChanged(self):
        f = open('AppData/Pictures/Pictures.txt')
        for line in f:
            if line == '#':
                pass
            else:
                if self.approachFlowComboBox.currentText() == line[:19].strip():
                    self.approachPictureLabel.setPixmap(QtGui.QPixmap(line[19:].strip()))
                else:
                    pass

        f.close()

    #Methods for window
    def stayOnTop(self):
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    #Methods for IDS1 Atis Tab
    def atisAirportChanged(self):
        if self.idAirportList.currentIndex() == -1:
            pass
        else:
            currairport = str(self.idAirportList.currentText())
            conn = self.engine.connect()
            s = select([self.atis]).where(self.atis.c.COLUMNNAME == currairport)#USE OWN DATABASE INFO
            result = conn.execute(s)
            row = result.fetchone()
            atis = row[1]
            self.idAtisCodeEdit.setText(atis)
            conn.close()

    def setAtis(self):
        atis = str(self.idAtisCodeEdit.text())
        atis1 = atis.upper()
        self.idAtisCodeEdit.setText(atis1)
        if atis1.isupper:
            atis = (self.idAtisCodeEdit.text())
            currairport = str(self.idAirportList.currentText())
            conn = self.engine.connect()
            upd = self.atis.update().\
                where(self.atis.c.COLUMNNAME == currairport).\
                values(COLUMNNAME = atis1)#USE YOUR OWN INFORMATION
            conn.execute(upd)
            conn.close()
            self.sendData('atis')
        else:
            atis = (self.idAtisCodeEdit.text())
            atis1 = str(atis.upper())
            self.idAtisCodeEdit.setText(atis1)
    #Methods for IDS WX Stuff
    #Methods for IDS WX Threads
    def getMetar(self):
        currairport = str(self.idAirportList.currentText())
        metar = requests.get('http://metar.vatsim.net/metar.php', params={'id':currairport}).text
        Wx=metar.strip()
        self.idWxBrowser.setText(Wx)
    def getMetarThread(self):
        while True:
            if self.idAirportList.currentIndex() == -1:
                continue
                time.sleep(5)
            else:
                self.getMetar()
                time.sleep(20)
    #close event
    def closeEvent(self, e):
        reactor.stop()




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainApp = ProgramWindow()
    MainApp.show()
    Popup = PopupWindow()
    #Threading Weather
    wxthread = threading.Thread(target=MainApp.getMetarThread)
    wxthread.setDaemon(True)
    wxthread.start()
    #twisted stuff

    reactor.connectTCP('HOSTNAME', PORTNUMBER,ClientFactory()) #USE YOUR OWN INFORMATION
    reactor.run()


    #App Close
    sys.exit(app.exec_())
