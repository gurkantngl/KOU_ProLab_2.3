import psycopg2
from psycopg2 import sql, extensions
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QLineEdit
from PyQt5 import QtGui
import threading
import datetime
import time

kullanıcı_no = 1
noList = []

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
cursor.close()

cursor = connection.cursor()
cursor.execute("DELETE FROM alan_bilgileri")
cursor.close()

cursor = connection.cursor()
cursor.execute("DELETE FROM işletme_bilgileri")
cursor.close()

cursor = connection.cursor()
cursor.execute("DELETE FROM kiralama_bilgileri")
cursor.close()

cursor = connection.cursor()
cursor.execute("DELETE FROM satış_bilgileri")
cursor.close()

cursor = connection.cursor()
cursor.execute("DELETE FROM günlük_giderler")
cursor.close()

cursor = connection.cursor()
cursor.execute("DELETE FROM çalışan_bilgileri")
cursor.close()

cursor = connection.cursor()
cursor.execute("DELETE FROM oyun_bilgileri")
cursor.close()
connection.commit()


autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
connection.set_isolation_level(autocommit)

cursor = connection.cursor()
cursor.execute("SELECT * FROM kullanıcı_bilgileri")
rows = cursor.fetchall()
cursor.close()


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
            global kullanıcı_no
            insert_table = "INSERT INTO kullanıcı_bilgileri (no, isim, soyİsim, şifre) VALUES (%s, %s, %s, %s)"
            inserted_values = (kullanıcı_no, self.txtİsim.text(), self.txtsoyİsim.text(), self.txtŞifre.text())
            noList.append(kullanıcı_no)
            kullanıcı_no += 1
            oyuncuList.append(kullanıcı_no)
            self.txtİsim.setText("")
            self.txtsoyİsim.setText("")
            self.txtŞifre.setText("")
            
            cursor = connection.cursor()
            cursor.execute(insert_table, inserted_values)
            cursor.close()

            count = cursor.rowcount
            print(count, ". kayıt tabloya eklendi")
            
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM kullanıcı_bilgileri")            
            rows = cursor.fetchall()
            cursor.close()
            
            for i in range(len(rows)):
                print(rows)
        
        except(Exception, psycopg2.Error) as error:
            print("PostgreSQL veri tabanına bağlanırken bir hata oluştu.: ", error)
            #connection = None
    
    def start(self):
        global kullanıcı_no
        global connection
        x = int(self.txtX.text())
        y = int(self.txtY.text())
        
        insert_boyut = "INSERT INTO oyun_bilgileri (boyut_x, boyut_y) VALUES (%s, %s)"
        inserted_values = (x, y)
        
        cursor = connection.cursor()
        cursor.execute(insert_boyut, inserted_values)
        cursor.close()
        
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
        
        self.kullanici_bilgiList = []
        for i in range(len(oyuncuList)):
            self.kullanici_bilgiList.append([])
            self.myFont.setPointSize(8)
            
            self.lblNo = QLabel(self)
            self.lblNo.setText("No: " + str(i+1))
            self.lblNo.setFixedSize(75, 20)
            self.lblNo.move(900 + ((i%5) * 200), 0 + (int(i/5) * 300))
            self.lblNo.setFont(self.myFont)
            self.lblNo.setVisible(True)
            self.kullanici_bilgiList[i].append(self.lblNo)
            
            cursor = connection.cursor()
            cursor.execute("SELECT isim FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            isim = cursor.fetchone()
            cursor.close()
            if isim:
                isim = isim[0]
            self.lblİsim = QLabel(self)
            self.lblİsim.setText("İsim: " + str(isim))
            self.lblİsim.setFixedSize(125, 20)
            self.lblİsim.move(900 + ((i%5) * 200), 30 + (int(i/5) * 300))
            self.lblİsim.setFont(self.myFont)
            self.lblİsim.setVisible(True)
            self.kullanici_bilgiList[i].append(self.lblİsim)
        
            cursor = connection.cursor()
            cursor.execute("SELECT soyİsim FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            soyİsim = cursor.fetchone()
            cursor.close()
            if soyİsim:
                soyİsim = soyİsim[0]
            self.lblsoyİsim = QLabel(self)
            self.lblsoyİsim.setText("Soyisim: " + str(soyİsim))
            self.lblsoyİsim.setFixedSize(125, 20)
            self.lblsoyİsim.move(900 + ((i%5) * 200), 60 + (int(i/5) * 300))
            self.lblsoyİsim.setFont(self.myFont)
            self.lblsoyİsim.setVisible(True)
            self.kullanici_bilgiList[i].append(self.lblsoyİsim)
            
            cursor = connection.cursor()
            cursor.execute("SELECT kalan_yemek FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            yemek = cursor.fetchone()
            cursor.close()
            if yemek:
                yemek = yemek[0]
            self.lblYemek = QLabel(self)
            self.lblYemek.setText("Yemek: " + str(yemek))
            self.lblYemek.setFixedSize(125, 20)
            self.lblYemek.move(900 + ((i%5) * 200), 90 + (int(i/5) * 300))
            self.lblYemek.setFont(self.myFont)
            self.lblYemek.setVisible(True)
            self.kullanici_bilgiList[i].append(self.lblYemek)
            
            cursor = connection.cursor()
            cursor.execute("SELECT kalan_eşya FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            eşya = cursor.fetchone()
            cursor.close()
            
            if eşya:
                eşya = eşya[0]
            self.lblEşya = QLabel(self)
            self.lblEşya.setText("Eşya: " + str(eşya))
            self.lblEşya.setFixedSize(125, 20)
            self.lblEşya.move(900 + ((i%5) * 200), 120 + (int(i/5) * 300))
            self.lblEşya.setFont(self.myFont)
            self.lblEşya.setVisible(True)
            self.kullanici_bilgiList[i].append(self.lblEşya)
            
            cursor = connection.cursor()
            cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1)))
            para = cursor.fetchone()
            cursor.close()
            
            if para:
                para = para[0]
            self.lblPara = QLabel(self)
            self.lblPara.setText("Para: " + str(para))
            self.lblPara.setFixedSize(125, 20)
            self.lblPara.move(900 + ((i%5) * 200), 150 + (int(i/5) * 300))
            self.lblPara.setFont(self.myFont)
            self.lblPara.setVisible(True)
            self.kullanici_bilgiList[i].append(self.lblPara)
        
            cursor = connection.cursor()
            cursor.execute("SELECT işletme_no FROM çalışan_bilgileri WHERE oyuncu_no = %s",(str(i+1)))
            work = cursor.fetchone()
            cursor.close()
            
            if work:
                work = work[0]
            self.lblWork = QLabel(self)
            self.lblWork.setText("Çalıştığı Alan: " + str(work))
            self.lblWork.setFixedSize(125, 20)
            self.lblWork.move(900 + ((i%5) * 200), 180 + (int(i/5) * 300))
            self.lblWork.setFont(self.myFont)
            self.lblWork.setVisible(True)
            self.kullanici_bilgiList[i].append(self.lblWork)
            
            
        for i in range(x * y):
            if i == 0:
                insert_table = "INSERT INTO alan_bilgileri (alan_kare_no, alan_türü) VALUES (%s, %s)"
                inserted_values = (i+1, "Market")
                cursor = connection.cursor()
                cursor.execute(insert_table, inserted_values)
                cursor.close()
                buttonList[i].setText(str(i+1) + "\n" + "Alan Türü: Market" + "\n" + "Alan Sahibi: Yönetici" + "\n" + "Çalışan Kapasitesi: Sınırsız")
            
            elif i == 1:
                insert_table = "INSERT INTO alan_bilgileri (alan_kare_no, alan_türü) VALUES (%s, %s)"
                inserted_values = (i+1, "Mağaza")
                cursor = connection.cursor()
                cursor.execute(insert_table, inserted_values)
                cursor.close()
                buttonList[i].setText(str(i+1) + "\n" + "Alan Türü: Mağaza" + "\n" + "Alan Sahibi: Yönetici" + "\n" + "Çalışan Kapasitesi: Sınırsız")
            
            elif i == 2:
                insert_table = "INSERT INTO alan_bilgileri (alan_kare_no, alan_türü) VALUES (%s, %s)"
                inserted_values = (i+1, "Emlak")
                cursor = connection.cursor()
                cursor.execute(insert_table, inserted_values)
                cursor.close()
                buttonList[i].setText(str(i+1) + "\n" + "Alan Türü: Emlak" + "\n" + "Alan Sahibi: Yönetici")
            
            else:
                insert_table = "INSERT INTO alan_bilgileri (alan_kare_no, alan_türü) VALUES (%s, %s)"
                inserted_values = (i+1, "Arsa")
                cursor = connection.cursor()
                cursor.execute(insert_table, inserted_values)
                cursor.close()
                buttonList[i].setText(str(i+1) + "\n" + "Alan Türü: Arsa" + "\n" + "Alan Sahibi: Yönetici")
            
        t = threading.Thread(target= self.thread, args = ())
        t.start()
        #self.thread()
            
    def thread(self):
        global connection
        global kullanıcı_no
        
        delete = []
        curDate = datetime.datetime.today().date()
        length = len(oyuncuList)
        while(True):
        
            currDate = datetime.datetime.today().date()
            
            if currDate != curDate:
                fark = ((currDate - curDate).days)
                fark = int(fark)
                curDate = currDate

                for i in range(length):
                    cursor = connection.cursor()
                    cursor.execute("SELECT kalan_yemek FROM kullanıcı_bilgileri WHERE no = %s", str(noList[i]))
                    yemek = cursor.fetchone()
                    cursor.close()
                    if yemek:
                        yemek = yemek[0]
                        yemek -= (fark*10)
                        if yemek < 0:
                            yemek = 0
                        
                    cursor = connection.cursor()   
                    cursor.execute("SELECT kalan_eşya FROM kullanıcı_bilgileri WHERE no = %s", str(noList[i]))
                    eşya = cursor.fetchone()
                    cursor.close()
                    if eşya:
                        eşya = eşya[0]
                        eşya -= (fark*10)
                        if eşya < 0:
                            eşya = 0
                        
                    cursor = connection.cursor()    
                    cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(noList[i]))
                    para = cursor.fetchone()
                    cursor.close()
                    if para:
                        para = para[0]
                        para -= (fark*10)
                        if para < 0:
                            para = 0
                                        
                    updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_yemek = %s, kalan_eşya = %s, kalan_para = %s WHERE no = %s"
                    cursor = connection.cursor()
                    cursor.execute(updateQuery, (yemek, eşya, para, noList[i]))
                    cursor.close()
                        
                    cursor = connection.cursor()
                    cursor.execute("SELECT kalan_yemek FROM kullanıcı_bilgileri WHERE no = %s",(str(noList[i])))
                    nyemek = cursor.fetchone()
                    cursor.close()
                    if nyemek:
                        nyemek = nyemek[0]
                    self.kullanici_bilgiList[i][3].setText("Yemek: " + str(nyemek))
                    
                    cursor = connection.cursor()
                    cursor.execute("SELECT kalan_eşya FROM kullanıcı_bilgileri WHERE no = %s",(str(noList[i])))
                    neşya = cursor.fetchone()
                    cursor.close()
                    if neşya:
                        neşya = neşya[0]
                    self.kullanici_bilgiList[i][4].setText("Eşya: " + str(neşya))
                    
                    cursor = connection.cursor()
                    cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s",(str(noList[i])))
                    npara = cursor.fetchone()
                    cursor.close()
                    if npara:
                        npara = npara[0]
                    self.kullanici_bilgiList[i][5].setText("Para: " + str(npara))    

                    if int(yemek) <= 0 or int(eşya) <= 0:
                        delete.append(i)
                    
                for j in range(len(delete)):
                    del noList[delete[j]-j]
                    del self.kullanici_bilgiList[delete[j]-j]
                    length -= 1
                
                time.sleep(1)
                
                delete = []
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = yonetici()
    ex.show()
    sys.exit(app.exec_())