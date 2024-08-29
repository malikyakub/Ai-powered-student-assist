import tkinter as tk

window = tk.Tk()
window.geometry('400x400')

def Label_Creator(msg):
    msg_1.pack(side='bottom', padx=2, pady=2)
    msg_1.configure(text=msg)

message_text = tk.StringVar()

lower_fram = tk.Frame(window, width=400)
message_frame = tk.Frame(window)

en = tk.Entry(lower_fram,width=50, textvariable=message_text)
btn = tk.Button(lower_fram, text='click', command=lambda:Label_Creator(message_text.get()))

lower_fram.pack(side='bottom', pady=10, ipady=5, expand=False)
message_frame.pack(side='top', expand=True, fill='both')
en.pack(side='top', ipady=3)
btn.pack(side='bottom', padx=5)


# message labels
msg_1 = tk.Label(message_frame, text='', background='#000000', fg='#ffffff')

window.mainloop()