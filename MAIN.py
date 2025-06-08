from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
import random
import string

# --------------------- DATABASE METHODS ---------------------
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT,
            strength TEXT,
            length INTEGER,
            remark TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def load_data(search_query=None):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT * FROM passwords WHERE remark LIKE ? ORDER BY id ASC", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM passwords ORDER BY id ASC")
    records = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for rec in records:
        tree.insert('', 'end', values=rec)
    cursor.close()
    conn.close()

def insert_password(password, strength, length, remark):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (password, strength, length, remark) VALUES (?, ?, ?, ?)",
                   (password, strength, length, remark))
    conn.commit()
    cursor.close()
    conn.close()
    load_data()

def update_password(record_id, password, strength, length, remark):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE passwords SET password=?, strength=?, length=?, remark=? WHERE id=?",
                   (password, strength, length, remark, record_id))
    conn.commit()
    cursor.close()
    conn.close()
    load_data()

def delete_password(record_id):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE id=?", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    load_data()

# --------------------- PASSWORD GENERATION FUNCTIONS ---------------------
def generate_password():
    strength_val = gen_strength.get()
    length_val = int(gen_length.get())
    keyword = keyword_var.get().strip()
    
    # انتخاب کاراکترهای مجاز بر اساس قدرت انتخابی
    if strength_val == 1:
        available_chars = string.ascii_uppercase + string.ascii_lowercase
        strength_text = "POOR"
    elif strength_val == 2:
        available_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        strength_text = "AVERAGE"
    elif strength_val == 3:
        available_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + """`~!@#$%^&*()_-+={}[]\|:;"'<>,.?/"""
        strength_text = "STRONG"
    else:
        tkMessageBox.showwarning("Warning", "Please select a valid password strength!")
        return ""
    
    # اگر کلیدواژه تعیین شده باشد، مطمئن می‌شویم طول پسورد کافی است
    if keyword:
        if length_val < len(keyword):
            tkMessageBox.showerror("Error", "Password length must be at least equal to keyword length!")
            return ""
        # تولید بخش باقی‌مانده پسورد
        remaining_length = length_val - len(keyword)
        rand_part = ''.join(random.choices(available_chars, k=remaining_length))
        # درج کلیدواژه در یک موقعیت تصادفی در پسورد نهایی
        insertion_index = random.randint(0, remaining_length)
        gen_pass = rand_part[:insertion_index] + keyword + rand_part[insertion_index:]
    else:
        # تولید پسورد به صورت تصادفی
        try:
            gen_pass = ''.join(random.choices(available_chars, k=length_val))
        except Exception as e:
            tkMessageBox.showerror("Error", "Error in generating password: " + str(e))
            return ""
    
    result_label.config(text=gen_pass)
    return gen_pass, strength_text, length_val

def on_generate():
    res = generate_password()
    if res:
        gen_pass, str_text, length_val = res
        pwd_var.set(gen_pass)
        str_var.set(str_text)
        len_var.set(length_val)

def on_save_gen():
    pwd = pwd_var.get()
    stren = str_var.get()
    leng = len_var.get()
    remark = gen_remark.get()
    if pwd == "":
        tkMessageBox.showwarning("Warning", "No password generated!")
        return
    insert_password(pwd, stren, leng, remark)
    # پاکسازی فیلدهای تولید
    pwd_var.set("")
    str_var.set("")
    len_var.set("")
    keyword_var.set("")
    gen_remark.set("")
    result_label.config(text="")

# --------------------- MANUAL ENTRY FUNCTIONS ---------------------
def on_save_manual():
    manual_pwd = manual_pwd_var.get().strip()
    manual_remark = manual_remark_var.get().strip()
    manual_strength = manual_strength_var.get().strip()
    if manual_pwd == "":
        tkMessageBox.showwarning("Warning", "Please enter a password!")
        return
    # در صورت خالی بودن قدرت، به صورت Unknown در نظر بگیریم
    if manual_strength == "":
        manual_strength = "Unknown"
    manual_length = len(manual_pwd)
    insert_password(manual_pwd, manual_strength, manual_length, manual_remark)
    manual_pwd_var.set("")
    manual_strength_var.set("")
    manual_remark_var.set("")

# --------------------- UPDATE WINDOW (for both tabs) ---------------------
def on_tree_double_click(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, 'values')
    global update_id
    update_id = values[0]
    global update_window
    update_window = Toplevel(root)
    update_window.title("Update Password")
    update_window.resizable(0, 0)
    
    Label(update_window, text="Password:").grid(row=0, column=0, padx=10, pady=5)
    upd_password = Entry(update_window, width=30)
    upd_password.grid(row=0, column=1, padx=10, pady=5)
    upd_password.insert(0, values[1])
    
    Label(update_window, text="Strength:").grid(row=1, column=0, padx=10, pady=5)
    upd_strength = Entry(update_window, width=30)
    upd_strength.grid(row=1, column=1, padx=10, pady=5)
    upd_strength.insert(0, values[2])
    
    Label(update_window, text="Length:").grid(row=2, column=0, padx=10, pady=5)
    upd_length = Entry(update_window, width=30)
    upd_length.grid(row=2, column=1, padx=10, pady=5)
    upd_length.insert(0, values[3])
    
    Label(update_window, text="Remark:").grid(row=3, column=0, padx=10, pady=5)
    upd_remark = Entry(update_window, width=30)
    upd_remark.grid(row=3, column=1, padx=10, pady=5)
    upd_remark.insert(0, values[4])
    
    def save_update():
        new_pwd = upd_password.get().strip()
        new_str = upd_strength.get().strip()
        try:
            new_len = int(upd_length.get().strip())
        except:
            tkMessageBox.showerror("Error", "Length must be a number!")
            return
        new_remark = upd_remark.get().strip()
        update_password(update_id, new_pwd, new_str, new_len, new_remark)
        update_window.destroy()
    
    Button(update_window, text="Update", command=save_update, width=20).grid(row=4, columnspan=2, pady=10)

def on_delete():
    selected_items = tree.selection()
    if not selected_items:
        tkMessageBox.showwarning("Warning", "Please select a record to delete!")
        return
    for item in selected_items:
        values = tree.item(item, 'values')
        ans = tkMessageBox.askquestion("Delete", "Are you sure you want to delete the record?")
        if ans == 'yes':
            delete_password(values[0])


def on_search():
    query = search_entry.get().strip()
    load_data(search_query=query)

# --------------------- STYLE & MAIN WINDOW SETUP ---------------------
root = Tk()
root.state("normal")
root.resizable(True, True)
root.title("Password Generator & Manager")
root.geometry("600x760")


# استفاده از استایل مدرن ttk
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 10))
style.configure("Treeview", font=("Helvetica", 9))
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

# متغیرهای مربوط به تب تولید پسورد
gen_strength = IntVar()
pwd_var = StringVar()
str_var = StringVar()
len_var = StringVar()
keyword_var = StringVar()
gen_remark = StringVar()

# Notebook برای جدا سازی تب‌ها
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ---------- Tab 1: Password Generator ----------
tab_gen = ttk.Frame(notebook)
notebook.add(tab_gen, text="Generator")

gen_frame = ttk.LabelFrame(tab_gen, text="Password Generator", padding=10)
gen_frame.pack(fill="x", padx=10, pady=10)

# انتخاب قدرت پسورد
Label(gen_frame, text="Select Password Strength:").grid(row=0, column=0, sticky=W, pady=5)
Radiobutton(gen_frame, text="POOR", variable=gen_strength, value=1, background="#f0f0f0").grid(row=0, column=1, padx=5, pady=5)
Radiobutton(gen_frame, text="AVERAGE", variable=gen_strength, value=2, background="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
Radiobutton(gen_frame, text="STRONG", variable=gen_strength, value=3, background="#f0f0f0").grid(row=0, column=3, padx=5, pady=5)

# انتخاب طول پسورد
Label(gen_frame, text="Password Length:").grid(row=1, column=0, sticky=W, pady=5)
gen_length = Spinbox(gen_frame, from_=4, to=24, width=5)
gen_length.grid(row=1, column=1, sticky=W, pady=5)

# ورودی کلیدواژه برای درج در پسورد
Label(gen_frame, text="Include Keyword (optional):").grid(row=2, column=0, sticky=W, pady=5)
Entry(gen_frame, textvariable=keyword_var, width=20).grid(row=2, column=1, sticky=W, pady=5)

# دکمه تولید پسورد
Button(gen_frame, text="Generate Password", command=on_generate, bg="#4da6ff", width=20).grid(row=3, column=0, columnspan=2, pady=10)

# نمایش پسورد تولید شده
Label(gen_frame, text="Generated Password:").grid(row=4, column=0, sticky=W, pady=5)
result_label = Label(gen_frame, text="", fg="blue", font=("Helvetica", 12), background="#f0f0f0")
result_label.grid(row=4, column=1, columnspan=3, sticky=W, pady=5)

# فیلد توضیحات
Label(gen_frame, text="Remark:").grid(row=5, column=0, sticky=W, pady=5)
Entry(gen_frame, textvariable=gen_remark, width=40).grid(row=5, column=1, columnspan=3, sticky=W, pady=5)

# دکمه ذخیره پسورد تولید شده
Button(gen_frame, text="Save Password", command=on_save_gen, bg="#66cc66", width=20).grid(row=6, column=0, columnspan=2, pady=10)

# ---------- Tab 2: Manual Entry (for past/old passwords) ----------
tab_manual = ttk.Frame(notebook)
notebook.add(tab_manual, text="Manual Entry")

manual_frame = ttk.LabelFrame(tab_manual, text="Add Existing Password", padding=10)
manual_frame.pack(fill="x", padx=10, pady=10)

Label(manual_frame, text="Password:").grid(row=0, column=0, sticky=W, pady=5)
manual_pwd_var = StringVar()
Entry(manual_frame, textvariable=manual_pwd_var, width=30).grid(row=0, column=1, padx=5, pady=5)

Label(manual_frame, text="Strength (optional):").grid(row=1, column=0, sticky=W, pady=5)
manual_strength_var = StringVar()
Entry(manual_frame, textvariable=manual_strength_var, width=30).grid(row=1, column=1, padx=5, pady=5)

Label(manual_frame, text="Remark:").grid(row=2, column=0, sticky=W, pady=5)
manual_remark_var = StringVar()
Entry(manual_frame, textvariable=manual_remark_var, width=30).grid(row=2, column=1, padx=5, pady=5)

Button(manual_frame, text="Save Password", command=on_save_manual, bg="#66cc66", width=20).grid(row=3, column=0, columnspan=2, pady=10)

# ---------- Section: Password Records & Search (common for both tabs) ----------
records_frame = ttk.LabelFrame(root, text="Password Records", padding=10)
records_frame.pack(fill="both", expand=True, padx=10, pady=10)

search_frame = ttk.Frame(records_frame)
search_frame.pack(fill="x", pady=5)

search_entry = Entry(search_frame, width=40)
search_entry.grid(row=0, column=0, padx=5)
Button(search_frame, text="Search", command=on_search, width=15).grid(row=0, column=1, padx=5)
Button(search_frame, text="Show All", command=lambda: load_data(), width=15).grid(row=0, column=2, padx=5)

table_frame = Frame(records_frame)
table_frame.pack(fill="both", expand=True, pady=5)

scrollbarx = Scrollbar(table_frame, orient=HORIZONTAL)
scrollbary = Scrollbar(table_frame, orient=VERTICAL)
tree = ttk.Treeview(table_frame, columns=("ID", "Password", "Strength", "Length", "Remark"),
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

tree.heading("ID", text="ID", anchor=W)
tree.heading("Password", text="Password", anchor=W)
tree.heading("Strength", text="Strength", anchor=W)
tree.heading("Length", text="Length", anchor=W)
tree.heading("Remark", text="Remark", anchor=W)
tree['show'] = 'headings'
tree.column("ID", width=50, anchor=W)
tree.column("Password", width=150)
tree.column("Strength", width=80)
tree.column("Length", width=80)
tree.column("Remark", width=200)
tree.pack(fill="both", expand=True)

Button(records_frame, text="Delete Selected", command=on_delete, bg="#ff4d4d", fg="white", width=15).pack(pady=5)

tree.bind('<Double-Button-1>', on_tree_double_click)

# --------------------- INITIALIZATION ---------------------
init_db()
load_data()

root.mainloop()
