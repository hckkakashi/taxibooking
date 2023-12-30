from tkinter import *
from PIL import Image, ImageTk
import connection
from tkinter import messagebox
import cust_dashboard
import superuser
import  admin_dash
class LoginPage:
    def __init__(self, window):
        self._connection_=connection.mysql_conecton.Conect()
        self.window = window
        self.window.geometry("720x480")
        self.window.title('Login Page')

        self.create_widget() 

    def create_widget(self):
        bg_image = Image.open("taxi.png")
        bg_image = bg_image.resize((720, 480))
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Set the background image on the window
        self.bg_label = Label(self.window, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.lbl = Label(self.window, text="CITY TAXI", width=100, fg="white", bg="black", font=("Times", 40, "bold"))
        self.lbl.place(x=210, y=50,width=300)

        self.lbl_1 = Label(self.window, text="Email", width=20, bg="black", fg="white", font=("Times", 15, "bold"))
        self.lbl_1.place(x=230, y=150, width=50)
        self.enter_1 = Entry(self.window, font=("Times", 10))
        self.enter_1.place(x=340, y=150, width=200)

        self.lbl_2 = Label(self.window, text="Password", width=20, bg="black", fg="white", font=("Times", 15, "bold"))
        self.lbl_2.place(x=180, y=200, width=90)
        self.enter_2 = Entry(self.window, show="*", font=("Times", 10))
        self.enter_2.place(x=340, y=200, width=200)

        self.btn_1 = Button(self.window, text="Login", width=10, font=("Times", 16, "bold"), bg="#4CAF50", fg="white",command=self.login)
        self.btn_1.place(x=250, y=250)

        self.btn_2 = Button(self.window, text="Register", width=10, font=("Times", 16, "bold"), bg="#4CAF50", fg="white",command=self.register)
        self.btn_2.place(x=400, y=250)



    def login(self):
        try:
            email = self.enter_1.get()
            password = self.enter_2.get()

            # Check if email and password are not empty
            if email=='' and password=='':
                messagebox.showerror("Taxi", "Please enter both email and password.")

            elif email=='':

                messagebox.showerror("Taxi", "Please enter email ")

            elif password=='':
                messagebox.showerror("Taxi", "Please enter  password")

            elif email!='' and password!='':

                with self._connection_.cursor() as cursor:
                    cursor.execute("SELECT * FROM registration WHERE email=%s AND password=%s", (email, password))
                    record = cursor.fetchone()

                    cursor.execute("SELECT * FROM admin WHERE email=%s AND password=%s", (email, password))
                    admin = cursor.fetchone()

                    cursor.execute("SELECT * FROM driver WHERE email=%s AND password=%s", (email, password))
                    driver = cursor.fetchone()

                    if record:
                        messagebox.showinfo("Taxi", "Login successful")

                        superuser.customer=record

                        self.window.destroy()
                        new_window = Tk()
                        cust_dashboard.customers(new_window)
                        new_window.mainloop()
                    elif admin:

                        import admin_dash
                        messagebox.showinfo("Taxi", "Admin Login successful")
                        self.window.destroy()
                        new_window = Tk()
                        admin_dash.Admindash(new_window)
                        new_window.mainloop()

                    elif driver:

                        import driver_dash
                        messagebox.showinfo("Taxi", "Driver Login successful")
                        self.window.destroy()
                        new_window = Tk()
                        driver_dash.Driverdash(new_window)
                        new_window.mainloop()

                    else:

                        messagebox.showerror("Taxi", "Invalid email or password")
        except Exception as e:
            print(e)


    def register(self):
        from regestration import (regpage)
        self.window.destroy()
        new_window = Tk()
        regpage(new_window)
        new_window.mainloop()

if __name__ == "__main__":
    window = Tk()
    app = LoginPage(window)
    window.mainloop()


