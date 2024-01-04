from tkinter import *
from tkinter import messagebox

import mysql.connector

import connection
from tkinter import  ttk
import tkinter as tk
class Adminhistory:
    def __init__(self, window):
        self._connection_ = connection.mysql_conecton.Conect()
        self.window = window
        self.window.title("Admin History")
        self.window.geometry("720x428")
        self.window.configure(bg="black")

        self.tree_frame = ttk.Frame(window)
        self.tree_frame.place(x=1, y=2)

        column = ("Booking_id", "Pickup", "Drop-off", "date_of_booking", "booking status", "customer id")

        self.tree_booking = ttk.Treeview(self.tree_frame, columns=column, show="headings", height=40)
        for col in column:
            self.tree_booking.heading(col, text=col, anchor="center")
            self.tree_booking.column(col, anchor="center", width=120)

        self.tree_booking.pack()
        try:
            with self._connection_.cursor() as cursor:
                query = "SELECT * FROM `bookings`"
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

if __name__ == "__main__":
    root = tk.Tk()
    app = Adminhistory(root)
    root.mainloop()