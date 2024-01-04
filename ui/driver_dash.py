import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
import connection
import superuser
class Driverdash:
    def __init__(self, window):
        self._connection_ = connection.mysql_conecton.Conect()
        self.window = window
        self.window.title("Driver Dashboard")
        self.window.geometry("720x428")
        self.window.configure(bg="black")

        # Initialize database
        # self.conn = sqlite3.connect('taxi_booking.db')
        self.lbl=Label(self.window, text="MAKE JOURNEY BETTER", fg="white", bg="gray", font=("Helvetica", 30 , "bold"))
        self.lbl.place(x=1,y=5,width=720)

        # Create GUI components
        self.label_from = Label(window, text="Booking Id:", fg="white", bg="gray",font="Times")
        self.entry_from = Entry(window,width=10)

        self.label_to = Label(window, text="Booking Status:", fg="white", bg="gray",font="Times")
        self.var_stat = StringVar()

        self.booking_stat = OptionMenu(self.window, self.var_stat, "booked", "completed")
        self.booking_stat.place(x=135, y=140)



        self.button_book = Button(window, text="DONE", command=self.assign_driver)
        self.button_view = Button(window, text="View Bookings", command=self.view_bookings)


        self.label_from.place(x=10, y=110)
        self.entry_from.place(x=100, y=110)
        self.label_to.place(x=10, y=140)

        self.button_log = Button(window, text="Log Out", command=self.logout)
        self.button_log.place(x=280, y=110)
        self.button_book.place(x=230, y=110)
        self.button_view.place(x=250, y=140)

        # Create a frame for the Treeview
        self.tree_frame = ttk.Frame(window)
        self.tree_frame.place(x=1, y=200)

        # Create the Treeview
        column = ("Booking_id", "Pickup", "Drop-off", "date_of_booking", "booking status","driver id")
        self.tree_booking = ttk.Treeview(self.tree_frame, columns=column, show="headings", height=10)
        self.tree_booking.bind("<<TreeviewSelect>>",self.selectedRow)
        for col in column:
            self.tree_booking.heading(col, text=col, anchor="center")
            self.tree_booking.column(col, anchor="center", width=120)

        self.tree_booking.pack()
        try:
            self.driverid = superuser.Driver[0]
            with self._connection_.cursor() as cursor:
                query = f"SELECT `booking_id`, `from_location`, `to_location`, `date_booking`, `booking_status`, `Driverid` FROM `bookings` WHERE `Driverid` = {self.driverid} and `booking_status` ='booked'"

                cursor.execute(query)
                rows = cursor.fetchmany(size=10)  # Adjust the size as needed

            for item in self.tree_booking.get_children():
                self.tree_booking.delete(item)

            for row in rows:
                self.tree_booking.insert(parent='', index='end',
                                         values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")

    def assign_driver(self):
        try:
            with self._connection_.cursor() as cursor:
                query = f"UPDATE bookings SET `booking_status`='completed' WHERE `booking_id`={self.entry_from.get()}"
                query1 = f"UPDATE driver SET `driver_stat`='active' where `driver_id`='{self.driverid}'"
                cursor.execute(query)
                cursor.execute(query1)
            # Commit the transaction
            self._connection_.commit()

            messagebox.showinfo("Taxi", "Trip Completed")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Update Failure: {err}")

    def selectedRow(self,event):
        selected_item = self.tree_booking.focus()
        values = self.tree_booking.item(selected_item, "values")

        if values:
            # self.booking_id.insert(0, values[0])

            self.entry_from.delete(0, "end")
            self.entry_from.insert(0, values[0])


            self.var_stat.set(values[4])



    def view_bookings(self):
        try:
            driverid = superuser.Driver[0]
            with self._connection_.cursor() as cursor:
                query = f"SELECT `booking_id`, `from_location`, `to_location`, `date_booking`, `booking_status`, `Driverid` FROM `bookings` WHERE `Driverid` = {driverid} and `booking_status` ='completed'"
                cursor.execute(query)
                rows = cursor.fetchmany(size=10)  # Adjust the size as needed

            for item in self.tree_booking.get_children():
                self.tree_booking.delete(item)

            for row in rows:
                self.tree_booking.insert(parent='', index='end',
                                         values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")

    def logout(self):
        from login import (LoginPage)
        self.window.destroy()
        new_window = Tk()
        LoginPage(new_window)
        new_window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = Driverdash(root)
    root.mainloop()
