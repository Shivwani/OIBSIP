import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk

class WeatherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Weather App")

        # Load the background image
        try:
            bg_image_path = "C:/Users/SHIVWANI/OneDrive/Desktop/SYBSCIT/OIBSIP/weather.jpg"
            original_image = Image.open(bg_image_path)
            self.bg_image = ImageTk.PhotoImage(original_image)

        except Exception as e:
            messagebox.showerror("Error", f"Unable to load background image: {e}")
            return

        # Create a label to display the background image
        bg_label = tk.Label(root, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)  # Make the label span the entire window
        bg_label.image = self.bg_image  # Keep a reference to the image
        
        space_frame = tk.Frame(root, height=200, bg="snow")  # Adjust the height as needed
        space_frame.pack()


        # Create and configure GUI elements
        heading_label = tk.Label(root, text="WEATHER APP", font=("Comic Sans MS", 24, "bold"), bg="snow", fg="black")
        heading_label.pack(pady=(20, 40))

        
        self.api_key = "ac247c5d52262933366d7e8e281d2379"  # Replace with your OpenWeatherMap API key
        self.temperature_unit = tk.StringVar(value="Celsius")  # Default unit is Celsius
        self.temperature_unit.trace_add("write", self.update_temperature)

        # Initialize the buttons
        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for location input
        location_frame = tk.Frame(self.master, bg="snow")
        location_frame.pack(padx=10, pady=10)

        self.location_label = ttk.Label(location_frame, text="Enter Location:", font=("Comic Sans MS", 12), background="snow", foreground="black")
        self.location_label.pack(side="left", padx=10, pady=10)

        self.location_entry = ttk.Entry(location_frame, width=30, font=("Comic Sans MS", 12))
        self.location_entry.pack(side="left", padx=10, pady=10)

        # Button to get weather
        self.get_weather_button = ttk.Button(self.master,text="Get Weather", command=self.get_weather, style="TButton")
        self.get_weather_button.pack(pady=(10, 20))

        # Button for automatic location detection
        self.detect_location_button = ttk.Button(self.master, text="Detect Location", command=self.detect_location, style="TButton")
        self.detect_location_button.pack(pady=10)

        # Exit Button
        self.exit_button = ttk.Button(self.master, text="Exit", command=self.master.destroy, style="TButton")
        self.exit_button.pack(pady=10)

    def get_weather(self):
        location = self.location_entry.get()

        if not location:
            messagebox.showerror("Error", "Please enter a location.")
            return

        try:
            self.display_weather(location)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching weather data: {e}")

    def detect_location(self):
        try:
            # Use ipinfo.io to get the user's public IP address
            ip_info_response = requests.get("https://ipinfo.io")
            ip_info_data = ip_info_response.json()

            # Use the IP address to determine the location
            location = f"{ip_info_data.get('city', '')}, {ip_info_data.get('region', '')}, {ip_info_data.get('country', '')}"
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, location)
            self.display_weather(location)

        except Exception as e:
            messagebox.showerror("Error", f"Error detecting location: {e}")


    def display_weather(self, location):
        try:
            # Destroy existing weather_popup (if any)
            if hasattr(self, 'weather_popup') and self.weather_popup:
                self.weather_popup.destroy()

            # Make API request
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            data = response.json()

            # Check if 'weather' key is present in the response
            if 'weather' not in data or not data['weather']:
                messagebox.showerror("Error", f"Unable to fetch weather data for {location}. Please check the location.")
                return

            # Create a new pop-up window for weather display with increased size
            self.weather_popup = tk.Toplevel(self.master)
            self.weather_popup.title(f"Weather in {location}")
            self.weather_popup.geometry("400x400")  # Set the size of the pop-up window

            weather_description = data['weather'][0]['description'].capitalize()
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            # Celsius and Fahrenheit Radio Buttons
            celsius_button_popup = ttk.Radiobutton(self.weather_popup, text="Celsius", variable=self.temperature_unit, value="Celsius", style="TRadiobutton")
            celsius_button_popup.grid(row=2, column=1, padx=10, pady=5)

            fahrenheit_button_popup = ttk.Radiobutton(self.weather_popup, text="Fahrenheit",variable=self.temperature_unit, value="Fahrenheit", style="TRadiobutton")
            fahrenheit_button_popup.grid(row=2, column=2, padx=10, pady=5)

            # Convert temperature based on user's choice
            if self.temperature_unit.get() == "Celsius":
                temperature_unit_label = "°C"
                temperature_value = temperature - 273.15  # Convert temperature to Celsius
            else:
                temperature_unit_label = "°F"
                temperature_value = (temperature * 9/5) + 32  # Convert temperature to Fahrenheit

            # Display weather information in row-column format
            ttk.Label(self.weather_popup, text=f"Weather: {weather_description}", font=("Comic Sans MS", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(self.weather_popup, text=f"Temperature: {temperature_value:.2f}{temperature_unit_label}", font=("Comic Sans MS", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(self.weather_popup, text=f"Humidity: {humidity}%", font=("Comic Sans MS", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(self.weather_popup, text=f"Wind Speed: {wind_speed} m/s", font=("Comic Sans MS", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")

            # Display weather icon in the pop-up window
            icon_id = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/w/{icon_id}.png"
            icon = self.load_image_from_url(icon_url)
            weather_icon_label = ttk.Label(self.weather_popup, image=icon)
            weather_icon_label.image = icon
            weather_icon_label.grid(row=5, column=0, rowspan=4, padx=10, pady=10)
                
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Error", f"HTTP Error: {e}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching weather data: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def update_temperature(self, *args):
            # Update displayed temperature when the temperature unit changes
            location = self.location_entry.get()
            if location:
                self.display_weather(location)

    def load_image_from_url(self, url):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        img = Image.open(response.raw)
        img = img.resize((50, 50), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.geometry("1000x1000")  # Set the size of the main window
    root.configure(bg="#336699")
    root.mainloop()
