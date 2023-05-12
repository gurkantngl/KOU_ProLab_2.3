import psycopg2
from psycopg2 import sql, extensions
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QLineEdit
from PyQt5 import QtGui

kullanıcı_no = 1

connection = psycopg2.connect(
    host="127.0.0.1",
    database="meta-land",
    user="postgres",
    password="gtongel553",
    port = "5432"
)

connection.autocommit = True

cursor = connection.cursor()

cursor.execute("DELETE FROM kullanıcı_bilgileri")
cursor.execute("DELETE FROM alan_bilgileri")
cursor.execute("DELETE FROM işletme_bilgileri")
cursor.execute("DELETE FROM kiralama_bilgileri")
cursor.execute("DELETE FROM satış_bilgileri")
cursor.execute("DELETE FROM günlük_giderler")
cursor.execute("DELETE FROM çalışan_bilgileri")
cursor.execute("DELETE FROM oyun_bilgileri")
connection.commit()


autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
connection.set_isolation_level(autocommit)

cursor.execute("SELECT * FROM kullanıcı_bilgileri")
rows = cursor.fetchall()


oyuncuList = []


class yonetici(QWidget):
    
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        #self.setLayout(grid)

        self.myFont = QtGui.QFont('MS Shell Dlg2',14)
        self.myFont.setBold(True)
        self.myFont.setPointSize(12)

        self.label1 = QLabel(self)
        self.label1.setText("Oyun Alanı Boyutları")
        self.label1.setFixedSize(250, 70)
        self.label1.move(90, 180)
        self.label1.setFont(self.myFont)
        
        self.label2 = QLabel(self)
        self.label2.setText("İsim")
        self.label2.setFixedSize(100, 50)
        self.label2.move(450, 150)
        self.label2.setFont(self.myFont)
        
        self.label3 = QLabel(self)
        self.label3.setText("Soy İsim")
        self.label3.setFixedSize(100, 50)
        self.label3.move(450, 200)
        self.label3.setFont(self.myFont)
        
        self.label4 = QLabel(self)
        self.label4.setText("Şifre")
        self.label4.setFixedSize(100, 50)
        self.label4.move(450, 250)
        self.label4.setFont(self.myFont)
        
        
        self.txtİsim = QLineEdit(self)
        self.txtİsim.move(550, 150)
        self.txtİsim.resize(160, 40)
        
        self.txtsoyİsim = QLineEdit(self)
        self.txtsoyİsim.move(550, 200)
        self.txtsoyİsim.resize(160, 40)
        
        
        self.txtŞifre = QLineEdit(self)
        self.txtŞifre.move(550, 250)
        self.txtŞifre.resize(160, 40)
        
        self.label3 = QLabel(self)
        self.label3.setText("X")
        self.label3.setFixedSize(20, 30)
        self.label3.move(170, 260)
        self.label3.setFont(self.myFont)
        
        self.txtX = QLineEdit(self)
        self.txtX.move(100, 250)
        self.txtX.resize(60, 40)
        
        self.txtY = QLineEdit(self)
        self.txtY.move(200, 250)
        self.txtY.resize(60, 40)
        
        
        
        
        self.myFont.setPointSize(10)
        self.btnaddGamer = QPushButton(self)
        self.btnaddGamer.setText("Oyuncuyu Ekle")
        self.btnaddGamer.setFont(self.myFont)
        self.btnaddGamer.clicked.connect(self.oyuncuEkle)
        self.btnaddGamer.setFixedSize(150, 60)
        self.btnaddGamer.move(500, 300)
        
        self.btnStart = QPushButton(self)
        self.btnStart.setText("Oyunu Başlat")
        self.btnStart.setFont(self.myFont)
        self.btnStart.clicked.connect(self.start)
        self.btnStart.setFixedSize(150, 60)
        self.btnStart.move(320, 390)
        
        
        self.setFixedSize(800, 600)
        self.move(500, 200)
        self.setWindowTitle('Yönetici')
        #self.show()

    
    def oyuncuEkle(self):
        try:
            global connection
            global cursor
            global kullanıcı_no
            insert_table = "INSERT INTO kullanıcı_bilgileri (no, isim, soyİsim, şifre) VALUES (%s, %s, %s, %s)"
            inserted_values = (kullanıcı_no, self.txtİsim.text(), self.txtsoyİsim.text(), self.txtŞifre.text())
            kullanıcı_no += 1
            oyuncuList.append(kullanıcı_no)
            self.txtİsim.setText("")
            self.txtsoyİsim.setText("")
            self.txtŞifre.setText("")
            cursor.execute(insert_table, inserted_values)

            count = cursor.rowcount
            print(count, ". kayıt tabloya eklendi")
            
            
            cursor.execute("SELECT * FROM kullanıcı_bilgileri")
            rows = cursor.fetchall()

            for i in range(len(rows)):
                print(rows)
        
        except(Exception, psycopg2.Error) as error:
            print("PostgreSQL veri tabanına bağlanırken bir hata oluştu.: ", error)
            connection = None
    
    def start(self):
        global kullanıcı_no
        global connection
        global cursor
        x = int(self.txtX.text())
        y = int(self.txtY.text())
        
        insert_boyut = "INSERT INTO oyun_bilgileri (boyut_x, boyut_y) VALUES (%s, %s)"
        inserted_values = (x, y)
        cursor.execute(insert_boyut, inserted_values)
        
        self.setFixedSize(1900, 900)
        self.move(0, 0)
        self.setWindowTitle('Oyun Alanı')
        
        self.label1.close()
        self.label2.close()
        self.label3.close()
        self.txtX.close()
        self.txtY.close()
        self.txtİsim.close()
        self.btnaddGamer.close()
        self.btnStart.close()
        
        currX = 0
        currY = 0 

        buttonList = []
        
        for _ in range(y):
            for _ in range(x):
                button = QPushButton(self)
                button.resize(int(900/x), int(900/y))
                button.move(int(currX), int(currY))
                currX += 900 / x
                button.setEnabled(False)
                button.setVisible(True)
                buttonList.append(button)

                
            currX = 0    
            currY += 900 / y
        
        kullanici_bilgiList = []
        for i in range(len(oyuncuList)):
            kullanici_bilgiList.append([])
            self.myFont.setPointSize(8)
            
            self.lblNo = QLabel(self)
            self.lblNo.setText("No: " + str(i+1))
            self.lblNo.setFixedSize(75, 20)
            self.lblNo.move(900 + ((i%5) * 200), 0 + (int(i/5) * 300))
            self.lblNo.setFont(self.myFont)
            self.lblNo.setVisible(True)
            kullanici_bilgiList[i].append(self.lblNo)
            
            cursor.execute("SELECT isim FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            isim = cursor.fetchone()
            if isim:
                isim = isim[0]
            self.lblİsim = QLabel(self)
            self.lblİsim.setText("İsim: " + str(isim))
            self.lblİsim.setFixedSize(125, 20)
            self.lblİsim.move(900 + ((i%5) * 200), 30 + (int(i/5) * 300))
            self.lblİsim.setFont(self.myFont)
            self.lblİsim.setVisible(True)
            kullanici_bilgiList[i].append(self.lblİsim)
        
            cursor.execute("SELECT soyİsim FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            soyİsim = cursor.fetchone()
            if soyİsim:
                soyİsim = soyİsim[0]
            self.lblsoyİsim = QLabel(self)
            self.lblsoyİsim.setText("Soyisim: " + str(soyİsim))
            self.lblsoyİsim.setFixedSize(125, 20)
            self.lblsoyİsim.move(900 + ((i%5) * 200), 60 + (int(i/5) * 300))
            self.lblsoyİsim.setFont(self.myFont)
            self.lblsoyİsim.setVisible(True)
            kullanici_bilgiList[i].append(self.lblsoyİsim)
            
            cursor.execute("SELECT kalan_yemek FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            yemek = cursor.fetchone()
            if yemek:
                yemek = yemek[0]
            self.lblYemek = QLabel(self)
            self.lblYemek.setText("Yemek: " + str(yemek))
            self.lblYemek.setFixedSize(125, 20)
            self.lblYemek.move(900 + ((i%5) * 200), 90 + (int(i/5) * 300))
            self.lblYemek.setFont(self.myFont)
            self.lblYemek.setVisible(True)
            kullanici_bilgiList[i].append(self.lblYemek)
            
            cursor.execute("SELECT kalan_eşya FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            eşya = cursor.fetchone()
            if eşya:
                eşya = eşya[0]
            self.lblEşya = QLabel(self)
            self.lblEşya.setText("Eşya: " + str(eşya))
            self.lblEşya.setFixedSize(125, 20)
            self.lblEşya.move(900 + ((i%5) * 200), 120 + (int(i/5) * 300))
            self.lblEşya.setFont(self.myFont)
            self.lblEşya.setVisible(True)
            kullanici_bilgiList[i].append(self.lblEşya)
            
            cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            para = cursor.fetchone()
            if para:
                para = para[0]
            self.lblPara = QLabel(self)
            self.lblPara.setText("Para: " + str(para))
            self.lblPara.setFixedSize(125, 20)
            self.lblPara.move(900 + ((i%5) * 200), 150 + (int(i/5) * 300))
            self.lblPara.setFont(self.myFont)
            self.lblPara.setVisible(True)
            kullanici_bilgiList[i].append(self.lblPara)
        
            cursor.execute("SELECT işletme_no FROM çalışan_bilgileri WHERE oyuncu_no = %s",(str(i+1)))
            work = cursor.fetchone()
            if work:
                work = work[0]
            self.lblWork = QLabel(self)
            self.lblWork.setText("Çalıştığı Alan: " + str(work))
            self.lblWork.setFixedSize(125, 20)
            self.lblWork.move(900 + ((i%5) * 200), 180 + (int(i/5) * 300))
            self.lblWork.setFont(self.myFont)
            self.lblWork.setVisible(True)
    
    
    def thread(self):
        global connection
        global cursor
        global kullanıcı_no
    
        while(True):
            
            for i in range(kullanıcı_no):
                cursor.execute("SELECT date_part()")
                work = cursor.fetchone()
                if work:
                    work = work[0]
    
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = yonetici()
    ex.show()
    sys.exit(app.exec_())