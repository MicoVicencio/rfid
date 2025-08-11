import keyboard
import tkinter as tk
from tkinter import ttk
import sqlite3
import threading
import tkinter.font as tkfont
from PIL import Image, ImageTk
import time


class UI:
    def __init__(self):
        self.conn = sqlite3.connect("rfid.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.student_waiting = {}
        self.parents_waiting = {}
        self.students_pickup = {}
        self.parent_num = 0
        self.student_num = 0
        self.student_rfid = []
        self.parents_rfid = []
        self.pickup_rfid = set()

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

        style = ttk.Style(self.root)
        style.configure("Treeview",
                        font=self.big_font,
                        rowheight=50,
                        borderwidth=2,
                        relief="solid")
        style.configure("Treeview.Heading", font=self.big_font)
        style.map('Treeview', background=[('selected', '#347083')])

        columns = ("name", "section")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', style="Treeview")
        self.tree.heading("name", text="Name", anchor='center')
        self.tree.heading("section", text="Section", anchor='center')
        self.tree.column("name", width=600, anchor='center')
        self.tree.column("section", width=300, anchor='center')

        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="#e6f2ff")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipadx=2, ipady=2)

        self.current_index = 0
        self.items_per_page = 10

        self.update_treeview()

    def load_seal_image(self):
        image = Image.open("seal.png")
        max_width, max_height = 700, 700
        image.thumbnail((max_width, max_height), Image.LANCZOS)
        self.seal_photo = ImageTk.PhotoImage(image)

    def cleanup_expired_pickups(self):
        now = time.time()
        expired_rfids = [
            rfid for rfid, info in self.pickup_list.items()
            if "time" in info and now - info["time"] >= 10
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
            else:
                print("Parent already exisit")
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
                self.remove_data_on_waiting(self.student_waiting,rfid)   
                self.remove_data_on_waiting(self.parents_waiting,rfid)   
                
                
                 
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
