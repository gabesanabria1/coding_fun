import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# === DATABASE SETUP ===
conn = sqlite3.connect("entries.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        content TEXT NOT NULL
    )
""")
conn.commit()

# === APPLICATION CLASS ===
class TextEntryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Entry Application")
        self.show_home()

    def show_home(self):
        self.clear_frame()

        home_frame = ttk.Frame(self.root, padding=20)
        home_frame.pack(fill="both", expand=True)

        ttk.Label(home_frame, text="Welcome to Text Entry App!", font=("Helvetica", 16)).pack(pady=10)
        ttk.Button(home_frame, text="Create New Entry", command=self.new_entry).pack(pady=10)
        ttk.Button(home_frame, text="View Past Entries", command=self.view_entries).pack(pady=10)

    def new_entry(self):
        self.clear_frame()

        entry_frame = ttk.Frame(self.root, padding=20)
        entry_frame.pack(fill="both", expand=True)

        ttk.Label(entry_frame, text="Enter your text:", font=("Helvetica", 12)).pack(anchor="w")
        text_box = tk.Text(entry_frame, width=60, height=15)
        text_box.pack(pady=10)

        def save_entry():
            content = text_box.get("1.0", tk.END).strip()
            if not content:
                messagebox.showwarning("Empty", "Please enter some text.")
                return
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO entries (timestamp, content) VALUES (?, ?)", (timestamp, content))
            conn.commit()
            messagebox.showinfo("Saved", "Entry saved successfully!")
            self.show_home()

        ttk.Button(entry_frame, text="Save", command=save_entry).pack(pady=5)
        ttk.Button(entry_frame, text="Back", command=self.show_home).pack()

    def view_entries(self):
        self.clear_frame()

        view_frame = ttk.Frame(self.root, padding=20)
        view_frame.pack(fill="both", expand=True)

        ttk.Label(view_frame, text="Past Entries", font=("Helvetica", 12)).pack()

        listbox = tk.Listbox(view_frame, width=60, height=10)
        listbox.pack(pady=10)

        cursor.execute("SELECT id, timestamp FROM entries ORDER BY id DESC")
        entries = cursor.fetchall()

        entry_map = {}

        for entry_id, timestamp in entries:
            display_text = f"{entry_id}: {timestamp}"
            listbox.insert(tk.END, display_text)
            entry_map[display_text] = entry_id

        def show_content():
            selected = listbox.get(tk.ACTIVE)
            if not selected:
                return
            entry_id = entry_map[selected]
            cursor.execute("SELECT content FROM entries WHERE id=?", (entry_id,))
            content = cursor.fetchone()[0]
            messagebox.showinfo("Entry Content", content)

        ttk.Button(view_frame, text="View Selected Entry", command=show_content).pack()
        ttk.Button(view_frame, text="Back", command=self.show_home).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# === RUN APP ===
if __name__ == "__main__":
    root = tk.Tk()
    app = TextEntryApp(root)
    root.mainloop()