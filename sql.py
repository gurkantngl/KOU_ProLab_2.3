import psycopg2
from psycopg2 import sql, extensions
import sys

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
connection.commit()


autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
connection.set_isolation_level(autocommit)

cursor.execute("SELECT * FROM kullanıcı_bilgileri")
rows = cursor.fetchall()


def insertTable(isim, soyİsim, şifre):
    try:
        global connection
        global cursor
        global kullanıcı_no
        insert_table = "INSERT INTO kullanıcı_bilgileri (no, isim, soyİsim, şifre) VALUES (%s, %s, %s, %s)"
        inserted_values = (kullanıcı_no, isim, soyİsim, şifre)
        kullanıcı_no += 1
        cursor.execute(insert_table, inserted_values)

        count = cursor.rowcount
        print(count, ". kayıt tabloya eklendi")
        
        
        cursor.execute("SELECT * FROM kullanıcı_bilgileri")
        rows = cursor.fetchall()

        for i in range(len(rows)):
            for j in range(len(rows[i])):
                print(rows[i][j])
        
    except(Exception, psycopg2.Error) as error:
        print("PostgreSQL veri tabanına bağlanırken bir hata oluştu.: ", error)
        connection = None
    
    
def selectTable():
    try:
        global connection
        global cursor
        
        
        selectQuery = "SELECT * FROM kullanıcı_bilgileri"
        cursor.execute(selectQuery)
        users = cursor.fetchall()
        
        for user in users:
            print(user)
        
        count = cursor.rowcount
        print("Tabloda toplam: ",count, " kayıt bulunmaktadır.")
        
        
    except(Exception, psycopg2.Error) as error:
        print("PostgreSQL veri tabanına bağlanırken bir hata oluştu.: ", error)
        connection = None
    
    
 
def updateTable(no, kalan_yemek, kalan_eşya, kalan_para):
    try:
        global connection
        global cursor
        updateQuery = "UPDATE kullanıcı_bilgileri SET kalan_yemek = %s, kalan_eşya = %s, kalan_para = %s WHERE no = %s"
        cursor.execute(updateQuery, (kalan_yemek, kalan_eşya, kalan_para, no))

        count = cursor.rowcount
        print(count, " kayıt başarıyla veritabanında güncellenmiştir.")
        
    except(Exception, psycopg2.Error) as error:
        print("PostgreSQL veri tabanına bağlanırken bir hata oluştu.: ", error)
        connection = None


def menu():
    print("==============================")
    print("Hoşgeldiniz, Seçiminizi yapınız")
    print("1- Tüm Kayıtları Listele")
    print("2- Yeni Kayıt Ekle")
    print("3- Kayıt Güncelleme")
    print("4- Kayıt Silme")
    print("5- Çıkış")


def main():
    global cursor
    global connection
    while True:
        menu()
        secim = int(input("Lütfen Seçiminizi Yapınız: "))
        if secim == 1:
            selectTable()
        
        elif secim == 2:
            #no = input("no: ")
            isim = input("isim: ")
            soyİsim = input("soyİsim: ")
            şifre = input("şifre: ")
            """kalan_yemek = input("kalan_yemek: ")
            kalan_eşya = input("kalan_eşya: ")
            kalan_para = input("kalan_para: ")"""
            insertTable(isim, soyİsim, şifre)
    
        elif secim == 3:
            kullanıcı_no = input("kullanıcı_no: ")
            amount_of_food = input("amount_of_food: ")
            amount_of_stuff = input("amount_of_stuff: ")
            amount_of_money = input("amount_of_money: ")
            updateTable(kullanıcı_no, amount_of_food, amount_of_stuff, amount_of_money)

        elif secim == 4:
            kullanıcı_no = input("kullanıcı_no: ")
            deleteTable(kullanıcı_no)
    
        elif secim == 5:
            if connection != None:
                cursor.close()
                connection.close()
            print("PostgreSQL veri tabanına şu an kapatılmıştır.")
            sys.exit()
    
    
def deleteTable(kullanıcı_no):
    try:
        global connection
        global cursor
        deleteQuery = "DELETE FROM kullanıcı_bilgileri WHERE no = '{}'".format(kullanıcı_no)
        cursor.execute(deleteQuery)
        
        count = cursor.rowcount
        print(count, " kayıt başarıyla veritabanına güncellenmiştir.")
        
    except(Exception, psycopg2.Error) as error:
        print("PostgreSQL veri tabanına bağlanırken bir hata oluştu.: ", error)
        connection = None
        
main()       
        
"""    
if __name__ == "__main__":
    insertTable("Yasemin", "Egeli", "Y2001@Egeli", 100, 100, 100)
    insertTable("Gürkan", "Töngel", "gtongel553", 95, 95, 95)
    selectTable()
    updateTable("Yasemin", 90, 90, 90)
    selectTable()
    deleteTable("Gürkan")
    selectTable()
    
    if connection != None:
            cursor.close()
            connection.close()
            print("PostgreSQL veri tabanına şu an kapatılmıştır.")
"""