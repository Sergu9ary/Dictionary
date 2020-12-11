import sys
from PyQt5.QtCore import QTimer, QTime, QSize
from PyQt5.QtGui import QIcon
import sqlite3
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem

global loggin


class Login_Password(QWidget):
    def __init__(self):
        global loggin
        super().__init__()
        uic.loadUi('Login_Password.ui', self)
        self.setWindowTitle('Log In')
        self.setWindowIcon(QIcon('dictionary.png'))
        self.pushButton.clicked.connect(self.entr)
        self.pushButton_2.clicked.connect(self.create_acc)
        self.label_3.setVisible(False)
        self.label_4.setVisible(False)
        self.con = sqlite3.connect("cards.sqlite")
        self.cur = self.con.cursor()

    def entr(self):
        global loggin
        loggin = self.cur.execute('''SELECT Login FROM cards WHERE Login = ?''', (self.lineEdit.text(),)).fetchall()
        print(loggin)
        passw = self.cur.execute('''SELECT  Password FROM cards WHERE Password = (?)''',
                                 (self.lineEdit_2.text(),)).fetchall()
        print(passw)
        if loggin == [] or passw == []:
            print('Неверно')
            self.label_3.setVisible(True)
        else:
            for p in loggin:
                for i in passw:
                    if p[0] == self.lineEdit.text() and i[0] == self.lineEdit_2.text():
                        self.label_3.setVisible(False)
                        self.label_4.setVisible(True)
                        print('Верно')
                        self.login = Login_Password()
                        self.login.hide()
                        self.login.destroy()

    def create_acc(self):
        print(1)
        self.login = Login_Password()
        self.login.close()
        self.create_ac = Create()
        self.create_ac.show()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('Cards.ui', self)
        self.setWindowTitle('Dictionary')
        self.setWindowIcon(QIcon('dictionary.png'))
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)
        self.show_time()
        self.connection = sqlite3.connect("cards.sqlite")
        self.pushButton.clicked.connect(self.plus_card)
        self.pushButton_2.clicked.connect(self.search_words)
        self.pushButton_3.clicked.connect(self.entry)
        self.pushButton_4.clicked.connect(self.delete)

    def show_time(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.label_2.setText(label_time)

    def entry(self):
        print(1)
        self.login = Login_Password()
        self.login.show()

    try:
        def search_words(self):
            self.words = SearchWord()
            self.words.show()
    except:
        pass

    def delete(self):
        self.delet = DeleteWord()
        self.delet.show()

    def plus_card(self):
        self.ex = MainWindow()
        self.ex.setVisible(False)
        self.card = Card()
        self.card.show()


class Card(QWidget):
    def __init__(self):
        global loggin
        super().__init__()
        uic.loadUi('learn_words.ui', self)
        self.setWindowTitle('Plus Word')
        self.setWindowIcon(QIcon('dictionary.png'))
        self.pushButton.clicked.connect(self.save)
        self.label_2.setVisible(False)

    def save(self):
        try:
            global loggin
            print(2)
            self.con = sqlite3.connect("cards.sqlite")
            self.cur = self.con.cursor()
            word = self.lineEdit.text().lower()
            translate_word = self.lineEdit_2.text().lower()
            language = self.comboBox.currentText()
            translate_language = self.comboBox_2.currentText()
            print(language)
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            for p in loggin:
                pass
            self.cur.execute('''INSERT INTO words VALUES(?, ?, ?, ?, ?)''',
                             (p[0], word, language, translate_word, translate_language,))
            self.con.commit()
        except:
            self.label_2.setVisible(True)


class Create(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Create.ui', self)
        self.setWindowTitle('Create')
        self.setWindowIcon(QIcon('dictionary.png'))
        self.con = sqlite3.connect("cards.sqlite")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.send_values)
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)

    def send_values(self):
        global loggin
        self.cur = self.con.cursor()
        log = self.lineEdit_2.text()
        pas = self.lineEdit_3.text()
        nam = self.lineEdit.text()
        loggin = log
        check_log = self.cur.execute('''SELECT Login FROM cards WHERE Login = (?) ''', (log,)).fetchall()
        check_pas = self.cur.execute('''SELECT Password FROM cards WHERE Password = (?) ''', (pas,)).fetchall()
        if check_log == [] and check_pas == []:
            self.cur.execute('''INSERT INTO cards(Login, Password, Name) VALUES(?, ? , ?)''', (log, pas, nam,))
            self.con.commit()
            self.label_5.setVisible(False)
            self.label_4.setVisible(True)
            self.create = Create()
            self.create.close()
        else:
            self.label_5.setVisible(True)


class SearchWord(QWidget):
    def __init__(self):
        try:
            global loggin
            super().__init__()
            uic.loadUi('search_words.ui', self)
            self.setWindowTitle('Search')
            self.setWindowIcon(QIcon('dictionary.png'))
            self.connection = sqlite3.connect("cards.sqlite")
            for p in loggin:
                pass
            query = self.lineEdit.text()
            res = self.connection.cursor().execute('''SELECT DISTINCT * FROM words WHERE Login = (?) ''', (p[0],)) \
 \
                .fetchall()
            for i, row in enumerate(res):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))

            self.pushButton.clicked.connect(self.select_data)
        except:
            pass

    def select_data(self):
        global loggin
        self.tableWidget.clear()
        for p in loggin:
            pass
        query = self.lineEdit.text()
        print(query)
        res = self.connection.cursor().execute('''SELECT DISTINCT * FROM words WHERE Login = (?) AND Word = (?)
                ''', (p[0], query,)) \
 \
            .fetchall()
        for u in res:
            print(u[0])

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()


class DeleteWord(QWidget):
    def __init__(self):
        global loggin
        super().__init__()
        uic.loadUi('Delete_Words.ui', self)
        self.setWindowTitle('Delete')
        self.setWindowIcon(QIcon('dictionary.png'))
        self.con = sqlite3.connect("cards.sqlite")
        self.pushButton.clicked.connect(self.delete_word)
        self.label.setVisible(False)

    def delete_word(self):
        try:
            global loggin
            for p in loggin:
                pass
            query = self.lineEdit.text().lower()
            print(query)
            res = self.con.cursor().execute('''DELETE  FROM words WHERE Login = (?) AND Word = (?)
                        ''', (p[0], query,))
            self.con.commit()
            self.word_delet = Create()
            self.word_delet.close()
            self.lineEdit.clear()
        except:
            self.label.setVisible(True)


class Dictionary:
    def __init__(self):
        super().__init__()
        uic.loadUi('Dictionary.ui', self)
        self.con = sqlite3.connect("cards.sqlite")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Dictionary_icon.png'))
    window = MainWindow()
    window.show()
    window.update()
    sys.exit(app.exec_())
