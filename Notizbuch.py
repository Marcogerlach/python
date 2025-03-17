import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import json
import os

DATA_FILE = "entries.json"

class Notizbuch(ttk.Frame):
    def load_entries(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.entries = json.load(f)
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Einträge: {e}")

    def __init__(self, master):
        super().__init__(master)
        master.title("Notizbuch")
        master.state('zoomed')
        master.configure(background="#ADD8E6")
        self.master = master

        self.style = ttk.Style()
        self.style.theme_use("clam")
        base_font_size = 12
        self.base_font = "Arial"
        self.style.configure("TLabel", font=(self.base_font, base_font_size),
                             background="#ADD8E6", foreground="black")
        self.style.configure("TButton", font=(self.base_font, base_font_size),
                             background="#d9d9d9")
        self.style.configure("TEntry", font=(self.base_font, base_font_size))
        self.style.configure("TFrame", background="#ADD8E6")
        self.style.configure("TLabelframe", background="#ADD8E6", foreground="black")
        self.style.configure("TLabelframe.Label", font=(self.base_font, 14, "bold"))

        self.entries = []
        self.load_entries()

        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Beenden", command=self.master.quit)
        menubar.add_cascade(label="Datei", menu=filemenu)
        
        size_menu = tk.Menu(menubar, tearoff=0)
        size_menu.add_command(label="Klein (600x400)", command=lambda: self.master.geometry("600x400"))
        size_menu.add_command(label="Mittel (800x600)", command=lambda: self.master.geometry("800x600"))
        size_menu.add_command(label="Groß (1024x768)", command=lambda: self.master.geometry("1024x768"))
        menubar.add_cascade(label="Größe", menu=size_menu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Über", command=self.show_about)
        menubar.add_cascade(label="Hilfe", menu=helpmenu)
        self.master.config(menu=menubar)

        self.pack(fill=tk.BOTH, expand=True)

        frame_list = ttk.LabelFrame(self, text="Einträge")
        frame_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.listbox = tk.Listbox(frame_list, height=20, font=(self.base_font, base_font_size), bg="white")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        scrollbar = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.refresh_listbox()

        self.master.bind("<Configure>", self.on_resize)

        # Add legend for priority colors
        frame_legend = ttk.LabelFrame(self, text="Priorität Legende")
        frame_legend.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        priorities = {
            1: "#FF0000",  # Red
            2: "#FF7F00",  # Orange
            3: "#FFFF00",  # Yellow
            4: "#7FFF00",  # Light Green
            5: "#00FF00"   # Green
        }

        for priority, color in priorities.items():
            label = ttk.Label(frame_legend, text=f"Priorität {priority}", background=color)
            label.pack(fill=tk.X, padx=5, pady=2)

        # Add entry form at the bottom
        self.entry_form_frame = ttk.LabelFrame(self, text="Neue Aufgabe hinzufügen")
        self.entry_form_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        ttk.Label(self.entry_form_frame, text="Eintrag:").pack(anchor="w", padx=5, pady=(5, 0))
        self.entry_text = ttk.Entry(self.entry_form_frame, width=40)
        self.entry_text.pack(padx=5, pady=5)

        ttk.Label(self.entry_form_frame, text="Anzahl Tage ab heute:").pack(anchor="w", padx=5, pady=(5, 0))
        self.deadline_entry = ttk.Entry(self.entry_form_frame, width=40)
        self.deadline_entry.pack(padx=5, pady=5)

        ttk.Label(self.entry_form_frame, text="Priorität (1-5):").pack(anchor="w", padx=5, pady=(5, 0))
        self.priority_entry = ttk.Entry(self.entry_form_frame, width=40)
        self.priority_entry.pack(padx=5, pady=5)

        btn_add = ttk.Button(self.entry_form_frame, text="Hinzufügen", command=self.add_entry)
        btn_add.pack(fill=tk.X, padx=5, pady=2)

        # Load icons
        try:
            self.icon_edit = tk.PhotoImage(file="edit_icon.png")
            self.icon_delete = tk.PhotoImage(file="delete_icon.png")
            self.icon_done = tk.PhotoImage(file="done_icon.png")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Icons: {e}")
        self.icon_edit = self.icon_edit if 'self.icon_edit' in locals() else None
        self.icon_delete = self.icon_delete if 'self.icon_delete' in locals() else None
        self.icon_done = self.icon_done if 'self.icon_done' in locals() else None

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for index, entry in enumerate(self.entries):
            text = entry.get("text")
            deadline = entry.get("deadline")
            priority = entry.get("priority")
            status = " [Erledigt]" if entry.get("done") else ""
            display_text = f"{text} (bis {deadline}){status}"
            self.listbox.insert(tk.END, display_text)
            self.listbox.itemconfig(tk.END, {'bg': self.get_priority_color(priority)})

            # Add buttons
            btn_frame = tk.Frame(self.listbox)
            btn_frame.pack(fill=tk.X)

            if self.icon_delete:
                btn_delete = ttk.Button(btn_frame, image=self.icon_delete, command=lambda idx=index: self.delete_entry(idx))
                btn_delete.pack(side=tk.LEFT, padx=5, pady=2)

            if self.icon_edit:
                btn_update = ttk.Button(btn_frame, image=self.icon_edit, command=lambda idx=index: self.update_entry(idx))
                btn_update.pack(side=tk.LEFT, padx=5, pady=2)

            if self.icon_done:
                btn_done = ttk.Button(btn_frame, image=self.icon_done, command=lambda idx=index: self.mark_done(idx))
                btn_done.pack(side=tk.LEFT, padx=5, pady=2)

    def get_priority_color(self, priority):
        colors = {
            1: "#FF0000",  # Red
            2: "#FF7F00",  # Orange
            3: "#FFFF00",  # Yellow
            4: "#7FFF00",  # Light Green
            5: "#00FF00"   # Green
        }
        return colors.get(priority, "#FFFFFF")

    def on_resize(self, event=None):
        new_width = self.master.winfo_width()
        scale = new_width / 800
        new_size = max(8, int(12 * scale))
        new_labelframe_label_size = max(8, int(14 * scale))
        self.style.configure("TLabel", font=(self.base_font, new_size))
        self.style.configure("TButton", font=(self.base_font, new_size))
        self.style.configure("TEntry", font=(self.base_font, new_size))
        self.style.configure("TLabelframe.Label", font=(self.base_font, new_labelframe_label_size, "bold"))
        self.listbox.configure(font=(self.base_font, new_size))

    def add_entry(self):
        text = self.entry_text.get().strip()
        days_text = self.deadline_entry.get().strip()
        priority_text = self.priority_entry.get().strip()
        if not text or not days_text or not priority_text:
            messagebox.showwarning("Warnung", "Bitte füllen Sie alle Felder aus.")
            return
        try:
            days = int(days_text)
            priority = int(priority_text)
            if priority < 1 or priority > 5:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warnung", "Bitte geben Sie gültige Werte ein.")
            return

        deadline = (datetime.datetime.today() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        entry = {"text": text, "deadline": deadline, "priority": priority, "done": False}
        self.entries.append(entry)
        self.refresh_listbox()
        self.save_entries()
        self.clear_entry_form()

    def clear_entry_form(self):
        self.entry_text.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

    def delete_entry(self, index):
        del self.entries[index]
        self.refresh_listbox()
        self.save_entries()

    def update_entry(self, index):
        entry = self.entries[index]
        update_window = tk.Toplevel(self.master)
        update_window.title("Aufgabe bearbeiten")
        update_window.geometry("400x300")
        update_window.configure(background="#ADD8E6")

        ttk.Label(update_window, text="Eintrag:").pack(anchor="w", padx=5, pady=(5, 0))
        entry_text = ttk.Entry(update_window, width=40)
        entry_text.insert(0, entry["text"])
        entry_text.pack(padx=5, pady=5)

        ttk.Label(update_window, text="Anzahl Tage ab heute:").pack(anchor="w", padx=5, pady=(5, 0))
        deadline_entry = ttk.Entry(update_window, width=40)
        deadline_entry.pack(padx=5, pady=5)

        ttk.Label(update_window, text="Priorität (1-5):").pack(anchor="w", padx=5, pady=(5, 0))
        priority_entry = ttk.Entry(update_window, width=40)
        priority_entry.insert(0, entry["priority"])
        priority_entry.pack(padx=5, pady=5)

        def save_update():
            text = entry_text.get().strip()
            days_text = deadline_entry.get().strip()
            priority_text = priority_entry.get().strip()
            if not text or not days_text or not priority_text:
                messagebox.showwarning("Warnung", "Bitte füllen Sie alle Felder aus.")
                return
            try:
                days = int(days_text)
                priority = int(priority_text)
                if priority < 1 or priority > 5:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Warnung", "Bitte geben Sie gültige Werte ein.")
                return

            deadline = (datetime.datetime.today() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
            self.entries[index] = {"text": text, "deadline": deadline, "priority": priority, "done": False}
            self.refresh_listbox()
            self.save_entries()
            update_window.destroy()

        btn_save = ttk.Button(update_window, text="Speichern", command=save_update)
        btn_save.pack(fill=tk.X, padx=5, pady=2)

    def mark_done(self, index):
        self.entries[index]["done"] = not self.entries[index].get("done", False)
        self.refresh_listbox()
        self.save_entries()

    def sort_entries(self):
        try:
            self.entries.sort(key=lambda e: (datetime.datetime.strptime(e["deadline"], "%Y-%m-%d"), e["priority"]))
            self.refresh_listbox()
            self.save_entries()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Sortieren: {e}")

    def on_select(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        if index >= len(self.entries):
            return

    def save_entries(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Einträge: {e}")

    def show_about(self):
        messagebox.showinfo("Über", "Notizbuch v1.1\nErstellt mit Python und Tkinter.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Notizbuch(root)
    root.mainloop()
