import tkinter as tk
import tkinter.font as tkFont

class TextDisplay:
    def __init__(self, root):
         root.title("Text Display")
         height = 500
         width = 500
         screen_width = root.winfo_screenwidth()
         screen_height = root.winfo_screenheight()
         alignstr = 'center'
         root.geometry("%dx%d+%d+%d" % (width, height, (screen_width -width)/2, (screen_height - height)/2))
         root.resizable(False, False)

if __name__ == '__main__':
    root = tk.Tk()
    td = TextDisplay(root)
    root.mainloop()