import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
import connection
class Admindash:
    def __init__(self, window):
        self._connection_ = connection.mysql_conecton.Conect()
        self.window = window
        self.window.title("Taxi Booking Dashboard")
        self.window.geometry("720x428")
        self.window.configure(bg="black")
        self.bookid=StringVar()
        self.booking_id=Entry(textvariable=self.bookid)

        # Initialize database
        # self.conn = sqlite3.connect('taxi_booking.db')
        self.lbl=Label(self.window, text="CONTROL PANEL", fg="white", bg="gray", font=("Times", 55 , "bold"))
        self.lbl.place(x=1,y=5,width=720)

        # Create GUI components
        self.label_from = Label(window, text="Driver:", fg="white", bg="gray")
        # self.entry_from = Entry(window)
        try:
            with self._connection_.cursor() as cursor:
                query = "SELECT `driver_id` from driver where `driver_stat`='active' "
                cursor.execute(query)
                mydata = cursor.fetchall()

            mylist = [r for r, in mydata]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")
        self.options = tk.StringVar(window)
        self.options.set('Choose Driverid')  # default value

        self.om1 = OptionMenu(window, self.options,*mylist)
        self.om1.place(x=80, y=110)

        self.label_to = Label(window, text="Booking Id:", fg="white", bg="gray")
        self.entry_to = Entry(window)

        self.label_dob = Label(window, text="Booking status", fg="white", bg="gray")
        # self.booking_stat = Entry(window)

        self.button_book = Button(window, text="Assign",command=self.Driver_bookings)

        self.button_log = Button(window, text="Log Out",command=self.logout)
        self.button_view = Button(window, text="View Booking History")

        self.var_stat = StringVar()


        self.booking_stat = OptionMenu(self.window, self.var_stat, "pending", "booked")
        self.booking_stat.place(x=100, y=170)


        self.label_from.place(x=10, y=110)
        # self.entry_from.place(x=80, y=110)
        self.label_to.place(x=10, y=140)
        self.entry_to.place(x=80, y=140)
        self.label_dob.place(x=10, y=170)
        # self.booking_stat.place(x=100, y=170)
        self.button_book.place(x=230, y=110)
        self.button_view.place(x=230, y=140)
        self.button_log.place(x=280, y=110)
        # Create a frame for the Treeview
        self.tree_frame = ttk.Frame(window)
        self.tree_frame.place(x=1, y=200)


        # Create the Treeview
        column = ("Booking_id", "Pickup", "Drop-off", "date_of_booking", "booking status","customer id")

        self.tree_booking = ttk.Treeview(self.tree_frame, columns=column, show="headings", height=10)
        self.tree_booking.bind("<<TreeviewSelect>>", self.assign_driver)
        for col in column:
            self.tree_booking.heading(col, text=col, anchor="center")
            self.tree_booking.column(col, anchor="center", width=100)

        self.tree_booking.pack()
        try:
            with self._connection_.cursor() as cursor:
                query = "SELECT * FROM `bookings` where `booking_status`='pending'"
                cursor.execute(query)

                rows = cursor.fetchmany(size=10)

            for item in self.tree_booking.get_children():
                self.tree_booking.delete(item)

            for row in rows:
                self.tree_booking.insert(parent='', index='end',
                                         values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")

    def assign_driver(self,event):
            selected_item = self.tree_booking.focus()
            values = self.tree_booking.item(selected_item, "values")

            if values:
                self.entry_to.delete(0, "end")
                self.entry_to.insert(0, values[0])


                self.var_stat.set((values[4]))

    def Driver_bookings(self):
        try:
            with self._connection_.cursor() as cursor:
                query = f"UPDATE `bookings` SET `booking_status`='booked',`Driverid`={self.options.get()} WHERE `booking_id` ={self.entry_to.get()}"
                result =cursor.execute(query)
                query1 = f"UPDATE `driver` SET driver_stat='in active' where `driver_id`={self.options.get()}"
                result1 = cursor.execute(query1)
                self._connection_.commit()
                messagebox.showinfo("Taxi", "Driver Assigned")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Assigned Failure: {err}")

    def logout(self):
        from login import (LoginPage)
        self.window.destroy()
        new_window = Tk()
        LoginPage(new_window)
        new_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Admindash(root)
    root.mainloop()
