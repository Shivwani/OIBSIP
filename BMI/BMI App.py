import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Beanjelly@18",
    database="bmi_data"
)
cursor = db.cursor()

class BMIApp:
    def __init__(self, window):
        self.window = window
        self.window.title("BMI Tracker")
        self.window.geometry("1000x1000")  # Set initial window size

        # Create the BMI data table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                weight FLOAT,
                height FLOAT,
                bmi FLOAT,
                category VARCHAR(20),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()

        # Create the users table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL
            )
        """)
        db.commit()

        # Initialize ax attribute (for example, as None)
        self.ax = None

        # Initialize the current_user_id attribute
        self.current_user_id = None 

        # Store the login page for later destruction
        self.login_page = self.window

        # Create variables to store user login credentials
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Call the login page automatically
        self.login()

    def login(self):
        # Set background image for the login page
        background_image_intro = Image.open("C:/Users/SHIVWANI/OneDrive/Desktop/SYBSCIT/OIBSIP/bmi.jpg")
        background_image_intro = background_image_intro.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()), Image.BOX
        )
        background_image_intro = ImageTk.PhotoImage(background_image_intro)

        # Set window background image
        self.window.configure(background="#3C3C3C")  # Set background color as a fallback
        bg_label = tk.Label(self.window, image=background_image_intro)
        bg_label.image = background_image_intro
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        label_intro = tk.Label(
            self.window, text="", font=("Helvetica", 16, "bold")
        )
        label_intro.place(relx=0.5, rely=0.4, anchor="s")

        # Center the label vertically and horizontally
        heading_label = tk.Label(
            self.window, 
            text="Welcome to the BMI Tracker Application!\n"
                 "This application helps you track your BMI over time.\n"
                 "To get started, please enter your weight and height,\n"
                 "then calculate your BMI.",
            font=("comic sans ms", 20),
            fg="darkgreen",
            bg="peachpuff2"
        )
        heading_label.pack()

        # Create a custom style with the desired font
        style = ttk.Style()
        style.configure("TButton", font=("comic sans ms", 16), background="green")  # Adjust the font size and family as needed

        # Create a frame to organize the layout
        entry_frame = tk.Frame(self.window, bg="ivory")
        entry_frame.pack(pady=20)

        label_username = tk.Label(entry_frame, text="Username:", font=("Comic Sans MS", 14), fg="black", bg="ivory")
        label_username.grid(row=0, column=0, pady=5)
        self.entry_username = tk.Entry(entry_frame, textvariable=self.username_var, font=("Comic Sans MS", 14))
        self.entry_username.grid(row=0, column=1, pady=5, padx=10)

        label_password = tk.Label(entry_frame, text="Password:", font=("Comic Sans MS", 14), fg="black", bg="ivory")
        label_password.grid(row=1, column=0, pady=5)
        self.entry_password = tk.Entry(entry_frame, textvariable=self.password_var, font=("Comic Sans MS", 14), show="*")
        self.entry_password.grid(row=1, column=1, pady=5, padx=10)

        # Use the custom style for the ttk.Buttons
        login_button = ttk.Button(
            entry_frame, text="Login", command=self.verify_login, style="TButton", padding=(50, 5)
        )
        login_button.grid(row=2, column=0, pady=10, columnspan=2)  # Center the button horizontally

        # Create a Register button to register a new user
        register_button = ttk.Button(
            entry_frame, text="Register", command=self.register_user, style="TButton", padding=(20, 5)
        )
        register_button.grid(row=3, column=0, pady=10, columnspan=2)  # Center the button horizontally

        # Store the login page for later destruction
        self.login_page = self.window

        # Show the login page
        self.window.mainloop()

    def register_user(self):
        # Fetch the entered username and password
        username = self.username_var.get()
        password = self.password_var.get()

        # Check if the username and password are not empty
        if username and password:
            # Check if the username is already taken
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Registration Error", "Username already taken. Please choose a different username.")
            else:
                # Insert the new user into the users table
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                db.commit()
                messagebox.showinfo("Registration Successful", "User registered successfully.")
                # Set the current user_id upon successful registration
                self.current_user_id = cursor.lastrowid
                # If successful, proceed to the main page
                self.show_frame(self.current_user_id)  # Pass the user_id here


    def verify_login(self):
        # Fetch the entered username and password
        username = self.username_var.get()
        password = self.password_var.get()

        # Check if the username and password are not empty
        if username and password:
            # Check if the entered username and password match a user in the database
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            existing_user = cursor.fetchone()

            if existing_user:
                # Show a message box upon successful login
                messagebox.showinfo("Login Successful", "Login successful!")

                # Set the current user_id upon successful login
                self.current_user_id = existing_user[0]
                # If successful, proceed to the main page
                self.show_frame(self.current_user_id)  # Pass the user_id here
                return
        messagebox.showerror("Login Error", "Invalid username or password")


    def show_frame(self,user_id):
        # Hide the intro page
        self.login_page.withdraw()

        # Show the main BMI calculator page and pass the current_user_id
        self.create_main_page(user_id)

    def create_main_page(self, user_id):
        # Create a new instance of Toplevel for the main page
        main_page = tk.Toplevel(self.window)
        main_page.title("BMI Calculator")

        # Set the geometry to fill the screen
        main_page.geometry(f"{main_page.winfo_screenwidth()}x{main_page.winfo_screenheight()}")

        # Font settings
        font_style = ("Helvetica", 12)

        # Set the background color to beige
        main_page.configure(bg="beige")

        # Add a heading for the main BMI calculator page
        heading_label_main = tk.Label(main_page, text="BMI Calculator", font=("Helvetica", 34, "bold"))
        heading_label_main.pack(pady=10)

        space_frame_main = tk.Frame(main_page, height=50)
        space_frame_main.pack()

        # Color settings
        label_color = "#333333"
        entry_color = "#ffffff"
        button_color = "ivory"
        button_text_color = "black"

        # Set the current user_id for saving data
        self.current_user_id = user_id

        self.label_weight = tk.Label(main_page, text="Weight (kg):", font=(font_style, 16), fg=label_color, bg="ivory")
        self.label_weight.pack(pady=5)
        self.entry_weight = tk.Entry(main_page, font=font_style, bg=entry_color)
        self.entry_weight.pack(pady=5)

        self.label_height = tk.Label(main_page, text="Height (m):", font=(font_style, 16), fg=label_color, bg="ivory")
        self.label_height.pack(pady=5)
        self.entry_height = tk.Entry(main_page, font=font_style, bg=entry_color)
        self.entry_height.pack(pady=5)

        self.calculate_button = tk.Button(main_page, text="Calculate BMI", command=self.calculate_bmi,
                                          font=(font_style, 16),
                                          bg=button_color, fg=button_text_color)
        self.calculate_button.pack(pady=10)

        self.save_button = tk.Button(main_page, text="Save Data", command=self.save_data, font=(font_style, 16),
                                     bg=button_color, fg=button_text_color)
        self.save_button.pack(pady=10)

        self.plot_button = tk.Button(main_page, text="Show BMI Trend", command=self.show_bmi_trend,
                                     font=(font_style, 16),
                                     bg=button_color, fg=button_text_color)
        self.plot_button.pack(pady=10)

        # Add an Update Records button
        update_button = tk.Button(main_page, text="Update Records", command=self.update_records, font=(font_style, 16),
                                 bg=button_color, fg=button_text_color)
        update_button.pack(pady=10)

        self.display_records_button = tk.Button(main_page, text="Display Records", command=lambda: self.display_all_records(self.current_user_id), font=(font_style, 16), bg=button_color, fg=button_text_color)
        self.display_records_button.pack(pady=10)

        self.delete_button = tk.Button(main_page, text="Delete Records", command=self.delete_all_records,
                                       font=(font_style, 16),
                                       bg=button_color, fg=button_text_color)
        self.delete_button.pack(pady=10)

        # Quit button to close the program
        quit_button = tk.Button(main_page, text="Quit", command=self.on_closing, font=(font_style, 16),
                                bg=button_color, fg=button_text_color)
        quit_button.pack(pady=10)

        # Store the main page for later destruction
        self.main_page = main_page

    def calculate_bmi(self):
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())

            if not (10 < weight < 500) or not (0.5 < height < 3):
                messagebox.showerror("Error", "Please enter valid weight (10-500 kg) and height (0.5-3 m).")
                return

            bmi = round(weight / (height ** 2), 2)
            category = self.get_bmi_category(bmi)

            messagebox.showinfo("BMI Result", f"Your BMI is: {bmi}\nCategory: {category}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height.")

    def save_data(self):
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())

            if not (10 < weight < 500) or not (0.5 < height < 3):
                messagebox.showerror("Error", "Please enter valid weight (10-500 kg) and height (0.5-3 m).")
                return

            bmi = round(weight / (height ** 2), 2)
            category = self.get_bmi_category(bmi)

            # Insert data into MySQL using the actual user ID
            cursor.execute("INSERT INTO bmi_data (user_id, weight, height, bmi, category) VALUES (%s, %s, %s, %s, %s)",
                           (self.current_user_id, weight, height, bmi, category))
            db.commit()
            messagebox.showinfo("Success", "Data saved successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height.")


    def display_all_records(self, user_id):
        try:
            # Fetch all BMI data from MySQL
            # user_id = 1  # You may implement user authentication to get the user_id
            cursor.execute("SELECT * FROM bmi_data WHERE user_id = %s", (user_id,))
            data = cursor.fetchall()

            if not data:
                messagebox.showwarning("Warning", "No data available.")
                return

            # Create a new window to display all records
            records_window = tk.Toplevel(self.main_page)
            records_window.title("All BMI Records")

            # Create a text widget to display the records
            text_widget = tk.Text(records_window, wrap="word", height=20, width=60)
            text_widget.pack(padx=20, pady=20)

            # Insert records into the text widget
            for record in data:
                text_widget.insert(tk.END, f"Record ID: {record[0]}\n"
                                           f"User ID: {record[1]}\n"
                                           f"Weight: {record[2]} kg\n"
                                           f"Height: {record[3]} m\n"
                                           f"BMI: {record[4]}\n"
                                           f"Category: {record[5]}\n"
                                           f"Timestamp: {record[6]}\n\n")

            # Make the text widget read-only
            text_widget.config(state=tk.DISABLED)

        except ValueError:
            messagebox.showerror("Error", "Error in retrieving BMI data.")


    def get_bmi_category(self, bmi):
        if 18.5 <= bmi < 24.9:
            return "Normal Weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        elif bmi >= 30:
            return "Obese"
        else:
            return "Underweight"

    def initialize_plot(self):
        # Initialize the plot with default values
        self.ax.set(xlabel='Timestamp', ylabel='BMI', title='BMI Trend')
        self.ax.grid()

        # Set x-axis tick locations and labels
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.fig.autofmt_xdate(rotation=45)

        # Draw the initial plot
        self.canvas.draw()

    def show_bmi_trend(self):
        try:
            # Fetch all BMI data from MySQL
            user_id = 1  # You may implement user authentication to get the user_id
            cursor.execute("SELECT timestamp, bmi FROM bmi_data WHERE user_id = %s", (user_id,))
            data = cursor.fetchall()

            if not data:
                messagebox.showwarning("Warning", "No data available.")
                return

            # Create a new window to display the BMI trend graph
            trend_window = tk.Toplevel(self.main_page)
            trend_window.title("BMI Trend Graph")

            # Matplotlib figure for the new window
            fig, ax = plt.subplots()
            canvas = FigureCanvasTkAgg(fig, master=trend_window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()

            # Navigation toolbar for the new window
            toolbar = NavigationToolbar2Tk(canvas, trend_window)
            toolbar.update()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # Plot the BMI trend
            timestamps = [row[0] for row in data]
            timestamps = [datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S') for ts in timestamps]
            bmi_values = [row[1] for row in data]
            ax.plot(timestamps, bmi_values, marker='o', linestyle='-', color='#007acc')

            # Set plot labels and title
            ax.set(xlabel='Timestamp', ylabel='BMI', title='BMI Trend')
            ax.grid()

            # Set x-axis tick locations and labels
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate(rotation=45)

            # Draw the plot
            canvas.draw()

        except ValueError:
            messagebox.showerror("Error", "Error in retrieving BMI data.")


    def update_records(self):
        try:
            # Fetch all BMI data from MySQL
            user_id = 1  # Replace this with the actual user ID (login or registration required)
            cursor.execute("SELECT * FROM bmi_data WHERE user_id = %s", (user_id,))
            data = cursor.fetchall()

            if not data:
                messagebox.showwarning("Warning", "No records available to update.")
                return

            # Create a new window to update records manually
            update_window = tk.Toplevel(self.main_page)
            update_window.title("Update Records Manually")

            # Create a text widget to display existing records
            text_widget = tk.Text(update_window, wrap="word", height=10, width=60)
            text_widget.pack(pady=20)

            # Insert existing records into the text widget
            for record in data:
                text_widget.insert(tk.END, f"Record ID: {record[0]}\n"
                                           f"User ID: {record[1]}\n"
                                           f"Weight: {record[2]} kg\n"
                                           f"Height: {record[3]} m\n"
                                           f"BMI: {record[4]}\n"
                                           f"Category: {record[5]}\n"
                                           f"Timestamp: {record[6]}\n\n")

            # Make the text widget read-only
            text_widget.config(state=tk.DISABLED)

            # Add entry widgets to allow the user to enter new values
            label_record_id = tk.Label(update_window, text="Record ID to Update:", font=("Comic Sans MS", 14))
            label_record_id.pack(pady=5)
            entry_record_id = tk.Entry(update_window, font=("Comic Sans MS", 14))
            entry_record_id.pack(pady=5)

            label_new_weight = tk.Label(update_window, text="New Weight (kg):", font=("Comic Sans MS", 14))
            label_new_weight.pack(pady=5)
            entry_new_weight = tk.Entry(update_window, font=("Comic Sans MS", 14))
            entry_new_weight.pack(pady=5)

            label_new_height = tk.Label(update_window, text="New Height (m):", font=("Comic Sans MS", 14))
            label_new_height.pack(pady=5)
            entry_new_height = tk.Entry(update_window, font=("Comic Sans MS", 14))
            entry_new_height.pack(pady=5)

            # Button to submit the updates
            submit_button = tk.Button(update_window, text="Submit Updates", command=lambda: self.submit_updates(
                entry_record_id.get(), entry_new_weight.get(), entry_new_height.get()), font=("Comic Sans MS", 14))
            submit_button.pack(pady=10)

        except ValueError:
            messagebox.showerror("Error", "Error in retrieving BMI data.")

    def submit_updates(self, record_id, new_weight, new_height):
        try:
            record_id = int(record_id)
            new_weight = float(new_weight)
            new_height = float(new_height)

            if not (10 < new_weight < 500) or not (0.5 < new_height < 3):
                messagebox.showerror("Error", "Please enter valid weight (10-500 kg) and height (0.5-3 m).")
                return

            new_bmi = round(new_weight / (new_height ** 2), 2)
            new_category = self.get_bmi_category(new_bmi)

            # Update data in MySQL
            cursor.execute("UPDATE bmi_data SET weight = %s, height = %s, bmi = %s, category = %s WHERE id = %s",
                           (new_weight, new_height, new_bmi, new_category, record_id))
            db.commit()

            messagebox.showinfo("Success", "Record updated successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid record ID, weight, and height.")


    def delete_all_records(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete all records?")
        if confirmation:
            if self.ax is not None:
                # Clear the plot
                self.ax.clear()

                # Reinitialize the plot settings
                self.initialize_plot()

            # Delete all records
            cursor.execute("DELETE FROM bmi_data WHERE user_id = %s", (self.current_user_id,))
            db.commit()
            messagebox.showinfo("Success", "All records deleted successfully.")

    def on_closing(self):
        # Handle any cleanup or confirmation before closing the application
        # For example, you might want to ask the user if they are sure they want to exit
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Close the database connection
            cursor.close()
            db.close()

            # Destroy the main page if it exists
            if hasattr(self, 'main_page') and self.main_page:
                self.main_page.destroy()

            # Destroy the root window
            self.window.destroy()

            # Exit the application
            sys.exit()



if __name__ == "__main__":
    root = tk.Tk()
    app = BMIApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Set the protocol before mainloop
    root.mainloop()
