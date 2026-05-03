import customtkinter as ctk
from tkinter import filedialog, ttk
from tkcalendar import Calendar
import tkinter as tk
import pandas as pd
import os

# ================= THEME =================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ================= APP =================
app = ctk.CTk()
app.title("GNSS Processing Panel")
app.geometry("800x400")

# ================= TABLE STYLE =================
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white")

style.configure("Treeview.Heading",
                background="#E3ECF5",
                foreground="black",
                font=('Arial', 10, 'bold'))

# ================= FILE SELECT FUNCTION =================
file_paths = []

def browse_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(
        filetypes=[
            ("Supported Files", "*.csv *.xlsx *.xls *.OU1 *.obs"),
            ("All files", "*.*")
        ]
    )

    if file_paths:
        show_frame(file_frame)  # ensure preview visible
        file_label.configure(text=os.path.basename(file_paths[0]))
        load_table(file_paths[0])

# ================= MAIN LAYOUT =================
main = ctk.CTkFrame(app, fg_color="#F7F9FC")
main.pack(fill="both", expand=True)

# ================= TOP TITLE =================
top_section = ctk.CTkFrame(main, fg_color="#E3ECF5")
top_section.pack(fill="x")

ctk.CTkLabel(
    top_section,
    text="GNSS Processing Panel",
    font=("Arial", 30, "bold"),
    text_color="#1F3A5F"
).pack(pady=10)

# ================= BODY =================
body = ctk.CTkFrame(main)
body.pack(fill="both", expand=True)

# ================= SIDEBAR =================
sidebar = ctk.CTkFrame(body, width=180, fg_color="#EAF0F6")
sidebar.pack(side="left", fill="y")

# ================= CONTENT =================
content = ctk.CTkFrame(body, fg_color="white")
content.pack(side="right", fill="both", expand=True)

# ================= FRAMES =================
file_frame = ctk.CTkFrame(content, fg_color="white")
process_frame = ctk.CTkFrame(content, fg_color="white")

def show_frame(frame):
    file_frame.pack_forget()
    process_frame.pack_forget()
    frame.pack(fill="both", expand=True)

# ================= SIDEBAR BUTTONS =================
ctk.CTkButton(sidebar, text="File Preview",
              command=lambda: show_frame(file_frame)).pack(pady=20, padx=10)

ctk.CTkButton(sidebar, text="Processing",
              command=lambda: show_frame(process_frame)).pack(pady=10, padx=10)

# =====================================================
# ================= FILE PREVIEW =================
# =====================================================

# 🔹 Top strip (button + filename)
top_strip = ctk.CTkFrame(file_frame, fg_color="white")
top_strip.pack(fill="x")

ctk.CTkButton(
    top_strip,
    text="📂 Select Files",
    height=40,
    width=160,
    font=("Arial", 14, "bold"),
    command=browse_files
).pack(side="left", padx=10, pady=10)

file_label = ctk.CTkLabel(top_strip, text="")
file_label.pack(side="left", padx=10)

# 🔹 Table
table_frame = ctk.CTkFrame(file_frame, fg_color="white")
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

scroll_y = tk.Scrollbar(table_frame)
scroll_y.pack(side="right", fill="y")

scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
scroll_x.pack(side="bottom", fill="x")

table = ttk.Treeview(
    table_frame,
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)
table.pack(fill="both", expand=True)

scroll_y.config(command=table.yview)
scroll_x.config(command=table.xview)

def load_table(path):
    for i in table.get_children():
        table.delete(i)

    ext = os.path.splitext(path)[1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(path)

        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(path)

        elif ext in [".ou1", ".obs"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()[:30]

            table["columns"] = ["Preview"]
            table["show"] = "headings"
            table.heading("Preview", text="GNSS File Content")

            for line in lines:
                table.insert("", "end", values=[line.strip()])
            return

        else:
            return

        table["columns"] = list(df.columns)
        table["show"] = "headings"

        for col in df.columns:
            table.heading(col, text=col)
            table.column(col, width=120)

        for _, row in df.head(30).iterrows():
            table.insert("", "end", values=list(row))

    except Exception as e:
        print("Error:", e)

# ================= PROCESSING =================

# 🔹 Center box (perfect center)
center_box = ctk.CTkFrame(process_frame, width=420, height=260, fg_color="white")
center_box.place(relx=0.44, rely=0.4, anchor="center")  
# relx=0.5 → center horizontally
# rely=0.4 → slightly below heading (not exact middle)

# 🔹 Input section
input_frame = ctk.CTkFrame(center_box, fg_color="white")
input_frame.pack(pady=10)

ctk.CTkLabel(input_frame, text="Station Name").grid(row=0, column=0, padx=10, pady=6)
station_entry = ctk.CTkEntry(input_frame, width=180)
station_entry.grid(row=0, column=1)

ctk.CTkLabel(input_frame, text="Date").grid(row=1, column=0, padx=10, pady=6)
date_entry = ctk.CTkEntry(input_frame, width=140)
date_entry.grid(row=1, column=1)

def open_calendar():
    top = tk.Toplevel(app)
    cal = Calendar(top, date_pattern='yyyy-mm-dd')
    cal.pack()

    def select_date():
        date_entry.delete(0, "end")
        date_entry.insert(0, cal.get_date())
        top.destroy()

    tk.Button(top, text="Select", command=select_date).pack()

ctk.CTkButton(input_frame, text="📅", width=35,
              command=open_calendar).grid(row=1, column=2)

# 🔹 Output box
output_box = ctk.CTkTextbox(center_box, height=200, width=400)
output_box.pack(pady=10)

# 🔹 Processing logic
def run_processing():
    station = station_entry.get()
    date = date_entry.get()

    output_box.delete("1.0", "end")

    if not file_paths or station == "" or date == "":
        output_box.insert("end", "⚠ Fill all fields and select files\n")
        return

    output_box.insert("end", "Processing...\n\n")

    for file in file_paths:
        output_box.insert("end", f"📄 {os.path.basename(file)}\n")

    output_box.insert("end", f"\n📍 Station: {station}")
    output_box.insert("end", f"\n📅 Date: {date}")
    output_box.insert("end", "\n\nStatus: SUCCESS ✅")

# 🔹 Button
ctk.CTkButton(center_box, text="Run Processing",
              command=run_processing).pack(pady=10)

# ================= DEFAULT =================
show_frame(file_frame)

# ================= RUN =================
app.mainloop()