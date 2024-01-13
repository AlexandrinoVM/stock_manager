import mysql.connector
import pandas as pd
import os
import subprocess
import db
import customtkinter as ctk
from tkinter import ttk


#connect to the database
try:
    connection = db.banco.connection
    cursor = db.banco.cursor
except mysql.connector.errors.DatabaseError:
     print('failed to connect in the server')
     
#catch where the xsml archive are
file_name = 'stock_data\\stock_data.xlsx'

class product:
    def insert_product(self,product,price,quantity):
        cursor.execute('SELECT * FROM produtos Where produto = %s',[product])
        duplicates = cursor.fetchall()
        
        # see if the product already exists in the database
        if duplicates != None and duplicates  != []:
            print('--------------------------------------------------')
            print('| !product already exists in the database! |')
            print('--------------------------------------------------')
        else:   
            cursor.execute("insert into produtos(produto,preco,quantidade) values (%s,%s,%s)",(product,price,quantity))  
            connection.commit()  
    

    #delete productes from the database
    def delete_product(self,product):
        cursor.execute("delete from produtos where produto= %s",[product])
        connection.commit()
        

    #change the product values
    def update_value(self,product,price,quantity):
        cursor.execute("UPDATE produtos SET preco = %s, quantidade = %s WHERE produto = %s",(price,quantity,product))
        connection.commit()
        
    #show the data in the terminal
    def show_data(self):
        
        sql_get = 'SELECT * FROM produtos'
        cursor.execute(sql_get)
        rows = cursor.fetchall()

        dados = {
            'produto': [row[1] for row in rows],
            'preco': [row[2] for row in rows],
            'quantidade': [row[3] for row in rows]
            }
        ind = [row[0] for row in rows]
        

        dataframe = pd.DataFrame(dados,index=[ind])
        print(dataframe)
        print(type(dataframe))
        tesel = list(dataframe)
        print(tesel)
        print(type(tesel))
       
        
    def download_stock_data(self):
        #query to fetch all data in the database
        sql_get = 'SELECT * FROM produtos'
        cursor.execute(sql_get)
        rows = cursor.fetchall()
        data = {
            'product': [row[1] for row in rows],
            'price': [row[2] for row in rows],
            'quantity': [row[3] for row in rows]
            }
        
        if osFunctions.check_archive('stock_data\\stock_data.xlsx'):
            more_tabString.set('arquive already exists')
        
        else:
            osFunctions.create_excel(data)
            more_tabString.set('file downloaded with sucessefully')
            osFunctions.user_options(data,file_name)


class osFunctions:
        #use pandas to create an excel arquive if nbot exist and place in stock_data path 
        @staticmethod
        def create_excel(data):
                    sock_data = pd.DataFrame(data)
                    datatoexcel = pd.ExcelWriter('stock_data\\stock_data.xlsx')
                    sock_data.to_excel(datatoexcel)
                    datatoexcel._save()

        #arquive manipulation open archive
        @staticmethod
        def open_excel():
            if osFunctions.check_archive(file_name):
                """
                you should put your system username where is <username> at path_dir variable
                 
                """
                path_dir = 'C:\\Users\\<vxsh>\\Desktop\\estoque\\stock_data\\stock_data.xlsx'
                
                subprocess.call(path_dir,shell=True)
            else:
                more_tabString.set("archive not find/exists")
        
        #check if the arquive already exist
        @staticmethod
        def check_archive(path_arquive):
                if os.path.exists(path_arquive):       
                    return True
                    
        #user selection functions for terminal use 
        @staticmethod
        def user_options(data,file_name):
                print('type 1 to open the archive:')
                print('type 2 update:')
                print('type 3 delet:')
                choice = input('(1/2/3)?')
                if choice == '1':
                    osFunctions.open_excel()      
                elif choice == '2':
                    print('atualizar')
                    os.remove(file_name)
                    osFunctions.create_excel(data)
                elif choice == '3':
                    print('removendo arquivo..')
                    os.remove(file_name)
                    print('!arquivo removido com sucesso!')


#instance the product class
system = product()

#creating window with ctk lib
window = ctk.CTk()

#principal windoww
window.title("app teste")
window.geometry("1200x700")
window.maxsize(width=1500,height=800)
window.minsize(width=850,height=300)

#Setting the window width and height
tab_view = ctk.CTkTabview(window,width=1500,height=800)
tab_view.pack()

tab_view.add("insert")
tab_view.add("list")
tab_view.add("update")
tab_view.add("delete")
tab_view.add("more")

tab_view.tab("insert").grid_columnconfigure(0,weight=1)
tab_view.tab("list").grid_columnconfigure(0,weight=1)
tab_view.tab("update").grid_columnconfigure(0,weight=1)
tab_view.tab("delete").grid_columnconfigure(0,weight=1)
tab_view.tab("more").grid_columnconfigure(0,weight=1)

#add data to the tables
def insert_prod():
    if name.get() != "" and price.get() != "" and quantity.get() != "":
        nome = name.get()
        preco = price.get()
        quantidade = quantity.get()
        print(nome," ",preco," ",quantidade)
        string_variable.set("product inserted sucessifully")
        system.insert_product(nome,preco,int(quantidade))
    else:
         string_variable.set("all inputs need some value")


#delete data
def del_prod():
    if delete_name.get() != "" and delete_name:
          delet = delete_name.get()
          system.delete_product(delet)
          delete_string.set("value deleted")
    else:
         delete_string.set("empty value/inexistent value")
     

#update data tab
def update():
    if update_name.get() !="" and update_price.get() != "" and update_quantity.get() != "" and update_price.get().isdigit() != False or update_quantity.get().isdigit() != False:
        
        up_name = update_name.get()
        price_up =update_price.get()
        quant_update = update_quantity.get()
        
        system.update_value(up_name,price_up,quant_update)
        update_string.set("updated product")
    else:
         update_string.set("empty input/inexistent value")
    
    
        

#insert tab
title = ctk.CTkLabel(tab_view.tab("insert"),text="insert a new product")
title.pack()

name = ctk.CTkEntry(tab_view.tab("insert"),placeholder_text="product name")
name.pack(pady=15)

price = ctk.CTkEntry(tab_view.tab("insert"),placeholder_text="product price")
price.pack(pady=15)

quantity = ctk.CTkEntry(tab_view.tab("insert"),placeholder_text="product quantity")
quantity.pack(pady=15)

btn_insert = ctk.CTkButton(tab_view.tab("insert") ,text="insert",command=insert_prod)
btn_insert.pack()

#var used to print a error message in the window 
string_variable = ctk.StringVar()

error_message = ctk.CTkLabel(tab_view.tab("insert"), textvariable=string_variable)
error_message.pack()

#delete tab 
delete_title = ctk.CTkLabel(tab_view.tab("delete"),text="delete a product")
delete_title.pack()

delete_name = ctk.CTkEntry(tab_view.tab("delete"),placeholder_text="insert the product name")
delete_name.pack(pady=5)

delete_entry = ctk.CTkButton(tab_view.tab("delete"),text="delete",command=del_prod)
delete_entry.pack(pady=10)

delete_string = ctk.StringVar()

delete_error = ctk.CTkLabel(tab_view.tab("delete"),textvariable=delete_string)
delete_error.pack()

#update tab
update_title = ctk.CTkLabel(tab_view.tab("update"),text="update a product")
update_title.pack(pady=5)

update_name = ctk.CTkEntry(tab_view.tab("update"),placeholder_text="product name")
update_name.pack(pady=5)

update_price = ctk.CTkEntry(tab_view.tab("update"),placeholder_text="product price")
update_price.pack(pady=5)

update_quantity = ctk.CTkEntry(tab_view.tab("update"),placeholder_text="product quantity")
update_quantity.pack(pady=5)

#var used to print a error message in the window 
update_string = ctk.StringVar()

update_button = ctk.CTkButton(tab_view.tab("update"),text="update",command=update)
update_button.pack()

update_status = ctk.CTkLabel(tab_view.tab("update"),textvariable=update_string)
update_status.pack()

#list tab
def get_itemns():
    sql_get = 'SELECT * FROM produtos'
    cursor.execute(sql_get)
    rows = cursor.fetchall()

    for row in rows: 
        list_prod = row[1]
        list_price = row[2] 
        list_quant = row[3]
        list_data = (list_prod,list_price,list_quant)
        list_table.insert(parent='',index='end',values= list_data) 
def refresh():
    for item in list_table.get_children():
         list_table.delete(item) 
    get_itemns()

list_style = ttk.Style()
list_style.theme_use("classic")
list_style.configure("Treeview",
                     background="silver",
                     foreground="black",
                     rowheight=30,
                     fildbackground="silver",)

list_style.map("Treeview",background=[('selected','blue')])

list_table = ttk.Treeview(tab_view.tab("list"),columns=("lp","lpri","lq"),show='headings')
list_table.heading('lp',text='product')
list_table.heading('lpri',text='price')
list_table.heading('lq',text='quantity')
list_table.pack(pady=5)

list_button = ctk.CTkButton(tab_view.tab("list"),text="refresh",command=refresh)
list_button.pack()

#more options tab download/open xlsx
def download_func():
    system.download_stock_data()

def open_arquive():
    osFunctions.open_excel()


#var used to print a error message in the window 
more_tabString = ctk.StringVar()

more_tab = ctk.CTkLabel(tab_view.tab("more"),text="download options")
more_tab.pack(pady=5)

moreDownload_tab = ctk.CTkButton(tab_view.tab("more"),text="download archive", command=download_func)
moreDownload_tab.pack(pady=5)

moreOpen_tab = ctk.CTkButton(tab_view.tab("more"),text="open archive" ,command=open_arquive)
moreOpen_tab.pack(pady=5)

more_errotab = ctk.CTkLabel(tab_view.tab("more"),textvariable=more_tabString)
more_errotab.pack()

window.mainloop()