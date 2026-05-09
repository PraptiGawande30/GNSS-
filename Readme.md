GNSS Processing Panel (GUI)
📌 Overview

This project is a desktop GUI application built using Python and CustomTkinter for processing and previewing GNSS-related files.

It allows users to:

Select multiple files
Preview CSV / Excel / GNSS files
Enter station details
Run basic processing workflow

🚀 Features
📂 File Preview
Supports:
.csv
.xlsx
.xls
.obs
.OU1
Displays first 30 rows of tabular data
GNSS files are shown as text preview

⚙️ Processing Panel
Input:
Station Name
Date (with calendar picker)
Output:
Displays selected files
Shows processing status

🖥️ Tech Stack
Python
CustomTkinter (Modern UI)
Tkinter
Pandas (Data handling)
TkCalendar

📁 Project Structure
GNSS/
│── GNSS.py
│── requirements.txt
│── README.md
│── .venv/


▶️ How to Run
1. Create Virtual Environment : 
python -m venv .venv

2. Activate Environment : 
.venv\Scripts\activate

3. Install Dependencies : 
pip install -r requirements.txt

4. Run Application : 
python GNSS.py
