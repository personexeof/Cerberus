import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import json
from PyQt5.QtGui import QPixmap
from random import shuffle


class MyWidget(QMainWindow):
    def __init__(self):

        super().__init__()
        uic.loadUi('data/ui/main.ui', self)
        self.update()
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.set_answers)
        self.action.triggered.connect(self.new_word)

    def run(self):
        self.update()
        self.flag = True
        self.pushButton.setText("Начать заново")
        self.label.setText(self.answ[self.i])

    def set_answers(self):
        if self.lineEdit.text().lstrip().rstrip().capitalize() in self.otv[
            self.answ[self.i]] and self.lineEdit.text().lstrip().rstrip().capitalize() != '':
            self.points += 1
        else:
            t = '\n'.join(i for i in self.otv[self.answ[self.i]])
            self.b = Bad(t)
            self.b.show()
        self.i += 1
        if self.i == self.length:
            self.rez = Rez(self.length, self.points)
            self.rez.show()
            self.update()
        else:
            self.lineEdit.setText('')
            self.label.setText(self.answ[self.i])

    def update(self):
        self.lineEdit.setText('')
        self.label.setText('')
        self.flag = False
        self.i = 0
        self.otv = self.get_words()
        self.answ = list(self.otv.keys())
        shuffle(self.answ)
        self.length = min(len(self.answ), 30)
        self.points = 0

    def get_words(self):
        with open('data/words.json', 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        return data

    def new_word(self):
        self.n_w = New_w(self.otv)
        self.n_w.show()
        self.update()


class Rez(QWidget):
    def __init__(self, length, points):
        self.length = length
        self.points = points
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('data/ui/pez.ui', self)
        self.run()

    def run(self):
        self.pixmap = QPixmap('data/img/good.jpg').scaled(200, 200)
        self.pixmap_2 = QPixmap('data/img/bad.jpg').scaled(200, 200)
        self.label_2.setText(
            f'Ты перевел {self.points} из  {self.length} слов правильно\nЭто {self.points * 100 // self.length} %')
        if self.points * 100 // self.length >= 80:

            self.label.setPixmap(self.pixmap)
        else:
            self.label.setPixmap(self.pixmap_2)


class Bad(QWidget):
    def __init__(self, word):
        self.word = word
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('data/ui/bad.ui', self)
        self.run()

    def run(self):
        self.label_2.setText(f'{self.word}')


class New_w(QWidget):
    def __init__(self, dict_n):
        self.dict_n = dict_n
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('data/ui/new_words.ui', self)
        self.save_button.clicked.connect(self.run)

    def run(self):
        self.dict_n[self.lineEdit_2.text().lstrip().rstrip().capitalize()] = [i.lstrip().rstrip().capitalize() for i in
                                                                              self.lineEdit.text().split(',')]
        with open('data/words.json', 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(self.dict_n, ensure_ascii=False))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
