import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
import connection
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
        self.entry_from = Entry(window)

        self.label_to = Label(window, text="Booking Status:", fg="white", bg="gray",font="Times")
        self.var_stat = StringVar()

        self.booking_stat = OptionMenu(self.window, self.var_stat, "booked", "completed")
        self.booking_stat.place(x=120, y=140)



        self.button_book = Button(window, text="DONE", command=self.assign_driver)
        self.button_view = Button(window, text="View Bookings", command=self.view_bookings)


        self.label_from.place(x=10, y=110)
        self.entry_from.place(x=90, y=110)
        self.label_to.place(x=10, y=140)



        self.button_book.place(x=230, y=110)
        self.button_view.place(x=230, y=140)

        # Create a frame for the Treeview
        self.tree_frame = ttk.Frame(window)
        self.tree_frame.place(x=1, y=200)

        # Create the Treeview
        column = ("Booking_id", "Pickup", "Drop-off", "date_of_booking", "booking status","driver id")
        self.tree_booking = ttk.Treeview(self.tree_frame, columns=column, show="headings", height=10)

        for col in column:
            self.tree_booking.heading(col, text=col, anchor="center")
            self.tree_booking.column(col, anchor="center", width=120)

        self.tree_booking.pack()

    def assign_driver(self):
        # Implement the booking logic here
        pass

    def view_bookings(self):
        try:
            with self._connection_.cursor() as cursor:
                query = "SELECT * FROM `bookings`"
                cursor.execute(query)

                # Fetch a limited number of rows at a time if there are a large number of rows
                rows = cursor.fetchmany(size=10)  # Adjust the size as needed

            for item in self.tree_booking.get_children():
                self.tree_booking.delete(item)

            for row in rows:
                self.tree_booking.insert(parent='', index='end',
                                         values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Driverdash(root)
    root.mainloop()
