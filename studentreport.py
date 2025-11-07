import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# ====================== BACKEND ====================== #

def connect_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll TEXT UNIQUE,
            course TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_record(name, roll, course, email):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO student (name, roll, course, email) VALUES (?, ?, ?, ?)",
                (name, roll, course, email))
    conn.commit()
    conn.close()

def fetch_records():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_record(roll):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE roll=?", (roll,))
    conn.commit()
    conn.close()

def update_record(name, roll, course, email):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("UPDATE student SET name=?, course=?, email=? WHERE roll=?",
                (name, course, email, roll))
    conn.commit()
    conn.close()

def search_record(roll):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student WHERE roll=?", (roll,))
    row = cur.fetchone()
    conn.close()
    return row


# ====================== FRONTEND ====================== #

connect_db()

root = Tk()
root.title("🎓 Student Enrollment and Information System")
root.geometry("900x600")
root.config(bg="#101820")

# Title
Label(root, text="Student Enrollment and Information System", font=("Poppins", 22, "bold"), bg="#101820", fg="#FEE715").pack(pady=20)

# Input Frame
frame = Frame(root, bg="#101820")
frame.pack(pady=10)

Label(frame, text="Name:", font=("Poppins", 12), bg="#101820", fg="white").grid(row=0, column=0, padx=10, pady=5)
name_var = StringVar()
Entry(frame, textvariable=name_var, width=30).grid(row=0, column=1, pady=5)

Label(frame, text="Roll No:", font=("Poppins", 12), bg="#101820", fg="white").grid(row=1, column=0, padx=10, pady=5)
roll_var = StringVar()
Entry(frame, textvariable=roll_var, width=30).grid(row=1, column=1, pady=5)

Label(frame, text="Course:", font=("Poppins", 12), bg="#101820", fg="white").grid(row=2, column=0, padx=10, pady=5)
course_var = StringVar()
Entry(frame, textvariable=course_var, width=30).grid(row=2, column=1, pady=5)

Label(frame, text="Email:", font=("Poppins", 12), bg="#101820", fg="white").grid(row=3, column=0, padx=10, pady=5)
email_var = StringVar()
Entry(frame, textvariable=email_var, width=30).grid(row=3, column=1, pady=5)


# ===== Functions ===== #
def add_student():
    if name_var.get() == "" or roll_var.get() == "":
        messagebox.showerror("Error", "Please fill all details")
        return
    try:
        insert_record(name_var.get(), roll_var.get(), course_var.get(), email_var.get())
        messagebox.showinfo("Success", "Record added successfully")
        show_records()
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Duplicate Roll No or DB Error\n{e}")

def show_records():
    records = fetch_records()
    table.delete(*table.get_children())
    for row in records:
        table.insert('', END, values=row)

def delete_student():
    if roll_var.get() == "":
        messagebox.showerror("Error", "Enter Roll No to delete")
        return
    delete_record(roll_var.get())
    messagebox.showinfo("Deleted", "Record deleted successfully")
    show_records()
    clear_fields()

def update_student():
    if roll_var.get() == "":
        messagebox.showerror("Error", "Enter Roll No to update")
        return
    update_record(name_var.get(), roll_var.get(), course_var.get(), email_var.get())
    messagebox.showinfo("Updated", "Record updated successfully")
    show_records()
    clear_fields()

def search_student():
    if roll_var.get() == "":
        messagebox.showerror("Error", "Enter Roll No to search")
        return
    record = search_record(roll_var.get())
    if record:
        clear_fields()
        name_var.set(record[1])
        roll_var.set(record[2])
        course_var.set(record[3])
        email_var.set(record[4])
    else:
        messagebox.showinfo("Not Found", "No record found for this roll number")

def clear_fields():
    name_var.set("")
    roll_var.set("")
    course_var.set("")
    email_var.set("")

# Buttons
btn_frame = Frame(root, bg="#101820")
btn_frame.pack(pady=15)

Button(btn_frame, text="Add", command=add_student, width=10, bg="#FEE715", fg="black", font=("Poppins", 11, "bold")).grid(row=0, column=0, padx=10)
Button(btn_frame, text="Update", command=update_student, width=10, bg="#FEE715", fg="black", font=("Poppins", 11, "bold")).grid(row=0, column=1, padx=10)
Button(btn_frame, text="Delete", command=delete_student, width=10, bg="#FEE715", fg="black", font=("Poppins", 11, "bold")).grid(row=0, column=2, padx=10)
Button(btn_frame, text="Search", command=search_student, width=10, bg="#FEE715", fg="black", font=("Poppins", 11, "bold")).grid(row=0, column=3, padx=10)
Button(btn_frame, text="Show All", command=show_records, width=10, bg="#FEE715", fg="black", font=("Poppins", 11, "bold")).grid(row=0, column=4, padx=10)
Button(btn_frame, text="Clear", command=clear_fields, width=10, bg="#FEE715", fg="black", font=("Poppins", 11, "bold")).grid(row=0, column=5, padx=10)

# Table Frame
table_frame = Frame(root)
table_frame.pack(pady=20)

scroll_y = Scrollbar(table_frame, orient=VERTICAL)
table = ttk.Treeview(table_frame, columns=("ID", "Name", "Roll", "Course", "Email"), yscrollcommand=scroll_y.set)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_y.config(command=table.yview)

table.heading("ID", text="ID")
table.heading("Name", text="Name")
table.heading("Roll", text="Roll No")
table.heading("Course", text="Course")
table.heading("Email", text="Email")
table['show'] = 'headings'

table.column("ID", width=50)
table.column("Name", width=150)
table.column("Roll", width=100)
table.column("Course", width=150)
table.column("Email", width=200)
table.pack(fill=BOTH, expand=1)

show_records()

Label(root, text="Developed by Swapnil Kumar", font=("Poppins", 10), bg="#101820", fg="white").pack(side=BOTTOM, pady=10)

root.mainloop()