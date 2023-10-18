import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import sqlite3
import pandas as pd
import random
import os
import sys
from tkinter import Scrollbar

# Setting the vibe with some cool color
bg_color = '#7F00FF'

# Function to get the available recipe tables
def fetch_tables(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    return tables

# Function to select a recipe and show the ingredients
def select_recipe(table_name, root, frame):
    if table_name == 'sqlite_sequence':
        # Restart the program if the table name is 'sqlite_sequence'
        print('Oops, something went wrong. Let me fix that for you!')
        python = sys.executable
        os.execl(python, python, *sys.argv)
    else:
        # Fetch the recipe details from the database
        ingredient = pd.DataFrame()
        conn = sqlite3.connect('data/recipes.db') 
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            ingredient = pd.concat([ingredient, pd.DataFrame([row])], ignore_index=True)
        conn.close()
        # Destroy the current frame and display the selected recipe details
        frame.destroy()
        frame2_start(table_name, ingredient, root)

# Function to show the selected recipe details in a separate frame
def frame2_start(table_name, ingredient, root):
    # Creating a new frame to display the recipe details
    frame = tk.Frame(root, width=600, height=700, bg=bg_color)
    frame.pack()
    frame.pack_propagate(False)

    # Display the recipe name on top
    label1 = tk.Label(frame, text=table_name, justify='left', anchor='w', font=("TKMenuFont", 25), background=bg_color, fg="white")
    label1.pack()

    # Display the ingredients using a scrollbar and a text box
    text_box = tk.Text(frame, font=('fonts\Shanti-Regular.ttf', 20), bg=bg_color, fg="white", width=20, relief=tk.SUNKEN)
    scrollbar = Scrollbar(frame, command=text_box.yview, width=20, relief=tk.FLAT) 

    text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0), pady=(10, 150))
    text_box.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 10), pady=10, ipady=100)
    
    # Show the ingredients in the text box
    ingredients_text = '\n'.join([' '.join(map(str, row)) for row in ingredient.values])
    text_box.insert(tk.END, ingredients_text)

    # Create a button to go back to the main screen
    button_frame = tk.Frame(frame, bg=bg_color)
    button_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 50))

    return_button = tk.Button(
        button_frame, 
        text="Return",
        font=("TKHeadingFont", 20),
        bg="#4C0099",
        fg="white",
        cursor='hand2',
        activebackground="#9999FF",
        activeforeground="black",
        command=lambda: frame1(root, frame)
    )
    return_button.pack()

# Function to handle table selection from the drop-down menu
def table_selection(event, selected_table, root, frame):
    selected_table_name = selected_table.get()
    if selected_table_name:
        select_recipe(selected_table_name, root, frame)

# Function to create the main screen for selecting a recipe
def frame1(root, frame=None):
    if frame:
        frame.destroy()

    # Creating the main frame for the app
    frame = tk.Frame(root, width=650, height=700, bg=bg_color)
    frame.pack()
    frame.pack_propagate(False)

    # Displaying the logo at the top
    logo_image = ImageTk.PhotoImage(file='img/LOGO.png')  
    logo_widget = tk.Label(frame, image=logo_image, bg=bg_color)
    logo_widget.image = logo_image
    logo_widget.pack()

    # Getting the list of available recipes from the database
    database_name = 'data/recipes.db'  
    tables = fetch_tables(database_name)

    # Displaying text and creating a dropdown menu for recipe selection
    text1 = tk.Label(
        frame, text='Choose your favorite recipe:\n',
        bg=bg_color,
        fg="white",
        font=("fonts/Ubuntu-Bold.ttf", 14)
    )
    text1.pack()

    selected_table = tk.StringVar(root)
    if tables:
        table_selector = ttk.Combobox(frame, text='select a recipe', textvariable=selected_table, values=tables, state='readonly')
        table_selector.config(font=("Arial", 20))
        table_selector.set(">>>Select a recipe<<<")
        table_selector.config(background='#9999FF')
        table_selector.pack(pady=10)

    table_selector.bind("<<ComboboxSelected>>", lambda event: table_selection(event, selected_table, root, frame))

    # Displaying text for shuffling
    text2 = tk.Label(
        frame, text='\nOr let us choose a recipe for you:\n',
        bg=bg_color,
        fg="white",
        font=("fonts/Ubuntu-Bold.ttf", 14)
    )
    text2.pack()

    # Adding a button for shuffling recipes
    tk.Button(
        frame, text="SHUFFLE",
        font=("TKHeadingFont", 20),
        bg="#4C0099",
        fg="white",
        cursor='hand2',
        activebackground="#9999FF",
        activeforeground="black",
        command=lambda: select_recipe(random.choice(tables), root, frame),
    ).pack()

# Configuring the root window
root = tk.Tk()
root.title('Recipe Lottery')  
root.iconbitmap('img\ICO.ico') 
root.geometry('650x700')  
root.configure(background=bg_color)  
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x_offset = (root.winfo_screenwidth() - width) // 2
y_offset = (root.winfo_screenheight() - height) // 2
root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")  

# Starting with the first frame
frame1(root)
root.mainloop()  
