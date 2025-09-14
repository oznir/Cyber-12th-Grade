import winreg


RUNMRU_PATH = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"




def get_runmru():
   """Read Run dialog history in MRU order."""
   history = {}
   try:
       with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUNMRU_PATH) as key:
           index = 0
           while True:
               try:
                   name, value, _ = winreg.EnumValue(key, index)
                   history[name] = value
                   index += 1
               except OSError:
                   break
   except FileNotFoundError:
       return []


   # Reorder based on MRUList
   order = history.get("MRUList", "")
   return [(ch, history[ch]) for ch in order if ch in history]








def add_runmru(command):
   """Add a new command to RunMRU history."""
   with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUNMRU_PATH, 0, winreg.KEY_SET_VALUE) as key:
       # Get current history
       current = dict(get_runmru())
       order = "".join(current.keys())


       # Find next letter (a–z)
       for ch in "abcdefghijklmnopqrstuvwxyz":
           if ch not in current:
               next_char = ch
               break
       else:
           print("No free slots available (a–z used).")
           return


       # Add new value
       winreg.SetValueEx(key, next_char, 0, winreg.REG_SZ, command)
       winreg.SetValueEx(key, "MRUList", 0, winreg.REG_SZ, next_char + order)
       print(f'Added "{command}" as {next_char}.')




def remove_runmru(command):
   """Remove a command from RunMRU history by its text."""
   with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUNMRU_PATH, 0, winreg.KEY_SET_VALUE) as key:
       current = dict(get_runmru())
       order = list(current.keys())


       # Find which letter stores this command
       for ch, value in current.items():
           if value == command:
               winreg.DeleteValue(key, ch)
               order.remove(ch)
               winreg.SetValueEx(key, "MRUList", 0, winreg.REG_SZ, "".join(order))
               print(f'Removed "{command}".')
               return


       print(f'Command "{command}" not found.')




if __name__ == "__main__":
   while True:
       print("\n--- RunMRU Manager ---")
       print("1. Show history")
       print("2. Add command")
       print("3. Remove command")
       print("4. Exit")


       choice = input("Select an option: ").strip()


       if choice == "1":
           history = get_runmru()
           if not history:
               print("No history found.")
           else:
               print("RunMRU history:")
               for ch, cmd in history:
                   print(f"{ch}: {cmd}")


       elif choice == "2":
           cmd = input("Enter command to add: ").strip()
           if cmd:
               add_runmru(cmd)


       elif choice == "3":
           cmd = input("Enter command to remove: ").strip()
           if cmd:
               remove_runmru(cmd)


       elif choice == "4":
           break


       else:
           print("Invalid choice.")

