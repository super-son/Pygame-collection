import tkinter
win = tkinter.Tk()
win.title("key Event generator")
win.geometry("600x200")

key=""
def key_down(e):
    global key
    key = e.keysym  
    print(key)

win.bind("<KeyPress>", key_down) 
win.mainloop()

