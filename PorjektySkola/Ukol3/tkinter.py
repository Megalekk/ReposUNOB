import tkinter as tk

window = tk.Tk()

text_frame = tk.Frame()
control_frame = tk.Frame()

label_text = tk.Label(master=text_frame,text='text frame')
label_text.pack()

text_box = tk.Text()

text_box.pack()

#greeting = tk.Label(text="Hello, Tkinter")

#greeting.pack()

window.mainloop()
