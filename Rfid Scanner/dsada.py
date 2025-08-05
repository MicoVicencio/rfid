import keyboard
print("Scan your RFID tag...")

rfid = ''
while True:
    key = keyboard.read_event()
    if key.event_type == keyboard.KEY_DOWN:
        if key.name == 'enter':
            print("RFID Tag:", rfid)
            rfid = ''
        else:
            rfid += key.name
