from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QKeySequence
from mainUI import Ui_MainWindow
import mysql.connector


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        print("INIT")
        #MySQL 접속 코드
        #본인이 만든 AWS EC2 URL 주소를 사용합니다.
        self.db = mysql.connector.connect(host='ec2-43-201-26-90.ap-northeast-2.compute.amazonaws.com', user='ssafydh', password='1234', database='kingDB', auth_plugin='mysql_native_password')
        self.cur = self.db.cursor()

        #timer setting
        self.timer = QTimer()
        self.timer.setInterval(500) #500ms
        self.timer.timeout.connect(self.pollingQuery)


    def start(self):
        print("Start")
        self.timer.start()

    def pollingQuery(self):
        # 최근 15개 정보만 가져오기
        self.cur.execute("select * from command order by time desc limit 15")
        self.logText.clear()
        self.statusText.clear()
        for (id, time, cmd_string, arg_string, is_finish) in self.cur:
            str = "%5d | %s | %6s | %6s | %4d" % (id, time.strftime("%Y%m%d %H:%M:%S"), cmd_string, arg_string, is_finish)
            self.logText.appendPlainText(str)

        #sensingTable 정보도 가져오기
        #최근 15개 정보만 가져오기
        self.cur.execute("select * from sensing order by time desc limit 15")
        self.sensingText.clear()
        for (id, time, pitch_value, roll_value, US_range_value, meta_string, is_finish, isAccident) in self.cur:
            str = "%d | %s | %6s | %6s | %6s | %15s | %4d %d" % (time.strftime("%Y%m%d %H:%M:%S"), pitch_value, roll_value, US_range_value, meta_string, is_finish, isAccident)
            self.sensingText.appendPlainText(str)
            if isAccident == 0:
                self.statusText.appendPlainText("정상운행중")
            elif isAccident == 1:
                self.statusText.appendPlainText("전복사고 발생!!")
                print("emergency stop")
                #self.insertCommand("stop", "0")
            elif isAccident == 2:
                self.statusText.appendPlainText("추돌사고 발생!!")
                print("emergency stop")

        self.db.commit()


    def insertCommand(self, cmd_string, arg_string):
        time = QDateTime().currentDateTime().toPython()
        is_finish = 0

        query = "insert into command(time, cmd_string, arg_string, is_finish) values (%s, %s, %s, %s)"
        value = (time, cmd_string, arg_string, is_finish)

        self.cur.execute(query, value)
        self.db.commit()


    def stop(self):
        print("stop")
        self.insertCommand("stop", "0")

    def go(self):
        print('go')
        self.insertCommand("go", "0")

    def mid(self):
        print('mid')
        self.insertCommand("mid", "0")

    def back(self):
        print('back')
        self.insertCommand("back", "0")

    def left(self):
        print('left')
        self.insertCommand("left", "0")

    def right(self):
        print('right')
        self.insertCommand("right", "0")

    def closeEvent(self, event):
        event.accept()
        #접속 종료
        self.cur.close()
        self.db.close()

if __name__ == '__main__':
    app = QApplication()
    win = MyApp()
    win.show()
    app.exec()