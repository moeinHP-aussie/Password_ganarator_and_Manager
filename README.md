<div align="center">

# 🔐 Password Generator & Manager

### A modern desktop application for generating, storing, searching, and managing passwords.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite)

</div>

---

## 📖 Overview

**Password Generator & Manager** is a desktop application developed with **Python**, **Tkinter**, and **SQLite** that helps users create secure passwords and manage them in a local database.

The application combines password generation and password management into a single user-friendly interface.

---

# ✨ Features

### 🔑 Password Generator

- Generate random passwords
- Three password strength levels
  - 🟢 Poor
  - 🟡 Average
  - 🔴 Strong
- Custom password length
- Optional keyword insertion inside generated password
- Automatic password strength labeling

---

### 💾 Password Management

- Save generated passwords
- Add existing passwords manually
- Store remarks for each password
- View all saved passwords
- Search passwords by remark
- Update existing records
- Delete selected passwords

---

### 🗄 Database

- Local SQLite database
- Automatic database initialization
- Persistent password storage

---

# 🖥 User Interface

The application contains two main tabs.

## Generator

- Select password strength
- Choose password length
- Optional keyword
- Generate password
- Save generated password

---

## Manual Entry

Add already existing passwords manually.

---

## Password Records

The records section allows users to:

- View all passwords
- Search records
- Edit records
- Delete records


```
images/
    generator.png
    manager.png
```

Example:

```markdown
![Generator](images/generator.png)

![Manager](images/manager.png)
```

---

# 🛠 Technologies

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| Tkinter | Graphical User Interface |
| SQLite | Local database |
| Random | Password generation |
| String | Character sets |

---

# 📂 Project Structure

```
Password-Generator-Manager/
│
├── MAIN.py
├── passwords.db
├── README.md
└── images/
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/your-username/Password-Generator-Manager.git
```

Go to project folder

```bash
cd Password-Generator-Manager
```

Run

```bash
python MAIN.py
```

---

# 🎯 Password Strength Levels

| Level | Characters Used |
|--------|-----------------|
| Poor | Letters |
| Average | Letters + Numbers |
| Strong | Letters + Numbers + Symbols |

---

# 📊 Application Workflow

```text
Start
   │
   ▼
Choose Generator or Manual Entry
   │
   ▼
Generate / Enter Password
   │
   ▼
Save to SQLite Database
   │
   ▼
View Records
   │
   ├──────── Search
   ├──────── Update
   └──────── Delete
```

---

# 🌟 Future Improvements

- AES encryption for stored passwords
- Master password authentication
- Copy password to clipboard
- Password visibility toggle
- Password categories
- Export to CSV
- Dark Mode
- Password expiration reminders
- Password reuse detection







Made with ❤️ using Python

</div>
