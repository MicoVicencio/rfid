import keyboard
import tkinter as tk
from tkinter import ttk
import sqlite3
import threading
import tkinter.font as tkfont
from PIL import Image, ImageTk
import time
import datetime

class UI:
    def __init__(self):
        self.conn = sqlite3.connect("rfid.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.parents_waiting = {}
        self.students_pickup = {}
        self.parent_num = 0
        self.student_num = 0
        self.student_rfid = []
        self.parents_rfid = []
        self.pickup_rfid = set()
        self.student_waiting = {
                'Student1': {'student_rfid': '0651888163', 'name': 'Allen Gabilo'},
                'Student2': {'student_rfid': '0651888164', 'name': 'Mico Vicencio'},
                'Student3': {'student_rfid': '0651888165', 'name': 'Sebastine Vargas'},
                'Student4': {'student_rfid': '0651888166', 'name': 'Juan Dela Cruz'},
                'Student5': {'student_rfid': '0651888167', 'name': 'Maria Santos'},
                'Student6': {'student_rfid': '0651888168', 'name': 'Pedro Pascual'},
                'Student7': {'student_rfid': '0651888169', 'name': 'Ana Reyes'},
                'Student8': {'student_rfid': '0651888170', 'name': 'Mark Anthony'},
                'Student9': {'student_rfid': '0651888171', 'name': 'Carla Mae'},
                'Student10': {'student_rfid': '0651888172', 'name': 'Jessa Mae'},
                'Student11': {'student_rfid': '0651888173', 'name': 'Leo Santos'},
                'Student12': {'student_rfid': '0651888174', 'name': 'Andrea Dela Cruz'},
                'Student13': {'student_rfid': '0651888175', 'name': 'Michael Tan'},
                'Student14': {'student_rfid': '0651888176', 'name': 'Sophia Cruz'},
                'Student15': {'student_rfid': '0651888177', 'name': 'Christian Lim'},
                'Student16': {'student_rfid': '0651888178', 'name': 'Grace Villanueva'},
                'Student17': {'student_rfid': '0651888179', 'name': 'John Paul'},
                'Student18': {'student_rfid': '0651888180', 'name': 'Kyla Ann'},
                'Student19': {'student_rfid': '0651888181', 'name': 'Joshua Kim'},
                'Student20': {'student_rfid': '0651888182', 'name': 'Liza Soberano'},
                'Student21': {'student_rfid': '0651888183', 'name': 'Daniel Padilla'},
                'Student22': {'student_rfid': '0651888184', 'name': 'Kathryn Bernardo'},
                'Student23': {'student_rfid': '0651888185', 'name': 'Enrique Gil'},
                'Student24': {'student_rfid': '0651888186', 'name': 'Julia Barretto'},
                'Student25': {'student_rfid': '0651888187', 'name': 'Gerald Anderson'},
                'Student26': {'student_rfid': '0651888188', 'name': 'Bea Alonzo'},
                'Student27': {'student_rfid': '0651888189', 'name': 'James Reid'},
                'Student28': {'student_rfid': '0651888190', 'name': 'Nadine Lustre'},
                'Student29': {'student_rfid': '0651888191', 'name': 'Coco Martin'},
                'Student30': {'student_rfid': '0651888192', 'name': 'Angel Locsin'},
        }


        # Demo data with timestamps
        now = time.time()
        self.pickup_list = {
            "RFID001": {"name": "Juan Dela Cruz", "section": "Grade 6 - A", "time": now},
            "RFID002": {"name": "Maria Santos", "section": "Grade 6 - B", "time": now},
            "RFID003": {"name": "Pedro Reyes", "section": "Grade 5 - A", "time": now},
            "RFID004": {"name": "Ana Dizon", "section": "Grade 4 - C", "time": now},
            "RFID005": {"name": "Josefina Cruz", "section": "Grade 5 - B", "time": now},
            "RFID006": {"name": "Carlos Lim", "section": "Grade 3 - A", "time": now},
            "RFID007": {"name": "Sofia Tan", "section": "Grade 2 - C", "time": now},
            "RFID008": {"name": "Miguel Bautista", "section": "Grade 1 - A", "time": now},
            "RFID009": {"name": "Elena Ramos", "section": "Kinder - B", "time": now},
            "RFID010": {"name": "Ricardo Villanueva", "section": "Grade 6 - C", "time": now},
            "RFID011": {"name": "Mark Lopez", "section": "Grade 5 - C", "time": now},
            "RFID012": {"name": "Jessa Morales", "section": "Grade 3 - B", "time": now},
            "RFID013": {"name": "Paolo Garcia", "section": "Grade 2 - A", "time": now},
            "RFID014": {"name": "Liza Fernandez", "section": "Grade 4 - A", "time": now},
            "RFID015": {"name": "Nina Villanueva", "section": "Grade 6 - D", "time": now},
            "RFID016": {"name": "Andrei Cruz", "section": "Grade 5 - A", "time": now},
            "RFID017": {"name": "Kristel Ramos", "section": "Grade 1 - C", "time": now},
            "RFID018": {"name": "Allan Diaz", "section": "Grade 3 - C", "time": now},
            "RFID019": {"name": "Mica Torres", "section": "Grade 2 - B", "time": now},
            "RFID020": {"name": "Robert Mendoza", "section": "Grade 6 - E", "time": now}
        }

        self.root = tk.Tk()
        self.root.title("MAIN UI")
        self.root.state('zoomed')

        self.load_seal_image()

        self.big_font = tkfont.Font(family="Arial", size=30)

        self.image_label = ttk.Label(self.root, image=self.seal_photo)
        self.image_label.pack(pady=10)
        # Date & Time Label
        self.datetime_label = ttk.Label(self.root, font=("Arial", 24))
        self.datetime_label.pack(pady=5)
        # "To be Pick up" Label
        self.pickup_label = ttk.Label(self.root, text="Students to be Pick up", font=("Arial", 28, "bold"))
        self.pickup_label.pack(pady=10)

        # Start updating time
        self.update_datetime()
        
        style = ttk.Style(self.root)
        style.configure("Treeview",
                        font=self.big_font,
                        rowheight=50,
                        borderwidth=2,
                        relief="solid")
        style.configure("Treeview.Heading", font=self.big_font)
        style.map('Treeview', background=[('selected', '#347083')])

        columns = ("name", "section")

        # Create frame for fixed size Treeview
        tree_frame = tk.Frame(self.root, width=2220, height=560)
        tree_frame.pack_propagate(False)  # Prevent auto-resize
        tree_frame.pack(pady=1)

        # Now attach Treeview to tree_frame
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', style="Treeview")
        self.tree.heading("name", text="Name", anchor='center')
        self.tree.heading("section", text="Section", anchor='center')
        self.tree.column("name", width=600, anchor='center')
        self.tree.column("section", width=300, anchor='center')

        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="#e6f2ff")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        
        
        self.pickup_label = ttk.Label(self.root, text="Waiting Students", font=("Arial", 18, "bold"))
        self.pickup_label.pack(pady=10)
        # Create the text widget once
        self.names_text = tk.Text(self.root, height=7, width=79, font=("Arial", 34))
        self.names_text.pack(padx=10, pady=10)
        

        self.current_index = 0
        self.items_per_page = 10

        self.update_treeview()
        self.populate_names()
        
        
        
        
    def populate_names(self, start_index=0):
        """Show student names in chunks of 10 every 7 seconds."""
        self.names_text.delete("1.0", tk.END)

        if self.student_waiting:
            names = [student["name"] for student in self.student_waiting.values()]

            # Slice for current batch
            batch = names[start_index:start_index + 10]

            # Join into comma-separated string
            names_str = " || ".join(batch)
            self.names_text.insert(tk.END, names_str)

            # Compute next start index (wrap around)
            next_index = start_index + 10
            if next_index >= len(names):
                next_index = 0  # restart from beginning

            # Schedule next update after 7 seconds
            self.names_text.after(7000, lambda: self.populate_names(next_index))
        else:
            self.names_text.insert(tk.END, "")


    def load_seal_image(self):
        image = Image.open("seal.png")
        max_width, max_height = 700, 700
        image.thumbnail((max_width, max_height), Image.LANCZOS)
        self.seal_photo = ImageTk.PhotoImage(image)

    def cleanup_expired_pickups(self):
        now = time.time()
        expired_rfids = [
            rfid for rfid, info in self.pickup_list.items()
            if "time" in info and now - info["time"] >= 180
        ]
        for rfid in expired_rfids:
            del self.pickup_list[rfid]

    def update_treeview(self):
        self.cleanup_expired_pickups()  # Auto-remove expired entries

        for row in self.tree.get_children():
            self.tree.delete(row)

        data_items = list(self.pickup_list.items())
        page_data = data_items[self.current_index:self.current_index + self.items_per_page]

        for idx, (rfid, info) in enumerate(page_data):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(info["name"], info["section"]), tags=(tag,))

        self.current_index += self.items_per_page
        if self.current_index >= len(data_items):
            self.current_index = 0

        self.root.after(8000, self.update_treeview)

    def get_pickup_details(self):
        current_time = time.time()
        for rfid in self.pickup_rfid:
            self.cursor.execute(
                "SELECT name, section FROM student WHERE student_rfid = ?",
                (rfid,)
            )
            row = self.cursor.fetchone()
            if row:
                name, section = row
                self.pickup_list[rfid] = {
                    "name": name,
                    "section": section,
                    "time": current_time
                }
        self.update_treeview()
        
        
    def update_datetime(self):
        current_time = time.strftime("%B %d, %Y - %I:%M:%S %p")
        self.datetime_label.config(text=current_time, anchor="center")
        self.root.after(1000, self.update_datetime)  # Update every second

         
            
            
    def rfid_scanner(self):
        rfid_code = ""
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                if key == 'enter':
                    print(rfid_code)
                    self.get_rfid(rfid_code)
                    rfid_code = ""  # reset for next scan
                elif len(key) == 1:
                    rfid_code += key
                    
                    
    def get_rfid(self,rfid_code):
        code = rfid_code
        
        self.cursor.execute("SELECT student_rfid, name, section FROM student WHERE student_rfid = ?",(code,))
        student_data = self.cursor.fetchone()
        if student_data:
            self.format_student(student_data)
            self.comparing()
        else:
            self.cursor.execute("SELECT parent_rfid, name, student_rfid FROM parent WHERE parent_rfid = ?",(code,))
            parent_data = self.cursor.fetchone()
            if parent_data:
                self.format_parent(parent_data) 
                self.comparing()
    
    
    def format_student(self,data):
        self.student_num += 1
        student_rfid = data[0]
        if student_rfid not in self.pickup_rfid:
            if not any(student["student_rfid"] == student_rfid for student in self.student_waiting.values()):
                self.student_waiting["Student"+str(self.student_num)]= {
                    "student_rfid" : data [0],
                    "name" : data[1],
                    "section": data[2]
                }
                self.populate_names()
                
            else:
                print("Student already exisit")
        else:
            print("Student Already in Pickup list")
            
    def format_parent(self,data):
        self.parent_num += 1
        parent_rfid  = data[0]
        student_rfid = data[2]
        if student_rfid not in self.pickup_rfid:
            if not any(parent["parent_rfid"] == parent_rfid for parent in self.parents_waiting.values()):
                self.parents_waiting["Parent" + str(self.parent_num)] = {
                    "parent_rfid": data [0],
                    "name": data[1],
                    "student_rfid": data[2]
                }
            else:
                print("Parent Already Exist")     
        else:
            print("Student Already in Pickup list")
              
        
    
    def comparing(self):
        self.student_rfid = [rfid["student_rfid"] for rfid in self.student_waiting.values()]
        self.parents_rfid = [rfid["student_rfid"] for rfid in self.parents_waiting.values()]
        
        for rfid in self.student_rfid:
            if rfid in self.parents_rfid:
                self.pickup_rfid.add(rfid)   
                self.get_pickup_details()

                # 1️⃣ Get student name from SQLite
                self.cursor.execute("SELECT name FROM student WHERE student_rfid = ?", (rfid,))
                row = self.cursor.fetchone()
                name = row[0] if row else "Unknown"

                # 2️⃣ Insert into rfid table with timestamp
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute(
                    "INSERT INTO logs (rfid, role, timestamp) VALUES (?, ?, ?)",
                    (rfid, name, current_time)
                )
                self.conn.commit()

                # 3️⃣ Remove from waiting lists
                self.remove_data_on_waiting(self.student_waiting, rfid)   
                self.remove_data_on_waiting(self.parents_waiting, rfid) 

                # 4️⃣ Update displayed names
                self.populate_names()
                
                 
    def remove_data_on_waiting(self,dict,rfid):
        key_to_delete = [key for key, val in dict.items() if val.get("student_rfid") == rfid]   
        for key in key_to_delete:
            del dict[key]
        
    
       
    def run_scanner(self):
        thread = threading.Thread(target=self.rfid_scanner, daemon=True)
        thread.start()
        
    def run_UI(self):
        self.run_scanner()  # start scanner before showing UI
        self.root.mainloop()
    



start = UI()
start.run_UI()
