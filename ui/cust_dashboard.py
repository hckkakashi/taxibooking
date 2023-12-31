import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime
import connection
import tkinter.font as tkfont
import mysql.connector
import superuser
class customers:
    def __init__(self, window):
        self._connection_=connection.mysql_conecton.Conect()
        self.window = window
        self.window.title("Taxi Booking Dashboard")
        self.window.geometry("720x428")
        self.window.configure(bg="gray")
        self.bookid = StringVar()
        self.booking_id=Entry(textvariable=self.bookid)

        # Initialize database
        # self.conn = sqlite3.connect('taxi_booking.db')
        self.lbl=Label(self.window, text="BOOK NOW", fg="white", bg="gray", font=("Times", 55 , "bold"))
        self.lbl.place(x=160,y=5)

        # Create GUI components
        self.label_from = Label(window, text="From:", fg="white", bg="gray")
        self.entry_from = Entry(window)

        self.label_to = Label(window, text="To:", fg="white", bg="gray")
        self.entry_to = Entry(window)

        self.label_dob = Label(window, text="Date:", fg="white", bg="gray")
        self.calander_bttn = DateEntry(self.window, text="Pick Date")

        self.button_book = Button(window, text="Book Taxi", command=self.book_taxi)
        self.button_view = Button(window, text="View Bookings", command=self.view_bookings)
        self.button_update = Button(window, text="Update",command=self.update_bookings)
        self.button_log = Button(window, text="Log Out", command=self.logout)

        self.label_from.place(x=10, y=110)
        self.entry_from.place(x=80, y=110)
        self.label_to.place(x=10, y=140)
        self.entry_to.place(x=80, y=140)
        self.label_dob.place(x=10, y=170)
        self.calander_bttn.place(x=90, y=170)
        self.button_book.place(x=230, y=110)
        self.button_view.place(x=230, y=170)
        self.button_update.place(x=230, y=140)
        self.button_log.place(x=290, y=140)

        # Create a frame for the Treeview
        self.tree_frame = ttk.Frame(window)
        self.tree_frame.place(x=1, y=200)


        # Create the Treeview
        column = ("Booking_id", "Pickup Address", "Drop-off Address","date_of_booking","Booking_status")
        self.tree_booking = ttk.Treeview(self.tree_frame, columns=column, show="headings", height=10)
        self.tree_booking.bind("<<TreeviewSelect>>", self.selectedRow)
        for col in column:
            self.tree_booking.heading(col, text=col, anchor="center")
            self.tree_booking.column(col, anchor="center", width=145)


        self.tree_booking.pack()

    def selectedRow(self,event):
        selected_item = self.tree_booking.focus()
        values = self.tree_booking.item(selected_item, "values")

        if values:
            self.booking_id.insert(0, values[0])

            self.entry_from.delete(0, "end")
            self.entry_from.insert(0, values[1])

            self.entry_to.delete(0, "end")
            self.entry_to.insert(0, values[2])

            self.calander_bttn.delete(0, "end")
            self.calander_bttn.insert(0, values[3])









    def book_taxi(self):
        self.customer_id=superuser.customer[0]
        if not all([self.entry_from.get(), self.entry_to.get(), self.calander_bttn.get_date()]):
            messagebox.showerror("Taxi", "Please fill in all fields before booking.")
            return

        try:
            with self._connection_.cursor() as cursor:

                query = f"INSERT INTO `bookings`(`booking_id`, `from_location`, `to_location`, `date_booking`,`customer_id`) VALUES ('{self.booking_id}','{self.entry_from.get()}','{self.entry_to.get()}','{self.calander_bttn.get_date()}','{self.customer_id}')"
                cursor.execute(query)
                connection.mysql_conecton.Conect().commit()
            messagebox.showinfo("Taxi", "Booked")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Booking Failure: {err}")

    def view_bookings(self):
        self.cust_id=superuser.customer[0]
        try:
            with self._connection_.cursor() as cursor:
                query = f"SELECT `booking_id`, `from_location`, `to_location`, `date_booking`, `booking_status` FROM `bookings`where `customer_id` ={self.cust_id} "
                cursor.execute(query)
                rows = cursor.fetchall()

            for item in self.tree_booking.get_children():
                self.tree_booking.delete(item)

            for row in rows:
                self.tree_booking.insert(parent='', index='end', values=(row[0], row[1], row[2], row[3], row[4]))

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def update_bookings(self):
        try:
            with self._connection_.cursor() as cursor:
                query = f"UPDATE bookings SET  `from_location`='{self.entry_from.get()}', `to_location`='{self.entry_to.get()}', `date_booking`='{self.calander_bttn.get_date()}' WHERE `booking_id`={self.bookid.get()}"

                cursor.execute(query)
            # Commit the transaction
            self._connection_.commit()

            messagebox.showinfo("Taxi", "Updated bookings")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Update Failure: {err}")

    def logout(self):
        from login import (LoginPage)
        self.window.destroy()
        new_window = Tk()
        LoginPage(new_window)
        new_window.mainloop()
if __name__ == "__main__":
    root = tk.Tk()
    app = customers(root)
    root.mainloop()
