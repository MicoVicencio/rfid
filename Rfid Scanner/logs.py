import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

class LogViewer:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("RFID Logs Viewer")
        self.root.geometry("1200x900")

        # Set style for bigger fonts
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=30)  # Bigger rows
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))  # Bigger headers

        # Create Treeview
        self.tree = ttk.Treeview(self.root, columns=("rfid", "role", "timestamp"), show="headings")
        self.tree.heading("rfid", text="RFID")
        self.tree.heading("role", text="Role")
        self.tree.heading("timestamp", text="Date & Time")

        self.tree.column("rfid", width=250)
        self.tree.column("role", width=150)
        self.tree.column("timestamp", width=300)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Define zebra style tags
        self.tree.tag_configure("oddrow", background="#f2f2f2")
        self.tree.tag_configure("evenrow", background="white")

        # Load data into Treeview
        self.load_logs()

    def load_logs(self):
        """Fetch logs from SQLite and insert into Treeview."""
        conn = sqlite3.connect("rfid.db")  # Change to your DB file
        cursor = conn.cursor()
        cursor.execute("SELECT rfid, role, timestamp FROM logs ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert fetched rows with zebra colors
        for index, (rfid, role, ts) in enumerate(rows):
            try:
                # Convert timestamp to a readable format
                date_str = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M %p")
            except ValueError:
                date_str = ts  # If formatting fails, keep original

            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(rfid, role, date_str), tags=(tag,))
    
    def run_log(self):
        self.root.mainloop()




