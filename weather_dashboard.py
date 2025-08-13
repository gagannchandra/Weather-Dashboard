import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

API_KEY = "a5dba0a68bb472d9843a260aa435b7d5"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
LOCATION_URL = "https://ipinfo.io/json"

# ------------- Helpers -------------
def get_current_city():
    try:
        r = requests.get(LOCATION_URL, timeout=6)
        if r.status_code == 200:
            return r.json().get("city")
    except requests.exceptions.RequestException:
        pass
    return None

def set_icon(icon_code):
    try:
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
        data = requests.get(icon_url, timeout=6).content
        img = Image.open(BytesIO(data))

        # scale relative to window size
        w = max(80, int(root.winfo_width() * 0.35))
        h = max(80, int(root.winfo_height() * 0.22))
        img = img.resize((w, h), Image.LANCZOS)

        photo = ImageTk.PhotoImage(img)
        icon_label.config(image=photo)
        icon_label.image = photo
    except Exception:
        icon_label.config(image="")
        icon_label.image = None

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        r = requests.get(WEATHER_URL, params=params, timeout=8)
        data = r.json()
        if r.status_code == 200:
            t = data["main"]["temp"]
            h = data["main"]["humidity"]
            desc = data["weather"][0]["description"].capitalize()
            ic = data["weather"][0]["icon"]

            weather_label.config(
                text=f"{city.title()} Weather\n"
                     f"🌡 Temp: {t}°C   💧 {h}%\n"
                     f"🌥 {desc}"
            )
            set_icon(ic)
        else:
            raise RuntimeError(data.get("message", "Unable to fetch weather"))
    except Exception as e:
        messagebox.showerror("Weather Error", str(e))

def pick_daily_points(forecast_list, tz_offset_seconds):
    """
    Convert each forecast timestamp to local time and select one entry per date:
    the one closest to local 12:00.
    Returns: labels[], temps[]
    """
    by_date = {}
    for entry in forecast_list:
        utc_dt = datetime.utcfromtimestamp(entry["dt"])
        local_dt = utc_dt + timedelta(seconds=tz_offset_seconds)
        date_key = local_dt.date()
        hour = local_dt.hour
        score = abs(hour - 12)  # closeness to noon

        temp = entry["main"]["temp"]
        if (date_key not in by_date) or (score < by_date[date_key]["score"]):
            by_date[date_key] = {
                "score": score,
                "temp": temp,
                "label": local_dt.strftime("%a %d"),
            }

    # sort by date and take up to 5
    days = sorted(by_date.items(), key=lambda x: x[0])[:5]
    labels = [v["label"] for _, v in days]
    temps = [round(v["temp"], 1) for _, v in days]
    return labels, temps

def draw_forecast_chart(labels, temps):
    # clear previous
    for w in chart_frame.winfo_children():
        w.destroy()

    fig, ax = plt.subplots(figsize=(5, 2.6), dpi=100)
    ax.plot(labels, temps, marker="o", linewidth=2)
    ax.set_title("5-Day Temperature (Local Noon)")
    ax.set_ylabel("°C")
    ax.grid(True, linestyle="--", alpha=0.6)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.pack(fill="both", expand=True)
    plt.close(fig)  # free memory

def get_forecast(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        r = requests.get(FORECAST_URL, params=params, timeout=10)
        data = r.json()
        if r.status_code == 200:
            tz_offset = data.get("city", {}).get("timezone", 0)  # seconds
            labels, temps = pick_daily_points(data["list"], tz_offset)
            if not labels:
                raise RuntimeError("No forecast points found (try again in a bit).")
            draw_forecast_chart(labels, temps)
        else:
            raise RuntimeError(data.get("message", "Unable to fetch forecast"))
    except Exception as e:
        messagebox.showerror("Forecast Error", str(e))

def show_weather(city):
    get_weather(city)
    get_forecast(city)

def search_weather():
    city = city_entry.get().strip()
    if city:
        show_weather(city)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")

def auto_weather():
    city = get_current_city()
    if city:
        show_weather(city)
    else:
        messagebox.showerror("Location Error", "Could not detect location.")

# ------------- UI -------------
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("520x720")
root.minsize(420, 560)
root.config(bg="#B3E5FC")

# grid weights
for r in range(7):
    root.grid_rowconfigure(r, weight=1)
root.grid_columnconfigure(0, weight=1)

title_label = tk.Label(
    root, text="☀ Weather Dashboard ☁",
    font=("Arial Rounded MT Bold", 20), bg="#B3E5FC", fg="#01579B"
)
title_label.grid(row=0, column=0, sticky="nsew", pady=(10, 5))

city_entry = tk.Entry(root, font=("Arial", 14), justify="center", bd=2, relief="groove")
city_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

btn_frame = tk.Frame(root, bg="#B3E5FC")
btn_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
btn_frame.grid_columnconfigure(0, weight=1)
btn_frame.grid_columnconfigure(1, weight=1)

search_button = tk.Button(
    btn_frame, text="🔍 Search", command=search_weather,
    font=("Arial", 12, "bold"), bg="#0288D1", fg="white", relief="flat", height=2
)
search_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

auto_button = tk.Button(
    btn_frame, text="📍 Auto", command=auto_weather,
    font=("Arial", 12, "bold"), bg="#00796B", fg="white", relief="flat", height=2
)
auto_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

icon_label = tk.Label(root, bg="#B3E5FC")
icon_label.grid(row=3, column=0, sticky="nsew", pady=5)

weather_label = tk.Label(
    root, text="", font=("Arial", 14, "bold"),
    bg="#B3E5FC", fg="#01579B", justify="center"
)
weather_label.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

chart_frame = tk.Frame(root, bg="#B3E5FC")
chart_frame.grid(row=5, column=0, sticky="nsew", padx=12, pady=(8, 14))

# auto-load
root.after(800, auto_weather)

# keep icon responsive on resize
def _on_resize(event):
    # Re-scale current icon if one is shown
    img = getattr(icon_label, "image", None)
    # We don't have the original bitmap here; fetch the current weather again to redraw icon nicely.
    # Light + safe: just refresh icon via last city typed or auto city.
    # (No heavy calls here—Tk fires many resize events.)
    pass

root.mainloop()
