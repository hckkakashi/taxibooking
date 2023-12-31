from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import datetime
import connection
from tkinter import messagebox
import login
from tkinter import ttk
import logging
import mysql.connector

class regpage:
    def __init__(self, window):
        self. _connection_ = connection.mysql_conecton.Conect()
        self.window = window
        self.window.geometry("720x480")
        self.window.title('Registration Page')
        self.create_widget()

    def create_widget(self):
        bg_image = Image.open("reg.png")
        bg_image = bg_image.resize((720, 480))
        self.bg_image = ImageTk.PhotoImage(bg_image)
        self.id=0
        # Set the background image on the window
        self.bg_label = Label(self.window, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.lbl = Label(self.window, text="REGISTRATION", width=220, fg="white", bg="#A6A6A6", font=("Helvetica", 20, "bold"))
        self.lbl.place(x=10, y=10, width=220)
        self.lbl = Label(self.window, text="JOIN WITH US", width=220, fg="white", bg="#A6A6A6",
                         font=("Helvetica", 20, "bold"))
        self.lbl.place(x=10, y=400, width=220)

        self.lbls = Label(self.window, text="FAST.SAFE.CHEAP", width=480, fg="white", bg="black", font=("Times", 20))
        self.lbls.place(x=270, y=400, width=500)

        self.lbl_1 = Label(self.window, text="Fullname", width=20, bg="black", fg="white", font=("Helvetica", 15, "bold"))
        self.lbl_1.place(x=300, y=20, width=100)
        self.enter_1 = Entry(self.window, font=("Helvetica", 10))
        self.enter_1.place(x=450, y=20, width=200)

        self.lbl_2 = Label(self.window, text="Password", width=20, bg="black", fg="white", font=("Helvetica", 15, "bold"))
        self.lbl_2.place(x=300, y=70, width=100)
        self.enter_2 = Entry(self.window, show="*", font=("Helvetica", 10))
        self.enter_2.place(x=450, y=70, width=200)

        self.lbl_3 = Label(self.window, text="DOB", width=20, bg="black", fg="white", font=("Helvetica", 15, "bold"))
        self.lbl_3.place(x=300, y=120, width=100)
        self.calander_bttn = DateEntry(self.window, text="Pick Date", command=self.pick_date)
        self.calander_bttn.place(x=450, y=120)

        self.lbl_4 = Label(self.window, text="Gender", width=20, bg="black", fg="white", font=("Helvetica", 15, "bold"))
        self.lbl_4.place(x=300, y=170, width=100)

        self.var_gender = StringVar()
        self.radio_btn = ttk.Radiobutton(self.window, text="Male", variable=self.var_gender, value="Male",
                                  style="TRadiobutton")
        self.radio_btn.place(x=450, y=170)
        self.radio_btn1 = ttk.Radiobutton(self.window, text="Female", variable=self.var_gender, value="Female",
                                  style="TRadiobutton")
        self.radio_btn1.place(x=550, y=170)
        # self.gender_opt = "Male" if self.var_gender.get()=="Male" else "Female"
        self.lbl_5 = Label(self.window, text="Email", width=20, bg="black", fg="white", font=("Helvetica", 15, "bold"))
        self.lbl_5.place(x=300, y=220, width=100)
        self.enter_4 = Entry(self.window, font=("Helvetica", 10))
        self.enter_4.place(x=450, y=220, width=200)

        self.lbl_6 = Label(self.window, text="Phone Number", width=100, bg="black", fg="white", font=("Helvetica", 15, "bold"))
        self.lbl_6.place(x=270, y=270, width=200)
        self.enter_5 = Entry(self.window, font=("Helvetica", 10))
        self.enter_5.place(x=450, y=270, width=200)

        self.lbl_7 = Label(self.window, text="Payment Method", width=100, bg="black", fg="white",font=("Helvetica", 15, "bold"))
        self.lbl_7.place(x=260, y=310, width=200)

        self.var_pay = StringVar()
        self.var_pay.set("Select payment method")

        self.pay = OptionMenu(self.window,self.var_pay,"Cash", "Bank Transfer", "Online Payment")
        self.pay.place(x=460, y=310)


        self.button = Button(self.window, text="Register", command=self.register)
        self.button.place(x=460, y=350, width=70)

        self.button1 = Button(self.window, text="Clear", command=self.clear)
        self.button1.place(x=560, y=350, width=70)

    def pick_date(self):
        selected_date = self.calander_bttn.get()
        # Handle the selected date as needed
        print("Selected Date:", selected_date)

    def register(self):
        try:
            self.gender_opt = "Male" if self.var_gender.get() == "Male" else "Female"
            with self._connection_.cursor() as cursor:
                query = "INSERT INTO `registration` (`fullname`, `password`, `dob`, `gender`, `email`, `phonenumber`,`payment_method`) VALUES (%s, %s, %s, %s, %s, %s,%s)"
                data = (self.enter_1.get(), self.enter_2.get(), self.calander_bttn.get_date(), self.gender_opt,
                        self.enter_4.get(), self.enter_5.get(),self.var_pay.get())
                cursor.execute(query, data)
            self._connection_.commit()

            messagebox.showinfo("Taxi", "Registration Successful")
            self.window.destroy()
            new_window = Tk()
            login.LoginPage(new_window)
            new_window.mainloop()

        except Exception as e:
            print(e)
            messagebox.showerror("Taxi", "Registration Failure")

    def clear(self):
        # Clear all entry fields
        self.enter_1.delete(0, END)
        self.enter_2.delete(0, END)
        self.calander_bttn.set_date(datetime.date.today())
        self.radio_btn.deselect()
        self.radio_btn1.deselect()

        self.enter_4.delete(0, END)
        self.enter_5.delete(0, END)

if __name__ == "__main__":
    window = Tk()
    app = regpage(window)
    window.mainloop()
