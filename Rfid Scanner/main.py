import keyboard
import tkinter as tk
from tkinter import ttk
import sqlite3
import threading


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
        
        self.root = tk.Tk()
        self.root.title("MAIN UI")
        self.root.geometry("500x500")

        # Label to display scanned RFID
        self.label = ttk.Label(self.root, text="Waiting for scan...", font=("Arial", 14))
        self.label.pack(pady=20)
    
    def rfid_scanner(self):
        rfid_code = ""
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                if key == 'enter':
                    print(rfid_code)
                    self.get_rfid(rfid_code)
                    self.label.config(text=f"Scanned RFID: {rfid_code}")  # update GUI
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
                self.remove_data_on_waiting(self.student_waiting,rfid)   
                self.remove_data_on_waiting(self.parents_waiting,rfid)   
                
                 
    def remove_data_on_waiting(self,dict,rfid):
        key_to_delete = [key for key, val in dict.items() if val.get("student_rfid") == rfid]   
        for key in key_to_delete:
            del dict[key]
        
        
        
       
       #for student in self.student_waiting.values():
        #    if student["student_rfid"] in student_rfid:
        #        print(student)
        
    def run_scanner(self):
        thread = threading.Thread(target=self.rfid_scanner, daemon=True)
        thread.start()
        
    def run_UI(self):
        self.run_scanner()  # start scanner before showing UI
        self.root.mainloop()
    



start = UI()
start.run_UI()
