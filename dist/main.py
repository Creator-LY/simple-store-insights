import tkinter as tk
import spending
from tkinter import ttk, messagebox
from datetime import date
import datetime


class MainScreen(tk.Frame):
    def __init__(self, master, ws, hs):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.iconbitmap('./shopping.ico')
        self.master.resizable(0, 0)
        self.master.title("Search Database")
        self.w = 838
        self.h = 495
        self.ws = ws
        self.hs = hs
        self.master.geometry('%dx%d+%d+%d' % (self.w, self.h, (self.ws/2)-(self.w/2) , (self.hs/2)-(self.h/2)-50))
        self.db = spending.Items()
        self.st = tk.StringVar()
        self.search = ttk.Entry(self.master, width=25, textvariable=self.st)

        category = ('Bakery', 'Dairy and Egg', 'Meat and Fish', 'Fruit and Veg', 'Household', 'Drinks', 'Sauce', 'Snacks')
        self.catergory = tk.StringVar()
        self.filCat = ttk.OptionMenu(self.master, self.catergory, "Filter Category", *category)
        self.filCat.config(width=13)

        stores = ('LiDL', 'Tesco', "Sainsbury's", 'Co-op')
        self.stores = tk.StringVar()
        self.filSto = ttk.OptionMenu(self.master, self.stores, "Filter Stores", *stores)
        self.filSto.config(width=13)

        self.order = tk.StringVar()
        orderBy = ('Alphabet', "Low to High", "High to Low")
        self.orderBy = ttk.OptionMenu(self.master, self.order, "Order By", *orderBy)
        self.orderBy.config(width=13)

        self.listbox = ttk.Treeview(self.master, columns=('Name', 'Price', 'Quantity', 'Category', 'StoreName'), show='headings', height=21)
        self.listbox.bind("<Button-3>", self.popMenu)

        self.panel = tk.Frame(self.master, highlightbackground="black", highlightthickness=1)
        self.itemName = ttk.Entry(self.panel, width=25)
        self.price = ttk.Entry(self.panel, width=25)
        self.quantity = ttk.Spinbox(self.panel, width=10, from_=1, to=100, justify="center")
        self.quantity.insert(0, 1)
        self.catergoryOn = tk.StringVar()
        self.selectedCat = ttk.OptionMenu(self.panel, self.catergoryOn, "Select Category", *category)
        self.selectedCat.config(width=20)
        self.storeOn = tk.StringVar()
        self.selectStore = ttk.OptionMenu(self.panel, self.storeOn, "Select Store", *stores)
        self.selectStore.config(width=20)
        self.photo = tk.PhotoImage(file ='./shopping-image.png')
        self.canvas = tk.Canvas(self.panel, width=20, height=140, bg="red")
        self.canvas.create_image(-20, -20, image=self.photo, anchor="nw")

        self.initGrid()
        self.showList()
        self.st.trace_add("write", self.showList)
        self.catergory.trace_add("write", self.showList)
        self.stores.trace_add("write", self.showList)
        self.order.trace_add("write", self.showList)
        
    
    def initGrid(self):
        ttk.Label(self.master, text="Search: ").grid(column=0, row=0, padx=5, pady=5)
        self.search.grid(column=1, row=0, padx=(5,14), pady=5)
        self.search.focus_set()
        self.filCat.grid(column=2, row=0, pady=5, sticky="EW")
        self.filSto.grid(column=3, row=0, padx=5, pady=5, sticky="EW")
        self.orderBy.grid(column=4, row=0, pady=5, sticky="EW")
        ttk.Button(self.master, text="Spend", command=self.toSpending).grid(column=5, row=0, padx=5, pady=5, sticky="E")
        self.panel.grid(column=6, row=0, rowspan=2, sticky="NSEW", padx=5, pady=5)
        ttk.Label(self.panel, text="ItemName:").grid(column=0, row=0, padx=5, pady=5, sticky="W")
        self.itemName.grid(column=0, row=1, padx=5, pady=5, sticky="EW")
        ttk.Label(self.panel, text="Price:").grid(column=0, row=2, padx=5, pady=5, sticky="W")
        self.price.grid(column=0, row=3, padx=5, pady=5, sticky="EW")
        ttk.Label(self.panel, text="Quantity:").grid(column=0, row=4, padx=5, pady=5, sticky="W")
        self.quantity.grid(column=0, row=4, padx=5, pady=5, sticky="E")
        ttk.Label(self.panel, text="Category:").grid(column=0, row=5, padx=5, pady=5, sticky="W")
        self.selectedCat.grid(column=0, row=6, padx=5, pady=5, sticky="EW")
        ttk.Label(self.panel, text="Store:").grid(column=0, row=7, padx=5, pady=5, sticky="W")
        self.selectStore.grid(column=0, row=8, padx=5, pady=5, sticky="EW")
        ttk.Button(self.panel, text="Add", command=self.addItem).grid(column=0, row=9, padx=5, pady=5, sticky="E")
        ttk.Button(self.panel, text="Reset", command=self.reset).grid(column=0, row=9, padx=5, pady=5, sticky="W")
        self.canvas.grid(column=0, row=10, padx=5, pady=5, sticky="EW")
        
        self.listbox.heading('Name', text='Name')
        self.listbox.column('Name', width=140, anchor="center")
        self.listbox.heading('Price', text='Price (£)')
        self.listbox.column('Price', width=90, anchor="center")
        self.listbox.heading('Quantity', text='Quantity')
        self.listbox.column('Quantity', width=80, anchor="center")
        self.listbox.heading('Category', text='Category')
        self.listbox.column('Category', width=100, anchor="center")
        self.listbox.heading('StoreName', text='StoreName')
        self.listbox.column('StoreName', width=90, anchor="center")
        self.listbox.grid(column=0, row=1, padx=5, pady=5, columnspan=6, sticky="EW")

    def toSpending(self):
        Spending(self.ws, self.hs)

    def showList(self, *args):
        self.listbox.delete(*self.listbox.get_children())
        for item in self.db.show(self.st.get(), self.catergory.get(), self.stores.get(), self.order.get()):
            self.listbox.insert('', tk.END, values=item)

    def addItem(self):
        if self.itemName.get() and self.catergoryOn.get() != "Select Category" and self.storeOn.get() != "Select Store":
            try:
                price = "{:.2f}".format(float(self.price.get()))
                quantity = int(self.quantity.get())
                self.db.add(self.itemName.get(), price, quantity, self.catergoryOn.get(), self.storeOn.get())
                self.showList()
            except ValueError:
                messagebox.showerror(title="Wrong Type", message="The entered value is null or wrong type.", parent=self)
        else: messagebox.showerror(title="Wrong Type", message="The entered/selected value is null.", parent=self)
    
    def deleteItem(self):
        selected = self.listbox.item(self.listbox.focus())['values']
        if selected:
            self.db.delete(selected[0], selected[1], selected[2], selected[3], selected[4])
            self.showList()
        else:
            messagebox.showerror(title="Nothing Selected", message="Please select a row", parent=self)
    
    def popMenu(self, event):
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label="Delete", command=self.deleteItem)
        menu.tk_popup(event.x_root, event.y_root)
    
    def reset(self):
        self.st.set('')
        self.catergory.set('Filter Category')
        self.stores.set('Filter Stores')
        self.order.set('Order By')
        self.itemName.delete(0, tk.END)
        self.itemName.insert(0, '')
        self.price.delete(0, tk.END)
        self.price.insert(0, '')
        self.quantity.delete(0, tk.END)
        self.quantity.insert(0, 1)
        self.catergoryOn.set('Select Category')
        self.storeOn.set('Select Store')

        
class Spending(tk.Toplevel):
    def __init__(self, ws, hs):
        tk.Toplevel.__init__(self)
        self.focus_force()
        self.iconbitmap('./shopping.ico')
        self.resizable(0, 0)
        self.title("Spending")
        self.ws = ws
        self.hs = hs
        self.w = 452
        self.h = 300
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, (self.ws/2)-(self.w/2) , (self.hs/2)-(self.h/2)-50))
        
        self.db = spending.Spend()
        self.total = tk.StringVar()
        self.month = tk.StringVar()
        self.week = tk.StringVar()

        self.price = ttk.Entry(self, width=15)
        self.storeList = ttk.Combobox(self, values=["LiDL", "Tesco", "Sainsbury's", "Co-op"], state="readonly", width=15)
        self.storeList.current(0)

        self.tree = ttk.Treeview(self, columns=('Day Spend', 'Store', 'Date'), show='headings', height=7)
        self.tree.bind("<Button-3>", self.popMenu)

        self.setResult()
        self.initGrid()
        self.showList()

    def initGrid(self):
        ttk.Label(self, textvariable=self.total, font=("Courier", 20)).grid(column=2 , row=0, padx=5, pady=5, columnspan=2)
        ttk.Label(self, textvariable=self.month, font=("Courier", 10)).grid(column=1, row=1, padx=5, pady=5)
        ttk.Label(self, textvariable=self.week, font=("Courier", 10)).grid(column=3, row=1, padx=5, pady=5)

        self.price.grid(column=1, row=2, padx=5, pady=5)
        self.storeList.grid(column=2, row=2, padx=5, pady=5,)

        self.tree.heading('Day Spend', text='Day Spend (£)')
        self.tree.column('Day Spend', width=100, anchor="center")
        self.tree.heading('Store', text='Store')
        self.tree.column('Store', width=100, anchor="center")
        self.tree.heading('Date', text='Date')
        self.tree.column('Date', width=150, anchor="center")
        self.tree.grid(column=0, row=3, padx=5, pady=5, columnspan=4, sticky='NSEW')

        ttk.Label(self, text="Total Usage: ", font=("Courier", 20)).grid(column=0, row=0, padx=5, pady=5, columnspan=2)
        ttk.Label(self, text="Monthly Usage: ", font=("Courier", 10)).grid(column=0, row=1, padx=5, pady=5, sticky="W")
        ttk.Label(self, text="Weekly Usage: ", font=("Courier", 10)).grid(column=2, row=1, padx=5, pady=5, sticky="W")
        ttk.Label(self, text="Today Spend: ", font=("Courier", 10)).grid(column=0, row=2, padx=5, pady=5, sticky="W")
        ttk.Button(self, text="Add", command=self.add).grid(column=3, row=2, padx=5, pady=5)
    
    def setResult(self):
        self.total.set(self.calTotal())
        self.month.set(self.calMonth())
        self.week.set(self.calWeek())

    def showList(self):
        self.tree.delete(*self.tree.get_children())
        for spend in self.db.show():
            self.tree.insert('', tk.END, values=spend)

    def add(self):
        try:
            spend = "{:.2f}".format(float(self.price.get()))
            self.db.add(spend, self.storeList.get(), date.today())
            self.showList()
            self.setResult()
        except ValueError:
           messagebox.showerror(title="Wrong Type", message="The entered value is null or wrong type.", parent=self)

    def calTotal(self):
        sum = 0
        for price in self.db.allSpend():
            sum += price[0]
        
        return "£" + str("{:.2f}".format(sum))
    
    def calMonth(self):
        total = float(self.calTotal()[1:])
        dates = self.db.diffDates()
        if dates[0] != None and dates[1] != None:
            start_date = datetime.datetime(int(dates[0][0][0:4]), int(dates[0][0][5:7]), int(dates[0][0][8:]))
            end_date = datetime.datetime(int(dates[1][0][0:4]), int(dates[1][0][5:7]), int(dates[1][0][8:]))
            num = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            if num == 0:
                return "£0"
            else:
                return "£" + str("{:.2f}".format(total/num))
        else:
            return "£0"

    def calWeek(self):
        total = float(self.calTotal()[1:])
        dates = self.db.diffDates()
        if dates[0] != None and dates[1] != None:
            start_date = datetime.datetime(int(dates[0][0][0:4]), int(dates[0][0][5:7]), int(dates[0][0][8:]))
            end_date = datetime.datetime(int(dates[1][0][0:4]), int(dates[1][0][5:7]), int(dates[1][0][8:]))
            num = abs(start_date - end_date).days // 7
            if num == 0:
                return "£0"
            else:
                return "£" + str("{:.2f}".format(total/num))
        else:
            return "£0"

    def editRow(self):
        selected = self.tree.item(self.tree.focus())['values']
        if selected:
            EditTree(self, self.ws, self.hs, selected)
        else:
            messagebox.showerror(title="Nothing Selected", message="Please select a row", parent=self)

    def deleteRow(self):
        selected = self.tree.item(self.tree.focus())['values']
        if selected:
            self.db.delete(selected[0], selected[1], selected[2])
            self.showList()
            self.setResult()
        else:
            messagebox.showerror(title="Nothing Selected", message="Please select a row", parent=self)

    def popMenu(self, event):
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label="Edit", command=self.editRow)
        menu.add_command(label="Delete", command=self.deleteRow)
        menu.tk_popup(event.x_root, event.y_root)

class EditTree(tk.Toplevel):
    def __init__(self, master, ws, hs, selected):
        tk.Toplevel.__init__(self)
        self.master = master
        self.iconbitmap('./shopping.ico')
        self.resizable(0, 0)
        self.title("Edit")
        self.selected = selected
        self.ws = ws
        self.hs = hs
        self.w = 220
        self.h = 120
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, (self.ws/2)-(self.w/2) , (self.hs/2)-(self.h/2)-50))
        self.daySpend = ttk.Entry(self, width=17)
        self.daySpend.insert(0, selected[0])
        self.store = ttk.Combobox(self, values=["LiDL", "Tesco", "Sainsbury's", "Co-op"], state="readonly", width=14)
        self.store.current(["LiDL", "Tesco", "Sainsbury's", "Co-op"].index(selected[1]))
        self.date = ttk.Entry(self, width=17)
        self.date.insert(0, selected[2])
        self.initGrid()
    
    def initGrid(self):
        ttk.Label(self, text="Day Spend: ", font=("Courier", 10)).grid(column=0, row=0, padx=5, pady=5, sticky="W")
        ttk.Label(self, text="Store: ", font=("Courier", 10)).grid(column=0, row=1, padx=5, pady=5, sticky="W")
        ttk.Label(self, text="Date: ", font=("Courier", 10)).grid(column=0, row=2, padx=5, pady=5, sticky="W")
        self.daySpend.grid(column=1, row=0, padx=5, pady=5)
        self.store.grid(column=1, row=1, padx=5, pady=5, sticky="W")
        self.date.grid(column=1, row=2, padx=5, pady=5)
        ttk.Button(self, text="Update", command=self.updateRow).grid(column=0, row=3, columnspan=2)

    def updateRow(self):
        try:
            spend = "{:.2f}".format(float(self.daySpend.get()))
            self.master.db.updateRow(float(self.selected[0]), self.selected[1], self.selected[2], spend, self.store.get(), self.date.get())
            self.master.showList()
            self.master.setResult()
            self.destroy()
        except ValueError:
           messagebox.showerror(title="Wrong Type", message="The entered value is null or wrong type.", parent=self)
        


def main():
    root = tk.Tk()
    MainScreen(root, root.winfo_screenwidth(), root.winfo_screenheight()).grid(column=0, row=0, sticky="NESW")
    root.mainloop()

if __name__ == '__main__':
    main()