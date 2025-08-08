import keyboard
import tkinter as tk
from tkinter import ttk
import sqlite3
import threading
import tkinter.font as tkfont
from PIL import Image, ImageTk 


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
        self.pickup_list = {}
    
        
        self.root = tk.Tk()
        self.root.title("MAIN UI")
        self.root.state('zoomed')  # Fullscreen with title bar

        # Load seal.png image with Pillow
        self.load_seal_image()

        # Setup style and Treeview as before
        self.big_font = tkfont.Font(family="Arial", size=30)

        # Display the image instead of the label
        self.image_label = ttk.Label(self.root, image=self.seal_photo)
        self.image_label.pack(pady=10)

        style = ttk.Style(self.root)
        style.configure("Treeview",
                        font=self.big_font,
                        rowheight=50)
        style.configure("Treeview.Heading", font=self.big_font)
        style.map('Treeview', background=[('selected', '#347083')])
        style.configure("oddrow", background="white")
        style.configure("evenrow", background="#e6f2ff")

        columns = ("name", "section")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading("name", text="Name", anchor='center')
        self.tree.heading("section", text="Section", anchor='center')
        self.tree.column("name", width=600, anchor='center')
        self.tree.column("section", width=300, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def load_seal_image(self):
        # Open the image with PIL and convert for Tkinter
        image = Image.open("seal.png")
        # Optionally resize if image is too big
        max_width, max_height = 700, 700
        image.thumbnail((max_width, max_height), Image.LANCZOS)
        self.seal_photo = ImageTk.PhotoImage(image)

    def get_pickup_details(self):
        self.pickup_list.clear()
        for student in self.student_waiting.values():
            if student["student_rfid"] in self.pickup_rfid:
                self.pickup_list[student["student_rfid"]] = {
                    "name": student["name"],
                    "section": student["section"]
                }
        self.update_treeview()

    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for index, (rfid, info) in enumerate(self.pickup_list.items()):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(info["name"], info["section"]), tags=(tag,))

         
            
            
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
