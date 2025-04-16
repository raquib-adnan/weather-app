import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # API Key - Replace with your weatherstack API key
        self.api_key = "5ea6d56308687abe7684b2fe3fa9a405"
        self.base_url = "http://api.weatherstack.com/current"
        
        # Create and configure the main frame
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # City Entry
        tk.Label(self.main_frame, text="Enter City:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        self.city_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.city_entry.pack(pady=5, ipadx=50, ipady=5)
        
        # Search Button
        self.search_btn = tk.Button(self.main_frame, text="Get Weather", 
                                  command=self.get_weather,
                                  bg="#4CAF50", fg="white",
                                  font=("Arial", 12))
        self.search_btn.pack(pady=10, ipadx=20, ipady=5)
        
        # Weather Info Frame
        self.weather_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.weather_frame.pack(pady=20)
        
        # Weather Icon
        self.icon_label = tk.Label(self.weather_frame, bg="#f0f0f0")
        self.icon_label.pack(pady=10)
        
        # Temperature Label
        self.temp_label = tk.Label(self.weather_frame, text="", 
                                 font=("Arial", 24, "bold"), bg="#f0f0f0")
        self.temp_label.pack(pady=5)
        
        # Weather Description
        self.desc_label = tk.Label(self.weather_frame, text="", 
                                 font=("Arial", 14), bg="#f0f0f0")
        self.desc_label.pack(pady=5)
        
        # Humidity
        self.humidity_label = tk.Label(self.weather_frame, text="", 
                                     font=("Arial", 12), bg="#f0f0f0")
        self.humidity_label.pack(pady=5)
        
        # Wind Speed
        self.wind_label = tk.Label(self.weather_frame, text="", 
                                 font=("Arial", 12), bg="#f0f0f0")
        self.wind_label.pack(pady=5)
        
    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
            
        try:
            # Make API request
            params = {
                'access_key': self.api_key,
                'query': city,
                'units': 'm'  # metric units
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if 'success' in data and not data['success']:
                messagebox.showerror("Error", f"Error: {data['error']['info']}")
                return
                
            if response.status_code == 200:
                # Update weather information
                current = data['current']
                location = data['location']
                
                # Update labels
                self.temp_label.config(text=f"{current['temperature']}°C")
                self.desc_label.config(text=current['weather_descriptions'][0])
                self.humidity_label.config(text=f"Humidity: {current['humidity']}%")
                self.wind_label.config(text=f"Wind: {current['wind_speed']} km/h")
                
                # Get and display weather icon
                if current['weather_icons']:
                    icon_url = current['weather_icons'][0]
                    icon_response = requests.get(icon_url)
                    icon_data = icon_response.content
                    icon_image = Image.open(io.BytesIO(icon_data))
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    self.icon_label.config(image=icon_photo)
                    self.icon_label.image = icon_photo
                
            else:
                messagebox.showerror("Error", "Failed to fetch weather data")
                
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Could not connect to the weather service")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop() 