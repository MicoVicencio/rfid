import tkinter as tk
from tkinter import messagebox
import sqlite3
import threading
import keyboard  # Make sure this is installed
import time
from tkinter import ttk
import tkinter.font as tkfont
import logs 


class RFID:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RFID Data Management")
        self.root.geometry("900x470")
        self.root.config(bg="#f2f2f2")

        # Universal DB connection
        self.conn = sqlite3.connect("rfid.db",check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup_database()

        self.create_widgets()

    def setup_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_rfid TEXT ,
                name TEXT,
                section TEXT,
                email TEXT,
                mobile TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS parent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_rfid TEXT ,
                student_rfid TEXT,
                name TEXT,
                section TEXT,
                email TEXT,
                mobile TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rfid TEXT,
                role TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        title = tk.Label(self.root, text="RFID DATA MANAGEMENT", font=("Arial", 28, "bold"), bg="#f2f2f2")
        title.pack(pady=20)

        button_frame = tk.Frame(self.root, bg="#f2f2f2")
        button_frame.pack(pady=50)

        add_btn = tk.Button(button_frame, text="Add User", width=20, height=2, bg="#4CAF50", fg="white",
                            font=("Arial", 14, "bold"), command=self.add_user)
        add_btn.grid(row=0, column=0, padx=20, pady=10)

        view_btn = tk.Button(button_frame, text="View Users", width=20, height=2, bg="#2196F3", fg="white",
                             font=("Arial", 14, "bold"), command=self.view_users)
        view_btn.grid(row=0, column=1, padx=20, pady=10)

        update_btn = tk.Button(button_frame, text="Update User", width=20, height=2, bg="#FFC107", fg="black",
                               font=("Arial", 14, "bold"), command=self.update_user)
        update_btn.grid(row=1, column=0, padx=20, pady=10)

        # New View Logs button in the middl

        delete_btn = tk.Button(button_frame, text="Delete User", width=20, height=2, bg="#F44336", fg="white",
                               font=("Arial", 14, "bold"), command=self.delete_user)
        delete_btn.grid(row=1, column=1, padx=20, pady=10)
        
        logs_btn = tk.Button(button_frame, text="View Logs", width=20, height=2, bg="#9C27B0", fg="white",
                             font=("Arial", 14, "bold"), command=self.view_logs)
        logs_btn.grid(row=2, column=0,columnspan=2, padx=20, pady=10)

    def view_logs(self):
            show = logs.LogViewer()
            show.run_log()
            
    def add_user(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add User")
        add_window.geometry("800x500")

        font = ("Arial", 14)

        # Role Selection Frame
        role_frame = tk.Frame(add_window)
        role_frame.pack(pady=20)

        tk.Label(role_frame, text="Select Role:", font=font).pack(side="left", padx=10)
        role_var = tk.StringVar(value="")
        
        def submit():
                role = role_var.get()
                if role == "student":
                        data = (
                                student_rfid_entry.get(),
                                student_name_entry.get(),
                                student_section_entry.get(),
                                student_email_entry.get(),
                                student_mobile_entry.get()
                        )
                        self.cursor.execute( "INSERT OR REPLACE INTO student (student_rfid, name, section, email, mobile) VALUES (?, ?, ?, ?, ?)",
                                data)

                elif role == "parent":
                        
                        
                        
                        
                        data = (
                                parent_rfid_entry.get(),
                                matching_student_rfid_entry.get(),
                                parent_name_entry.get(),
                                parent_section_entry.get(),
                                parent_email_entry.get(),
                                parent_mobile_entry.get()
                        )
                        rfid_value = matching_student_rfid_entry.get()
                        self.cursor.execute("SELECT mobile FROM student WHERE student_rfid = ?", (rfid_value,))
                        student_data = self.cursor.fetchone()
                        
                        if student_data:
                                self.cursor.execute("INSERT OR REPLACE INTO parent (parent_rfid, student_rfid, name, section, email, mobile) VALUES (?, ?, ?, ?, ?, ?)",
                                data)
                        else:
                                messagebox.showerror("Error","The matching address can't be found on the database!")
                                add_window.destroy()
                                return
                        
                        
                        
                        
                        # Save matching info to logs or link table if needed later

                else:
                        messagebox.showerror("Error", "Please select a role before submitting.")
                        return

                self.conn.commit()
                messagebox.showinfo("Success", f"{role.title()} added successfully!")
                add_window.destroy() 
                
        def show_form():
                role = role_var.get()
                if role == "student":
                        parent_form.pack_forget()
                        student_form.pack(pady=10)
                elif role == "parent":
                        student_form.pack_forget()
                        parent_form.pack(pady=10)

        tk.Radiobutton(role_frame, text="Student", variable=role_var, value="student", font=font, command=show_form).pack(side="left", padx=10)
        tk.Radiobutton(role_frame, text="Parent", variable=role_var, value="parent", font=font, command=show_form).pack(side="left", padx=10)

        # ---------- Student Form ----------
        student_form = tk.Frame(add_window)

        tk.Label(student_form, text="Student RFID:", font=font).grid(row=0, column=0, sticky="w", pady=5)
        student_rfid_entry = tk.Entry(student_form, font=font)
        student_rfid_entry.grid(row=0, column=1)
        tk.Button(student_form, text="Scan", font=("Arial", 12), command=lambda: scan_rfid(student_rfid_entry)).grid(row=0, column=2, padx=10)

        tk.Label(student_form, text="Name:", font=font).grid(row=1, column=0, sticky="w", pady=5)
        student_name_entry = tk.Entry(student_form, font=font)
        student_name_entry.grid(row=1, column=1)

        tk.Label(student_form, text="Section:", font=font).grid(row=2, column=0, sticky="w", pady=5)
        student_section_entry = tk.Entry(student_form, font=font)
        student_section_entry.grid(row=2, column=1)

        tk.Label(student_form, text="Email:", font=font).grid(row=3, column=0, sticky="w", pady=5)
        student_email_entry = tk.Entry(student_form, font=font)
        student_email_entry.grid(row=3, column=1)

        tk.Label(student_form, text="Mobile No.:", font=font).grid(row=4, column=0, sticky="w", pady=5)
        student_mobile_entry = tk.Entry(student_form, font=font)
        student_mobile_entry.grid(row=4, column=1)
        tk.Button(student_form, text="Submit", font=font, bg="green", fg="white", command=submit).grid(row=5, column=1, sticky="w", pady=5)

        # ---------- Parent Form ----------
        parent_form = tk.Frame(add_window)

        tk.Label(parent_form, text="Parent RFID:", font=font).grid(row=0, column=0, sticky="w", pady=5)
        parent_rfid_entry = tk.Entry(parent_form, font=font)
        parent_rfid_entry.grid(row=0, column=1)
        tk.Button(parent_form, text="Scan", font=("Arial", 12), command=lambda: scan_rfid(parent_rfid_entry)).grid(row=0, column=2, padx=10)

        tk.Label(parent_form, text="Matching Student RFID:", font=font).grid(row=1, column=0, sticky="w", pady=5)
        matching_student_rfid_entry = tk.Entry(parent_form, font=font)
        matching_student_rfid_entry.grid(row=1, column=1)
        tk.Button(parent_form, text="Scan", font=("Arial", 12), command=lambda: scan_rfid(matching_student_rfid_entry)).grid(row=1, column=2, padx=10)

        tk.Label(parent_form, text="Name:", font=font).grid(row=2, column=0, sticky="w", pady=5)
        parent_name_entry = tk.Entry(parent_form, font=font)
        parent_name_entry.grid(row=2, column=1)

        tk.Label(parent_form, text="Section:", font=font).grid(row=3, column=0, sticky="w", pady=5)
        parent_section_entry = tk.Entry(parent_form, font=font)
        parent_section_entry.grid(row=3, column=1)

        tk.Label(parent_form, text="Email:", font=font).grid(row=4, column=0, sticky="w", pady=5)
        parent_email_entry = tk.Entry(parent_form, font=font)
        parent_email_entry.grid(row=4, column=1)

        tk.Label(parent_form, text="Mobile No.:", font=font).grid(row=5, column=0, sticky="w", pady=5)
        parent_mobile_entry = tk.Entry(parent_form, font=font)
        parent_mobile_entry.grid(row=5, column=1)
        
        tk.Button(parent_form, text="Submit", font=font, bg="green", fg="white", command=submit).grid(row=6, column=1, sticky="w", pady=5)
        
        

        # ---------- RFID Scan Logic ----------
        def scan_rfid(entry_box):
                entry_box.delete(0, tk.END)
                entry_box.insert(0, "Place RFID Tag...")

                def listen():
                        rfid_code = ""
                        while True:
                                event = keyboard.read_event(suppress=True)
                                if event.event_type == keyboard.KEY_DOWN:
                                        key = event.name
                                        if key == 'enter':
                                                break
                                        elif len(key) == 1:
                                                rfid_code += key
                        entry_box.delete(0, tk.END)
                        entry_box.insert(0, rfid_code)

                threading.Thread(target=listen, daemon=True).start()

        # ---------- Submit Logic ----------
        

        


    def view_users(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Users")
        view_window.geometry("900x600")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11))

        # Student Section
        student_label = tk.Label(view_window, text="Student Users", font=("Arial", 14, "bold"))
        student_label.pack(pady=10)

        student_tree = ttk.Treeview(view_window, columns=("ID", "Name", "Section", "RFID"), show="headings", height=8)
        student_tree.heading("ID", text="ID")
        student_tree.heading("Name", text="Name")
        student_tree.heading("Section", text="Section")
        student_tree.heading("RFID", text="RFID")
        student_tree.pack(pady=10)

        self.cursor.execute("SELECT id, name, section, student_rfid FROM student")
        for row in self.cursor.fetchall():
            student_tree.insert("", "end", values=row)

        # Parent Section
        parent_label = tk.Label(view_window, text="Parent Users", font=("Arial", 14, "bold"))
        parent_label.pack(pady=10)

        parent_tree = ttk.Treeview(view_window, columns=("ID", "Name", "Section", "RFID"), show="headings", height=8)
        parent_tree.heading("ID", text="ID")
        parent_tree.heading("Name", text="Name")
        parent_tree.heading("Section", text="Section")
        parent_tree.heading("RFID", text="RFID")
        parent_tree.pack(pady=10)

        self.cursor.execute("SELECT id, name, section, parent_rfid FROM parent")
        for row in self.cursor.fetchall():
            parent_tree.insert("", "end", values=row)

    def update_user(self):

        def scan_rfid():
                scan_entry.delete(0, tk.END)
                scan_entry.insert(0, "Place RFID Tag...")

                def listen():
                        scanned_rfid = ""
                        while True:
                                event = keyboard.read_event(suppress=True)
                                if event.event_type == keyboard.KEY_DOWN:
                                        if event.name == 'enter':
                                                break
                                        scanned_rfid += event.name
                        scan_entry.delete(0, tk.END)
                        scan_entry.insert(0, scanned_rfid)
                        search_records(scanned_rfid)

                threading.Thread(target=listen, daemon=True).start()

        def search_records(rfid_code):
                self.cursor.execute("SELECT student_rfid, name, section, email, mobile FROM student WHERE student_rfid = ?", (rfid_code,))
                student_data = self.cursor.fetchone()

                self.cursor.execute("SELECT parent_rfid, student_rfid, name, section, email, mobile FROM parent WHERE parent_rfid = ?", (rfid_code,))
                parent_data = self.cursor.fetchone()

                for widget in form_frame.winfo_children():
                        widget.destroy()

                data_entries.clear()

                if student_data:
                        role_label.config(text="Student Found", fg="green")
                        current_role.set("student")
                        current_rfid.set(student_data[0])
                        show_form(student_data, student_labels)
                elif parent_data:
                        role_label.config(text="Parent Found", fg="blue")
                        current_role.set("parent")
                        current_rfid.set(parent_data[0])
                        show_form(parent_data, parent_labels)
                else:
                        role_label.config(text="No Record Found", fg="red")
                        current_role.set("")
                        current_rfid.set("")

        def show_form(data, label_list):
                for i, label in enumerate(label_list):
                        tk.Label(form_frame, text=label, font=font).grid(row=i, column=0, sticky="w", pady=4, padx=10)
                        entry = tk.Entry(form_frame, font=font, width=30)
                        if i < len(data):
                                entry.insert(0, data[i])
                        entry.grid(row=i, column=1, pady=4)
                        data_entries.append(entry)

        def save_updates():
                values = [entry.get() for entry in data_entries]
                if current_role.get() == "student":
                        self.cursor.execute("""
                                UPDATE student SET 
                                student_rfid = ?, name = ?, section = ?, email = ?, mobile = ?
                                WHERE student_rfid = ?
                        """, (*values, current_rfid.get()))
                elif current_role.get() == "parent":
                        self.cursor.execute("""
                                UPDATE parent SET 
                                parent_rfid = ?, student_rfid = ?, name = ?, section = ?, email = ?, mobile = ?
                                WHERE parent_rfid = ?
                        """, (*values, current_rfid.get()))
                self.conn.commit()
                messagebox.showinfo("Success", "User information updated.")

                # GUI setup
        update_form = tk.Toplevel(self.root)
        update_form.title("Update User")
        update_form.geometry("900x600")

        font = tkfont.Font(family="Arial", size=16)

        # Configure columns of the main window
        update_form.grid_columnconfigure(0, weight=1)

        # Frame for Scan RFID section
        scan_frame = tk.Frame(update_form)
        scan_frame.grid(row=0, column=0, pady=20)

        tk.Label(scan_frame, text="Scan RFID", font=font).grid(row=0, column=0, padx=10)
        scan_entry = tk.Entry(scan_frame, font=font, width=30)
        scan_entry.grid(row=0, column=1, padx=10)
        tk.Button(scan_frame, text="Scan", command=scan_rfid, bg="blue", fg="white", font=font).grid(row=0, column=2, padx=10)

        role_label = tk.Label(update_form, text="", font=font)
        role_label.grid(row=1, column=0, pady=10)

        # Frame for form fields
        form_frame = tk.Frame(update_form)
        form_frame.grid(row=2, column=0, pady=20)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        # Save button
        tk.Button(update_form, text="Save", command=save_updates, bg="green", fg="white", font=font, width=20, height=2).grid(row=3, column=0, pady=20)

        # Labels and entries (initialize here)
        student_labels = ["RFID", "Name", "Section", "Email", "Mobile"]
        parent_labels = ["RFID", "Linked Student RFID", "Name", "Section", "Email", "Mobile"]
        data_entries = []
        current_role = tk.StringVar()
        current_rfid = tk.StringVar()





    def delete_user(self):
        def student():
                self.cursor.execute("SELECT name FROM student")
                students = self.cursor.fetchall()
                names = [row[0] for row in students]
                selection['values'] = names
                selection.set('')

        def parent():
                self.cursor.execute("SELECT name FROM parent")
                parents = self.cursor.fetchall()
                names = [row[0] for row in parents]
                selection['values'] = names
                selection.set('')

        def delete_selected():
                selected_name = selection.get()
                if not selected_name:
                        tk.messagebox.showwarning("No Selection", "Please select a name to delete.")
                        return

                confirm = tk.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_name}'?")
                if not confirm:
                        return

                self.cursor.execute("SELECT name FROM student")
                student_names = [row[0] for row in self.cursor.fetchall()]

                if selected_name in student_names:
                        self.cursor.execute("DELETE FROM student WHERE name = ?", (selected_name,))
                else:
                        self.cursor.execute("DELETE FROM parent WHERE name = ?", (selected_name,))

                self.conn.commit()
                tk.messagebox.showinfo("Deleted", f"{selected_name} has been deleted.")
                selection.set('')
                selection['values'] = []

        # Main frame setup
        self.delete_frame = tk.Toplevel(self.root)
        self.delete_frame.geometry("600x400")
        self.delete_frame.title("Delete User")

        # Fonts
        header_font = ("Arial", 18, "bold")
        label_font = ("Arial", 14)
        btn_font = ("Arial", 14)

        # Center layout using grid
        self.delete_frame.columnconfigure(0, weight=1)

        tk.Label(self.delete_frame, text="Select User Type", font=header_font).grid(row=0, column=0, pady=20)

        radio_frame = tk.Frame(self.delete_frame)
        radio_frame.grid(row=1, column=0, pady=10)
        tk.Radiobutton(radio_frame, text="Student", font=label_font, value="student", command=student).pack(side="left", padx=20)
        tk.Radiobutton(radio_frame, text="Parent", font=label_font, value="parent", command=parent).pack(side="left", padx=20)

        tk.Label(self.delete_frame, text="Select Name", font=label_font).grid(row=2, column=0, pady=(20, 5))
        selection = ttk.Combobox(self.delete_frame, font=("Arial", 14), width=35, state="readonly")
        selection.grid(row=3, column=0, pady=10)

        delete_btn = ttk.Button(self.delete_frame, text="Delete", command=delete_selected)
        delete_btn.grid(row=4, column=0, pady=30)
        delete_btn.configure(style="Delete.TButton")

        # Style the delete button
        style = ttk.Style()
        style.configure("Delete.TButton", font=btn_font, padding=10)


        
        

    def run(self):
        self.root.mainloop()


# Run the app
start = RFID()
start.run()
