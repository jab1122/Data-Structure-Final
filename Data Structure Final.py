#Data Structure Final
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import unittest

class GroceryItem:
    def __init__(self, name, category):
        self.name = name
        self.category = category

class GroceryStore:
    def __init__(self):
        self.items = []
        self.categories = defaultdict(list)

    def add_item(self, item):
        self.items.append(item)
        self.categories[item.category].append(item)

    def get_categories(self):
        return {category: len(items) for category, items in self.categories.items()}

    def get_items_in_category(self, category):
        return self.categories.get(category, [])

class GroceryStoreApp:
    def __init__(self, root):
        self.store = GroceryStore()
        self.root = root
        self.root.title("Grocery Store Item Organizer")

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.pack()
        self.category_entry = tk.Entry(root)
        self.category_entry.pack()
        self.item_label = tk.Label(root, text="Item Name:")
        self.item_label.pack()
        self.item_entry = tk.Entry(root)
        self.item_entry.pack()
        self.add_button = tk.Button(root, text="Add Item", command=self.add_item)
        self.add_button.pack()
        self.show_button = tk.Button(root, text="Show Categories", command=self.show_categories)
        self.show_button.pack()
        self.category_listbox = tk.Listbox(root)  
        self.category_listbox.pack()
        self.category_listbox.bind('<<ListboxSelect>>', self.show_items_in_category)
#Had to relearn most of the GUI stuff since I last did python last semester
    def add_item(self):
        category = self.category_entry.get()
        item_name = self.item_entry.get()
        if category and item_name:
            item = GroceryItem(item_name.upper(), category.upper())
            self.store.add_item(item)
            messagebox.showinfo("Success", f"Added {item_name} to {category}")
            self.category_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both category and item name.")

    def show_categories(self):
        self.category_listbox.delete(0, tk.END)
        categories = self.store.get_categories()
        for category, count in categories.items():
            self.category_listbox.insert(tk.END, f"{category} ({count})")

    def show_items_in_category(self, event):
        selected = self.category_listbox.curselection()
        if selected:
            category = self.category_listbox.get(selected).split(' ')[0]
            items = self.store.get_items_in_category(category)
            items_list = "\n".join(item.name for item in items)
            messagebox.showinfo("Items in Category", items_list if items_list else "No items in this category.")

class TestGroceryStore(unittest.TestCase):
    def setUp(self):
        self.store = GroceryStore()

    def test_add_item(self):
        item = GroceryItem("APPLE", "FRUITS")
        self.store.add_item(item)
        self.assertEqual(len(self.store.items), 1)
        self.assertIn(item, self.store.items)
        self.assertIn(item, self.store.get_items_in_category("FRUITS"))

    def test_get_categories(self):
        self.store.add_item(GroceryItem("APPLE", "FRUITS"))
        self.store.add_item(GroceryItem("BANANA", "FRUITS"))
        self.store.add_item(GroceryItem("CARROT", "VEGETABLES"))
        categories = self.store.get_categories()
        self.assertEqual(categories, {"FRUITS": 2, "VEGETABLES": 1})

    def test_get_items_in_category(self):
        self.store.add_item(GroceryItem("APPLE", "FRUITS"))
        self.store.add_item(GroceryItem("BANANA", "FRUITS"))
        items = self.store.get_items_in_category("FRUITS")
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, "APPLE")
        self.assertEqual(items[1].name, "BANANA")

if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryStoreApp(root)
    root.mainloop()
    unittest.main()