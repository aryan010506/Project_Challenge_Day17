import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

# ------------- LOAD DATA -------------
try:
    data = pd.read_csv("full_grouped.csv")
except FileNotFoundError:
    messagebox.showerror("Error", "Could not find full_grouped.csv in the folder")
    exit()

# Check column names dynamically
cols = [c.lower() for c in data.columns]

# Identify possible column names
date_col = [c for c in data.columns if 'date' in c.lower()][0]
country_col = [c for c in data.columns if 'country' in c.lower()][0]
confirmed_col = [c for c in data.columns if 'confirmed' in c.lower()][0]
deaths_col = [c for c in data.columns if 'death' in c.lower()][0]
recovered_col = [c for c in data.columns if 'recovered' in c.lower()][0]

# Convert date column to datetime
data[date_col] = pd.to_datetime(data[date_col])

# ------------- BUILD GUI -------------
root = tk.Tk()
root.title("COVID-19 Data Dashboard – Day 17")
root.geometry("1000x700")
root.configure(bg="#1e1e1e")

title_lbl = tk.Label(
    root,
    text="COVID-19 Data Dashboard (Day 17)",
    font=("Arial", 20, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title_lbl.pack(pady=10)

# Dropdown for countries
countries = sorted(data[country_col].unique())
country_var = tk.StringVar(value="Worldwide")

country_label = tk.Label(root, text="Select Country:", font=("Arial", 12), bg="#1e1e1e", fg="white")
country_label.pack()

country_cb = ttk.Combobox(root, textvariable=country_var, values=["Worldwide"] + countries, width=40)
country_cb.pack(pady=5)

# ------------- FIGURE SETUP -------------
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor('#1e1e1e')
ax.set_facecolor('#2e2e2e')
ax.tick_params(colors='white')
ax.title.set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

# ------------- FUNCTIONS -------------
def plot_data():
    ax.clear()

    selected_country = country_var.get()

    if selected_country == "Worldwide":
        df_plot = data.groupby(date_col)[[confirmed_col, deaths_col, recovered_col]].sum().reset_index()
    else:
        df_plot = data[data[country_col] == selected_country].groupby(date_col)[
            [confirmed_col, deaths_col, recovered_col]
        ].sum().reset_index()

    # Plot lines
    ax.plot(df_plot[date_col], df_plot[confirmed_col], label="Confirmed", color="yellow")
    ax.plot(df_plot[date_col], df_plot[deaths_col], label="Deaths", color="red")
    ax.plot(df_plot[date_col], df_plot[recovered_col], label="Recovered", color="green")

    ax.set_title(f"COVID-19 Trend: {selected_country}", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")
    ax.legend(facecolor='#2e2e2e', edgecolor='white', labelcolor='white')
    ax.grid(True, alpha=0.3)

    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#2e2e2e')

    canvas.draw()

# Initial plot
plot_data()

country_cb.bind("<<ComboboxSelected>>", lambda e: plot_data())

# ------------- MAINLOOP -------------
root.mainloop()
