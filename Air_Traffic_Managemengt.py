import tkinter as tk
from tkinter import *
import random
import tkinter.font as tkFont
from tkinter import PhotoImage
from PIL import Image,ImageTk
from tkinter import messagebox
from tkinter.messagebox import askyesno
import datetime
from datetime import timedelta,date,datetime
import mysql.connector
from tkcalendar import DateEntry

login=None
menu=None
company=None
upcom=None
remcom=None
menupg=None
addcompany=None
chkusrt={"normal":'disabled',"admin":'normal'}
flag="disabled"
w=900
h=550
menubg="./Images/menupg.jpg"
companybg="./Images/companyname.jpg"
planebg="./Images/planeimg.png"
captainbg="./Images/captainpg.jpg"
loginbg="./Images/login.jpg"
flightpageimg="./Images/flightpage.png"
airportbg="./Images/airportbg.jpg"

def quitfn():
    global menu,window
    menu.destroy()
    window.deiconify()
    
def verified():
    global menupg
    menupg = Toplevel()
    window.withdraw()
    menupg.geometry(str(w)+"x"+str(h))
    menupg.title("Menu")
    dat=date.today()
    qry="select f.fid,p.pid,sum(f.ftime),max(f.fdate) from flight f,takes t,plane p where f.fid=t.fid and t.pid=p.pid and t.flag=0 and f.fdate<'{}' group by pid;".format(dat)
    cursor.execute(qry)
    table = cursor.fetchall()
    for i in table:
        fid,pid,time,da=i[0],int(i[1]),i[2],i[3]
        qr2="update plane set pflytime=pflytime+{},pflydate='{}' where pid={}".format(time,da,pid)
        qr3="update takes set flag=1 where pid={} and fid={}".format(pid,fid)
        cursor.execute(qr2)
        cursor.execute(qr3)
    con.commit()
    img= (Image.open(menubg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    imgl = tk.Label(menupg,image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    op=tk.Label(menupg, text="MENU",bg="#7ab0d8",font=('Helvetica bold', 18)).place(relx=.50, rely=.1, anchor="center")
    company = tk.Button(menupg,width=15,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", bd=5, padx=5, pady=5, text="Add Company", command=cpage).place(relx=.50, rely=.25, anchor="center")
    plane = tk.Button(menupg,width=15,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", bd=5, padx=5, pady=5, text="Add Plane", command=planepage).place(relx=.50, rely=.35, anchor="center")
    flight = tk.Button(menupg,width=15,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", bd=5, padx=5, pady=5, text="Add Flight", command=flightpage).place(relx=.50, rely=.45, anchor="center") 
    captain = tk.Button(menupg,width=15,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", bd=5, padx=5, pady=5, text="Assign Captain", command=cappage).place(relx=.50, rely=.55, anchor="center")
    airport = tk.Button(menupg,width=15,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", bd=5, padx=5, pady=5, text="Assign Airport", command=apage).place(relx=.50, rely=.65, anchor="center")
    quit = tk.Button(menupg,width=15, bd=5,activebackground="#8A2212", bg="red",activeforeground="#fff", padx=5, pady=5, text="QUIT", command=lambda :closecon(menupg)).place(relx=.50, rely=.75, anchor="center")
    tk.Button(menupg,activebackground="#8A2212", bg="red",activeforeground="#fff", text="Sign Out",command=lambda :back(window,menupg),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    menupg.protocol("WM_DELETE_WINDOW",lambda :closecon(menupg))
    menupg.resizable(False,False)
    menupg.mainloop()
    
def back(x,y):
    x.deiconify()
    y.withdraw()
    
def cpage():
    menupg.withdraw()
    global company
    company=Toplevel()#tk.Tk()
    company.geometry(str(w)+"x"+str(h))
    company.title("Plane Company")
    img= (Image.open(companybg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(company,image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Label(company,text="Company Page",bg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    addcom= tk.Button(company,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Add new Company detail",command=addcomp,width=25, bd=5,padx=5, pady=5).place(relx=.5,rely=.3,anchor='center')
    modcom= tk.Button(company,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"),activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Modify old Company detail",command=upcompage,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.4,anchor='center')
    delcom= tk.Button(company,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"),activebackground="#8A2212", bg="red",activeforeground="#fff", text="Delete old company detail",command=remcompage,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.5,anchor='center')
    shocom= tk.Button(company,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"),activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Show Company table",command=showtable,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.6,anchor='center')
    tk.Button(company,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(menupg,company),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    company.protocol("WM_DELETE_WINDOW",lambda :closecon(company))
    company.resizable(False,False)
    company.mainloop()

def showtable():
    global company,showcom
    showcom=Toplevel()#tk.Tk()
    cursor = con.cursor()
    query1 = "select * from company"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    company.withdraw()
    showcom.geometry(str(w)+"x"+str(h))
    showcom.title("Company Table Details")
    img= (Image.open(companybg))
    global new_image
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(showcom, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Label(showcom, text="All Company Data",bg="#f87984",fg="black",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(showcom, text="Select Data :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i)[1:-1] for i in table]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    
    def updateopt(o):
        n,vname,vadd,vphone=o.split(",")
        compreg = tk.Label(showcom, text="Comp Regno/id :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        compreg_val = Entry(showcom,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        name = tk.Label(showcom, text="Comp Name :",bg="#f87984",fg="black",font=('Helvetica bold', 12))
        name.place(relx=.40, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(vname[2:-1])
        compname_val = Entry(showcom,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.4, anchor="center")
        phone = tk.Label(showcom, text="Comp Phone :",bg="#f87984",fg="black",font=('Helvetica bold', 12))
        phone.place(relx=.40, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(vphone[2:-1])
        compphone_val = Entry(showcom,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.5, anchor="center")
        add = tk.Label(showcom, text="Comp Address :",bg="#f87984",fg="black",font=('Helvetica bold', 12))
        add.place(relx=.40, rely=.6, anchor="center")
        mystr = StringVar()
        mystr.set(vadd[2:-1])
        compadd_val = Entry(showcom,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.6, anchor="center")
        fin= tk.Button(showcom,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Done",font=('Helvetica bold', 14),command=doneshow,width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.75,anchor='center')
    
    drop = OptionMenu( showcom, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#f87984",fg="black",activebackground="#f87984")
    drop["menu"].config(bg="white",activebackground="#f87984",activeforeground="white")
    drop.place(relx=.55,rely=.2,anchor='center')
    tk.Button(showcom,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",text="Back",command=lambda :back(company,showcom),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    showcom.protocol("WM_DELETE_WINDOW",lambda :closecon(showcom))
    showcom.resizable(False,False)
    showcom.mainloop()

def doneshow():
    global company,showcom
    company.deiconify()
    showcom.destroy()

def addcomptocpge(a,b,c,d):
    a=a
    b=b.get()
    c=c.get()
    d=d.get()
    tk.Button(company,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(addcompany,company),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    query1 = "insert into company values({},'{}','{}',{})".format(a,b,c,d)
    table=[]
    try:
        cursor.execute(query1)
    except Exception as e:
        messagebox.showerror("Error",e)
        return
    con.commit()
    messagebox.showinfo("Done","Added")
    addcompany.destroy()
    company.deiconify()
    
def addcomp():
    global addcompany
    global company
    global w,h
    cursor = con.cursor()
    query1 = "select * from company"
    cursor.execute(query1)
    table = cursor.fetchall()
    idset=set([i[0] for i in table])
    n=random.randrange(3000,4000)
    while n in idset:n=random.randrange(20)
    mystr = tk.StringVar()
    mystr.set(n)
    addcompany = Toplevel()#tk.Tk()
    window.withdraw()
    menupg.withdraw()
    company.withdraw()
    addcompany.geometry(str(w)+"x"+str(h))
    addcompany.title("Add New Company")
    img= (Image.open(companybg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    op=tk.Label(addcompany, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    op=tk.Label(addcompany, text="Add a new Company",bg="#f87984",fg="black",font=('Helvetica bold', 18)).place(relx=.50, rely=.1, anchor="center")
    compreg = tk.Label(addcompany, text="Comp Regno/id :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.40, rely=.2, anchor="center")
    compreg_val = tk.Entry(addcompany,bg="#f88e79",fg="black",text=mystr,state=DISABLED).place(relx=.60, rely=.2, anchor="center")
    compname = tk.Label(addcompany, text="Comp Name :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
    name = tk.Entry(addcompany,bg="#f88e79",fg="black")
    name.place(relx=.60, rely=.3, anchor="center")
    compphone = tk.Label(addcompany, text="Comp Phone :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
    phone = tk.Entry(addcompany,bg="#f88e79",fg="black")
    phone.place(relx=.60, rely=.4, anchor="center")
    compadd = tk.Label(addcompany, text="Comp Address :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.40, rely=.5, anchor="center")
    add = tk.Entry(addcompany,bg="#f88e79",fg="black")
    add.place(relx=.60, rely=.5, anchor="center")
    addcompbtn = tk.Button(addcompany,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",width=15, bd=5, padx=5, pady=5, text="Submit", command=lambda :addcomptocpge(n,name,add,phone)).place(relx=.50, rely=.7, anchor="center")
    tk.Button(addcompany,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(company,addcompany),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    addcompany.protocol("WM_DELETE_WINDOW",lambda :closecon(addcompany))
    addcompany.resizable(False,False)
    addcompany.mainloop()

def confirm(n):
    global company,remcom
    answer = askyesno(title='confirmation',message='Are you sure that you want to delete?')
    if answer==True:
        query1 = "delete from company where compid={}".format(n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Deleted")
        company.deiconify()
        remcom.destroy()
        
def confirmupd(n,a,b,c):
    global company,upcom
    answer = askyesno(title='confirmation',message='Are you sure that you want to Update?')
    if answer==True:
        query1 = "update company set compname='{}' , compadd='{}', comptel={} where compid={} ".format(a,b,c,n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Updated")
        company.deiconify()
        upcom.destroy()
        
def remcompage():
    global company,remcom
    remcom=Toplevel()#tk.Tk()
    cursor = con.cursor()
    query1 = "select * from company"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    company.withdraw()
    remcom.geometry(str(w)+"x"+str(h))
    remcom.title("Remove Company")
    img= (Image.open(companybg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(remcom, image=new_image).place(x=0, y=0, relwidth=1, relheight=1) 
    tk.Label(remcom, text="Remove Company Data",bg="#f87984",fg="black",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(remcom, text="Select Data :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i)[1:-1] for i in table]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
     
    def updateopt(o):
        n,vname,vadd,vphone=o.split(",")
        compreg = tk.Label(remcom, text="Comp Regno/id :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        compreg_val = Entry(remcom,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        name = tk.Label(remcom, text="Comp Name :",bg="#f87984",fg="black",font=('Helvetica bold', 12))
        name.place(relx=.40, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(vname[2:-1])
        compname_val = Entry(remcom,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.4, anchor="center")
        phone = tk.Label(remcom, text="Comp Phone :",bg="#f87984",fg="black",font=('Helvetica bold', 12))
        phone.place(relx=.40, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(vphone)
        compphone_val = Entry(remcom,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.5, anchor="center")
        add = tk.Label(remcom, text="Comp Address :",bg="#f87984",fg="black",font=('Helvetica bold', 12))
        add.place(relx=.40, rely=.6, anchor="center")
        mystr = StringVar()
        mystr.set(vadd[2:-1])
        compadd_val = Entry(remcom,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.6, anchor="center")
        fin= tk.Button(remcom,activebackground="#8A2212", bg="red",activeforeground="#fff", text="Remove",font=('Helvetica bold', 14),command=lambda :confirm(n),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.75,anchor='center')
    
    drop = OptionMenu( remcom, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#f87984",fg="black",activebackground="#f87984")
    drop["menu"].config(bg="white",activebackground="#f87984",activeforeground="white")
    drop.place(relx=.55,rely=.2,anchor='center')
    tk.Button(remcom,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(company,remcom),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    remcom.protocol("WM_DELETE_WINDOW",lambda :closecon(remcom))
    remcom.resizable(False,False)
    remcom.mainloop()

def upcompage():
    global company,upcom
    upcom=Toplevel()#tk.Tk()
    cursor = con.cursor()
    query1 = "select * from company"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    company.withdraw()
    upcom.geometry(str(w)+"x"+str(h))
    upcom.title("Update Company")
    img= (Image.open(companybg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(upcom, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Label(upcom, text="Update Company Data",bg="#f87984",fg="black",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(upcom, text="Select Data :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i)[1:-1] for i in table]
    pclicked = StringVar()
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    
    def updateopt(o):
        def chng(o,n):
            n=o
        n,vname,vadd,vphone=o.split(",")
        compreg = tk.Label(upcom, text="Comp Regno/id :",bg="#f87984",fg="black",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        compreg_val = Entry(upcom,bg="#f88e79",fg="black",textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        name = tk.Label(upcom, text="Comp Name :",bg="#f87984",fg="black",font=('Helvetica bold', 12))
        name.place(relx=.40, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(vname[2:-1])
        vname = Entry(upcom,bg="#f88e79",fg="black",textvariable=mystr)
        vname.place(relx=.60, rely=.4, anchor="center")
        phone = tk.Label(upcom, text="Comp Phone :",bg="#f87984",fg="black",font=('Helvetica bold', 12))
        phone.place(relx=.40, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(vphone[2:-1])
        vphone = Entry(upcom,bg="#f88e79",fg="black",textvariable=mystr)
        vphone.place(relx=.60, rely=.5, anchor="center")
        add = tk.Label(upcom, text="Comp Address :",bg="#f87984",fg="black",font=('Helvetica bold', 12))
        add.place(relx=.40, rely=.6, anchor="center")
        mystr = StringVar()
        mystr.set(vadd[2:-1])
        vadd = Entry(upcom,bg="#f88e79",fg="black",textvariable=mystr)
        vadd.place(relx=.60, rely=.6, anchor="center")
        fin= tk.Button(upcom,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Update",font=('Helvetica bold', 14),command=lambda :confirmupd(n,vname.get(),vadd.get(),vphone.get()),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.75,anchor='center')
        
    drop = OptionMenu( upcom, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#f87984",fg="black",activebackground="#f87984")
    drop["menu"].config(bg="white",activebackground="#f87984",activeforeground="white")
    drop.place(relx=.55,rely=.2,anchor='center')
    tk.Button(upcom,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(company,upcom),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    upcom.protocol("WM_DELETE_WINDOW",lambda :closecon(upcom))
    upcom.resizable(False,False)
    upcom.mainloop()
    
def planepage():
    menupg.withdraw()
    global plane
    plane=Toplevel()#tk.Tk()
    plane.geometry(str(w)+"x"+str(h))
    plane.title("Plane Detail")
    img= (Image.open(planebg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(plane,image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Label(plane,text="Plane Page",bg="#1D005A",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    addplane= tk.Button(plane,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Add new Plane detail",command=addplanedet,width=25, bd=5,padx=5, pady=5).place(relx=.5,rely=.3,anchor='center')
    modplane= tk.Button(plane,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"),activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Modify old Plane detail",command=modplanedet,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.4,anchor='center')
    delplane= tk.Button(plane,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"),activebackground="#8A2212", bg="red",activeforeground="#fff", text="Delete old Plane detail",command=delplanedet,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.5,anchor='center')
    shoplane= tk.Button(plane,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"),activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Show Plane table",command=showplanetable,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.6,anchor='center')
    tk.Button(plane,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(menupg,plane),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    plane.protocol("WM_DELETE_WINDOW",lambda :closecon(plane))
    plane.resizable(False,False)
    plane.mainloop()

def addplanedet():
    global addplane
    global plane
    window.withdraw()
    menupg.withdraw()
    plane.withdraw()
    cursor = con.cursor()
    query1 = "select * from plane"
    cursor.execute(query1)
    table = cursor.fetchall()
    idset=set([i[0] for i in table])
    n=random.randrange(1000,2000)
    while n in idset:n=random.randrange(20)
    query2 = "select compid,compname from company"
    cursor.execute(query2)
    table2 = cursor.fetchall()
    mystr = tk.StringVar()
    mystr.set(n)
    addplane = Toplevel()
    addplane.geometry(str(w)+"x"+str(h))
    addplane.title("Add New Plane")
    img= (Image.open(planebg))
    global new_image
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(addplane, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    op=tk.Label(addplane, text="Add a new Plane",bg="#1D005A",fg="white",font=('Helvetica bold', 18)).place(relx=.50, rely=.1, anchor="center")
    tk.Label(addplane, text="Select Company :",bg="#DD0074",fg="white",font=('Helvetica bold', 12)).place(relx=.3,rely=.7,anchor='center')
    options = [str(i)[1:-1] for i in table2]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0

    def updateopt(o):
        global compid
        compid,name=o.split(",")
    drop = OptionMenu( addplane, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#620063",fg="white",activebackground="#620063",activeforeground="white")
    drop["menu"].config(bg="white",activebackground="#DD0074")
    drop.place(relx=.55,rely=.7,anchor='center')
    planereg = tk.Label(addplane, text="Plane Regno/id : ",bg="#5175A6",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.2, anchor="center")
    planereg_val = tk.Entry(addplane,text=mystr,state=DISABLED).place(relx=.60, rely=.2, anchor="center")
    planenum = tk.Label(addplane, text="Plane No. :",bg="#380063",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
    pnum = tk.Entry(addplane)
    pnum.place(relx=.60, rely=.3, anchor="center")
    planeType = tk.Label(addplane, text="Plane Type :",bg="#620063",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
    ptype = tk.Entry(addplane)
    ptype.place(relx=.60, rely=.4, anchor="center")
    planeFlydate = tk.Label(addplane, text="Plane Flydate :",bg="#DD0074",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.5, anchor="center")
    mystr = StringVar()
    mystr.set("00-00-0000")
    pflydate = tk.Entry(addplane,text=mystr,state=DISABLED)
    pflydate.place(relx=.60, rely=.5, anchor="center")
    planeFlytime = tk.Label(addplane, text="Plane Flytime :",bg="#DD0074",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.6, anchor="center")
    mystr = StringVar()
    mystr.set("0")
    pflytime = tk.Entry(addplane,text=mystr,state=DISABLED)
    pflytime.place(relx=.60, rely=.6, anchor="center")
    addcompbtn = tk.Button(addplane,width=15,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", bd=5, padx=5, pady=5, text="Submit", command=lambda :addplanetocpge(n,pnum,ptype,pflydate,pflytime,compid)).place(relx=.50, rely=.9, anchor="center")
    addplane.protocol("WM_DELETE_WINDOW",lambda :closecon(addplane))
    tk.Button(addplane,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(plane,addplane),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    addplane.resizable(False,False)
    addplane.mainloop()

def confirmupdplane(n,pnum,ptype,pflydate,pflytime,compid):
    global plane,upplane
    answer = askyesno(title='confirmation',message='Are you sure that you want to Update?')
    if answer==True:
        query1 = "update plane set pno='{}' , ptype='{}', pflydate={}, pflytime={}, compid={} where pid={} ".format(pnum,ptype,f"\"{datetime.strptime(pflydate, '%Y-%m-%d').date()}\"",pflytime,compid,n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Updated")
        plane.deiconify()
        upplane.destroy()

def confirmdelplane(n):
    global plane,remplane
    answer = askyesno(title='confirmation',message='Are you sure that you want to delete?')
    if answer==True:
        query1 = "delete from plane where pid={}".format(n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Deleted")
        plane.deiconify()
        remplane.destroy()

def showplanetable():
    global plane,showplane
    showplane=Toplevel()
    cursor = con.cursor()
    query1 = "select * from plane"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    plane.withdraw()
    showplane.geometry(str(w)+"x"+str(h))
    showplane.title("Plane Table Details")
    img= (Image.open(planebg))
    global new_image
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(showplane, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Label(showplane, text="All Plane Data",bg="#1F0060",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(showplane, text="Select Data :",bg="#5A81AD",fg="white",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i)[1:-1] for i in table]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    tk.Button(showplane,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(plane,showplane),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')

    def updateopt(o):
        def chng(o,n):
            n=o
        n,pnum,ptype,pflydateyear,pflydatemonth,pflydateday,m,w,pflytime,pcompid=o.split(",")
        planereg = tk.Label(showplane, text="Plane Regno/id :",bg="#31005D",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        planereg_val = Entry(showplane,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        pnumb = tk.Label(showplane, text="Plane no. :",bg="#650065",fg="white",font=('Helvetica bold', 12))
        pnumb.place(relx=.40, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(pnum)
        pnum_val = Entry(showplane,textvariable=mystr,state=DISABLED)
        pnum_val.place(relx=.60, rely=.4, anchor="center")
        ptypee = tk.Label(showplane, text="Plane Type :",bg="#AA0064",fg="white",font=('Helvetica bold', 12))
        ptypee.place(relx=.40, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(ptype[2:-1])
        ptype_val = Entry(showplane,textvariable=mystr,state=DISABLED)
        ptype_val.place(relx=.60, rely=.5, anchor="center")
        pflydatel = tk.Label(showplane, text="Plane Flydate :",bg="#D0005F",fg="white",font=('Helvetica bold', 12))
        pflydatel.place(relx=.40, rely=.6, anchor="center")
        mystr = StringVar()
        z,y=pflydateyear.split(".")
        myval=y.split("(")
        mystr.set(pflydateday+"-"+pflydatemonth+"-"+myval[1])
        pflydate_val = Entry(showplane,textvariable=mystr,state=DISABLED)
        pflydate_val.place(relx=.60, rely=.6, anchor="center")
        pflytimel = tk.Label(showplane, text="Plane Flytime :",bg="#D40072",fg="white",font=('Helvetica bold', 12))
        pflytimel.place(relx=.40, rely=.7, anchor="center")
        mystr = StringVar()
        mystr.set(pflytime)
        pflytime_val = Entry(showplane,textvariable=mystr,state=DISABLED)
        pflytime_val.place(relx=.60, rely=.7, anchor="center")
        pfcompid = tk.Label(showplane, text="Plane CompanyId :",bg="#E00061",fg="white",font=('Helvetica bold', 12))
        pfcompid.place(relx=.40, rely=.8, anchor="center")
        mystr = StringVar()
        mystr.set(pcompid)
        pfcompid_val = Entry(showplane,textvariable=mystr,state=DISABLED)
        pfcompid_val.place(relx=.60, rely=.8, anchor="center")
        fin= tk.Button(showplane,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Done",font=('Helvetica bold', 14),command=lambda :doneplaneshow(),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.9,anchor='center')
    drop = OptionMenu( showplane, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#650065",fg="white",activebackground="#650065",activeforeground="white")
    drop["menu"].config(bg="white",activebackground="#D0005F")
    drop.place(relx=.55,rely=.2,anchor='center')
    showplane.protocol("WM_DELETE_WINDOW",lambda :closecon(showplane))
    showplane.resizable(False,False)
    showplane.mainloop()

def doneplaneshow():
    global plane,showplane
    plane.deiconify()
    showplane.destroy()

def addplanetocpge(a,b,c,d,e,f):
    b=b.get()
    c=c.get()
    d=d.get()
    e=e.get()
    new="0000-00-00".replace(" ","")
    query1 = "insert into plane values({},{},'{}','{}', {},{})".format(a,int(b),c,date.today(),int(e),int(f))
    table=[]
    try:
        cursor.execute(query1)
    except Exception as e:
        messagebox.showerror("Error",e)
        return
    con.commit()
    messagebox.showinfo("Done","Added")
    addplane.destroy()
    plane.deiconify()

def modplanedet():
    global plane,upplane
    upplane=Toplevel()#tk.Tk()
    cursor = con.cursor()
    query1 = "select * from plane"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    plane.withdraw()
    upplane.geometry(str(w)+"x"+str(h))
    upplane.title("Update Plane")
    query2 = "select compid,compname from company"
    cursor.execute(query2)
    table2 = cursor.fetchall()
    img= (Image.open(planebg))
    global new_image
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(upplane, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Label(upplane, text="Update Plane Data",bg="#1D005A",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(upplane, text="Select Data :",bg="#5175A6",fg="white",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i)[1:-1] for i in table]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    tk.Button(upplane,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(plane,upplane),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    
    def updateopt(o):
        tk.Label(upplane, text="Select Company :",bg="#CD005E",fg="white",font=('Helvetica bold', 12)).place(relx=.3,rely=.8,anchor='center')
        optionspl = [str(i)[1:-1] for i in table2]
        clicked = StringVar()
        clicked.set("Select an Option")
        global op
        op=0
        
        def updateoptpl(op):
            global compid
            compid,name=op.split(",")
            
        drop = OptionMenu( upplane, clicked , *optionspl,command=updateoptpl)
        drop.config(width=30,bg="#620063",fg="white",activebackground="#620063",activeforeground="white")
        drop["menu"].config(bg="white",activebackground="#DD0074",activeforeground="white")
        drop.place(relx=.55,rely=.8,anchor='center')
        
        def chng(o,n):n=o
            
        n,pnum,ptype,pflydateyear,pflydatemonth,pflydateday,m,w,pflytime,pcompid=o.split(",")
        planereg = tk.Label(upplane, text="Plane Regno/id :",bg="#3D0062",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        planereg_val = Entry(upplane,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        pnumb = tk.Label(upplane, text="Plane no. :",bg="#690067",fg="white",font=('Helvetica bold', 12))
        pnumb.place(relx=.40, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(pnum)
        pnum_val = Entry(upplane,textvariable=mystr)
        pnum_val.place(relx=.60, rely=.4, anchor="center")
        ptypee = tk.Label(upplane, text="Plane Type :",bg="#B20066",fg="white",font=('Helvetica bold', 12))
        ptypee.place(relx=.40, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(ptype[2:-1])
        ptype_val = Entry(upplane,textvariable=mystr)
        ptype_val.place(relx=.60, rely=.5, anchor="center")
        pflydatel = tk.Label(upplane, text="Plane Flydate :",bg="#CD005E",fg="white",font=('Helvetica bold', 12))
        pflydatel.place(relx=.40, rely=.6, anchor="center")
        mystr = StringVar()
        z,y=pflydateyear.split(".")
        myval=y.split("(")
        mystr.set(pflydateday+"-"+pflydatemonth+"-"+myval[1])
        pflydate_val = Entry(upplane,textvariable=mystr,state=DISABLED)
        pflydate_val.place(relx=.60, rely=.6, anchor="center")
        pflytimel = tk.Label(upplane, text="Plane Flytime :",bg="#CD005E",fg="white",font=('Helvetica bold', 12))
        pflytimel.place(relx=.40, rely=.7, anchor="center")
        mystr = StringVar()
        mystr.set(pflytime)
        pflytime_val = Entry(upplane,textvariable=mystr,state=DISABLED)
        pflytime_val.place(relx=.60, rely=.7, anchor="center")
        new = myval[1]+"-"+pflydatemonth+"-"+pflydateday
        new = new.replace(" ","")
        fin= tk.Button(upplane,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Update",font=('Helvetica bold', 14),command=lambda :confirmupdplane(n,pnum_val.get(),ptype_val.get(),str(new),pflytime_val.get(),compid),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.9,anchor='center')
    drop = OptionMenu( upplane, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#690067",fg="white",activebackground="#690067")
    drop["menu"].config(bg="white",activebackground="#690067")
    drop.place(relx=.55,rely=.2,anchor='center')
    upplane.protocol("WM_DELETE_WINDOW",lambda :closecon(upplane))
    upplane.resizable(False,False)
    upplane.mainloop()

def delplanedet():
    global plane,remplane
    remplane=Toplevel()#tk.Tk()
    cursor = con.cursor()
    query1 = "select * from plane"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    plane.withdraw()
    remplane.geometry(str(w)+"x"+str(h))
    remplane.title("Remove Plane")
    img= (Image.open(planebg))
    global new_image
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(remplane, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Label(remplane,text="Remove Plane Data", bg="#1F0060",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(remplane, text="Select Data :",bg="#5A81AD",fg="white",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i)[1:-1] for i in table]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    tk.Button(remplane,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(plane,remplane),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')

    def updateopt(o):
        def chng(o,n):n=o
        n,pnum,ptype,pflydateyear,pflydatemonth,pflydateday,m,w,pflytime,pcompid=o.split(",")
        planereg = tk.Label(remplane, text="Plane Regno/id :",bg="#31005D",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        planereg_val = Entry(remplane,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        pnumb = tk.Label(remplane, text="Plane no. :",bg="#650065",fg="white",font=('Helvetica bold', 12))
        pnumb.place(relx=.40, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(pnum)
        pnum_val = Entry(remplane,textvariable=mystr,state=DISABLED)
        pnum_val.place(relx=.60, rely=.4, anchor="center")
        ptypee = tk.Label(remplane, text="Plane Type :",bg="#AA0064",fg="white",font=('Helvetica bold', 12))
        ptypee.place(relx=.40, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(ptype[2:-1])
        ptype_val = Entry(remplane,textvariable=mystr,state=DISABLED)
        ptype_val.place(relx=.60, rely=.5, anchor="center")
        pflydatel = tk.Label(remplane, text="Plane Flydate :",bg="#D0005F",fg="white",font=('Helvetica bold', 12))
        pflydatel.place(relx=.40, rely=.6, anchor="center")
        mystr = StringVar()
        z,y=pflydateyear.split(".")
        myval=y.split("(")
        mystr.set(pflydateday+"-"+pflydatemonth+"-"+myval[1])
        pflydate_val = Entry(remplane,textvariable=mystr,state=DISABLED)
        pflydate_val.place(relx=.60, rely=.6, anchor="center")
        pflytimel = tk.Label(remplane, text="Plane Flytime :",bg="#D40072",fg="white",font=('Helvetica bold', 12))
        pflytimel.place(relx=.40, rely=.7, anchor="center")
        mystr = StringVar()
        mystr.set(pflytime)
        pflytime_val = Entry(remplane,textvariable=mystr,state=DISABLED)
        pflytime_val.place(relx=.60, rely=.7, anchor="center")
        pfcompid = tk.Label(remplane, text="Plane CompanyId :",bg="#E00061",fg="white",font=('Helvetica bold', 12))
        pfcompid.place(relx=.40, rely=.8, anchor="center")
        mystr = StringVar()
        mystr.set(pcompid)
        pfcompid_val = Entry(remplane,textvariable=mystr,state=DISABLED)
        pfcompid_val.place(relx=.60, rely=.8, anchor="center")
        fin= tk.Button(remplane,activebackground="#8A2212", bg="red",activeforeground="#fff", text="Delete",font=('Helvetica bold', 14),command=lambda :confirmdelplane(n),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.9,anchor='center')
    drop = OptionMenu( remplane, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#650065",fg="white",activebackground="#650065",activeforeground="white")
    drop["menu"].config(bg="white",activebackground="#D0005F")
    drop.place(relx=.55,rely=.2,anchor='center')
    remplane.protocol("WM_DELETE_WINDOW",lambda :closecon(remplane))
    remplane.resizable(False,False)
    remplane.mainloop()

def flightpage():
    img= (Image.open(flightpageimg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    menupg.withdraw()
    global flight
    flight=Toplevel()#tk.Tk()
    flight.geometry(str(w)+"x"+str(h))
    flight.title("Flight Detail")
    tk.Label(flight, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Button(flight, text="Back",command=lambda :back(menupg,flight),activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    tk.Label(flight, text="Flight Page",activebackground="#1a4a0f", bg="#00c6f7",activeforeground="#fff",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    addplane= tk.Button(flight, text="Add new Flight detail",activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",command=addflightdet,width=25, bd=5,padx=5, pady=5).place(relx=.5,rely=.3,anchor='center')
    modplane= tk.Button(flight,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"), text="Modify old Flight detail",activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",command=modflightdet,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.4,anchor='center')
    delplane= tk.Button(flight,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"), text="Delete old Flight detail",activebackground="#8A2212", bg="red",activeforeground="#fff",command=delflightdet,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.5,anchor='center')
    shoplane= tk.Button(flight,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"), text="Show Flight table",activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",command=showflighttable,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.6,anchor='center')
    flight.protocol("WM_DELETE_WINDOW",lambda :closecon(flight))
    flight.resizable(False,False)
    flight.mainloop()

def addflightdet():
    global addflight
    global flight,flightavl
    window.withdraw()
    menupg.withdraw()
    flight.withdraw()
    img= (Image.open(flightpageimg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    cursor = con.cursor()
    query1 = "select * from flight"
    cursor.execute(query1)
    table = cursor.fetchall()
    idset=set([i[0] for i in table])
    n=random.randrange(100,200)
    while n in idset:n=random.randrange(20)
    query2 = "select aname,aid, type, tid from airport "
    cursor.execute(query2)
    table2 = cursor.fetchall()
    query3 = "select aname,aid, type, tid from airport "
    cursor.execute(query3)
    table3 = cursor.fetchall()
    query3 = "select pid,ptype from plane "
    cursor.execute(query3)
    tablepl = cursor.fetchall()
    dpl={}
    for i in tablepl:dpl["{} Plane with plane no. {}".format(i[1],i[0])]=i[0]
    mystr = tk.StringVar()
    mystr.set(n)
    addflight = Toplevel()
    addflight.geometry(str(w)+"x"+str(h))
    tk.Label(addflight, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    addflight.title("Add New Flight")
    op=tk.Label(addflight, text="Add a new Flight",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 18)).place(relx=.50, rely=.1, anchor="center")
    global kpt
    tk.Label(addflight, text="Select Plane :",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.75,rely=.2,anchor='center')
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    
    def updatepln(o):
        global fnum,fdur,totpass,flightdept,opt
        opt=dpl[o]
        flightreg = tk.Label(addflight, text="Flight id : ",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.2, anchor="center")
        flightreg_val = tk.Entry(addflight,text=mystr,state=DISABLED).place(relx=.60, rely=.2, anchor="center")
        flightnum = tk.Label(addflight, text="Flight No. :",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        fnum = tk.Entry(addflight)
        fnum.place(relx=.60, rely=.3, anchor="center")
        global fdate
        
        def abc(a):
            query1 = "select aname,aid, type, tid from airport;"
            cursor.execute(query1)
            table1 = cursor.fetchall()
            query2 = "select * from avl;"
            cursor.execute(query2)
            global table2,dt,l1
            kpt=cal.get_date()
            table2 = cursor.fetchall()
            dt={}
            l1=[]
            for i in table1:
                w,x,y,z=i
                p=" - ".join([w,y])
                dt[p]=[x,z]
                l1.append(p)
                for j in table2:
                    f,g,h,m=j
                    if h==cal.get_date() and m<1 and x==f and g==z:
                        del dt[l1[-1]]
                        l1.pop()
                        break
            global fdate
            fdate=cal.get_date()
            tk.Label(addflight, text="Flight Departure From :",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.7,anchor='center')
            options = [str(i)[1:-1] for i in table2]
            clicked = StringVar()
            clicked.set("Select an Option")
            global o
            o=0

            def updateopt(o):
                global aid1,tid1,addflight,dt,l1
                aid1,tid1=dt[o]
                query2 = "select * from avl;"
                cursor.execute(query2)
                kpt=cal.get_date()
                table2 = cursor.fetchall()
                dt={}
                l1=[]
                for i in table1:
                    w,x,y,z=i
                    p=" - ".join([w,y])
                    dt[p]=[x,z]
                    l1.append(p)
                    for j in table2:
                        f,g,h,m=j
                        if h==cal.get_date() and m<1 and x==f and g==z:
                            del dt[l1[-1]]
                            l1.pop()
                            break
                del dt[o]
                tk.Label(addflight, text="Flight Arrival To:",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.8,anchor='center')
                options1 = [str(i)[1:-1] for i in table3]
                clicked1 = StringVar()
                clicked1.set("Select an Option")
                global o1
                o1=0

                def updateopt1(o1):
                    global aid2,tid2,dt
                    aid2,tid2=dt[o1]
                drop1 = OptionMenu( addflight, clicked1 , *dt.keys(),command=updateopt1)
                drop1.config(width=30,bg="#16aaf4",activebackground="#16aaf4",fg="white",activeforeground="white")
                drop1["menu"].config(bg="white",activebackground="#16aaf4")
                drop1.place(relx=.45,rely=.8,anchor='center')
            drop = OptionMenu( addflight, clicked , *dt.keys(),command=updateopt)
            drop["menu"].config(bg="white",activebackground="#16aaf4")
            drop.config(width=30,bg="#16aaf4",activebackground="#16aaf4",fg="white",activeforeground="white")
            drop.place(relx=.45,rely=.7,anchor='center')
            
        td = date.today() + timedelta(days=1)
        flightdate = tk.Label(addflight, text="Flight Date :",bg="#80ccfc", activebackground="#70c5f5",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
        cal = DateEntry(addflight, width=12, year=2023, month=1, day=22, 
        background='blue', foreground='black', borderwidth=2,mindate=td,headersbackground="#16c2f4")
        cal.place(relx=.60, rely=.4, anchor="center")
        cal.bind("<<DateEntrySelected>>", abc)
        flightduration = tk.Label(addflight, text="Flight duration :",bg="#fafdff",font=('Helvetica bold', 12)).place(relx=.40, rely=.5, anchor="center")
        fdur = tk.Entry(addflight)
        fdur.place(relx=.60, rely=.5, anchor="center")
        passwngerno = tk.Label(addflight, text="Total Passenger :",bg="#606163",font=('Helvetica bold', 12)).place(relx=.40, rely=.6, anchor="center")
        totpass = tk.Entry(addflight)
        totpass.place(relx=.60, rely=.6, anchor="center")
        global flightval
        
        def chngarrival(a,n):
            global flightavl
            try:
                a,b,c=map(int,a.get().split(":"))
                k=(b+int(n))%60
                a=a+(b+int(n))/60
                var = StringVar()
                var.set("%02d:%02d:%02d"%(a,k,c))
                passwngerno = tk.Label(addflight, text="Arrival Time :",bg="#92c83e",font=('Helvetica bold', 12)).place(relx=.70, rely=.8, anchor="center")
                flightavl = tk.Entry(addflight,state=DISABLED,textvariable=var)
                flightavl.place(relx=.90, rely=.8, anchor="center")
            except:
                return
            
        var = StringVar()
        var.trace("w", lambda name, index,mode, var=var: chngarrival(var,fdur.get()))
        passwngerno = tk.Label(addflight, text="Departure Time :",bg="#92c83e",font=('Helvetica bold', 12)).place(relx=.70, rely=.7, anchor="center")
        flightdept = tk.Entry(addflight,textvariable=var)
        flightdept.place(relx=.90, rely=.7, anchor="center")
    drop11 = OptionMenu( addflight, clicked , *dpl.keys(),command=updatepln)
    drop11.config(width=15,bg="#16aaf4",activebackground="#16aaf4",fg="white",activeforeground="white")
    drop11["menu"].config(bg="white",activebackground="#16aaf4")
    drop11.place(relx=.90,rely=.2,anchor='center')
    addflightbtn = tk.Button(addflight,width=15,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", bd=5, padx=5, pady=5, text="Submit", command=lambda :addflighttocpge(n,fnum,fdate,fdur,totpass,flightdept,flightavl,aid1,tid1,aid2,tid2,opt)).place(relx=.50, rely=.9, anchor="center")
    tk.Button(addflight, text="Back",command=lambda :back(flight,addflight),activebackground="#12218A", bg="#1D37E8",activeforeground="#fff",width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    addflight.protocol("WM_DELETE_WINDOW",lambda :closecon(addflight))
    addflight.resizable(False,False)
    addflight.mainloop()

def modflightdet():
    global flight,upflight
    upflight=Toplevel()#tk.Tk()
    cursor = con.cursor()
    da=date.today()
    query1 = "select * from flight where fdate>='{}'".format(da)
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    flight.withdraw()
    upflight.geometry(str(w)+"x"+str(h))
    upflight.title("Update flight")
    query2 = "select aname,aid, type,tid from airport "
    cursor.execute(query2)
    table2 = cursor.fetchall()
    query3 = "select aname,aid, type,tid from airport "
    cursor.execute(query3)
    table3 = cursor.fetchall()
    d2={}
    for i in table2:
        a,b,c,d=i
        d2[b,d]=a+" - "+c
    query3 = "select * from flight f,fromto t where f.fid=t.fid"
    cursor.execute(query3)
    table4 = cursor.fetchall()
    d3={}
    for i in table4:
        a,b,c,d,e,f,g=i[2],i[8],i[9],i[10],i[11],i[5],i[6]
        d3["From {} To {} on {} {}-{}".format(d2[b,c],d2[d,e],a,f,g)]=i
    img= (Image.open(flightpageimg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(upflight, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Button(upflight, text="Back",command=lambda :back(flight,upflight),width=5, bd=5, padx=5, pady=5,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff").place(relx=.1,rely=.1,anchor='center')
    tk.Label(upflight, text="Update Flight Data",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 20)).place(relx=.5,rely=.03,anchor='center')
    tk.Label(upflight, text="Select Data :",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.3,rely=.12,anchor='center')
    options = [str(i)[1:-1] for i in table]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    
    def updateopt(o):
        a,b,c,d,e,f,g,h,i,j,k,l=d3[o]
        n=a
        tk.Label(upflight, text="Flight Departure From :",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.7,anchor='center')
        options2 = [str(i)[1:-1] for i in table2]
        clicked2 = StringVar()
        clicked2.set("Select an Option")
        global o2
        o2=0
        mystr = StringVar()
        mystr.set(a)
        flightreg = tk.Label(upflight, text="Flight id : ",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.2, anchor="center")
        flightreg_val = tk.Entry(upflight,text=mystr,state=DISABLED).place(relx=.60, rely=.2, anchor="center")
        flightnum = tk.Label(upflight, text="Flight No. :",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(b)
        fnum = tk.Entry(upflight,text=mystr)
        fnum.place(relx=.60, rely=.3, anchor="center")
        global fdate

        def abc(a):
            query1 = "select aname,aid, type, tid from airport;"
            cursor.execute(query1)
            table1 = cursor.fetchall()
            query2 = "select * from avl;"
            cursor.execute(query2)
            global table2,dt,l1
            kpt=cal.get_date()
            table2 = cursor.fetchall()
            dt={}
            l1=[]
            for i in table1:
                w,x,y,z=i
                p=" - ".join([w,y])
                dt[p]=[x,z]
                l1.append(p)
                for j in table2:
                    f,g,h,m=j
                    if h==cal.get_date() and m<1 and x==f and g==z:
                        del dt[l1[-1]]
                        l1.pop()
                        break
            global fdate
            fdate=cal.get_date()
            tk.Label(upflight, text="Flight Departure From :",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.7,anchor='center')
            options = [str(i)[1:-1] for i in table2]
            clicked = StringVar()
            clicked.set("Select an Option")
            global o
            o=0
            
            def updateopt(o):
                global aid1,tid1,upflight
                global dt,l1
                aid1,tid1=dt[o]
                query2 = "select * from avl;"
                cursor.execute(query2)
                kpt=cal.get_date()
                table2 = cursor.fetchall()
                dt={}
                l1=[]
                for i in table1:
                    w,x,y,z=i
                    p=" - ".join([w,y])
                    dt[p]=[x,z]
                    l1.append(p)
                    for j in table2:
                        f,g,h,m=j
                        if h==cal.get_date() and m<1 and x==f and g==z:
                            del dt[l1[-1]]
                            l1.pop()
                            break
                del dt[o]
                tk.Label(upflight, text="Flight Arrival To:",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.8,anchor='center')
                options1 = [str(i)[1:-1] for i in table3]
                clicked1 = StringVar()
                clicked1.set("Select an Option")
                global o1
                o1=0
                
                def updateopt1(o1):
                    global aid2,tid2,dt
                    aid2,tid2=dt[o1]
                drop1 = OptionMenu( upflight, clicked1 , *dt.keys(),command=updateopt1)
                drop1.config(width=30,bg="#16aaf4",activebackground="#16aaf4",fg="white",activeforeground="white")
                drop1["menu"].config(bg="white",activebackground="#16aaf4")
                drop1.place(relx=.45,rely=.8,anchor='center')
            drop = OptionMenu( upflight, clicked , *dt.keys(),command=updateopt)
            drop.config(width=30,bg="#16aaf4",activebackground="#16aaf4",fg="white",activeforeground="white")
            drop["menu"].config(bg="white",activebackground="#16aaf4")
            drop.place(relx=.45,rely=.7,anchor='center')
        td = date.today() + timedelta(days=1)
        flightdate = tk.Label(upflight, text="Flight Date :",bg="#80ccfc", activebackground="#70c5f5",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
        cy,cm,cd=map(int,str(c).split("-"))
        cal = DateEntry(upflight, width=12, year=cy, month=cm, day=cd, 
        background='darkblue', foreground='black', borderwidth=2,command=abc,mindate=td,normalforeground='white')
        cal.place(relx=.60, rely=.4, anchor="center")
        cal.bind("<<DateEntrySelected>>", abc)
        mystr = StringVar()
        mystr.set(d)
        flightduration = tk.Label(upflight, text="Flight duration :",bg="#fafdff",font=('Helvetica bold', 12)).place(relx=.40, rely=.5, anchor="center")
        fdur = tk.Entry(upflight,textvariable=mystr)
        fdur.place(relx=.60, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(e)
        passwngerno = tk.Label(upflight, text="Total Passenger :",bg="#606163",font=('Helvetica bold', 12)).place(relx=.40, rely=.6, anchor="center")
        totpass = tk.Entry(upflight,textvariable=mystr)
        totpass.place(relx=.60, rely=.6, anchor="center")
        global flightval
        def chngarrival(a,n):
            global flightavl
            try:
                a,b,c=map(int,a.get().split(":"))
                k=(b+int(n))%60
                a=a+(b+int(n))/60
                var = StringVar()
                var.set("%02d:%02d:%02d"%(a,k,c))
                passwngerno = tk.Label(upflight, text="Arrival Time :",bg="#92c83e",font=('Helvetica bold', 12)).place(relx=.70, rely=.8, anchor="center")
                flightavl = tk.Entry(upflight,state=DISABLED,textvariable=var)
                flightavl.place(relx=.90, rely=.8, anchor="center")
            except:
                return
        var = StringVar()
        var.set(f)
        var.trace("w", lambda name, index,mode, var=var: chngarrival(var,fdur.get()))
        passwngerno = tk.Label(upflight, text="Departure Time :",bg="#92c83e",font=('Helvetica bold', 12)).place(relx=.70, rely=.7, anchor="center")
        flightdept = tk.Entry(upflight,textvariable=var)
        flightdept.place(relx=.90, rely=.7, anchor="center")
        upflightbtn = tk.Button(upflight,width=15, bd=5, padx=5, pady=5,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Submit", command=lambda :confirmupdflight(n,fnum.get(),fdate,fdur.get(),totpass.get(),flightdept.get(),flightavl.get(),aid1,tid1,aid2,tid2)).place(relx=.50, rely=.9, anchor="center")
        tk.Button(upflight, text="Back",command=lambda :back(flight,upflight),width=5, bd=5, padx=5, pady=5,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff").place(relx=.1,rely=.1,anchor='center')
    drop = OptionMenu( upflight, clicked , *d3.keys(),command=updateopt)
    drop.place(relx=.55,rely=.12,anchor='center')
    drop.config(width=30,bg="#58b042",activebackground="#58b042",fg="white",activeforeground="white")
    drop["menu"].config(bg="white",activebackground="#92c83e")
    upflight.protocol("WM_DELETE_WINDOW",lambda :closecon(upflight))
    upflight.resizable(False,False)
    upflight.mainloop()

def delflightdet():
    global flight,delflight
    delflight=Toplevel()
    cursor = con.cursor()
    query1 = "select * from flight"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    flight.withdraw()
    delflight.geometry(str(w)+"x"+str(h))
    delflight.title("Delete flight")
    query2 = "select aname,aid, type,tid from airport "
    cursor.execute(query2)
    table2 = cursor.fetchall()
    query3 = "select aname,aid, type,tid from airport "
    cursor.execute(query3)
    table3 = cursor.fetchall()
    d2={}
    for i in table2:
        a,b,c,d=i
        d2[b,d]=a+" - "+c
    query3 = "select * from flight f,fromto t where f.fid=t.fid"
    cursor.execute(query3)
    table4 = cursor.fetchall()
    d3={}
    for i in table4:
        a,b,c,d,e,f,g=i[2],i[8],i[9],i[10],i[11],i[5],i[6]
        d3["From {} To {} on {} {}-{}".format(d2[b,c],d2[d,e],a,f,g)]=i
    img= (Image.open(flightpageimg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(delflight, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Button(delflight, text="Back",command=lambda :back(flight,delflight),width=5, bd=5, padx=5, pady=5,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff").place(relx=.1,rely=.1,anchor='center')
    tk.Label(delflight, text="Delete Flight Data",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 20)).place(relx=.5,rely=.03,anchor='center')
    tk.Label(delflight, text="Select Data :",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.3,rely=.12,anchor='center')
    options = [str(i)[1:-1] for i in table]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    
    def updateopt(o):
        a,b,c,d,e,f,g,h,i,j,k,l=d3[o]
        n=a
        global table2,dt,l1
        tk.Label(delflight, text="Flight Departure From :",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.7,anchor='center')
        clicked2 = StringVar()
        clicked2.set("Select an Option")
        global o2
        o2=0
        mystr = StringVar()
        mystr.set(a)
        flightreg = tk.Label(delflight, text="Flight id : ",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.2, anchor="center")
        flightreg_val = tk.Entry(delflight,text=mystr,state=DISABLED).place(relx=.60, rely=.2, anchor="center")
        flightnum = tk.Label(delflight, text="Flight No. :",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(b)
        fnum = tk.Entry(delflight,text=mystr,state=DISABLED)
        fnum.place(relx=.60, rely=.3, anchor="center")
        global fdate
        tk.Label(delflight, text="Flight Departure From :",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.7,anchor='center')
        clicked = StringVar()
        clicked.set(d2[i,j])
        o=0
        tk.Label(delflight, text="Flight Arrival To:",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.8,anchor='center')
        options1 = [str(i)[1:-1] for i in table3]
        clicked1 = StringVar()
        clicked1.set(d2[k,l])
        global o1
        o1=0
        
        def updateopt1(o1):
            global aid2,tid2,dt
            aid2,tid2=dt[o1]
        drop1 = OptionMenu( delflight, clicked1 , *dt.keys(),command=updateopt1)
        drop1.config(width=30,state=DISABLED,disabledforeground="white",bg="#16aaf4",activebackground="#16aaf4",fg="white",activeforeground="white")
        drop1["menu"].config(bg="white",activebackground="#16aaf4")
        drop1.place(relx=.45,rely=.8,anchor='center')
        drop = OptionMenu( delflight, clicked , *dt.keys(),command=updateopt)
        drop.config(width=30,state=DISABLED,disabledforeground="white",bg="#16aaf4",activebackground="#16aaf4",fg="white",activeforeground="white")
        drop["menu"].config(bg="white",activebackground="#16aaf4")
        drop.place(relx=.45,rely=.7,anchor='center')
        td = date.today() + timedelta(days=1)
        flightdate = tk.Label(delflight, text="Flight Date :",bg="#80ccfc", activebackground="#70c5f5",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
        cy,cm,cd=map(int,str(c).split("-"))
        mystr=StringVar()
        mystr.set("%04d-%02d-%02d"%(cy,cm,cd))
        cal=Entry(delflight,textvariable=mystr,state=DISABLED)
        # cal = DateEntry(delflight, width=12, year=cy, month=cm, day=cd, 
        # background='darkblue', foreground='white', borderwidth=2,mindate=td,state=DISABLED)
        # cal.pack(padx=10, pady=10)
        cal.place(relx=.60, rely=.4, anchor="center")
        # cal.bind("<<DateEntrySelected>>", abc)
        mystr = StringVar()
        mystr.set(d)
        flightduration = tk.Label(delflight, text="Flight duration :",bg="#fafdff",font=('Helvetica bold', 12)).place(relx=.40, rely=.5, anchor="center")
        fdur = tk.Entry(delflight,textvariable=mystr,state=DISABLED)
        fdur.place(relx=.60, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(e)
        passwngerno = tk.Label(delflight, text="Total Passenger :",bg="#606163",font=('Helvetica bold', 12)).place(relx=.40, rely=.6, anchor="center")
        totpass = tk.Entry(delflight,textvariable=mystr,state=DISABLED)
        totpass.place(relx=.60, rely=.6, anchor="center")
        global flightval
        var = StringVar()
        var.set(g)
        passwngerno = tk.Label(delflight, text="Arrival Time :",bg="#92c83e",font=('Helvetica bold', 12)).place(relx=.70, rely=.8, anchor="center")
        flightavl = tk.Entry(delflight,state=DISABLED,textvariable=var)
        flightavl.place(relx=.90, rely=.8, anchor="center")
        var = StringVar()
        var.set(f)
        passwngerno = tk.Label(delflight, text="Departure Time :",bg="#92c83e",font=('Helvetica bold', 12)).place(relx=.70, rely=.7, anchor="center")
        flightdept = tk.Entry(delflight,textvariable=var,state=DISABLED)
        flightdept.place(relx=.90, rely=.7, anchor="center")
        addflightbtn = tk.Button(delflight,width=15, bd=5, padx=5, pady=5,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Submit", command=lambda :addflighttocpge(n,fnum,fdate,fdur,totpass,flightdept,flightavl,aid1,aid2)).place(relx=.50, rely=.9, anchor="center")
        fin= tk.Button(delflight, text="Delete",activebackground="#8a2212",bg="red",activeforeground="white",font=('Helvetica bold', 14),command=lambda :confirmdelflight(n),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.9,anchor='center')
    drop = OptionMenu( delflight, clicked , *d3.keys(),command=updateopt)
    drop.config(width=30,bg="#58b042",activebackground="#58b042",fg="white",activeforeground="white")
    drop["menu"].config(bg="white",activebackground="#92c83e")
    drop.place(relx=.55,rely=.12,anchor='center')
    delflight.protocol("WM_DELETE_WINDOW",lambda :closecon(delflight))
    delflight.resizable(False,False)
    delflight.mainloop()

def confirmupdflight(n,fnum,fdate,fdur,totpass,flightdept,flightavl,aid1,tid1,aid2,tid2):
    global flight,upflight
    answer = askyesno(title='confirmation',message='Are you sure that you want to Update?')
    if answer==True:
        query1 = "update flight set fno={} , fdate='{}', ftime={}, pasno={}, flightdept='{}', flightarrival='{}' where fid={} ".format(fnum,fdate,fdur,totpass,flightdept,flightavl,n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        query2 = "update fromto set aid1={} , tid1={}, aid2={}, tid2={} where fid={} ".format(aid1,tid1,aid2,tid2,n)
        try:
            cursor.execute(query2)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Updated")
        capassign()
        flight.deiconify()
        upflight.destroy()

def confirmdelflight(n):
    global flight,delflight
    answer = askyesno(title='confirmation',message='Are you sure that you want to delete?')
    if answer==True:
        query1 = "delete from fromto where fid={}".format(n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        query2 = "delete from flight where fid={}".format(n)
        try:
            cursor.execute(query2)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Deleted")
        capassign()
        flight.deiconify()
        delflight.destroy()

def showflighttable():
    global flight,showflight
    showflight=Toplevel()#tk.Tk()
    cursor = con.cursor()
    query1 = "select * from flight"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    flight.withdraw()
    showflight.geometry(str(w)+"x"+str(h))
    showflight.title("Show flight")
    query2 = "select aname,aid, type,tid from airport "
    cursor.execute(query2)
    table2 = cursor.fetchall()
    query3 = "select aname,aid, type,tid from airport "
    cursor.execute(query3)
    table3 = cursor.fetchall()
    d2={}
    for i in table2:
        a,b,c,d=i
        d2[b,d]=a+" - "+c
    query3 = "select * from flight f,fromto t where f.fid=t.fid"
    cursor.execute(query3)
    table4 = cursor.fetchall()
    d3={}
    for i in table4:
        a,b,c,d,e,f,g=i[2],i[8],i[9],i[10],i[11],i[5],i[6]
        d3["From {} To {} on {} {}-{}".format(d2[b,c],d2[d,e],a,f,g)]=i
    img= (Image.open(flightpageimg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(showflight, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Button(showflight, text="Back",command=lambda :back(flight,showflight),width=5, bd=5, padx=5, pady=5,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff").place(relx=.1,rely=.1,anchor='center')
    tk.Label(showflight, text="Show Flight Data",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 20)).place(relx=.5,rely=.03,anchor='center')
    tk.Label(showflight, text="Select Data :",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.3,rely=.12,anchor='center')
    options = [str(i)[1:-1] for i in table]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    
    def updateopt(o):
        a,b,c,d,e,f,g,h,i,j,k,l=d3[o]
        n=a
        global table2,dt,l1
        tk.Label(showflight, text="Flight Departure From :",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.7,anchor='center')
        clicked2 = StringVar()
        clicked2.set("Select an Option")
        global o2
        o2=0
        mystr = StringVar()
        mystr.set(a)
        flightreg = tk.Label(showflight, text="Flight id : ",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.2, anchor="center")
        flightreg_val = tk.Entry(showflight,text=mystr,state=DISABLED).place(relx=.60, rely=.2, anchor="center")
        flightnum = tk.Label(showflight, text="Flight No. :",bg="#16c2f4", activebackground="#181a1b",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(b)
        fnum = tk.Entry(showflight,text=mystr,state=DISABLED)
        fnum.place(relx=.60, rely=.3, anchor="center")
        global fdate
        tk.Label(showflight, text="Flight Departure From :",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.7,anchor='center')
        clicked = StringVar()
        clicked.set(d2[i,j])
        o=0
        tk.Label(showflight, text="Flight Arrival To:",bg="#58b042",font=('Helvetica bold', 12)).place(relx=.15,rely=.8,anchor='center')
        options1 = [str(i)[1:-1] for i in table3]
        clicked1 = StringVar()
        clicked1.set(d2[k,l])
        global o1
        o1=0
        
        def updateopt1(o1):
            global aid2,tid2,dt
            aid2,tid2=dt[o1]
        drop1 = OptionMenu( showflight, clicked1 , *d2.keys(),command=updateopt1)
        drop1.config(width=30,state=DISABLED,disabledforeground="white",bg="#16aaf4",activebackground="#16aaf4",fg="white",activeforeground="white")
        drop1["menu"].config(bg="white",activebackground="#16aaf4")
        drop1.place(relx=.45,rely=.8,anchor='center')
        drop = OptionMenu( showflight, clicked , *d2.keys(),command=updateopt)
        drop.config(width=30,state=DISABLED,disabledforeground="white",bg="#16aaf4",activebackground="#16aaf4",fg="white",activeforeground="white")
        drop["menu"].config(bg="white",activebackground="#16aaf4")
        drop.place(relx=.45,rely=.7,anchor='center')
        td = date.today() + timedelta(days=1)
        flightdate = tk.Label(showflight, text="Flight Date :",bg="#80ccfc", activebackground="#70c5f5",activeforeground="#fff",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
        cy,cm,cd=map(int,str(c).split("-"))
        mystr=StringVar()
        mystr.set("%04d-%02d-%02d"%(cy,cm,cd))
        cal=Entry(showflight,textvariable=mystr,state=DISABLED)
        cal.place(relx=.60, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(d)
        flightduration = tk.Label(showflight, text="Flight duration :",bg="#fafdff",font=('Helvetica bold', 12)).place(relx=.40, rely=.5, anchor="center")
        fdur = tk.Entry(showflight,textvariable=mystr,state=DISABLED)
        fdur.place(relx=.60, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(e)
        passwngerno = tk.Label(showflight, text="Total Passenger :",bg="#606163",font=('Helvetica bold', 12)).place(relx=.40, rely=.6, anchor="center")
        totpass = tk.Entry(showflight,textvariable=mystr,state=DISABLED)
        totpass.place(relx=.60, rely=.6, anchor="center")
        global flightval
        var = StringVar()
        var.set(g)
        passwngerno = tk.Label(showflight, text="Arrival Time :",bg="#92c83e",font=('Helvetica bold', 12)).place(relx=.70, rely=.8, anchor="center")
        flightavl = tk.Entry(showflight,state=DISABLED,textvariable=var)
        flightavl.place(relx=.90, rely=.8, anchor="center")
        var = StringVar()
        var.set(f)
        passwngerno = tk.Label(showflight, text="Departure Time :",bg="#92c83e",font=('Helvetica bold', 12)).place(relx=.70, rely=.7, anchor="center")
        flightdept = tk.Entry(showflight,textvariable=var,state=DISABLED)
        flightdept.place(relx=.90, rely=.7, anchor="center")
        addflightbtn = tk.Button(showflight,width=15, bd=5, padx=5, pady=5, text="Submit", command=lambda :addflighttocpge(n,fnum,fdate,fdur,totpass,flightdept,flightavl,aid1,aid2)).place(relx=.50, rely=.9, anchor="center")
        fin= tk.Button(showflight, text="Done",activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",font=('Helvetica bold', 14),command=lambda :doneflightshow(),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.9,anchor='center')
    drop = OptionMenu( showflight, clicked , *d3.keys(),command=updateopt)
    drop.config(width=30,bg="#58b042",activebackground="#58b042",fg="white",activeforeground="white")
    drop["menu"].config(bg="white",activebackground="#92c83e")
    drop.place(relx=.55,rely=.12,anchor='center')
    showflight.protocol("WM_DELETE_WINDOW",lambda :closecon(showflight))
    showflight.resizable(False,False)
    showflight.mainloop()

def doneflightshow():
    global flight,showflight
    flight.deiconify()
    showflight.destroy()


def addflighttocpge(a,b,c,d,e,f,g,h,i,j,k,l):
    b=b.get()
    d=d.get()
    e=e.get()
    f=f.get()
    g=g.get()
    new="0000-00-00".replace(" ","")
    query1 = "insert into flight values({},{},'{}',{}, {},'{}','{}')".format(a,int(b),c,int(d),int(e),f,g)
    table=[]
    try:
        cursor.execute(query1)
    except Exception as e:
        messagebox.showerror("Error",e)
        return
    con.commit()
    query2 = "insert into fromto values({},{},{},{},{})".format(a,h,i,j,k)
    table=[]
    try:
        cursor.execute(query2)
    except Exception as e:
        messagebox.showerror("Error",e)
        return
    query1 = "insert into takes values({},{})".format(l,a)
    try:
        cursor.execute(query1)
    except Exception as e:
        messagebox.showerror("Error",e)
        return 
    con.commit()
    messagebox.showinfo("Done","Added")
    capassign()
    addflight.destroy()
    flight.deiconify()
    
def upcompagetocpage():
    global company,upcom
    upcom.destroy()
    company.deiconify()
    
def unsuccess():
    messagebox.showerror('LOGIN FAILED', 'Not able to login.\nWrong ID or Password!')
    
def loginfn(username_entry,password_entry):
    global window
    cursor.execute("select * from users")
    l=cursor.fetchall()
    username = username_entry.get()
    password = password_entry.get()
    window.deiconify()
    global usertype 
    global flag
    usertype = None
    for i in l:
        if username == i[1] and password == i[2]:
            usertype = i[3]
            flag=chkusrt[usertype]
            verified()
            break
    if usertype is None:
        unsuccess()

def closecon(a):
    a.quit()
    a.destroy()
    global window
    window.destroy()

def addairportdet():
    global addairport
    global flight
    airport.withdraw()
    cursor = con.cursor()
    query1 = "select * from airport"
    cursor.execute(query1)
    table = cursor.fetchall()
    idset=set([i[0] for i in table])
    n=random.randrange(10,100)
    while n in idset:n=random.randrange(20)
    mystr = tk.StringVar()
    mystr.set(n)
    mystr2 = tk.StringVar()
    mystr2.set("1/2 Default")
    mystr3 = tk.StringVar()
    mystr3.set("International/Domestic Default")
    addairport = Toplevel()
    addairport.geometry(str(w)+"x"+str(h))
    img= (Image.open(airportbg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(addairport, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Button(addairport, text="Back",command=lambda :back(airport,addairport),width=5, bd=5, padx=5, pady=5,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff").place(relx=.1,rely=.1,anchor='center')
    addairport.title("Add New Airport")
    op=tk.Label(addairport, text="Add a new Airport",fg="white",bg="#a3b0a2",font=('Helvetica bold', 18)).place(relx=.50, rely=.1, anchor="center")
    flightreg = tk.Label(addairport, text="AirPORT id : ",bg="#a3b0a2",font=('Helvetica bold', 12)).place(relx=.40, rely=.2, anchor="center")
    flightreg_val = tk.Entry(addairport,text=mystr,state=DISABLED).place(relx=.60, rely=.2, anchor="center")
    flightnum = tk.Label(addairport, text="Terminal No. :",bg="#d8d3c0",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
    tk.Entry(addairport,text=mystr2,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
    flightdate = tk.Label(addairport, text="Type :",bg="#44b9be",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
    tk.Entry(addairport,text=mystr3,state=DISABLED).place(relx=.60, rely=.4, anchor="center")
    flightduration = tk.Label(addairport, text="AirPORT Availability :",bg="#00688f",font=('Helvetica bold', 12)).place(relx=.37, rely=.5, anchor="center")
    avail = tk.Entry(addairport)
    avail.place(relx=.60, rely=.5, anchor="center")
    passwngerno = tk.Label(addairport, text="AirPORT Name :",bg="#dbd8bd",font=('Helvetica bold', 12)).place(relx=.40, rely=.6, anchor="center")
    aname = tk.Entry(addairport)
    aname.place(relx=.60, rely=.6, anchor="center")
    addairportbtn = tk.Button(addairport,width=15, activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",bd=5, padx=5, pady=5, text="Submit", command=lambda :addairporttocpge(n,avail,aname)).place(relx=.50, rely=.7, anchor="center")
    addairport.protocol("WM_DELETE_WINDOW",lambda :closecon(addairport))
    addairport.resizable(False,False)
    addairport.mainloop()
    
def addairporttocpge(a,b,c):
    b=b.get()
    c=c.get()
    query1 = "insert into airport values({},1,'International',{},'{}'),({},2,'Domestic',{},'{}')".format(a,b,c,a,b,c)
    table=[]
    try:
        cursor.execute(query1)
    except Exception as e:
        messagebox.showerror("Error",e)
        return
    con.commit()
    messagebox.showinfo("Done","Added")
    addairport.destroy()
    airport.deiconify()
    
def apage():
    global airport
    menupg.withdraw()
    airport=Toplevel()
    airport.geometry(str(w)+"x"+str(h))
    airport.title("AirPORT Page")
    img= (Image.open(airportbg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(airport, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Button(airport, text="Back",command=lambda :back(menupg,airport),width=5, bd=5, padx=5, pady=5,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff").place(relx=.1,rely=.1,anchor='center')
    tk.Label(airport, text="Airport Page",bg="#a3b0a2",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    addcom= tk.Button(airport, text="Add new AirPORT",command=addairportdet,width=25, activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",padx=5, bd=5,pady=5).place(relx=.5,rely=.3,anchor='center')
    modcom= tk.Button(airport,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"), text="Modify old AirPORT detail",activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",command=upairpage,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.4,anchor='center')
    delcom= tk.Button(airport,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"), text="Delete old AirPORT detail",activebackground="#8a2212", bg="red",activeforeground="#fff",command=remairpage,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.5,anchor='center')
    shocom= tk.Button(airport,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"), text="Show AirPORT table",activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",command=showairpage,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.6,anchor='center')
    airport.protocol("WM_DELETE_WINDOW",lambda :closecon(airport))
    airport.resizable(False,False)
    airport.mainloop()    

def airportconfirmrem(n):
    global airport,remair
    answer = askyesno(title='confirmation',message='Are you sure that you want to Delete?')
    if answer==True:
        query1 = " delete from airport where aid={} ".format(n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Deleted")
        airport.deiconify()
        remair.destroy()
        
def airportconfirmupd(n,a,b):
    global airport,upair
    answer = askyesno(title='confirmation',message='Are you sure that you want to Update?')
    if answer==True:
        query1 = "update airport set avail={} , aname='{}' where aid={} ".format(a,b,n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Updated")
        airport.deiconify()
        upair.destroy()
        
def remairpage():
    global airport,remair
    remair=Toplevel()#tk.Tk()
    cursor = con.cursor()
    query1 = "select * from airport where tid=1"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    l=[]
    for i in table:
        l.append([i[0],i[3],i[4]])
    airport.withdraw()
    remair.geometry(str(w)+"x"+str(h))
    remair.title("Remove AirPORT")
    img= (Image.open(airportbg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(remair, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Button(remair, text="Back",command=lambda :back(airport,remair),width=5, bd=5, padx=5, pady=5,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff").place(relx=.1,rely=.1,anchor='center')
    tk.Label(remair, text="Remove AirPORT Data",bg="#a3b0a2",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(remair, text="Select Data :",bg="#a3b0a2",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i[0])+","+str(i[1])+","+i[2] for i in l]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    def updateopt(o):
        def chng(o,n):n=o
        n,avail,oname=o.split(",")
        compreg = tk.Label(remair, text="AirPORT id :",bg="#d8d3c0",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        compreg_val = Entry(remair,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        name = tk.Label(remair, text="Availability :",bg="#44b9be",font=('Helvetica bold', 12))
        name.place(relx=.40, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(avail)
        vavl = Entry(remair,textvariable=mystr,state=DISABLED)
        vavl.place(relx=.60, rely=.4, anchor="center")
        phone = tk.Label(remair, text="AirPORT Name :",bg="#4bb3c5",font=('Helvetica bold', 12))
        phone.place(relx=.40, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(oname)
        vname = Entry(remair,textvariable=mystr,state=DISABLED)
        vname.place(relx=.60, rely=.5, anchor="center")
        fin= tk.Button(remair,activebackground="#8A2212", bg="red",activeforeground="#fff", text="Delete",font=('Helvetica bold', 14),command=lambda :airportconfirmrem(n),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.75,anchor='center')
    drop = OptionMenu( remair, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#00688f",activebackground="#00688f",fg="white",activeforeground="white")
    drop["menu"].config(bg="white",activebackground="#4bb3c5")
    drop.place(relx=.55,rely=.2,anchor='center')
    remair.protocol("WM_DELETE_WINDOW",lambda :closecon(remair))
    remair.resizable(False,False)
    remair.mainloop()

def upairpage():
    global airport,upair
    upair=Toplevel()
    cursor = con.cursor()
    query1 = "select * from airport where tid=1"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    l=[]
    for i in table:l.append([i[0],i[3],i[4]])
    airport.withdraw()
    upair.geometry(str(w)+"x"+str(h))
    upair.title("Update AirPORT")
    img= (Image.open(airportbg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(upair, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Button(upair, text="Back",command=lambda :back(airport,upair),width=5, bd=5, padx=5, pady=5,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff").place(relx=.1,rely=.1,anchor='center')
    tk.Label(upair, text="Update AirPORT Data",bg="#a3b0a2",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(upair, text="Select Data :",bg="#a3b0a2",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i[0])+","+str(i[1])+","+i[2] for i in l]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    
    def updateopt(o):
        def chng(o,n):n=o
        n,avail,oname=o.split(",")
        compreg = tk.Label(upair, text="AirPORT id :",bg="#d8d3c0",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        compreg_val = Entry(upair,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        name = tk.Label(upair, text="Availability :",bg="#44b9be",font=('Helvetica bold', 12))
        name.place(relx=.40, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(avail)
        vavl = Entry(upair,textvariable=mystr)
        vavl.place(relx=.60, rely=.4, anchor="center")
        phone = tk.Label(upair, text="AirPORT Name :",bg="#4bb3c5",font=('Helvetica bold', 12))
        phone.place(relx=.40, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(oname)
        vname = Entry(upair,textvariable=mystr)
        vname.place(relx=.60, rely=.5, anchor="center")
        fin= tk.Button(upair,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Update",font=('Helvetica bold', 14),command=lambda :airportconfirmupd(n,vavl.get(),vname.get()),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.75,anchor='center')
    drop = OptionMenu( upair, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#00688f",activebackground="#00688f",fg="white",activeforeground="white")
    drop["menu"].config(bg="white",activebackground="#4bb3c5")
    drop.place(relx=.55,rely=.2,anchor='center')
    upair.protocol("WM_DELETE_WINDOW",lambda :closecon(upair))
    upair.resizable(False,False)
    upair.mainloop()
    
def showairpage():
    global airport,showair
    showair=Toplevel()#tk.Tk()
    cursor = con.cursor()
    query1 = "select * from airport where tid=1"
    cursor.execute(query1)
    c=0
    table = cursor.fetchall()
    n=len(table)
    l=[]
    for i in table:l.append([i[0],i[3],i[4]])
    airport.withdraw()
    showair.geometry(str(w)+"x"+str(h))
    showair.title("Show AirPORT")
    img= (Image.open(airportbg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(showair, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Button(showair, text="Back",command=lambda :back(airport,showair),width=5, bd=5, padx=5, pady=5,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff").place(relx=.1,rely=.1,anchor='center')
    tk.Label(showair, text="Show AirPORT Data",bg="#a3b0a2",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(showair, text="Select Data :",bg="#a3b0a2",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i[0])+","+str(i[1])+","+i[2] for i in l]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    
    def updateopt(o):
        def chng(o,n):n=o
        n,avail,oname=o.split(",")
        compreg = tk.Label(showair, text="AirPORT id :",bg="#d8d3c0",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        compreg_val = Entry(showair,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        name = tk.Label(showair, text="Availability :",bg="#44b9be",font=('Helvetica bold', 12))
        name.place(relx=.40, rely=.4, anchor="center")
        mystr = StringVar()
        mystr.set(avail)
        vavl = Entry(showair,textvariable=mystr,state=DISABLED)
        vavl.place(relx=.60, rely=.4, anchor="center")
        phone = tk.Label(showair, text="AirPORT Name :",bg="#4bb3c5",font=('Helvetica bold', 12))
        phone.place(relx=.40, rely=.5, anchor="center")
        mystr = StringVar()
        mystr.set(oname)
        vname = Entry(showair,textvariable=mystr,state=DISABLED)
        vname.place(relx=.60, rely=.5, anchor="center")
        fin= tk.Button(showair, text="Done",activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",font=('Helvetica bold', 14),command=lambda :back(airport,showair),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.75,anchor='center')
    drop = OptionMenu( showair, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#00688f",activebackground="#00688f",fg="white",activeforeground="white")
    drop["menu"].config(bg="white",activebackground="#4bb3c5")
    drop.place(relx=.55,rely=.2,anchor='center')
    showair.protocol("WM_DELETE_WINDOW",lambda :closecon(showair))
    showair.resizable(False,False)
    showair.mainloop()
    
def addcapdet():
    global addcapport
    capport.withdraw()
    cursor = con.cursor()
    query1 = "select * from captain"
    cursor.execute(query1)
    table = cursor.fetchall()
    idset=set([i[0] for i in table])
    n=random.randrange(6000,7000)
    while n in idset:n=random.randrange(20)
    addcapport = Toplevel()
    mystr = tk.StringVar()
    mystr.set(n)
    mystr2 = tk.StringVar()
    mystr2.set("First Name")
    mystr4 = tk.StringVar()
    mystr4.set("Last Name")
    options = ["M","F"]
    clicked = StringVar()
    clicked.set("Select an Option")
    addcapport.geometry(str(w)+"x"+str(h))
    addcapport.title("Add New Captain")
    img= (Image.open(captainbg))
    global new_image
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(addcapport, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    op=tk.Label(addcapport, text="Add a new Captain",bg="#022f49",fg="white",font=('Helvetica bold', 18)).place(relx=.50, rely=.1, anchor="center")
    flightreg = tk.Label(addcapport, text="cap id : ",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.2, anchor="center")
    flightreg_val = tk.Entry(addcapport,text=mystr,state=DISABLED).place(relx=.60, rely=.2, anchor="center")
    flightnum = tk.Label(addcapport, text="Captain Name :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
    fname=tk.Entry(addcapport,text=mystr2,width=15)
    fname.place(relx=.56, rely=.3, anchor="center")
    lname=tk.Entry(addcapport,text=mystr4,width=15)
    lname.place(relx=.72, rely=.3, anchor="center")
    g="M"
    
    def updateopt(a):g=a
    flightdate = tk.Label(addcapport, text="Gender :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
    drop = OptionMenu( addcapport, clicked , *options,command=updateopt)
    drop.config(width=15,bg="#0057a9",fg="white",activebackground="#0057a9")
    drop["menu"].config(bg="#0057a9",activebackground="#0057a9")
    drop.place(relx=.60,rely=.4,anchor='center')
    flightduration = tk.Label(addcapport, text="Phone Number :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.37, rely=.5, anchor="center")
    phone = tk.Entry(addcapport)
    phone.place(relx=.60, rely=.5, anchor="center")
    addcapportbtn = tk.Button(addcapport,width=15,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", bd=5, padx=5, pady=5, text="Submit", command=lambda :addcapporttocpge(n,fname,lname,phone,g)).place(relx=.50, rely=.7, anchor="center")
    tk.Button(addcapport,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(capport,addcapport),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    addcapport.protocol("WM_DELETE_WINDOW",lambda :closecon(addcapport))
    addcapport.resizable(False,False)
    addcapport.mainloop()
    
def addcapporttocpge(a,b,c,d,e):
    b=b.get()
    c=c.get()
    d=d.get()
    global capport,addcapport
    query1 = "insert into captain values({},'{}','{}','{}',{})".format(a,b,c,e,d)
    table=[]
    try:
        cursor.execute(query1)
    except Exception as e:
        messagebox.showerror("Error",e)
        return
    con.commit()
    messagebox.showinfo("Done","Added")
    capassign()
    addcapport.destroy()
    capport.deiconify()
    
def cappage():
    global capport
    menupg.withdraw()
    capport=Toplevel()
    capport.geometry(str(w)+"x"+str(h))
    capport.title("Captain Info")
    img= (Image.open(captainbg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(capport,image=new_image ).place(x=0, y=0, relwidth=1, relheight=1)
    tk.Label(capport, text="Captain Page",bg="#00c6f7",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    addcom= tk.Button(capport,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Add new Captain",command=addcapdet,width=25, bd=5,padx=5, pady=5).place(relx=.5,rely=.3,anchor='center')
    modcom= tk.Button(capport,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"),activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Modify old Captain detail",command=upcappage,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.4,anchor='center')
    delcom= tk.Button(capport,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"),activebackground="#8A2212", bg="red",activeforeground="#fff", text="Delete old Captain detail",command=remcappage,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.5,anchor='center')
    shocom= tk.Button(capport,state=flag,fg=("#E1D9D1" if flag=="disabled" else "black"),activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Show Captain table",command=showcappage,width=25, bd=5, padx=5, pady=5).place(relx=.5,rely=.6,anchor='center')
    tk.Button(capport,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(menupg,capport),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    capport.protocol("WM_DELETE_WINDOW",lambda :closecon(capport))
    capport.resizable(False,False)
    capport.mainloop()    

def capportconfirmrem(n):
    global capport,remcap
    answer = askyesno(title='confirmation',message='Are you sure that you want to Delete?')
    if answer==True:
        query1 = " delete from captain where capid={} ".format(n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Deleted")
        capassign()
        capport.deiconify()
        remcap.destroy()
        
def capportconfirmupd(n,a,b,c,d):
    global capport,upcap
    answer = askyesno(title='confirmation',message='Are you sure that you want to Update?')
    if answer==True:
        query1 = "update captain set fname='{}' , lname='{}',gender='{}', phno={} where capid={} ".format(b,c,a,d,n)
        try:
            cursor.execute(query1)
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        con.commit()
        messagebox.showinfo("Done","Updated")
        capassign()
        capport.deiconify()
        upcap.destroy()
    
def remcappage():
    global remcap,capport
    capport.withdraw()
    cursor = con.cursor()
    query1 = "select * from captain"
    cursor.execute(query1)
    table = cursor.fetchall()
    idset=set([i[0] for i in table])
    n=random.randrange(6000,7000)
    while n in idset:n=random.randrange(20)
    remcap = Toplevel()
    mystr = tk.StringVar()
    mystr.set(n)
    mystr2 = tk.StringVar()
    mystr2.set("First Name")
    mystr4 = tk.StringVar()
    mystr4.set("Last Name")
    optionsg = ["M","F"]
    clicked = StringVar()
    clicked.set("Select an Option")
    remcap.geometry(str(w)+"x"+str(h))
    remcap.title("Remove Captain")
    img= (Image.open(captainbg))
    global new_image
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(remcap,image=new_image ).place(x=0, y=0, relwidth=1, relheight=1)
    op=tk.Label(remcap, text="Remove an old Captain",bg="#022f49",fg="white",font=('Helvetica bold', 18)).place(relx=.50, rely=.1, anchor="center")
    l=[]
    for i in table:l.append(i)
    tk.Button(remcap, text="Back",command=lambda :back(capport,remcap),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    tk.Label(remcap, text="Remove Captain Data",bg="#022f49",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(remcap, text="Select Data :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i[0])+","+str(i[1])+" "+str(i[2]) for i in l]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0

    def updateopt(o):
        def chng(o,n):n=o
        global g
        g="M"
        n,oname=o.split(",")
        for i in table:
            if i[0]==int(n):
                n,fname,lname,g,ph=i
                break
        clickedg = StringVar()
        clickedg.set(g)
        
        def updateopt(a):
            global g
            g=a
        
        flightdate = tk.Label(remcap, text="Gender :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.5, anchor="center")
        mystr4 = StringVar()
        mystr4.set(g)
        drop2 = tk.Entry(remcap,textvariable=mystr4,state=DISABLED)
        drop2.config(width=15)
        drop2.place(relx=.60,rely=.5,anchor='center')
        mystr4 = StringVar()
        mystr4.set(ph)
        flightduration = tk.Label(remcap, text="Phone Number :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.37, rely=.6, anchor="center")
        phone = tk.Entry(remcap,textvariable=mystr4,state=DISABLED)
        phone.place(relx=.60, rely=.6, anchor="center")
        compreg = tk.Label(remcap, text="Captain id :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        compreg_val = Entry(remcap,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        mystr2 = StringVar()
        mystr2.set(fname)
        mystr3 = StringVar()
        mystr3.set(lname)
        flightnum = tk.Label(remcap, text="Captain Name :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
        fname=tk.Entry(remcap,text=mystr2,width=15,state=DISABLED)
        fname.place(relx=.56, rely=.4, anchor="center")
        lname=tk.Entry(remcap,text=mystr3,width=15,state=DISABLED)
        lname.place(relx=.72, rely=.4, anchor="center")
        fin= tk.Button(remcap,activebackground="#8A2212", bg="red",activeforeground="#fff", text="Remove",font=('Helvetica bold', 14),command=lambda :capportconfirmrem(n),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.75,anchor='center')
    drop = OptionMenu( remcap, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#0057a9",fg="white",activebackground="#0057a9")
    drop["menu"].config(bg="#0057a9",activebackground="#0057a9")
    drop.place(relx=.55,rely=.2,anchor='center')
    tk.Button(remcap,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(capport,remcap),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    remcap.protocol("WM_DELETE_WINDOW",lambda :closecon(remcap))
    remcap.resizable(False,False)
    remcap.mainloop()

def upcappage():
    global upcap,capport
    capport.withdraw()
    cursor = con.cursor()
    query1 = "select * from captain"
    cursor.execute(query1)
    table = cursor.fetchall()
    idset=set([i[0] for i in table])
    n=random.randrange(6000,7000)
    while n in idset:n=random.randrange(20)
    upcap = Toplevel()
    mystr = tk.StringVar()
    mystr.set(n)
    mystr2 = tk.StringVar()
    mystr2.set("First Name")
    mystr4 = tk.StringVar()
    mystr4.set("Last Name")
    optionsg = ["M","F"]
    clicked = StringVar()
    clicked.set("Select an Option")
    upcap.geometry(str(w)+"x"+str(h))
    upcap.title("Update Captain")
    img= (Image.open(captainbg))
    global new_image
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(upcap, image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    op=tk.Label(upcap, text="Update Captain Data",bg="#022f49",fg="white",font=('Helvetica bold', 18)).place(relx=.50, rely=.1, anchor="center")
    l=[]
    for i in table:l.append(i)
    tk.Label(upcap, text="Update Captain Data",bg="#022f49",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(upcap, text="Select Data :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i[0])+","+str(i[1])+" "+str(i[2]) for i in l]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0
    def updateopt(o):
        def chng(o,n):n=o
        global g
        g="M"
        n,oname=o.split(",")
        for i in table:
            if i[0]==int(n):
                n,fname,lname,g,ph=i 
                break
        clickedg = StringVar()
        clickedg.set(g)
        def updateopt(a):
            global g
            g=a
        flightdate = tk.Label(upcap, text="Gender :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.5, anchor="center")
        drop2 = OptionMenu( upcap, clickedg , *optionsg,command=updateopt)
        drop2.config(width=15,bg="#0057a9",fg="white",activebackground="#0057a9")
        drop2["menu"].config(bg="#0057a9",activebackground="#0057a9")
        drop2.place(relx=.60,rely=.5,anchor='center')
        mystr4 = StringVar()
        mystr4.set(ph)
        flightduration = tk.Label(upcap, text="Phone Number :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.37, rely=.6, anchor="center")
        phone = tk.Entry(upcap,textvariable=mystr4)
        phone.place(relx=.60, rely=.6, anchor="center")
        compreg = tk.Label(upcap, text="Captain id :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        compreg_val = Entry(upcap,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        mystr2 = StringVar()
        mystr2.set(fname)
        mystr3 = StringVar()
        mystr3.set(lname)
        flightnum = tk.Label(upcap, text="Captain Name :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
        fname=tk.Entry(upcap,text=mystr2,width=15)
        fname.place(relx=.56, rely=.4, anchor="center")
        lname=tk.Entry(upcap,text=mystr3,width=15)
        lname.place(relx=.72, rely=.4, anchor="center")
        fin= tk.Button(upcap,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Update",font=('Helvetica bold', 14),command=lambda :capportconfirmupd(n,g,fname.get(),lname.get(),phone.get()),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.75,anchor='center')
    drop = OptionMenu( upcap, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#0057a9",fg="white",activebackground="#0057a9")
    drop["menu"].config(bg="#0057a9",activebackground="#0057a9")
    drop.place(relx=.55,rely=.2,anchor='center')
    tk.Button(upcap,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(capport,upcap),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    upcap.protocol("WM_DELETE_WINDOW",lambda :closecon(upcap))
    upcap.resizable(False,False)
    upcap.mainloop()
    
def showcappage():
    global showcap,capport
    capport.withdraw()
    cursor = con.cursor()
    query1 = "select * from captain"
    cursor.execute(query1)
    table = cursor.fetchall()
    idset=set([i[0] for i in table])
    n=random.randrange(6000,7000)
    while n in idset:n=random.randrange(20)
    showcap = Toplevel()
    mystr = tk.StringVar()
    mystr.set(n)
    mystr2 = tk.StringVar()
    mystr2.set("First Name")
    mystr4 = tk.StringVar()
    mystr4.set("Last Name")
    optionsg = ["M","F"]
    clicked = StringVar()
    clicked.set("Select an Option")
    showcap.geometry(str(w)+"x"+str(h))
    showcap.title("Show Captains Details")
    img= (Image.open(captainbg))
    global new_image
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    tk.Label(showcap,image=new_image).place(x=0, y=0, relwidth=1, relheight=1)
    l=[]
    for i in table:l.append(i)
    tk.Label(showcap, text="All Captain Data",bg="#022f49",fg="white",font=('Helvetica bold', 20)).place(relx=.5,rely=.1,anchor='center')
    tk.Label(showcap, text="Select Data :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.3,rely=.2,anchor='center')
    options = [str(i[0])+","+str(i[1])+" "+str(i[2]) for i in l]
    clicked = StringVar()
    clicked.set("Select an Option")
    global o
    o=0

    def updateopt(o):
        def chng(o,n):n=o
        global g
        g="M"
        n,oname=o.split(",")
        for i in table:
            if i[0]==int(n):
                n,fname,lname,g,ph=i
                break
        clickedg = StringVar()
        clickedg.set(g)
        def updateopt(a):
            global g
            g=a
        
        flightdate = tk.Label(showcap, text="Gender :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.5, anchor="center")
        mystr4 = StringVar()
        mystr4.set(g)
        drop2 = tk.Entry(showcap,textvariable=mystr4,state=DISABLED)
        drop2.config(width=15)
        drop2.place(relx=.60,rely=.5,anchor='center')
        mystr4 = StringVar()
        mystr4.set(ph)
        flightduration = tk.Label(showcap, text="Phone Number :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.37, rely=.6, anchor="center")
        phone = tk.Entry(showcap,textvariable=mystr4,state=DISABLED)
        phone.place(relx=.60, rely=.6, anchor="center")
        compreg = tk.Label(showcap, text="Captain id :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.3, anchor="center")
        mystr = StringVar()
        mystr.set(n)
        compreg_val = Entry(showcap,textvariable=mystr,state=DISABLED).place(relx=.60, rely=.3, anchor="center")
        mystr2 = StringVar()
        mystr2.set(fname)
        mystr3 = StringVar()
        mystr3.set(lname)
        flightnum = tk.Label(showcap, text="Captain Name :",bg="#022f49",fg="white",font=('Helvetica bold', 12)).place(relx=.40, rely=.4, anchor="center")
        fname=tk.Entry(showcap,text=mystr2,width=15,state=DISABLED)
        fname.place(relx=.56, rely=.4, anchor="center")
        lname=tk.Entry(showcap,text=mystr3,width=15,state=DISABLED)
        lname.place(relx=.72, rely=.4, anchor="center")
        fin= tk.Button(showcap,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff", text="Done",font=('Helvetica bold', 14),command=lambda :back(capport,showcap),width=18, bd=5, padx=5, pady=5).place(relx=.5,rely=.75,anchor='center')
    drop = OptionMenu( showcap, clicked , *options,command=updateopt)
    drop.config(width=30,bg="#0057a9",fg="white",activebackground="#0057a9")
    drop["menu"].config(bg="#0057a9",activebackground="#0057a9")
    drop.place(relx=.55,rely=.2,anchor='center')
    tk.Button(showcap,activebackground="#12218A", bg="#1D37E8",activeforeground="#fff", text="Back",command=lambda :back(capport,showcap),width=5, bd=5, padx=5, pady=5).place(relx=.1,rely=.1,anchor='center')
    showcap.protocol("WM_DELETE_WINDOW",lambda :closecon(showcap))
    showcap.resizable(False,False)
    showcap.mainloop()  

def init():
    global window
    window=tk.Tk()
    window.geometry(str(w)+"x"+str(h))
    window.title("Login")
    img= (Image.open(loginbg))
    resized_image= img.resize((w,h), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    global a,b
    a,b=0,0
    imgl = tk.Label(window,image=new_image)
    imgl.lower()
    hu = tk.Label(window, text="Hello User :D",bg="#5daefe",font=('Helvetica bold', 24)).place(relx=0.5, rely=0.25, anchor="center")
    username_label = tk.Label(window, bg="#cac0e8",text="Username:").place(relx=0.4, rely=0.35, anchor="center")
    username_entry = tk.Entry(window)
    username_entry.place(relx=0.6, rely=0.35, anchor="center")
    password_label = tk.Label(window,bg="#f3cfeb" ,text="Password:").place(relx=0.4, rely=0.45, anchor="center")
    password_entry = tk.Entry(window, show="*")
    password_entry.place(relx=0.6, rely=0.45, anchor="center")
    login_button = tk.Button(window,width=13,activebackground="#1a4a0f", bg="#4cd12a",activeforeground="#fff",text="Login", command=lambda :loginfn(username_entry,password_entry)).place(relx=0.5, rely=0.55, anchor="center")
    window.bind('<Return>', lambda x:loginfn(username_entry,password_entry))
    imgl.place(x=0, y=0, relwidth=1, relheight=1)
    window.bind_all('<Escape>', lambda x:window.destroy())
    window.protocol("WM_DELETE_WINDOW",lambda :window.destroy())
    window.resizable(False,False)
    window.mainloop()
    
def capassign():
    q="select fid from notassignflight"
    cursor.execute(q)
    t=cursor.fetchall()
    q5="select f.fid,fdate,flightdept,aid1,tid1 from fromto t,flight f where f.fid=t.fid;"
    cursor.execute(q5)
    t5=cursor.fetchall()
    d={}
    for i in t5:d[i[0]]=i[1:]
    fl=[]
    for i in t:
        cl=[]
        q2="select * from capassign"
        cursor.execute(q2)
        t2=cursor.fetchall()
        for j in t2:
            if j[1]==0:
                cl.append(j[0])
                if len(cl)>1:
                    break
            else:
                q4="select * from latestflight"
                cursor.execute(q4)
                t4=cursor.fetchall()
                d2={}
                for k in t4:d2[k[0],k[1]]=k[1:]
                fdate,flast,faid,ftid=d[i[0]]
                if (j[0],fdate) in d2:
                    cdate,temp,caid,ctid,clast=d2[j[0],fdate]
                    if flast>clast and faid==caid and ftid==ctid and fdate==cdate:
                        cl.append(j[0])
                        if len(cl)>1:
                            break
                    elif fdate!=cdate:
                        cl.append(j[0])
                        if len(cl)>1:
                            break
                else:
                    cl.append(j[0])
                    if len(cl)>1:
                        break
        if len(cl)>1:
            q3="insert into controlledby values({},{},{})".format(i[0],cl[0],cl[1])
            cursor.execute(q3)
            con.commit()
        else:
            fl.append(i[0])
    if len(fl)>0:
        query3 = "select aname,aid, type,tid from airport "
        cursor.execute(query3)
        table3 = cursor.fetchall()
        d2={}
        for i in table3:
            a,b,c,d=i
            d2[b,d]=a+" - "+c
        query3 = "select * from flight f,fromto t where f.fid=t.fid"
        cursor.execute(query3)
        table4 = cursor.fetchall()
        d3={}
        ct=1
        s="Can't assign captain for flight(s) :\n"
        for i in table4:
            fid,a,b,c,d,e,f,g=i[0],i[2],i[8],i[9],i[10],i[11],i[5],i[6]
            if fid in fl:
                s+="\n{}. From {} To {} on {} at {}-{}".format(ct,d2[b,c],d2[d,e],a,f,g)
                ct+=1
        s+="\n\nKindly add new captain or Reschedule the flights.\n              Thank You"
        messagebox.showwarning("Captain Assign Warning",s) 
    else:
        messagebox.showinfo("Auto Captain Assign","Auto Captain assigned successfully.")  
try:
    global con,cursor
    print("Connecting to the MySQL DataBase...")
    con = mysql.connector.connect(
    host="localhost", user="root",
    password="", database="dbms")
    cursor = con.cursor()
    print("Starting the application...")
    init()
except Exception as e:
    print("Unable to connect to MySql Database,Check the Server Status")
    print("Can't connect to MySQL server on 'localhost:3306' (111 Connection refused)")
    raise e