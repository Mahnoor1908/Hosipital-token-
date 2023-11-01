import heapq
import tkinter as tk

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class TokenSystem:
    def __init__(self):
        self.emergency_queue = []
        self.current_token_number = 0
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur_node = self.head
            while cur_node.next is not None:
                cur_node = cur_node.next
            cur_node.next = new_node

    def get_token(self, is_emergency=False):
        self.current_token_number += 1
        token = (self.current_token_number, is_emergency)
        if is_emergency:
            heapq.heappush(self.emergency_queue, token)
        else:
            self.insert(self.current_token_number)
        return self.current_token_number

    def next_patient(self, is_emergency=False):
        if is_emergency:
            if self.emergency_queue:
                return heapq.heappop(self.emergency_queue)[0]
            else:
                return None
        elif self.head is not None:
            cur_node = self.head
            self.head = cur_node.next
            return cur_node.data
        
        elif self.head is None:
            if self.emergency_queue:
                return heapq.heappop(self.emergency_queue)[0]
        
        else:
            return None

def get_next_patient(is_emergency=False):
    global token_system
    next_patient_number = token_system.next_patient(is_emergency)
    if next_patient_number:
        if is_emergency:
            eNext_label.config(text=f"Next Emergency Patient for checkup: {next_patient_number}")
        else:
            normalNext_label.config(text=f"Next Normal Patient for checkup: {next_patient_number}")
            
    else:
        if token_system.head==None:
            normalNext_label.config(text="No patients")
        if len(token_system.emergency_queue)==0:
            eNext_label.config(text="No patients")
        if token_system.head==None and len(token_system.emergency_queue)==0:
            result_label.config(text="no more patients")

def get_emergency_token():
    global token_system
    token_number = token_system.get_token(is_emergency=True)
    result_label.config(text=f"\nEmergency Patient get token number: {token_number}")

def get_normal_token():
    global token_system
    token_number = token_system.get_token()
    result_label.config(text=f"\nNormal Patient get token number: {token_number}")

# Create GUI window
window = tk.Tk()
window.geometry("300x300")
window.title("Hospital Token System")


# Create buttons

normal_token_button = tk.Button(window, text="Normal Token", command=get_normal_token)
normal_token_button.pack()

emergency_token_button = tk.Button(window, text="Emergency Token", command=get_emergency_token)
emergency_token_button.pack()


doc1_label = tk.Label(window, text="\nNormal Doctor")
doc1_label.pack()

next_normal_patient_button = tk.Button(window, text="Next", command=lambda: get_next_patient(False))
next_normal_patient_button.pack()

normalNext_label = tk.Label(window, text="")
normalNext_label.pack()

doc2_label = tk.Label(window, text="\nEmergency Doctor")
doc2_label.pack()

next_emergency_patient_button = tk.Button(window, text="Next", command=lambda: get_next_patient(True))
next_emergency_patient_button.pack()

eNext_label = tk.Label(window, text="")
eNext_label.pack()


# Create result label
result_label = tk.Label(window, text="")
result_label.pack()

# Initialize token system
token_system = TokenSystem()

# Start GUI main loop
window.mainloop()
