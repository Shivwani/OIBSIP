import tkinter as tk
from tkinter import ttk, messagebox
import string
import pyperclip
import secrets


class PasswordGenerator:
    AMBIGUOUS_CHARACTERS = 'l1Io0O'  # Define ambiguous characters as a constant

    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")

       
        #self.master.configure(bg='#333333')

        # Use a themed style
        style = ttk.Style()
        style.theme_use("clam")

        # Heading label
        self.heading_label = ttk.Label(master, text="-*-*-*-*---Secure Password Generator---*-*-*-*-", font=("Comic sans ms", 24, "bold"), foreground='white', background='#333333')
        self.heading_label.grid(row=0, column=0, pady=(20, 10), padx=10, columnspan=5, sticky='n')  # Adjusted columnspan

        # Center the heading label
        for i in range(5):  # Adjusted the range to match the number of columns
            self.master.grid_columnconfigure(i, weight=1)

        # Colorful labels
        self.length_label = ttk.Label(master, text="Password Length:", font=("Comic sans ms", 14))
        self.length_label.grid(row=2, column=1, pady=5, padx=5, sticky='w')  # Adjusted row

        # Entry widget with rounded corners
        self.length_entry = ttk.Entry(master, font=("Comic sans ms", 14), justify='center', style='TEntry')
        self.length_entry.grid(row=3, column=1, pady=5, padx=5, sticky='w')  # Adjusted row

        # Label for custom characters
        self.include_label = ttk.Label(master, text="Please enter what you would like to include:", font=("Comic sans ms", 14))
        self.include_label.grid(row=4, column=1, pady=5, padx=5, sticky='w')  # Adjusted columnspan

        # Checkboxes for character types, one below the other
        self.uppercase_var = tk.IntVar()
        self.uppercase_checkbox = ttk.Checkbutton(master, text="Uppercase", variable=self.uppercase_var, style='TCheckbutton')
        self.uppercase_checkbox.grid(row=5, column=1, pady=5, sticky='w')  # Adjusted row

        self.lowercase_var = tk.IntVar()
        self.lowercase_checkbox = ttk.Checkbutton(master, text="Lowercase", variable=self.lowercase_var, style='TCheckbutton')
        self.lowercase_checkbox.grid(row=6, column=1, pady=5, sticky='w')  # Adjusted row

        self.digits_var = tk.IntVar()
        self.digits_checkbox = ttk.Checkbutton(master, text="Digits", variable=self.digits_var, style='TCheckbutton')
        self.digits_checkbox.grid(row=7, column=1, pady=5, sticky='w')  # Adjusted row

        self.symbols_var = tk.IntVar()
        self.symbols_checkbox = ttk.Checkbutton(master, text="Symbols", variable=self.symbols_var, style='TCheckbutton')
        self.symbols_checkbox.grid(row=8, column=1, pady=5, padx=5, sticky='w')  # Adjusted row

        # Entry widget for custom characters to include
        self.include_chars_label = ttk.Label(master, text="Include Characters:", font=("Comic sans ms", 14))
        self.include_chars_label.grid(row=9, column=1, pady=5, padx=5, sticky='w')  # Adjusted row

        self.custom_chars_entry = ttk.Entry(master, font=("Comic sans ms", 14), justify='center', style='TEntry')
        self.custom_chars_entry.grid(row=10, column=1, pady=5, padx=5, sticky='w')  # Adjusted row

        # Entry widget for custom characters to exclude
        self.exclude_chars_label = ttk.Label(master, text="Exclude Characters:", font=("Comic sans ms", 14))
        self.exclude_chars_label.grid(row=11, column=1, pady=5, padx=5, sticky='w')  # Adjusted row

        self.exclude_chars_entry = ttk.Entry(master, font=("Comic sans ms", 14), justify='center', style='TEntry')
        self.exclude_chars_entry.grid(row=12, column=1, pady=5, padx=5, sticky='w')  # Adjusted row

        # Entry widget for user to input their own password
        self.custom_password_label = ttk.Label(master, text="Custom Password:", font=("Comic sans ms", 14))
        self.custom_password_label.grid(row=2, column=2, pady=5, padx=5, sticky='w')  # Adjusted column

        self.custom_password_entry = ttk.Entry(master, font=("Comic sans ms", 14), justify='center', style='TEntry')
        self.custom_password_entry.grid(row=3, column=2, pady=5, padx=5, sticky='w')  # Adjusted column

        # Colorful and rounded button to check security rules for custom password
        self.check_custom_password_button = ttk.Button(master, text="Check Password", command=self.check_custom_password, style='TButton')
        self.check_custom_password_button.grid(row=4, column=2, pady=5, padx=5,sticky='w')  # Adjusted columnspan

        # Colorful and rounded button
        self.generate_button = ttk.Button(master, text="Generate Password", command=self.generate_password, style='TButton')
        self.generate_button.grid(row=9, column=2, pady=5, padx=5, columnspan=2,sticky='w')  # Adjusted row and columnspan

        # Entry widget to display the password with rounded corners
        self.password_entry = ttk.Entry(master, show='*', font=("Comic sans ms", 14), justify='center', style='TEntry')
        self.password_entry.grid(row=10, column=2, pady=5, padx=5, columnspan=2,sticky='w')  # Adjusted row and columnspan

        # Checkbox to show/hide password
        self.show_password_var = tk.IntVar()
        self.show_password_checkbox = ttk.Checkbutton(master, text="Show Password", variable=self.show_password_var,
                                                      command=self.toggle_password_visibility, style='TCheckbutton')
        self.show_password_checkbox.grid(row=11, column=2, pady=5, padx=5, columnspan=2,sticky='w')  # Adjusted row and columnspan

        # Colorful and rounded button
        self.copy_button = ttk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard, style='TButton')
        self.copy_button.grid(row=12, column=2, pady=5, padx=5, columnspan=2,sticky='w')  # Adjusted row and columnspan

        # Exit button
        self.exit_button = ttk.Button(master, text="Exit", command=self.master.destroy, style='TButton')
        self.exit_button.grid(row=17, column=2, pady=5, padx=5, columnspan=2,sticky='w')  # Adjusted columnspan

        # Configure style for the themed widgets
        style.configure('TButton', background='#4CAF50', foreground='white', font=("Comic sans ms", 12), padding=10)
        style.configure('TEntry', padding=10)
        style.configure('TCheckbutton', padding=5)

    def center_window(self):
        w = 800  # Width of the window
        h = 500  # Height of the window

        # Get the screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # Set the dimensions of the screen and where it is placed
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def validate_input(self, length):
        try:
            length = int(length)
            if length <= 0:
                raise ValueError("Length must be a positive integer.")
            return length
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return None

    def generate_password(self):
        # Validate the input length
        length = self.validate_input(self.length_entry.get())
        if length is None:
            return

        # Define character sets for different types of characters
        uppercase_chars = string.ascii_uppercase
        lowercase_chars = string.ascii_lowercase
        digit_chars = string.digits
        symbol_chars = string.punctuation

        # Ensure that at least one character type is selected
        if not any([self.uppercase_var.get(), self.lowercase_var.get(), self.digits_var.get(), self.symbols_var.get()]):
            messagebox.showerror("Error", "Select at least one character type.")
            return

        # Create the character set based on selected types
        character_set = ''
        if self.uppercase_var.get():
            character_set += uppercase_chars
        if self.lowercase_var.get():
            character_set += lowercase_chars
        if self.digits_var.get():
            character_set += digit_chars
        if self.symbols_var.get():
            character_set += symbol_chars

        # Exclude ambiguous characters
        character_set_no_ambiguous = ''.join(char for char in character_set if char not in self.AMBIGUOUS_CHARACTERS)

        # Ensure the password is at least as long as specified
        if len(character_set_no_ambiguous) < length:
            messagebox.showerror("Error", "Selected character types are not sufficient for the specified length.")
            return

        # Generate the password using secrets module for cryptographically secure randomness
        password = ''.join(secrets.choice(character_set_no_ambiguous) for _ in range(length))

        # Exclude user-defined excluded characters
        exclude_chars = self.exclude_chars_entry.get()
        password = ''.join(char for char in password if char not in exclude_chars)

        # Include user-defined custom characters
        custom_chars = self.custom_chars_entry.get()
        password += custom_chars

        # Display the generated password
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Clipboard", "Password copied to clipboard.")
        else:
            messagebox.showerror("Error", "Generate a password first.")

    def check_security_rules(self, password):
        # Check if the password meets specific security rules
        if len(password) < 8:
            return False  # Password should be at least 8 characters long

        # Check if the password contains at least one uppercase letter
        if not any(char.isupper() for char in password):
            return False

        # Check if the password contains at least one lowercase letter
        if not any(char.islower() for char in password):
            return False

        # Check if the password contains at least one digit
        if not any(char.isdigit() for char in password):
            return False

        # Check if the password contains at least one special character
        special_characters = string.punctuation
        if not any(char in special_characters for char in password):
            return False
        return True  # Password meets all specified rules

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def check_custom_password(self):
        # Check if the custom password follows security rules
        custom_password = self.custom_password_entry.get()
        if self.check_security_rules(custom_password):
            messagebox.showinfo("Password Check", "The custom password follows security rules. And is good to use")
        else:
            messagebox.showwarning("Password Check", "The custom password does not follow security rules. Please review the rules.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
