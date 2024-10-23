import subprocess
from tkinter import *
from tkinter import messagebox, filedialog
import os

def run_john(attack_type, wordlist=None, hash_file=None):
    john_executable = os.path.join(os.getcwd(), "john", "run", "john")

    # Ensure the user has uploaded a wordlist for dictionary and hybrid attacks
    if not wordlist or wordlist == "":
        messagebox.showerror("Error", "You must upload a wordlist for Dictionary or Hybrid attacks.")
        return

    command = [john_executable]

    # Modify based on the attack type
    if attack_type == "Dictionary":
        command += ['--wordlist=' + wordlist, hash_file]
    elif attack_type == "Hybrid":
        command += ['--wordlist=' + wordlist, '--rules', hash_file]
    elif attack_type == "Combination":
        command += ['--incremental=All', hash_file]

    # Run John the Ripper as a subprocess and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Display the output in the text box
    output_text.delete(1.0, END)
    output_text.insert(END, result.stdout)

def open_file(entry_field):
    # Open a file dialog to select a wordlist or hash file (accept both .txt and .lst)
    file_path = filedialog.askopenfilename(filetypes=[("Wordlist files", "*.txt *.lst")])
    entry_field.delete(0, END)
    entry_field.insert(0, file_path)

def run_attack():
    # Run John the Ripper with the appropriate attack
    run_john(attack_var.get(), wordlist_entry.get(), "hashes.txt")  # Assuming hash file exists

def toggle_wordlist_entry():
    if attack_var.get() == "Combination":
        wordlist_entry.config(state=DISABLED)
        browse_wordlist_button.config(state=DISABLED)
    else:
        wordlist_entry.config(state=NORMAL)
        browse_wordlist_button.config(state=NORMAL)

# Create the GUI window
root = Tk()
root.title('Password Cracking Tool')

# Heading label
Label(root, text="Select form of password attack:").pack(pady=10)
Label(root, text="(You must upload a wordlist for Dictionary or Hybrid attacks)").pack()

# Upload wordlist file section
browse_wordlist_button = Button(root, text="Upload Wordlist", command=lambda: open_file(wordlist_entry))
browse_wordlist_button.pack(pady=5)

# Wordlist input
wordlist_entry = Entry(root, width=50)
wordlist_entry.pack(pady=5)

# Attack type selection with radio buttons
attack_var = StringVar(value="Dictionary")

Radiobutton(root, text="Dictionary", variable=attack_var, value="Dictionary", command=toggle_wordlist_entry).pack(anchor=W)
Radiobutton(root, text="Hybrid", variable=attack_var, value="Hybrid", command=toggle_wordlist_entry).pack(anchor=W)
Radiobutton(root, text="Combination", variable=attack_var, value="Combination", command=toggle_wordlist_entry).pack(anchor=W)

# Run button
run_button = Button(root, text="Run", bg="red", fg="white", command=run_attack)
run_button.pack(pady=20)

# Output Text Box
output_text = Text(root, height=10, width=70)
output_text.pack()

# Start the GUI event loop
root.mainloop()
