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
oyunSırası = 1
marketList = []
mağazaList = []
emlakList = []
satılıkArsalar = []
arsaFiyatı = 25
isletmeFiyatı = 25

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
            oyuncu = Player(kullanıcı_no, self.txtİsim.text(), self.txtsoyİsim.text(), self.txtŞifre.text())
            insert_table = "INSERT INTO kullanıcı_bilgileri (no, isim, soyİsim, şifre, kalan_yemek, kalan_eşya, kalan_para) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            inserted_values = (oyuncu.no, oyuncu.first_name, oyuncu.last_name, oyuncu.password, oyuncu.food, oyuncu.item, oyuncu.money)
            noList.append(kullanıcı_no)
            kullanıcı_no += 1
            oyuncuList.append(oyuncu)
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
                print(rows[i])
        
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

        self.buttonList = []
        
        for _ in range(y):
            for _ in range(x):
                button = QPushButton(self)
                
                palette = QtGui.QPalette()
                palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor("black"))
                button.setPalette(palette)
                button.resize(int(900/x), int(900/y))
                button.move(int(currX), int(currY))
                currX += 900 / x
                button.setEnabled(False)
                button.setVisible(True)
                self.buttonList.append(button)   
                
            currX = 0    
            currY += 900 / y
        
        for i in range(x*y-3):
            satılıkArsalar.append(i+1)
        
        
        self.lblList = []
        for i in range(len(oyuncuList)):
            self.lblList.append([])
            self.myFont.setPointSize(8)
            
            self.lblNo = QLabel(self)
            self.lblNo.setText("No: " + str(i+1))
            self.lblNo.setFixedSize(75, 20)
            self.lblNo.move(900 + ((i%5) * 200), 0 + (int(i/5) * 300))
            self.lblNo.setFont(self.myFont)
            self.lblNo.setVisible(True)
            self.lblList[i].append(self.lblNo)
            
            cursor = connection.cursor()
            cursor.execute("SELECT isim FROM kullanıcı_bilgileri WHERE no = %s",(str(i+1),))
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
            self.lblList[i].append(self.lblİsim)
        
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
            self.lblList[i].append(self.lblsoyİsim)
            
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
            self.lblList[i].append(self.lblYemek)
            
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
            self.lblList[i].append(self.lblEşya)
            
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
            self.lblList[i].append(self.lblPara)
        
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
            self.lblList[i].append(self.lblWork)
            
            
            cursor = connection.cursor()
            cursor.execute("SELECT isim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
            currPlayerName = cursor.fetchone()
            if currPlayerName:
                currPlayerName = currPlayerName[0]
            cursor.close()
            
            cursor = connection.cursor()
            cursor.execute("SELECT soyİsim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
            currPlayerSurName = cursor.fetchone()
            if currPlayerSurName:
                currPlayerSurName = currPlayerSurName[0]
            cursor.close()
            
            
            self.lblCurr = QLabel(self)
            #self.lblCurr.setText("Oyun Sırası: " + str(currPlayerName) + " " + str(currPlayerSurName))
            self.lblCurr.setFixedSize(250, 70)
            self.lblCurr.move(1450, 650)
            self.lblCurr.setFont(self.myFont)
            self.lblCurr.setVisible(True)
            
            
        for i in range(x * y):
            if i == x * y - 1:
                insert_table = "INSERT INTO alan_bilgileri (alan_kare_no, alan_türü) VALUES (%s, %s)"
                inserted_values = (x * y - 1 + 1, "Market")
                cursor = connection.cursor()
                cursor.execute(insert_table, inserted_values)
                cursor.close()
                self.buttonList[i].setText(str(i+1) + "\n" + "Alan Türü: Market" + "\n" + "Alan Sahibi: Yönetici" + "\n" + "Çalışan Kapasitesi: Sınırsız")
            
            elif i == x * y - 2:
                insert_table = "INSERT INTO alan_bilgileri (alan_kare_no, alan_türü) VALUES (%s, %s)"
                inserted_values = (x * y - 2 + 1, "Mağaza")
                cursor = connection.cursor()
                cursor.execute(insert_table, inserted_values)
                cursor.close()
                self.buttonList[i].setText(str(i+1) + "\n" + "Alan Türü: Mağaza" + "\n" + "Alan Sahibi: Yönetici" + "\n" + "Çalışan Kapasitesi: Sınırsız")
            
            elif i == x * y - 3:
                insert_table = "INSERT INTO alan_bilgileri (alan_kare_no, alan_türü) VALUES (%s, %s)"
                inserted_values = (x * y - 3 + 1, "Emlak")
                cursor = connection.cursor()
                cursor.execute(insert_table, inserted_values)
                cursor.close()
                self.buttonList[i].setText(str(i+1) + "\n" + "Alan Türü: Emlak" + "\n" + "Alan Sahibi: Yönetici" + "\n" + "Çalışan Kapasitesi: Sınırsız")
            
            else:
                insert_table = "INSERT INTO alan_bilgileri (alan_kare_no, alan_türü) VALUES (%s, %s)"
                inserted_values = (i+1, "Arsa")
                cursor = connection.cursor()
                cursor.execute(insert_table, inserted_values)
                cursor.close()
                self.buttonList[i].setText(str(i+1) + "\n" + "Alan Türü: Arsa" + "\n" + "Alan Sahibi: Yönetici")
            
                insert_table = "INSERT INTO satış_bilgileri (alan_kare_no, satış_fiyatı, komisyon, satan_emlak_no, alan_türü) VALUES (%s, %s, %s, %s, %s)"
                inserted_values = (str(i + 1), str(arsaFiyatı), str(0), str(x*y-3), "Arsa")
                cursor = connection.cursor()
                cursor.execute(insert_table, inserted_values)
                cursor.close()

        
        self.myFont.setPointSize(8)
        self.btnBuyProperty = QPushButton(self)
        self.btnBuyProperty.setText("Alan Satın Al")
        self.btnBuyProperty.setFont(self.myFont)
        self.btnBuyProperty.clicked.connect(self.buyProperty)
        self.btnBuyProperty.setFixedSize(120, 60)
        self.btnBuyProperty.move(1300, 700)
        self.btnBuyProperty.setVisible(True)
        
        
        # Kiralamak
        self.btnRentProperty = QPushButton(self)
        self.btnRentProperty.setText("Alan Kirala")
        self.btnRentProperty.setFont(self.myFont)
        self.btnRentProperty.clicked.connect(self.rentProperty)
        self.btnRentProperty.setFixedSize(120, 60)
        self.btnRentProperty.move(1300, 760)
        self.btnRentProperty.setVisible(True)
        
        
        self.btnSellProperty = QPushButton(self)
        self.btnSellProperty.setText("Satılığa Çıkar")
        self.btnSellProperty.setFont(self.myFont)
        self.btnSellProperty.clicked.connect(self.sellProperty)
        self.btnSellProperty.setFixedSize(120, 60)
        self.btnSellProperty.move(1450, 700)
        self.btnSellProperty.setVisible(True)
        
        
        # Kiraya vermek
        self.btnLetProperty = QPushButton(self)
        self.btnLetProperty.setText("Kiraya Ver")
        self.btnLetProperty.setFont(self.myFont)
        self.btnLetProperty.clicked.connect(self.letProperty)
        self.btnLetProperty.setFixedSize(120, 60)
        self.btnLetProperty.move(1450, 760)
        self.btnLetProperty.setVisible(True)
        
        
        self.btnBuyFood = QPushButton(self)
        self.btnBuyFood.setText("Yemek Al")
        self.btnBuyFood.setFont(self.myFont)
        self.btnBuyFood.clicked.connect(self.buyFood)
        self.btnBuyFood.setFixedSize(120, 60)
        self.btnBuyFood.move(1600, 700)
        self.btnBuyFood.setVisible(True)
        
        
        self.btnBuyItem = QPushButton(self)
        self.btnBuyItem.setText("Eşya Al")
        self.btnBuyItem.setFont(self.myFont)
        self.btnBuyItem.clicked.connect(self.buyItem)
        self.btnBuyItem.setFixedSize(120, 60)
        self.btnBuyItem.move(1600, 760)
        self.btnBuyItem.setVisible(True)
        
        
        self.btnIsKur = QPushButton(self)
        self.btnIsKur.setText("İşletme Kur")
        self.btnIsKur.setFont(self.myFont)
        self.btnIsKur.clicked.connect(self.Iskur)
        self.btnIsKur.setFixedSize(120, 60)
        self.btnIsKur.move(1750, 700)
        self.btnIsKur.setVisible(True)
        
        
        self.btnIsegir = QPushButton(self)
        self.btnIsegir.setText("İşe Gir")
        self.btnIsegir.setFont(self.myFont)
        self.btnIsegir.clicked.connect(self.Isegir)
        self.btnIsegir.setFixedSize(120, 60)
        self.btnIsegir.move(1750, 760)
        self.btnIsegir.setVisible(True)
        
        
        
        self.btnChangePlayer = QPushButton(self)
        self.btnChangePlayer.setText("Sıradaki Oyuncu")
        self.btnChangePlayer.setFont(self.myFont)
        self.btnChangePlayer.clicked.connect(self.changePlayer)
        self.btnChangePlayer.setFixedSize(120, 60)
        self.btnChangePlayer.move(1450, 830)
        self.btnChangePlayer.setVisible(True)
        
        
        t = threading.Thread(target= self.thread, args = ())
        t.start()
        #self.thread()
    
    
    
    def buyProperty(self):
        self.btnBuyProperty.setVisible(False)
        self.btnRentProperty.setVisible(False)
        self.btnSellProperty.setVisible(False)
        self.btnLetProperty.setVisible(False)
        self.btnBuyFood.setVisible(False)
        self.btnBuyItem.setVisible(False)
        self.btnChangePlayer.setVisible(False)
        self.btnIsKur.setVisible(False)
        self.btnIsegir.setVisible(False)
        
        cursor = connection.cursor()
        cursor.execute("SELECT alan_kare_no FROM alan_bilgileri WHERE alan_türü = %s", ("Arsa",))
        arsaList = cursor.fetchall()
        cursor.close()
        
        text = "Arsalar: "
        
        for arsa in arsaList:
            arsa = arsa[0]
            text += str(arsa) + ", "
        
        
        self.lblBuyProperty = QLabel(self)
        self.lblBuyProperty.setText(text)
        self.lblBuyProperty.setFixedSize(900, 70)
        self.lblBuyProperty.move(1200, 700)
        self.lblBuyProperty.setFont(self.myFont)
        self.lblBuyProperty.setVisible(True)
        
        self.lblBuyProperty1 = QLabel(self)
        self.lblBuyProperty1.setText("Alan no girin: ")
        self.lblBuyProperty1.setFixedSize(250, 70)
        self.lblBuyProperty1.move(1450, 750)
        self.lblBuyProperty1.setFont(self.myFont)
        self.lblBuyProperty1.setVisible(True)
        
        self.txtAlan = QLineEdit(self)
        self.txtAlan.move(1560, 760)
        self.txtAlan.resize(60, 40)
        self.txtAlan.setVisible(True)
        
        
        self.btnBuy = QPushButton(self)
        self.btnBuy.setText("Al")
        self.btnBuy.setFont(self.myFont)
        self.btnBuy.clicked.connect(self.buyProperty2)
        self.btnBuy.setFixedSize(70, 40)
        self.btnBuy.move(1520, 850)
        self.btnBuy.setVisible(True)
    
    
    
    def buyProperty2(self):  
        text = self.txtAlan.text() + " no'lu alan satın alındı"
        lblIslem = QLabel(self)
        lblIslem.setText(text)
        oyuncuList[oyunSırası-1].islemList.append(lblIslem)
        
        if len(oyuncuList[oyunSırası-1].islemList) == 1:
            oyuncuList[oyunSırası-1].islemList[-1].move(900, 600)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        else:
            y = oyuncuList[oyunSırası-1].islemList[-2].geometry().y()
            oyuncuList[oyunSırası-1].islemList[-1].move(900, y+30)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
          
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        
        cursor = connection.cursor()
        cursor.execute("SELECT komisyon FROM satış_bilgileri WHERE alan_kare_no = %s", str(self.txtAlan.text()))
        komisyon = cursor.fetchone()
        if komisyon:
            komisyon = komisyon[0]
        cursor.close()
        
        
        updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_para = %s WHERE no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(int(currPara) - int(arsaFiyatı) - int(komisyon)), str(oyunSırası)))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        
        self.lblList[oyunSırası-1][5].setText("Para: " + str(currPara))
        
        
        updateQuery = "UPDATE alan_bilgileri SET alan_sahibi_no = %s WHERE alan_kare_no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(oyunSırası), str(self.txtAlan.text())))
        cursor.close()
        
        oyuncuList[oyunSırası-1].properties.append(self.txtAlan.text())
        
        cursor = connection.cursor()
        cursor.execute("SELECT isim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        isim = cursor.fetchone()
        if isim:
            isim = isim[0]
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT soyİsim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        soyİsim = cursor.fetchone()
        if soyİsim:
            soyİsim = soyİsim[0]
        cursor.close()
        
        self.buttonList[int(self.txtAlan.text())-1].setText(str(self.txtAlan.text()) + "\n" + "Alan Türü: Arsa" + "\n" + "Alan Sahibi: " + str(isim) + " " + str(soyİsim))
        
        cursor = connection.cursor()
        cursor.execute("DELETE FROM satış_bilgileri WHERE alan_kare_no = %s",str(self.txtAlan.text()))
        cursor.close()
        connection.commit()
        
        
        self.lblBuyProperty.close()
        self.lblBuyProperty1.close()
        self.txtAlan.close()
        self.btnBuy.close()
        
        
        self.btnBuyProperty.setVisible(True)
        self.btnRentProperty.setVisible(True)
        self.btnSellProperty.setVisible(True)
        self.btnLetProperty.setVisible(True)
        self.btnBuyFood.setVisible(True)
        self.btnBuyItem.setVisible(True)
        self.btnChangePlayer.setVisible(True)
        self.btnIsKur.setVisible(True)
        self.btnIsegir.setVisible(True)
        
            
            

    
    
    def rentProperty(self):
        self.btnBuyProperty.setVisible(False)
        self.btnRentProperty.setVisible(False)
        self.btnSellProperty.setVisible(False)
        self.btnLetProperty.setVisible(False)
        self.btnBuyFood.setVisible(False)
        self.btnBuyItem.setVisible(False)
        self.btnChangePlayer.setVisible(False)
        self.btnIsKur.setVisible(False)
        self.btnIsegir.setVisible(False)
    
    
    
    def sellProperty(self):
        self.btnBuyProperty.setVisible(False)
        self.btnRentProperty.setVisible(False)
        self.btnSellProperty.setVisible(False)
        self.btnLetProperty.setVisible(False)
        self.btnBuyFood.setVisible(False)
        self.btnBuyItem.setVisible(False)
        self.btnChangePlayer.setVisible(False)
        self.btnIsKur.setVisible(False)
        self.btnIsegir.setVisible(False)
    
    
    
    def letProperty(self):
        self.btnBuyProperty.setVisible(False)
        self.btnRentProperty.setVisible(False)
        self.btnSellProperty.setVisible(False)
        self.btnLetProperty.setVisible(False)
        self.btnBuyFood.setVisible(False)
        self.btnBuyItem.setVisible(False)
        self.btnChangePlayer.setVisible(False)
        self.btnIsKur.setVisible(False)
        self.btnIsegir.setVisible(False)
        
    
            
    def buyFood(self):
        self.btnBuyProperty.setVisible(False)
        self.btnRentProperty.setVisible(False)
        self.btnSellProperty.setVisible(False)
        self.btnLetProperty.setVisible(False)
        self.btnBuyFood.setVisible(False)
        self.btnBuyItem.setVisible(False)
        self.btnChangePlayer.setVisible(False)
        self.btnIsKur.setVisible(False)
        self.btnIsegir.setVisible(False)
        
        
        cursor = connection.cursor()
        cursor.execute("SELECT alan_kare_no FROM alan_bilgileri WHERE alan_türü = %s", ("market",))
        marketList = cursor.fetchall()
        cursor.close()
        
        text = "Marketler: "
        
        for market in marketList:
            text += str(market) + ", "
        
        x = int(self.txtX.text())
        y = int(self.txtY.text())
        
        text += str(x*y-1+1)
        
        self.lblBuyFood = QLabel(self)
        self.lblBuyFood.setText(text)
        self.lblBuyFood.setFixedSize(250, 70)
        self.lblBuyFood.move(1450, 700)
        self.lblBuyFood.setFont(self.myFont)
        self.lblBuyFood.setVisible(True)
        
        self.lblBuyFood1 = QLabel(self)
        self.lblBuyFood1.setText("Market no girin: ")
        self.lblBuyFood1.setFixedSize(250, 70)
        self.lblBuyFood1.move(1450, 750)
        self.lblBuyFood1.setFont(self.myFont)
        self.lblBuyFood1.setVisible(True)
        
        self.txtMarket = QLineEdit(self)
        self.txtMarket.move(1560, 760)
        self.txtMarket.resize(60, 40)
        self.txtMarket.setVisible(True)
        
        self.lblBuyFood2 = QLabel(self)
        self.lblBuyFood2.setText("Yiyecek miktarı: ")
        self.lblBuyFood2.setFixedSize(250, 70)
        self.lblBuyFood2.move(1450, 800)
        self.lblBuyFood2.setFont(self.myFont)
        self.lblBuyFood2.setVisible(True)
    
        self.txtMarket2 = QLineEdit(self)
        self.txtMarket2.move(1560, 810)
        self.txtMarket2.resize(60, 40)
        self.txtMarket2.setVisible(True) 
        
        self.btnBuy = QPushButton(self)
        self.btnBuy.setText("Al")
        self.btnBuy.setFont(self.myFont)
        self.btnBuy.clicked.connect(self.buyFood2)
        self.btnBuy.setFixedSize(70, 40)
        self.btnBuy.move(1520, 850)
        self.btnBuy.setVisible(True)
    
    
    def buyFood2(self):
        text = self.txtMarket.text() + " no'lu marketten " + self.txtMarket2.text() + " yiyecek alındı"
        lblIslem = QLabel(self)
        lblIslem.setText(text)
        oyuncuList[oyunSırası-1].islemList.append(lblIslem)
        
        if len(oyuncuList[oyunSırası-1].islemList) == 1:
            oyuncuList[oyunSırası-1].islemList[-1].move(900, 600)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        else:
            y = oyuncuList[oyunSırası-1].islemList[-2].geometry().y()
            oyuncuList[oyunSırası-1].islemList[-1].move(900, y+30)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        
        
        miktar = int(self.txtMarket2.text())

        cursor = connection.cursor()
        cursor.execute("SELECT kalan_yemek FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currYemek = cursor.fetchone()
        if currYemek:
            currYemek = currYemek[0]
        cursor.close()
         
        updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_yemek = %s WHERE no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(int(currYemek) + int(miktar)), str(oyunSırası)))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_yemek FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currYemek = cursor.fetchone()
        if currYemek:
            currYemek = currYemek[0]
        cursor.close()
        
        self.lblList[oyunSırası-1][3].setText("Yemek: " + str(currYemek))
        
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        currPara = int(currPara)
        currPara -= miktar
        
        updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_para = %s WHERE no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(currPara), str(oyunSırası)))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        self.lblList[oyunSırası-1][5].setText("Para: " + str(currPara))
        
        self.lblBuyFood.close()
        self.lblBuyFood1.close()
        self.txtMarket.close()
        self.lblBuyFood2.close()
        self.txtMarket2.close()
        self.btnBuy.close()
        
        
        self.btnBuyProperty.setVisible(True)
        self.btnRentProperty.setVisible(True)
        self.btnSellProperty.setVisible(True)
        self.btnLetProperty.setVisible(True)
        self.btnBuyFood.setVisible(True)
        self.btnBuyItem.setVisible(True)
        self.btnChangePlayer.setVisible(True)
        self.btnIsKur.setVisible(True)
        self.btnIsegir.setVisible(True)
        
        
        
    def buyItem(self):
        self.btnBuyProperty.setVisible(False)
        self.btnRentProperty.setVisible(False)
        self.btnSellProperty.setVisible(False)
        self.btnLetProperty.setVisible(False)
        self.btnBuyFood.setVisible(False)
        self.btnBuyItem.setVisible(False)
        self.btnChangePlayer.setVisible(False)
        self.btnIsKur.setVisible(False)
        self.btnIsegir.setVisible(False)
        
        
        cursor = connection.cursor()
        cursor.execute("SELECT alan_kare_no FROM alan_bilgileri WHERE alan_türü = %s", ("mağaza",))
        mağazaList = cursor.fetchall()
        cursor.close()
        
        text = "Mağazalar: "
        
        for mağaza in mağazaList:
            text += str(mağaza) + ", "
        
        x = int(self.txtX.text())
        y = int(self.txtY.text())
        
        text += str(x*y-2+1)
        
        
        self.lblBuyItem = QLabel(self)
        self.lblBuyItem.setText(text)
        self.lblBuyItem.setFixedSize(250, 70)
        self.lblBuyItem.move(1450, 700)
        self.lblBuyItem.setFont(self.myFont)
        self.lblBuyItem.setVisible(True)
        
        self.lblBuyItem1 = QLabel(self)
        self.lblBuyItem1.setText("Mağaza no girin: ")
        self.lblBuyItem1.setFixedSize(250, 70)
        self.lblBuyItem1.move(1450, 750)
        self.lblBuyItem1.setFont(self.myFont)
        self.lblBuyItem1.setVisible(True)
        
        self.txtItem = QLineEdit(self)
        self.txtItem.move(1560, 760)
        self.txtItem.resize(60, 40)
        self.txtItem.setVisible(True)
        
        self.lblBuyItem2 = QLabel(self)
        self.lblBuyItem2.setText("Eşya miktarı: ")
        self.lblBuyItem2.setFixedSize(250, 70)
        self.lblBuyItem2.move(1450, 800)
        self.lblBuyItem2.setFont(self.myFont)
        self.lblBuyItem2.setVisible(True)
    
        self.txtItem2 = QLineEdit(self)
        self.txtItem2.move(1560, 810)
        self.txtItem2.resize(60, 40)
        self.txtItem2.setVisible(True) 
        
        self.btnBuyI = QPushButton(self)
        self.btnBuyI.setText("Al")
        self.btnBuyI.setFont(self.myFont)
        self.btnBuyI.clicked.connect(self.buyItem2)
        self.btnBuyI.setFixedSize(70, 40)
        self.btnBuyI.move(1520, 850)
        self.btnBuyI.setVisible(True)
    
    
    def buyItem2(self):
        text = self.txtItem.text() + " no'lu mağazadan " + self.txtItem2.text() + " eşya alındı"
        lblIslem = QLabel(self)
        lblIslem.setText(text)
        oyuncuList[oyunSırası-1].islemList.append(lblIslem)
        
        if len(oyuncuList[oyunSırası-1].islemList) == 1:
            oyuncuList[oyunSırası-1].islemList[-1].move(900, 600)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        else:
            y = oyuncuList[oyunSırası-1].islemList[-2].geometry().y()
            oyuncuList[oyunSırası-1].islemList[-1].move(900, y+30)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        
        
        miktar = int(self.txtItem2.text())
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_eşya FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currEşya = cursor.fetchone()
        if currEşya:
            currEşya = currEşya[0]
        cursor.close()
         
        updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_eşya = %s WHERE no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(int(currEşya) + int(miktar)), str(oyunSırası)))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_eşya FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currEşya = cursor.fetchone()
        if currEşya:
            currEşya = currEşya[0]
        cursor.close()
        
        self.lblList[oyunSırası-1][4].setText("Eşya: " + str(currEşya))
        
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        currPara = int(currPara)
        currPara -= miktar
        
        updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_para = %s WHERE no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(currPara), str(oyunSırası)))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        self.lblList[oyunSırası-1][5].setText("Para: " + str(currPara))
        
        self.lblBuyItem.close()
        self.lblBuyItem1.close()
        self.txtItem.close()
        self.lblBuyItem2.close()
        self.txtItem2.close()
        self.btnBuyI.close()
        
        self.btnBuyProperty.setVisible(True)
        self.btnRentProperty.setVisible(True)
        self.btnSellProperty.setVisible(True)
        self.btnLetProperty.setVisible(True)
        self.btnBuyFood.setVisible(True)
        self.btnBuyItem.setVisible(True)
        self.btnChangePlayer.setVisible(True)
        self.btnIsKur.setVisible(True)
        self.btnIsegir.setVisible(True)
        
        
    
    def Iskur(self):
        self.btnBuyProperty.setVisible(False)
        self.btnRentProperty.setVisible(False)
        self.btnSellProperty.setVisible(False)
        self.btnLetProperty.setVisible(False)
        self.btnBuyFood.setVisible(False)
        self.btnBuyItem.setVisible(False)
        self.btnChangePlayer.setVisible(False)
        self.btnIsKur.setVisible(False)
        self.btnIsegir.setVisible(False)

        text = "Arsalar: "
        
        for arsa in oyuncuList[oyunSırası-1].properties:
            text += arsa + ", "
        
        self.lblIskur = QLabel(self)
        self.lblIskur.setText(text)
        self.lblIskur.setFixedSize(900, 70)
        self.lblIskur.move(1500, 700)
        self.lblIskur.setFont(self.myFont)
        self.lblIskur.setVisible(True)
        
        
        self.lblIsletme = QLabel(self)
        self.lblIsletme.setText("Alan no girin: ")
        self.lblIsletme.setFixedSize(250, 70)
        self.lblIsletme.move(1450, 750)
        self.lblIsletme.setFont(self.myFont)
        self.lblIsletme.setVisible(True)
        
        self.txtIsletme = QLineEdit(self)
        self.txtIsletme.move(1560, 760)
        self.txtIsletme.resize(60, 40)
        self.txtIsletme.setVisible(True)
        
        
        self.lblMaas = QLabel(self)
        self.lblMaas.setText("Çalışan maaşını girin: ")
        self.lblMaas.setFixedSize(250, 70)
        self.lblMaas.move(1430, 800)
        self.lblMaas.setFont(self.myFont)
        self.lblMaas.setVisible(True)
        
        self.txtMaas = QLineEdit(self)
        self.txtMaas.move(1560, 805)
        self.txtMaas.resize(60, 40)
        self.txtMaas.setVisible(True)
        
        
        self.lblSaat = QLabel(self)
        self.lblSaat.setText("Çalışan saatlerini girin: ")
        self.lblSaat.setFixedSize(250, 70)
        self.lblSaat.move(1650, 800)
        self.lblSaat.setFont(self.myFont)
        self.lblSaat.setVisible(True)
        
        self.txtSaat1 = QLineEdit(self)
        self.txtSaat1.move(1800, 805)
        self.txtSaat1.resize(30, 40)
        self.txtSaat1.setVisible(True)
        
        self.txtSaat2 = QLineEdit(self)
        self.txtSaat2.move(1830, 805)
        self.txtSaat2.resize(30, 40)
        self.txtSaat2.setVisible(True)
        
        
        self.btnMarket = QPushButton(self)
        self.btnMarket.setText("Market")
        self.btnMarket.setFont(self.myFont)
        self.btnMarket.clicked.connect(self.market)
        self.btnMarket.setFixedSize(70, 40)
        self.btnMarket.move(1440, 850)
        self.btnMarket.setVisible(True)
        
        
        self.btnMagaza = QPushButton(self)
        self.btnMagaza.setText("Mağaza")
        self.btnMagaza.setFont(self.myFont)
        self.btnMagaza.clicked.connect(self.magaza)
        self.btnMagaza.setFixedSize(70, 40)
        self.btnMagaza.move(1520, 850)
        self.btnMagaza.setVisible(True)
        
        self.btnEmlak = QPushButton(self)
        self.btnEmlak.setText("Emlakçı")
        self.btnEmlak.setFont(self.myFont)
        self.btnEmlak.clicked.connect(self.emlak)
        self.btnEmlak.setFixedSize(70, 40)
        self.btnEmlak.move(1600, 850)
        self.btnEmlak.setVisible(True)
        
        
        
    def market(self):
        text = self.txtIsletme.text() + " no'lu arsaya market kuruldu"
        lblIslem = QLabel(self)
        lblIslem.setText(text)
        oyuncuList[oyunSırası-1].islemList.append(lblIslem)
           
        if len(oyuncuList[oyunSırası-1].islemList) == 1:
            oyuncuList[oyunSırası-1].islemList[-1].move(900, 600)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        else:
            y = oyuncuList[oyunSırası-1].islemList[-2].geometry().y()
            oyuncuList[oyunSırası-1].islemList[-1].move(900, y+30)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)      
        
        index = oyuncuList[oyunSırası-1].properties.index(self.txtIsletme.text())
        del oyuncuList[oyunSırası-1].properties[index]
        oyuncuList[oyunSırası-1].marketList.append(self.txtIsletme.text())
        
        cursor = connection.cursor()
        cursor.execute("SELECT isim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPlayerName = cursor.fetchone()
        if currPlayerName:
            currPlayerName = currPlayerName[0]
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT soyİsim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPlayerSurName = cursor.fetchone()
        if currPlayerSurName:
            currPlayerSurName = currPlayerSurName[0]
        cursor.close()
        
        updateQuery = "UPDATE alan_bilgileri SET alan_türü = %s WHERE alan_kare_no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str("Market"), str(self.txtIsletme.text())))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        currPara = int(currPara)
        currPara -= isletmeFiyatı
        
        updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_para = %s WHERE no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(currPara), str(oyunSırası)))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        self.lblList[oyunSırası-1][5].setText("Para: " + str(currPara))    
        self.buttonList[int(self.txtIsletme.text())-1].setText(str(self.txtIsletme.text()) + "\n" + "Alan Türü: Market" + "\n" + "Alan Sahibi: " + str(currPlayerName) + " " + str(currPlayerSurName) + "\n" + "Çalışan Kapasitesi: 3")


        insert_boyut = "INSERT INTO işletme_bilgileri (alan_kare_no, işletme_seviyesi, çalışan_kapasitesi, çalışan_sayısı, sabit_gelir_miktarı, sabit_gelir_oranı, işletme_türü, maas, başlangıç_saati, bitiş_saati) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        inserted_values = (self.txtIsletme.text(), str(1), str(3), str(0), str(50), str(50), str("Market"), str(self.txtMaas.text()), str(self.txtSaat1.text()), str(self.txtSaat2.text()))
        cursor = connection.cursor()
        cursor.execute(insert_boyut, inserted_values)
        cursor.close()
        

        self.lblIskur.close()
        self.lblIsletme.close()
        self.txtIsletme.close()
        self.btnMarket.close()
        self.btnMagaza.close()
        self.btnEmlak.close()
        self.lblMaas.close()
        self.txtMaas.close()
        self.lblSaat.close()
        self.txtSaat1.close()
        self.txtSaat2.close()
        
        self.btnBuyProperty.setVisible(True)
        self.btnRentProperty.setVisible(True)
        self.btnSellProperty.setVisible(True)
        self.btnLetProperty.setVisible(True)
        self.btnBuyFood.setVisible(True)
        self.btnBuyItem.setVisible(True)
        self.btnChangePlayer.setVisible(True)
        self.btnIsKur.setVisible(True)
        self.btnIsegir.setVisible(True)
    
    
    
    def magaza(self):
        text = self.txtIsletme.text() + " no'lu arsaya mağaza kuruldu"
        lblIslem = QLabel(self)
        lblIslem.setText(text)
        oyuncuList[oyunSırası-1].islemList.append(lblIslem)
        
        if len(oyuncuList[oyunSırası-1].islemList) == 1:
            oyuncuList[oyunSırası-1].islemList[-1].move(900, 600)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        else:
            y = oyuncuList[oyunSırası-1].islemList[-2].geometry().y()
            oyuncuList[oyunSırası-1].islemList[-1].move(900, y+30)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        
        index = oyuncuList[oyunSırası-1].properties.index(self.txtIsletme.text())
        del oyuncuList[oyunSırası-1].properties[index]
        oyuncuList[oyunSırası-1].magazaList.append(self.txtIsletme.text())
        
        cursor = connection.cursor()
        cursor.execute("SELECT isim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPlayerName = cursor.fetchone()
        if currPlayerName:
            currPlayerName = currPlayerName[0]
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT soyİsim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPlayerSurName = cursor.fetchone()
        if currPlayerSurName:
            currPlayerSurName = currPlayerSurName[0]
        cursor.close()
        
        updateQuery = "UPDATE alan_bilgileri SET alan_türü = %s WHERE alan_kare_no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str("Mağaza"), str(self.txtIsletme.text())))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        currPara = int(currPara)
        currPara -= isletmeFiyatı
        
        updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_para = %s WHERE no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(currPara), str(oyunSırası)))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        
        insert_boyut = "INSERT INTO işletme_bilgileri (alan_kare_no, işletme_seviyesi, çalışan_kapasitesi, çalışan_sayısı, sabit_gelir_miktarı, sabit_gelir_oranı, işletme_türü, maas, başlangıç_saati, bitiş_saati) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        inserted_values = (self.txtIsletme.text(), str(1), str(3), str(0), str(50), str(50), str("Market"), str(self.txtMaas.text()), str(self.txtSaat1.text()), str(self.txtSaat2.text()))
        cursor = connection.cursor()
        cursor.execute(insert_boyut, inserted_values)
        cursor.close()
        
        
        self.lblList[oyunSırası-1][5].setText("Para: " + str(currPara))    
        self.buttonList[int(self.txtIsletme.text())-1].setText(str(self.txtIsletme.text()) + "\n" + "Alan Türü: Mağaza" + "\n" + "Alan Sahibi: " + str(currPlayerName) + " " + str(currPlayerSurName) + "\n" + "Çalışan Kapasitesi: 3")    
    

        self.lblIskur.close()
        self.lblIsletme.close()
        self.txtIsletme.close()
        self.btnMarket.close()
        self.btnMagaza.close()
        self.btnEmlak.close()
        self.lblMaas.close()
        self.txtMaas.close()
        self.lblSaat.close()
        self.txtSaat1.close()
        self.txtSaat2.close()
        
        self.btnBuyProperty.setVisible(True)
        self.btnRentProperty.setVisible(True)
        self.btnSellProperty.setVisible(True)
        self.btnLetProperty.setVisible(True)
        self.btnBuyFood.setVisible(True)
        self.btnBuyItem.setVisible(True)
        self.btnChangePlayer.setVisible(True)
        self.btnIsKur.setVisible(True)
        self.btnIsegir.setVisible(True)
        
        
        
    def emlak(self):
        text = self.txtIsletme.text() + " no'lu arsaya emlakçı kuruldu"
        lblIslem = QLabel(self)
        lblIslem.setText(text)
        oyuncuList[oyunSırası-1].islemList.append(lblIslem)
        
        if len(oyuncuList[oyunSırası-1].islemList) == 1:
            oyuncuList[oyunSırası-1].islemList[-1].move(900, 600)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        else:
            y = oyuncuList[oyunSırası-1].islemList[-2].geometry().y()
            oyuncuList[oyunSırası-1].islemList[-1].move(900, y+30)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        
        index = oyuncuList[oyunSırası-1].properties.index(self.txtIsletme.text())
        del oyuncuList[oyunSırası-1].properties[index]
        oyuncuList[oyunSırası-1].emlakList.append(self.txtIsletme.text())
        
        cursor = connection.cursor()
        cursor.execute("SELECT isim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPlayerName = cursor.fetchone()
        if currPlayerName:
            currPlayerName = currPlayerName[0]
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT soyİsim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPlayerSurName = cursor.fetchone()
        if currPlayerSurName:
            currPlayerSurName = currPlayerSurName[0]
        cursor.close()
        
        updateQuery = "UPDATE alan_bilgileri SET alan_türü = %s WHERE alan_kare_no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str("Emlakçı"), str(self.txtIsletme.text())))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        currPara = int(currPara)
        currPara -= isletmeFiyatı
        
        updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_para = %s WHERE no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(currPara), str(oyunSırası)))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırası))
        currPara = cursor.fetchone()
        if currPara:
            currPara = currPara[0]
        cursor.close()
        
        
        insert_boyut = "INSERT INTO işletme_bilgileri (alan_kare_no, işletme_seviyesi, çalışan_kapasitesi, çalışan_sayısı, sabit_gelir_miktarı, sabit_gelir_oranı, işletme_türü, maas, başlangıç_saati, bitiş_saati) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        inserted_values = (self.txtIsletme.text(), str(1), str(3), str(0), str(50), str(50), str("Market"), str(self.txtMaas.text()))
        cursor = connection.cursor()
        cursor.execute(insert_boyut, inserted_values)
        cursor.close()
        
        
        self.lblList[oyunSırası-1][5].setText("Para: " + str(currPara))    
        self.buttonList[int(self.txtIsletme.text())-1].setText(str(self.txtIsletme.text()) + "\n" + "Alan Türü: Emlakçı" + "\n" + "Alan Sahibi: " + str(currPlayerName) + " " + str(currPlayerSurName) + "\n" + "Çalışan Kapasitesi: 3")
    
    
        self.lblIskur.close()
        self.lblIsletme.close()
        self.txtIsletme.close()
        self.btnMarket.close()
        self.btnMagaza.close()
        self.btnEmlak.close()
        self.lblMaas.close()
        self.txtMaas.close()
        self.lblSaat.close()
        self.txtSaat1.close()
        self.txtSaat2.close()
        
        self.btnBuyProperty.setVisible(True)
        self.btnRentProperty.setVisible(True)
        self.btnSellProperty.setVisible(True)
        self.btnLetProperty.setVisible(True)
        self.btnBuyFood.setVisible(True)
        self.btnBuyItem.setVisible(True)
        self.btnChangePlayer.setVisible(True)
        self.btnIsKur.setVisible(True)
        self.btnIsegir.setVisible(True)
        
    
    
    def Isegir(self):
        self.btnBuyProperty.setVisible(False)
        self.btnRentProperty.setVisible(False)
        self.btnSellProperty.setVisible(False)
        self.btnLetProperty.setVisible(False)
        self.btnBuyFood.setVisible(False)
        self.btnBuyItem.setVisible(False)
        self.btnChangePlayer.setVisible(False)
        self.btnIsKur.setVisible(False)
        self.btnIsegir.setVisible(False)
        

        text = "İşletmeler: "
        for oyuncu in oyuncuList:
            for market in oyuncu.marketList:
                cursor = connection.cursor()
                cursor.execute("SELECT çalışan_kapasitesi FROM işletme_bilgileri WHERE alan_kare_no = %s", str(market))
                kapasite = cursor.fetchone()
                if kapasite:
                    kapasite = kapasite[0]
                cursor.close()
                
                cursor = connection.cursor()
                cursor.execute("SELECT çalışan_sayısı FROM işletme_bilgileri WHERE alan_kare_no = %s", str(market))
                calisan = cursor.fetchone()
                if calisan:
                    calisan = calisan[0]
                cursor.close()

                if int(calisan) != int(kapasite):
                    text += market + ", "
                    
            for magaza in oyuncu.magazaList:
                cursor = connection.cursor()
                cursor.execute("SELECT çalışan_kapasitesi FROM işletme_bilgileri WHERE alan_kare_no = %s", str(magaza))
                kapasite = cursor.fetchone()
                if kapasite:
                    kapasite = kapasite[0]
                cursor.close()
                
                cursor = connection.cursor()
                cursor.execute("SELECT çalışan_sayısı FROM işletme_bilgileri WHERE alan_kare_no = %s", str(magaza))
                calisan = cursor.fetchone()
                if calisan:
                    calisan = calisan[0]
                cursor.close()

                if int(calisan) != int(kapasite):
                    text += magaza + ", "
                    
            for emlak in oyuncu.emlakList:
                cursor = connection.cursor()
                cursor.execute("SELECT çalışan_kapasitesi FROM işletme_bilgileri WHERE alan_kare_no = %s", str(emlak))
                kapasite = cursor.fetchone()
                if kapasite:
                    kapasite = kapasite[0]
                cursor.close()
                
                cursor = connection.cursor()
                cursor.execute("SELECT çalışan_sayısı FROM işletme_bilgileri WHERE alan_kare_no = %s", str(emlak))
                calisan = cursor.fetchone()
                if calisan:
                    calisan = calisan[0]
                cursor.close()

                if int(calisan) != int(kapasite):
                    text += emlak + ", "
        
        
        self.lblIsegir = QLabel(self)
        self.lblIsegir.setText(text)
        self.lblIsegir.setFixedSize(900, 70)
        self.lblIsegir.move(1500, 700)
        self.lblIsegir.setFont(self.myFont)
        self.lblIsegir.setVisible(True)
        
        
        self.lblIsyeri = QLabel(self)
        self.lblIsyeri.setText("İşletme no girin: ")
        self.lblIsyeri.setFixedSize(250, 70)
        self.lblIsyeri.move(1450, 750)
        self.lblIsyeri.setFont(self.myFont)
        self.lblIsyeri.setVisible(True)
        
        self.txtIsyeri = QLineEdit(self)
        self.txtIsyeri.move(1560, 760)
        self.txtIsyeri.resize(60, 40)
        self.txtIsyeri.setVisible(True)
        
        
        self.lblGun = QLabel(self)
        self.lblGun.setText("Gün Sayısı girin: ")
        self.lblGun.setFixedSize(250, 70)
        self.lblGun.move(1450, 800)
        self.lblGun.setFont(self.myFont)
        self.lblGun.setVisible(True)
        
        self.txtGun = QLineEdit(self)
        self.txtGun.move(1560, 805)
        self.txtGun.resize(60, 40)
        self.txtGun.setVisible(True)
        
        
        self.btnIsegir2 = QPushButton(self)
        self.btnIsegir2.setText("İşe gir")
        self.btnIsegir2.setFont(self.myFont)
        self.btnIsegir2.clicked.connect(self.Isegir2)
        self.btnIsegir2.setFixedSize(70, 40)
        self.btnIsegir2.move(1520, 850)
        self.btnIsegir2.setVisible(True)
        
    
    
    def Isegir2(self):
        cursor = connection.cursor()
        cursor.execute("SELECT çalışan_sayısı FROM işletme_bilgileri WHERE alan_kare_no = %s", str(self.txtIsyeri.text()))
        calisan = cursor.fetchone()
        cursor.close()
        if calisan:
            calisan = calisan[0]
            calisan = int(calisan) + 1
        
        
        updateQuery = "UPDATE işletme_bilgileri SET çalışan_sayısı = %s WHERE alan_kare_no = %s"
        cursor = connection.cursor()
        cursor.execute(updateQuery, (str(calisan), str(self.txtIsyeri.text())))
        cursor.close()
        
        
        
        text = self.txtIsyeri.text() + " no'lu işletmede işe girildi"
        lblIslem = QLabel(self)
        lblIslem.setText(text)
        oyuncuList[oyunSırası-1].islemList.append(lblIslem)
        
        if len(oyuncuList[oyunSırası-1].islemList) == 1:
            oyuncuList[oyunSırası-1].islemList[-1].move(900, 600)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        else:
            y = oyuncuList[oyunSırası-1].islemList[-2].geometry().y()
            oyuncuList[oyunSırası-1].islemList[-1].move(900, y+30)
            oyuncuList[oyunSırası-1].islemList[-1].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[-1].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[-1].setVisible(True)
        
        
        bitisTarihi = datetime.datetime.today() + datetime.timedelta(days = int(self.txtGun.text()))
        
        cursor = connection.cursor()
        cursor.execute("SELECT başlangıç_saati FROM işletme_bilgileri WHERE alan_kare_no = %s", str(self.txtIsyeri.text()))
        saat1 = cursor.fetchone()
        if saat1:
            saat1 = saat1[0]
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT bitiş_saati FROM işletme_bilgileri WHERE alan_kare_no = %s", str(self.txtIsyeri.text()))
        saat2 = cursor.fetchone()
        if saat2:
            saat2 = saat2[0]
        cursor.close()
            
        insert_boyut = "INSERT INTO çalışan_bilgileri (oyuncu_no, bitiş_tarihi, gün_sayısı, işletme_no, başlangıç_saati, bitiş_saati) VALUES (%s, %s, %s, %s, %s, %s)"
        inserted_values = (oyuncuList[oyunSırası-1].no, bitisTarihi, self.txtGun.text(), str(self.txtIsyeri.text()), str(saat1), str(saat2))
        cursor = connection.cursor()
        cursor.execute(insert_boyut, inserted_values)
        cursor.close()
        
        self.lblList[oyunSırası-1][6].setText("Çalıştığı Alan: "+ str(self.txtIsyeri.text()))
        
        
        cursor = connection.cursor()
        cursor.execute("SELECT maas FROM işletme_bilgileri WHERE alan_kare_no = %s", str(self.txtIsyeri.text()))
        maas = cursor.fetchone()
        if maas:
            maas = maas[0]
        cursor.close()
        
        oyuncuList[oyunSırası-1].maas = maas
    
        
        self.lblIsegir.close()
        self.lblIsyeri.close()
        self.txtIsyeri.close()
        self.btnIsegir2.close()
        self.lblGun.close()
        self.txtGun.close()
        
        self.btnBuyProperty.setVisible(True)
        self.btnRentProperty.setVisible(True)
        self.btnSellProperty.setVisible(True)
        self.btnLetProperty.setVisible(True)
        self.btnBuyFood.setVisible(True)
        self.btnBuyItem.setVisible(True)
        self.btnChangePlayer.setVisible(True)
        self.btnIsKur.setVisible(True)
        self.btnIsegir.setVisible(True)
            
    def changePlayer(self):
        global oyunSırası
        index = noList.index(oyunSırası)
        
        if index == len(noList) - 1:
            index = 0
        else:
            index += 1
            
        oyunSırası = noList[index]
        
        if oyunSırası == 1:
            for i in range(len(oyuncuList[-1].islemList)):
                oyuncuList[-1].islemList[i].setVisible(False)
                
        else:
            for i in range(len(oyuncuList[oyunSırası-2].islemList)):
                oyuncuList[oyunSırası-2].islemList[i].setVisible(False)
        

        for i in range (len(oyuncuList[oyunSırası-1].islemList)):
            oyuncuList[oyunSırası-1].islemList[i].setFixedSize(400, 30)
            oyuncuList[oyunSırası-1].islemList[i].move(900, 600+30*i)
            oyuncuList[oyunSırası-1].islemList[i].setFont(self.myFont)        
            oyuncuList[oyunSırası-1].islemList[i].setVisible(True)    
            
            
            
    def thread(self):
        global connection
        global kullanıcı_no
        
        delete = []
        curDate = datetime.datetime.today().date()
        length = len(noList)
        while(True):
            oyunSırasi = oyunSırası    
            cursor = connection.cursor()
            cursor.execute("SELECT isim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırasi))
            currPlayerName = cursor.fetchone()
            if currPlayerName:
                currPlayerName = currPlayerName[0]
            cursor.close()
            
            cursor = connection.cursor()
            cursor.execute("SELECT soyİsim FROM kullanıcı_bilgileri WHERE no = %s", str(oyunSırasi))
            currPlayerSurName = cursor.fetchone()
            cursor.close()
            if currPlayerSurName:
                currPlayerSurName = currPlayerSurName[0]
            
            self.lblCurr.setText("Oyun Sırası: " + str(currPlayerName) + " " + str(currPlayerSurName))
                   
            currDate = datetime.datetime.today().date()
            
            if currDate != curDate:
                self.fark = ((currDate - curDate).days)
                self.fark = int(self.fark)
                curDate = currDate

                for i in range(length):
                    cursor = connection.cursor()
                    cursor.execute("SELECT kalan_yemek FROM kullanıcı_bilgileri WHERE no = %s", str(oyuncuList[oyunSırasi-1].no))
                    yemek = cursor.fetchone()
                    cursor.close()
                    
                    if yemek:
                        yemek = yemek[0]
                        yemek -= (self.fark*10)
                        if yemek < 0:
                            yemek = 0
                        oyuncuList[i].food = yemek
                        
                    cursor = connection.cursor()   
                    cursor.execute("SELECT kalan_eşya FROM kullanıcı_bilgileri WHERE no = %s", str(oyuncuList[oyunSırasi-1].no))
                    eşya = cursor.fetchone()
                    cursor.close()
                    
                    if eşya:
                        eşya = eşya[0]
                        eşya -= (self.fark*10)
                        if eşya < 0:
                            eşya = 0
                        oyuncuList[i].item = eşya
                        
                    cursor = connection.cursor()    
                    cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s", str(oyuncuList[oyunSırasi-1].no))
                    para = cursor.fetchone()
                    cursor.close()
                    
                    if para:
                        para = para[0]
                        para -= (self.fark*10)
                    index = 0
                        
                    for j in range (len(oyuncuList)):
                        if oyuncuList[j].no == noList[i]:
                            index = j
                            break
                            
                    para += oyuncuList[index].maas
                    if para < 0:
                        para = 0
                    oyuncuList[i].money = para                                        
                    updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_yemek = %s, kalan_eşya = %s, kalan_para = %s WHERE no = %s"
                    cursor = connection.cursor()
                    cursor.execute(updateQuery, (str(yemek), str(eşya), str(para), str(oyuncuList[oyunSırasi-1].no)))
                    cursor.close()
                        
                    cursor = connection.cursor()
                    cursor.execute("SELECT kalan_yemek FROM kullanıcı_bilgileri WHERE no = %s",(str(oyuncuList[oyunSırasi-1].no)))
                    nyemek = cursor.fetchone()
                    cursor.close()
                    
                    if nyemek:
                        nyemek = nyemek[0]
                    self.lblList[i][3].setText("Yemek: " + str(nyemek))
                    
                    cursor = connection.cursor()
                    cursor.execute("SELECT kalan_eşya FROM kullanıcı_bilgileri WHERE no = %s",(str(oyuncuList[oyunSırasi-1].no)))
                    neşya = cursor.fetchone()
                    cursor.close()
                    
                    if neşya:
                        neşya = neşya[0]
                    self.lblList[i][4].setText("Eşya: " + str(neşya))
                    
                    cursor = connection.cursor()
                    cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s",(str(oyuncuList[oyunSırasi-1].no)))
                    npara = cursor.fetchone()
                    cursor.close()
                    if npara:
                        npara = npara[0]
                    
                    self.lblList[i][5].setText("Para: " + str(npara))    

                    if int(yemek) <= 0 or int(eşya) <= 0:
                        delete.append(i)
                    
                for j in range(len(delete)):
                    del noList[delete[j]-j]
                    del self.lblList[delete[j]-j]
                    length -= 1
                
                time.sleep(1)
                
                delete = []
                
                
                for i in range(len(oyuncuList)):   
                    for j in range(len(oyuncuList[i].marketList)):
                        cursor = connection.cursor()
                        cursor.execute("SELECT alan_türü FROM alan_bilgileri WHERE alan_kare_no = %s",(str(oyuncuList[i].marketList[j])))
                        alanTuru = cursor.fetchone()
                        cursor.close()
                        
                        if alanTuru:
                            alanTuru = alanTuru[0]
                        
                        if alanTuru != "Arsa":
                            cursor = connection.cursor()
                            cursor.execute("SELECT sabit_gelir_miktarı FROM işletme_bilgileri WHERE alan_kare_no = %s",(str(oyuncuList[i].marketList[j])))
                            sabitGelir = cursor.fetchone()
                            cursor.close()
                            
                            if sabitGelir:
                                sabitGelir = sabitGelir[0]
                            
                            cursor = connection.cursor()
                            cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s",(str(oyuncuList[i].no)))
                            currPara = cursor.fetchone()
                            cursor.close()
                            if currPara:
                                currPara = currPara[0]
                            
                            currPara = int(currPara)
                            currPara += int(sabitGelir) * self.fark
                            
                            updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_para = %s WHERE no = %s"
                            cursor = connection.cursor()
                            cursor.execute(updateQuery, (str(currPara), str(oyuncuList[i].no)))
                            oyuncuList[i].money = currPara
                            cursor.close()
                    
                    
                    for j in range(len(oyuncuList[i].magazaList)):
                        cursor = connection.cursor()
                        cursor.execute("SELECT alan_türü FROM alan_bilgileri WHERE alan_kare_no = %s",(str(oyuncuList[i].magazaList[j])))
                        alanTuru = cursor.fetchone()
                        cursor.close()
                        if alanTuru:
                            alanTuru = alanTuru[0]
                        
                        if alanTuru != "Arsa":
                            cursor = connection.cursor()
                            cursor.execute("SELECT sabit_gelir_miktarı FROM işletme_bilgileri WHERE alan_kare_no = %s",(str(oyuncuList[i].magazaList[j])))
                            sabitGelir = cursor.fetchone()
                            cursor.close()
                            if sabitGelir:
                                sabitGelir = sabitGelir[0]
                            
                            
                            cursor = connection.cursor()
                            cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s",(str(oyuncuList[i].no)))
                            currPara = cursor.fetchone()
                            cursor.close()
                            if currPara:
                                currPara = currPara[0]
                            
                            currPara = int(currPara)
                            currPara += int(sabitGelir) * self.fark

                            
                            updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_para = %s WHERE no = %s"
                            cursor = connection.cursor()
                            cursor.execute(updateQuery, (str(currPara), str(oyuncuList[i].no)))
                            oyuncuList[i].money = currPara
                            cursor.close()
                    
                    
                    
                    for j in range(len(oyuncuList[i].emlakList)):
                        cursor = connection.cursor()
                        cursor.execute("SELECT alan_türü FROM alan_bilgileri WHERE alan_kare_no = %s",(str(oyuncuList[i].emlakList[j])))
                        alanTuru = cursor.fetchone()
                        cursor.close()
                        if alanTuru:
                            alanTuru = alanTuru[0]
                        
                        if alanTuru != "Arsa":
                            cursor = connection.cursor()
                            cursor.execute("SELECT sabit_gelir_miktarı FROM işletme_bilgileri WHERE alan_kare_no = %s",(str(oyuncuList[i].emlakList[j])))
                            sabitGelir = cursor.fetchone()
                            cursor.close()
                            if sabitGelir:
                                sabitGelir = sabitGelir[0]
                            
                            
                            cursor = connection.cursor()
                            cursor.execute("SELECT kalan_para FROM kullanıcı_bilgileri WHERE no = %s",(str(oyuncuList[i].no)))
                            currPara = cursor.fetchone()
                            cursor.close()
                            if currPara:
                                currPara = currPara[0]
                            
                            currPara = int(currPara)
                            currPara += int(sabitGelir) * self.fark

                            
                            updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_para = %s WHERE no = %s"
                            cursor = connection.cursor()
                            cursor.execute(updateQuery, (str(currPara), str(oyuncuList[i].no)))
                            oyuncuList[i].money = currPara
                            cursor.close()
                    
                    
                    for oyuncu in oyuncuList:
                        if oyuncu.maas > 0:
                            cursor = connection.cursor()
                            cursor.execute("SELECT bitiş_tarihi FROM çalışan_bilgileri WHERE oyuncu_no = %s",(str(oyuncu.no)))
                            finishDate = cursor.fetchone()
                            cursor.close()
                            if finishDate:
                                finishDate = finishDate[0]
                            
                            fark = ((finishDate - datetime.datetime.today().date()).days)
                            
                            if fark <= 0:
                                cursor = connection.cursor()
                                cursor.execute("DELETE FROM çalışan_bilgileri WHERE oyuncu_no = %s",str(oyuncu.no))
                                cursor.close()
                                oyuncu.maas = 0
                    
                cursor = connection.cursor()
                cursor.execute("SELECT alan_kare_no FROM işletme_bilgileri")
                isletmeList = cursor.fetchall()
                cursor.close()
                for isletme in isletmeList:
                    isletme = isletme[0]
                    cursor = connection.cursor()
                    cursor.execute("SELECT çalışan_kapasitesi FROM işletme_bilgileri WHERE alan_kare_no = %s", (str(isletme)))
                    kapasite = cursor.fetchone()
                    cursor.close()
                    if kapasite:
                        kapasite = kapasite[0]
                        kapasite = int(kapasite)
                        
                    cursor = connection.cursor()
                    cursor.execute("SELECT çalışan_sayısı FROM işletme_bilgileri WHERE alan_kare_no = %s", (str(isletme)))
                    calisan = cursor.fetchone()
                    cursor.close()
                    if calisan:
                        calisan = calisan[0]
                        calisan = int(calisan)
                    
                    if int(calisan) == int(kapasite):
                        cursor = connection.cursor()
                        cursor.execute("SELECT tam_kapasite_gun_sayısı FROM işletme_bilgileri WHERE alan_kare_no = %s", (str(isletme)))
                        tamGun = cursor.fetchone()
                        cursor.close()
                        if tamGun:
                            tamGun = tamGun[0]
                            tamGun = int(tamGun)
                            tamGun += self.fark
                        
                        if tamGun >= 7:
                            tamGun -= 7
                            
                            updateQuery = "UPDATE işletme_bilgileri SET tam_kapasite_gun_sayısı = %s WHERE alan_kare_no = %s"
                            cursor = connection.cursor()
                            cursor.execute(updateQuery, (str(tamGun), str(isletme)))
                            cursor.close()
                                
                            kapasite *= 2
                            
                            cursor = connection.cursor()
                            cursor.execute("SELECT işletme_seviyesi FROM işletme_bilgileri WHERE alan_kare_no = %s", (str(isletme)))
                            seviye = cursor.fetchone()
                            cursor.close()
                            if seviye:
                                seviye = seviye[0]
                                seviye = int(seviye)
                                seviye += 1
                                
                            updateQuery = "UPDATE işletme_bilgileri SET işletme_seviyesi = %s WHERE alan_kare_no = %s"
                            cursor = connection.cursor()
                            cursor.execute(updateQuery, (str(seviye), str(isletme)))
                            cursor.close()
                            
                            current_date = datetime.datetime.now().date()
                            
                            updateQuery = "UPDATE işletme_bilgileri SET seviye_tarihi = %s WHERE alan_kare_no = %s"
                            cursor = connection.cursor()
                            cursor.execute(updateQuery, (current_date, str(isletme)))
                            cursor.close()
                            
                        else:
                        
                            updateQuery = "UPDATE işletme_bilgileri SET tam_kapasite_gun_sayısı = %s WHERE alan_kare_no = %s"
                            cursor = connection.cursor()
                            cursor.execute(updateQuery, (str(tamGun), str(isletme)))
                            cursor.close()
                    
                    else:
                        updateQuery = "UPDATE işletme_bilgileri SET tam_kapasite_gun_sayısı = %s WHERE alan_kare_no = %s"
                        cursor = connection.cursor()
                        cursor.execute(updateQuery, (str(0), str(isletme)))
                        cursor.close()
                    
                    
                                
                                
            cursor = connection.cursor()
            cursor.execute("SELECT işletme_no FROM çalışan_bilgileri WHERE oyuncu_no = %s", str(oyuncuList[oyunSırası-1].no))
            isyeri = None
            isyeri = cursor.fetchone()
            cursor.close()
            self.tf = True
            if isyeri:
                cursor = connection.cursor()
                cursor.execute("SELECT başlangıç_saati FROM çalışan_bilgileri WHERE oyuncu_no = %s", str(oyuncuList[oyunSırası-1].no))
                saat1 = cursor.fetchone()
                cursor.close()
                if saat1:
                    saat1 = saat1[0]
                    
                cursor = connection.cursor()
                cursor.execute("SELECT bitiş_saati FROM çalışan_bilgileri WHERE oyuncu_no = %s", str(oyuncuList[oyunSırası-1].no))
                saat2 = cursor.fetchone()
                cursor.close()
                if saat2:
                    saat2 = saat2[0]
                    
                nowSaat = datetime.datetime.now().hour
                try:
                    if int(saat1) <= int(nowSaat) and int(nowSaat) <= int(saat2):
                        self.tf = False
                    
                    self.btnBuyProperty.setEnabled(self.tf)
                    self.btnRentProperty.setEnabled(self.tf)
                    self.btnSellProperty.setEnabled(self.tf)
                    self.btnLetProperty.setEnabled(self.tf)
                    self.btnBuyFood.setEnabled(self.tf)
                    self.btnBuyItem.setEnabled(self.tf)
                    self.btnIsKur.setEnabled(self.tf)
                    self.btnIsegir.setEnabled(self.tf)
                except:
                    pass
            
            cursor = connection.cursor()
            cursor.execute("SELECT alan_kare_no FROM alan_bilgileri WHERE alan_sahibi_no = %s AND alan_türü = %s", (str(oyuncuList[oyunSırası-1].no), "Arsa"))
            arsaList = cursor.fetchall()
            cursor.close()
            
            # arsa sayısı en fazla 2 olabilir
            if len(arsaList) == 2:
                self.btnBuyProperty.setEnabled(False)
            else:
                if self.tf:
                    self.btnBuyProperty.setEnabled(True)
            
            if len(arsaList) == 0:
                self.btnIsKur.setEnabled(False)
            else:
                if self.tf:
                    self.btnIsKur.setEnabled(True)
                
            
            # 1 yerde işe girilebilir
            cursor = connection.cursor()
            cursor.execute("SELECT işletme_no FROM çalışan_bilgileri WHERE oyuncu_no = %s", str(oyuncuList[oyunSırası-1].no))
            isyeri = cursor.fetchone()
            cursor.close()
            if isyeri:
                self.btnIsegir.setEnabled(False)
            else:
                if self.tf:
                    self.btnIsegir.setEnabled(True)
            
            
            # satmak için arsa veya işletme olması lazım
            cursor = connection.cursor()
            cursor.execute("SELECT alan_kare_no FROM alan_bilgileri WHERE alan_sahibi_no = %s", str(oyuncuList[oyunSırası-1].no))
            satılık = cursor.fetchone()
            cursor.close()
            if satılık and self.tf:
                self.btnSellProperty.setEnabled(True)
            else:
                self.btnSellProperty.setEnabled(False)
                
                
            # Kiraya vermek için işletme olması lazım    
            cursor = connection.cursor()
            cursor.execute("SELECT alan_kare_no FROM alan_bilgileri WHERE alan_sahibi_no = %s AND alan_türü != %s ", (str(oyuncuList[oyunSırası-1].no), str("Arsa")))
            kiralık = cursor.fetchone()
            cursor.close()
            if kiralık and self.tf:
                self.btnLetProperty.setEnabled(True)
            else:
                self.btnLetProperty.setEnabled(False)
            
            
            
            
                
            
            

class Player:
    def __init__(self, no, first_name, last_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.food = 100
        self.item = 100
        self.money = 100
        self.no = no
        # sahip olduğu arsalar
        self.properties = []
        # sahip olduğu marketler
        self.marketList = []
        # sahip olduğu mağazalar
        self.magazaList = []
        # sahip olduğu emlaklar
        self.emlakList = []
        # Çalıştığı yer
        self.workplace = None
        self.maas = 0
        self.islemList = []

    # alan satın al
    def buy_property(self, property, price):
        if len(self.properties) < 2:
            self.properties.append(property)
            self.money -= price

    # alan sat
    def sell_property(self, property, price):
        if property in self.properties:
            self.properties.remove(property)
            self.money += price

    # alan kirala
    def rent_property(self, property, price):
        property.owner = self
        self.money -= price




                
                
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = yonetici()
    ex.show()
    sys.exit(app.exec_())