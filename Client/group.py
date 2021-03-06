from tkinter import *
import tkinter.messagebox as messagebox
import requests
from json import loads
from widgets.lists import ScrolledList, GroupScrolledList, StudentScrolledList
from widgets.quitter import Quitter
from settings import SERVER

def get_students(event, text, studentList):
    r = requests.get('{0}query/{1}'.format(SERVER, text))
    receive = loads(r.text)
    if receive == 'Error':
        return messagebox.showerror(title='Query error', 
            message='Cannot handle query.')
    studentList.fillListbox(receive['persons'])

def main():
    root = Tk()
    root.title('StudentGroupApp')
    root.minsize(10, 10)
    root.maxsize(100, 10)
    root.maxsize
    try:
        r = requests.get('{0}groups'.format(SERVER))
        j = loads(r.text)
        options = [x['code'] for x in j['groups']]
        v = StringVar()
        ent = Entry(root, textvariable=v)
        ent.pack(side=TOP, expand=YES, fill=X)
        ent.insert(0, 'Enter here...')
        Quitter().pack(side=BOTTOM, anchor=E)
        st = StudentScrolledList(parent=root, key=('name', 'surname'), title='Students')
        st.pack(side=RIGHT)
        GroupScrolledList(st, elements=j['groups'], parent=root, key=('code',), title='Groups').pack()
        ent.bind('<Shift-Up>', lambda i=ent, x=v.get(), y=st: get_students(i, v.get(), y))
    except Exception as e: 
        messagebox.showerror(title='Connection error.', 
            message='Server does not response. Check your connection.')
        root.destroy()
    root.mainloop() 

if __name__=='__main__':
    main()
