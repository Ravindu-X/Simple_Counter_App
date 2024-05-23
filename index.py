import tkinter as tk
from tkinter import simpledialog, Menu, messagebox
from tkinter import ttk
import json

class NumberCounterApp:
    def __init__(self, master):
        self.master = master
        self.counts = {}
        self.load_counts()
        
        self.create_widgets()

    def create_widgets(self):
        self.master.title("The Counter App")

        # Entry for Category Name
        ttk.Label(self.master, text="Enter Category Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.category_entry = ttk.Entry(self.master)
        self.category_entry.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        # Enter Button
        self.enter_button = ttk.Button(self.master, text="Enter", command=self.enter_category)
        self.enter_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Increment and Decrement Buttons
        ttk.Button(self.master, text="+", command=self.increment_count).grid(row=0, column=3, padx=5, pady=5, sticky="w")
        ttk.Button(self.master, text="-", command=self.decrement_count).grid(row=0, column=4, padx=5, pady=5, sticky="w")

        # Save, Delete, and Reset Buttons
        ttk.Button(self.master, text="Save", command=self.save_counts).grid(row=0, column=5, padx=5, pady=5, sticky="e")
        ttk.Button(self.master, text="Reset", command=self.reset_entry_fields).grid(row=0, column=6, padx=5, pady=5, sticky="e")

        # Saved Counters
        self.saved_counters_frame = ttk.Frame(self.master)
        self.saved_counters_frame.grid(row=1, column=0, columnspan=7, padx=5, pady=5, sticky="nsew")

        self.saved_counters_label = ttk.Label(self.saved_counters_frame, text="Saved Counters:")
        self.saved_counters_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.saved_counters_listbox = tk.Listbox(self.saved_counters_frame, selectmode=tk.SINGLE, font=("Helvetica", 12))
        self.saved_counters_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.saved_counters_listbox.bind("<<ListboxSelect>>", self.populate_entry_fields)

        # Context menu for counters
        self.context_menu = Menu(self.saved_counters_listbox, tearoff=0)
        self.context_menu.add_command(label="Rename", command=self.rename_counter)
        self.context_menu.add_command(label="Delete", command=self.delete_counter)

        self.saved_counters_listbox.bind("<Button-3>", self.show_context_menu)

        self.update_saved_counters_list()

    def show_context_menu(self, event):
        # Select the item under the cursor
        self.saved_counters_listbox.selection_clear(0, "end")
        self.saved_counters_listbox.activate("@{},{}".format(event.x, event.y))
        self.saved_counters_listbox.selection_set("@{},{}".format(event.x, event.y))
        # Display the context menu at the cursor position
        self.context_menu.post(event.x_root, event.y_root)

    def rename_counter(self):
        selected_index = self.saved_counters_listbox.curselection()
        if selected_index:
            selected_counter = self.saved_counters_listbox.get(selected_index)
            category, _ = selected_counter.split(":")
            new_name = simpledialog.askstring("Rename Counter", "Enter new name:", initialvalue=category)
            if new_name:
                self.counts[new_name] = self.counts.pop(category)
                self.update_saved_counters_list()

    def enter_category(self):
        category = self.category_entry.get().strip()
        if category:
            existing_categories = list(self.counts.keys())
            if category in existing_categories:
                new_name = simpledialog.askstring("Update Counter Name", "Enter new name:", initialvalue=category)
                if new_name:
                    self.counts[new_name] = self.counts.pop(category)
            else:
                self.counts[category] = 0
            self.update_saved_counters_list()
            self.reset_entry_fields()

    def increment_count(self):
        category = self.category_entry.get().strip()
        if category:
            self.counts[category] += 1
            self.update_saved_counters_list()

    def decrement_count(self):
        category = self.category_entry.get().strip()
        if category and self.counts.get(category, 0) > 0:
            self.counts[category] -= 1
            self.update_saved_counters_list()

    def delete_counter(self):
        selected_index = self.saved_counters_listbox.curselection()
        if selected_index:
            selected_counter = self.saved_counters_listbox.get(selected_index)
            category, _ = selected_counter.split(":")
            del self.counts[category]
            self.update_saved_counters_list()

    def reset_entry_fields(self):
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, "")

    def save_counts(self):
        with open("counts.json", "w") as f:
            json.dump(self.counts, f)
        messagebox.showinfo("Save", "Counters saved successfully.")

    def load_counts(self):
        try:
            with open("counts.json", "r") as f:
                self.counts = json.load(f)
        except FileNotFoundError:
            pass  # If the file doesn't exist yet, start with an empty dictionary

    def update_saved_counters_list(self):
        self.saved_counters_listbox.delete(0, tk.END)
        for category, count in self.counts.items():
            self.saved_counters_listbox.insert(tk.END, f"{category}: {count}")

    def populate_entry_fields(self, event):
        selected_index = self.saved_counters_listbox.curselection()
        if selected_index:
            selected_counter = self.saved_counters_listbox.get(selected_index)
            category, _ = selected_counter.split(":")
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, category.strip())

def main():
    root = tk.Tk()
    app = NumberCounterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
