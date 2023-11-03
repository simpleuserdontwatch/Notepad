from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
root = Tk()
root.iconbitmap('icon.ico')
root.title('New - Notepad')
menubar = Menu(root)
saved = False
savedpath = None
def selfont():
    def change(font):
        text["font"] = font
    root.tk.call("tk", "fontchooser", "configure", "-font", text["font"], "-command", root.register(change))
    root.tk.call("tk", "fontchooser", "show")
def new():
    global saved, savepath
    if not saved:
        ques = messagebox.askyesno('Are you sure?','Are you sure to create a new file?')
        if ques:
            text.delete('1.0',END)
            saved = False
            savedpath = None
            root.title('New - Notepad')
def close():
    if not saved:
        ques = messagebox.askyesnocancel('Are you sure?','You have unsaved changes.\nDo you want to save?')
        if ques == True:
            save()
            root.destroy()
        elif ques == False:
            root.destroy()
    else:
        root.destroy()
def saveas():
    global saved,savedpath
    file = filedialog.asksaveasfilename(parent=root,title="Select where to save")
    if file:
        saved = True
        with open(file,'w') as f:
            f.write(text.get('1.0',END))
        savedpath = file
        root.title(f'{savedpath} - Notepad')
def save():
    if savedpath:
        with open(savedpath,'w') as f:
            f.write(text.get('1.0',END))
    else:
        saveas()
def openfile():
    global saved,savedpath
    file = filedialog.askopenfilename(parent=root,title="Select file")
    with open(file,'r') as f:
        if not saved:
            ques = messagebox.askyesnocancel('Are you sure?','You have unsaved changes.\nDo you want to save?')
            if ques == True:
                save()
                text.delete('1.0',END)
                text.insert('1.0',f.read())
                saved = True
                savedpath = file
                root.title(f'{savedpath} - Notepad')
            elif ques == False:
                text.delete('1.0',END)
                text.insert('1.0',f.read())
                saved = True
                savedpath = file
                root.title(f'{savedpath} - Notepad')
        else:
            text.delete('1.0',END)
            text.insert('1.0',f.read())
            saved = True
            savedpath = file
            root.title(f'{savedpath} - Notepad')
def unsavedstate(event):
    global saved
    excluded_keys = ["Up", "Down", "Left", "Right", "Next", "Prior", "Home", "Control_L", "Shift_L", "Control_R", "Shift_R"]
    if event.keysym not in excluded_keys:
        saved = False
def find():
    s = simpledialog.askstring('Find','What string to find?')
    if s:
        idx = '1.0'
        while 1:
            idx = text.search(s, idx, nocase=1, 
                stopindex=END) 
            if not idx:
                break
            lastidx = '%s+%dc' % (idx, len(s)) 
            text.tag_add('found', idx, lastidx)
            text.mark_set("insert", idx)
            text.see("insert")
            idx = lastidx
    text.tag_config('found', foreground='white', background='blue')
    root.after(7000,lambda: text.tag_remove('found', '1.0', END))
def replace():
    s = simpledialog.askstring('Replace','Replace what?')
    if s:
        s2 = simpledialog.askstring('Replace','Replace with?')
        if s2:
            u = text.get('1.0',END)
            u = u.replace(s,s2)
            text.delete('1.0',END)
            text.insert('1.0',u)
def select():
    text.tag_add(SEL, "1.0", END)
    text.mark_set(INSERT, "1.0")
    text.see(INSERT)
def about():
    new()
    text.insert('1.0','============Opensource notepad============\nVersion 0.1\nMade by simpleuserdontwatch\n\nOpensource notepad is an application,\nWhich is just an notepad application\nSimilar to windows app.\nAs well windows notepad is not opensource so\nI remade it in a simple language\nAnd made it opensource.')
def secret(e):
    text.insert(END,"\nPorting notepad everywhere!")
file = Menu(menubar,tearoff=0)
menubar.add_cascade(label="File", menu=file)
file.add_command(label='New file',command=new)
file.add_command(label='Open',command=openfile)
file.add_command(label='Save...',command=save)
file.add_command(label='Save as',command=saveas)
file.add_separator()
file.add_command(label='Exit',command=close)

edit = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Edit", menu=edit)
edit.add_command(label='Cut',command=lambda: text.event_generate("<<Cut>>"))
edit.add_command(label='Copy',command=lambda: text.event_generate("<<Copy>>"))
edit.add_command(label='Paste',command=lambda: text.event_generate("<<Paste>>"))
edit.add_separator()
edit.add_command(label='Find...',command=find)
edit.add_command(label='Replace',command=replace)
edit.add_separator()
edit.add_command(label='Select All',command=select)

help1 = Menu(menubar,tearoff=0)
menubar.add_cascade(label="More", menu=help1)
help1.add_command(label='Font...',command=selfont)

help1 = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help", menu=help1)
help1.add_command(label='About notepad',command=about)

root.config(menu=menubar)
scrollbar = Scrollbar() 
scrollbar.pack(side = RIGHT, fill = Y)
text = Text(yscrollcommand=scrollbar.set,font=("Arial",13))
text.bind('<KeyPress>', unsavedstate)
text.pack(expand=True,fill=BOTH)
scrollbar.config(command=text.yview)
root.protocol("WM_DELETE_WINDOW", close)
text.bind('<Control-b>',secret)
root.mainloop()
