import tkinter as tk
from tkinter import filedialog, messagebox
import os

MARKER = b'##HTA_START##'
STUB_EXE = 'stub.exe'  # Must be compiled and placed in the same folder

def select_hta_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTA Files", "*.hta")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def compile_exe():
    hta_path = entry_file.get()
    if not hta_path or not os.path.isfile(hta_path):
        messagebox.showerror("Error", "Please select a valid .hta file.")
        return

    if not os.path.isfile(STUB_EXE):
        messagebox.showerror("Error", f"Missing stub executable: {STUB_EXE}")
        return

    try:
        with open(STUB_EXE, 'rb') as stub_file:
            stub_data = stub_file.read()

        with open(hta_path, 'rb') as hta_file:
            hta_data = hta_file.read()

        output_path = os.path.splitext(hta_path)[0] + '_compiled.exe'
        with open(output_path, 'wb') as output_file:
            output_file.write(stub_data)
            output_file.write(MARKER)
            output_file.write(hta_data)

        messagebox.showinfo("Success", f"Executable created: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Compilation failed: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("HTA to Standalone EXE Compiler")

tk.Label(root, text="Select HTA File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_file = tk.Entry(root, width=50)
entry_file.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_hta_file).grid(row=0, column=2, padx=10, pady=10)

tk.Button(root, text="Compile to EXE", command=compile_exe).grid(row=1, column=1, padx=10, pady=10)

root.mainloop()