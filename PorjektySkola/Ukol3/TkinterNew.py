from tkinter import RIGHT, Frame, Label, Scrollbar, Tk, Menu, filedialog, Text, Y, END, askopenfilename, asksaveasfilename
from turtle import title 


def openFile():
    path=filedialog.askopenfilename(
        defaultextension="txt",
        filetypes=[("Text Files","*.txt"),("All Files","*.*")]
    )

    if path:
        with open(path,"r") as f:
            file=f.read()
        print(path)
        text_box.delete("1.0",END)
        text_box.insert(END,file)

    
def saveFile():
    path=filedialog.asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files","*.txt"),("All Files","*.*")]
    )

    if path:
        file=text_box.get("1.0",END)

        with open(path,"w") as f:
            f.write(file)
        print("Save")


# create main window
window = Tk()
window.title("Simple text editor")
# window.iconbitmap()
window.geometry("1200x800")

main_frame = Frame(window)
main_frame.pack(pady=5, padx=5)

text_scroll = Scrollbar(main_frame)
text_scroll.pack(side=RIGHT, fill=Y)

text_box = Text(main_frame, width=96, height=32, font=("Roboto", 16), selectbackground="yellow", selectforeground="black", yscrollcommand=text_scroll.set)
text_box.pack()

text_scroll.config(command=text_box.yview)

menu=Menu(window)
window.config(menu=menu)

file_menu = Menu(menu)
menu.add_cascade(label='File', menu=file_menu)

file_menu.add_command(label='Open', command=openFile)
file_menu.add_command(label='Save', command=saveFile)


window.mainloop()
