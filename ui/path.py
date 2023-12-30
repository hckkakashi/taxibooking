from tkinter import *

class Path:
    def __init__(self, window):
        self.window = window
        self.window.geometry("480x240")
        self.window.title('Path')

        self.widget()

    def widget(self):
        self.lbl = Label(self.window, text="CITY TAXI", width=480, fg="black", bg="white", font=("Helvetica", 50, "bold"))
        self.lbl.place(x=1, y=10, width=480)

        self.btn_1 = Button(self.window, text="Driver", width=10, font=("Helvetica", 20, "bold"), bg="#4CAF50", fg="white")
        self.btn_1.place(x=50, y=160)

        self.btn_2 = Button(self.window, text="Customer", width=10, font=("Helvetica", 20, "bold"), bg="#4CAF50",
                            fg="white",command=self.register)
        self.btn_2.place(x=250, y=160)

    def register(self):
        from regestration import (regpage)
        self.window.destroy()
        new_window = Tk()
        regpage(new_window)
        new_window.mainloop()

if __name__ == "__main__":
    window = Tk()
    app = Path(window)
    window.mainloop()
