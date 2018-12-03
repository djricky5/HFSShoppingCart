import tkinter as tk
from tkinter import ttk
from tkinter import font as tkf
import business as bs
import database as db

# Page Updater
def Refresher():
    global cartButton, cart, bodyResults

    # Refresh Cart Button
    cart = bs.Cart()
    total = cart.getItemCount()
    if total > 0:
        cartval = "Cart (" + str(total) + ")"
    else:
        cartval = "Cart (Empty)"
    cartButton.configure(text=cartval)
    root.after(1000, Refresher)

def Toggler(display=1, search=""):
    global cartButton, cart, bodyResults
    # Refresh List Results & Toggle Between Product List, Cart, and Checkout Confirmation
    for widget in bodyResults.winfo_children():
        widget.destroy()
    if display == 2:
        displaySort(bodyResults,"name","dsc")
    elif display == 3:
        displaySort(bodyResults,"price","asc")
    elif display == 4:
        displaySort(bodyResults,"price","dsc")
    elif display == 5:
        searchResults(bodyResults, search)
    elif display == 6:
        DisplayCart()
    elif display == 7:
        Checkout(bodyResults)
    else:
        displaySort(bodyResults,"name","asc")



def header():
    # Header
    global cartButton, cart, bodyResults
    header = ttk.Frame(root, padding="10 10 10 0")
    header.pack(fill=tk.BOTH, expand=True)
    ttk.Label(header, text="Welcome to the Healthy Food "
                           "Store!                                                      ",
              font=("Comic Sans MS", 16)).pack(side=tk.LEFT)

    cart = bs.Cart()
    total = cart.getItemCount()
    if total > 0:
        cartval = "Cart (" + str(total) + ")"
    else:
        cartval = "Cart (Empty)"

    cartButton = ttk.Button(header, text=cartval, command=lambda: Toggler(6))
    cartButton.pack(side=tk.RIGHT)


def subheader():
    # Subheader
    global cartButton, cart, bodyResults
    subheader = ttk.Frame(root, padding="10 0 10 10")
    subheader.pack(fill=tk.BOTH, expand=True)
    ttk.Label(subheader, text="Please make your selections from "
                              "the items listed below:", font=("Helvetica", 12)).pack(side=tk.LEFT)


def body():
    global cartButton, cart, bodyResults
    # Body - Top
    # 1 = List All Items from A to Z
    # 2 = List All Items from Z to A
    # 3 = List All Items Price Low to High
    # 4 = List All Items Price High to Low
    # 5 = List All Items Matching Search Input
    # 6 = Display Cart
    # 7 = Checkout Confirmation
    bodyResults = ttk.Frame(root, padding="10 10 10 10")
    bodyResults.pack(fill=tk.BOTH, expand=True)

    # Body - Results
    Toggler()


def displaySort(bodyResults, Sort, Method):
    grabcart = bs.Cart
    body = ttk.Frame(bodyResults, padding="10 0 10 10")
    body.pack(fill=tk.BOTH, expand=True)
    keyword = ttk.Entry(body, width=25)
    keyword.pack(side=tk.LEFT)
    keysearch = ttk.Button(body, text="Search Products", command=lambda: Toggler(5, keyword.get()))
    keysearch.pack(side=tk.LEFT)
    lsort = ttk.Combobox(body, textvariable="", values=("Sort by Name A to Z", "Sort by Name Z to A",
                                                        "Sort by Price Low to High",
                                                        "Sort by Price High to Low"), state="readonly")
    lsort.pack(side=tk.RIGHT)
    lsort.bind("<<ComboboxSelected>>", lambda x: Toggler(lsort.current()+1))

    data = db.listAllProducts(sort=Sort, method=Method)
    fullList = []
    for product in data:
        item = bs.Product(product[0], product[1], product[2], product[3], product[4])
        fullList.append(item)
    i=-1
    name = [None] * len(fullList)
    amount = [None] * len(fullList)
    amountL = [None] * len(fullList)
    toCart = [None] * len(fullList)

    for item in fullList:
        i += 1
        name[i] = ttk.Frame(bodyResults, padding="10 0 10 0")
        name[i].pack(fill=tk.BOTH, expand=True)
        ttk.Label(name[i], text=item.name, font=("Helvetica", 12)).pack(side=tk.LEFT)
        amount[i] = ttk.Entry(name[i], width=2)
        amountL[i] = ttk.Label(name[i], text="Qty (Default 1):", font=("Helvetica", 12))
        if item.quantity == 0:
            ttk.Button(name[i], text="Add to Cart", state=tk.DISABLED).pack(side=tk.RIGHT)
        else:
            toCart[i] = ttk.Button(name[i], text="Add to Cart",
                                   command=lambda i=i: grabcart.AddItem(self="",name=fullList[i].name,
                                                                       price=fullList[i].finalprice,
                                                                       qty=amount[i].get()))
            toCart[i].pack(side=tk.RIGHT)
        amount[i].pack(side=tk.RIGHT)
        amountL[i].pack(side=tk.RIGHT)
        OGprice = ttk.Frame(bodyResults, padding="10 0 10 5")
        OGprice.pack(fill=tk.BOTH, expand=True)
        Cprice = ttk.Frame(bodyResults, padding="10 0 10 5")
        Cprice.pack(fill=tk.BOTH, expand=True)
        boldFont = tkf.Font(family="Helvetica", size=9, overstrike=1, weight="bold")
        if item.discount == 1:
            strikeFont = tkf.Font(family="Helvetica", size=7, overstrike=1, slant="italic")
            ttk.Label(OGprice, text="Regular Price: $" + str(item.originalprice), font=strikeFont).pack(side=tk.LEFT)
            ttk.Label(Cprice, text="Sale Price: $" + str(item.finalprice), font=boldFont).pack(side=tk.LEFT)
        else:
            ttk.Label(Cprice, text="Regular Price: $" + str(item.originalprice), font=boldFont).pack(side=tk.LEFT)
        stock = ttk.Frame(bodyResults, padding="10 0 10 5")
        stock.pack(fill=tk.BOTH, expand=True)
        strikeFont = tkf.Font(family="Helvetica", size=9, overstrike=1)
        ttk.Label(stock, text=item.stock, font=strikeFont).pack(side=tk.LEFT)


def searchResults(bodyResults, search):
    grabcart = bs.Cart
    body = ttk.Frame(bodyResults, padding="10 0 10 10")
    body.pack(fill=tk.BOTH, expand=True)
    keyword = ttk.Entry(body, width=25)
    keyword.pack(side=tk.LEFT)
    keysearch = ttk.Button(body, text="Search Products", command=lambda: Toggler(5, keyword.get()))
    keysearch.pack(side=tk.LEFT)
    lsort = ttk.Combobox(body, textvariable="", values=("Sort by Name A to Z", "Sort by Name Z to A",
                                                        "Sort by Price Low to High",
                                                        "Sort by Price High to Low"), state="readonly")
    lsort.pack(side=tk.RIGHT)
    lsort.bind("<<ComboboxSelected>>", lambda x: Toggler(lsort.current() + 1))

    data = db.userSearch(search)
    resultsList = []
    for product in data:
        item = bs.Product(product[0], product[1], product[2], product[3], product[4])
        resultsList.append(item)

    if len(resultsList) == 0:
        name = ttk.Frame(bodyResults, padding="10 0 10 0")
        name.pack(fill=tk.BOTH, expand=True)
        ttk.Label(name, text="No Product Matches Found.", font=("Helvetica", 12)).pack(side=tk.LEFT)
    else:
        i = -1
        name = [None] * len(resultsList)
        amount = [None] * len(resultsList)
        toCart = [None] * len(resultsList)
        amountL = [None] * len(resultsList)

        for item in resultsList:
            i += 1
            name[i] = ttk.Frame(bodyResults, padding="10 0 10 0")
            name[i].pack(fill=tk.BOTH, expand=True)
            ttk.Label(name[i], text=item.name, font=("Helvetica", 12)).pack(side=tk.LEFT)

            amount[i] = ttk.Entry(name[i], width=2)
            amountL[i] = ttk.Label(name[i], text="Qty (Default 1):", font=("Helvetica", 12))
            if item.quantity == 0:
                ttk.Button(name[i], text="Add to Cart", state=tk.DISABLED).pack(side=tk.RIGHT)
            else:
                toCart[i] = ttk.Button(name[i], text="Add to Cart",
                                       command=lambda i=i: grabcart.AddItem(self="", name=resultsList[i].name,
                                                                            price=resultsList[i].finalprice,
                                                                            qty=amount[i].get()))
                toCart[i].pack(side=tk.RIGHT)
            amount[i].pack(side=tk.RIGHT)
            amountL[i].pack(side=tk.RIGHT)
            OGprice = ttk.Frame(bodyResults, padding="10 0 10 5")
            OGprice.pack(fill=tk.BOTH, expand=True)
            Cprice = ttk.Frame(bodyResults, padding="10 0 10 5")
            Cprice.pack(fill=tk.BOTH, expand=True)
            boldFont = tkf.Font(family="Helvetica", size=9, overstrike=1, weight="bold")
            if item.discount == 1:
                strikeFont = tkf.Font(family="Helvetica", size=7, overstrike=1, slant="italic")
                ttk.Label(OGprice, text="Regular Price: $" + str(item.originalprice), font=strikeFont).pack(side=tk.LEFT)
                ttk.Label(Cprice, text="Sale Price: $" + str(item.finalprice), font=boldFont).pack(side=tk.LEFT)
            else:
                ttk.Label(Cprice, text="Regular Price: $" + str(item.originalprice), font=boldFont).pack(side=tk.LEFT)
            stock = ttk.Frame(bodyResults, padding="10 0 10 5")
            stock.pack(fill=tk.BOTH, expand=True)
            strikeFont = tkf.Font(family="Helvetica", size=9, overstrike=1)
            ttk.Label(stock, text=item.stock, font=strikeFont).pack(side=tk.LEFT)

def cartUp(cartList, Name, Price, Qty):
    cartList.AddItem(name=Name, price=Price, qty=Qty)
    Toggler(6)

def cartDown(cartList, Name, Qty):
    cartList.RemoveItem(name=Name, qty=Qty)
    Toggler(6)

def DisplayCart():
    body = ttk.Frame(bodyResults, padding="10 0 10 10")
    body.pack(fill=tk.BOTH, expand=True)
    ttk.Label(body, text="View the items in your cart below:", font=("Helvetica", 12)).pack(side=tk.LEFT)
    ttk.Button(body, text="Back to Product List", command=Toggler).pack(side=tk.RIGHT)

    cartList = bs.Cart()
    if len(cartList.lineItems) == 0:
        name = ttk.Frame(bodyResults, padding="10 0 10 0")
        name.pack(fill=tk.BOTH, expand=True)
        ttk.Label(name, text="Your cart is empty.", font=("Helvetica", 12)).pack(side=tk.LEFT)
    else:
        i = -1
        Name = [None] * len(cartList.lineItems)
        qty = [None] * len(cartList.lineItems)
        price = [None] * len(cartList.lineItems)
        Price = [None] * len(cartList.lineItems)
        increase = [None] * len(cartList.lineItems)
        increaseQty = [None] * len(cartList.lineItems)
        decrease = [None] * len(cartList.lineItems)
        decreaseQty = [None] * len(cartList.lineItems)

        for item in cartList:
            i += 1
            # Name
            Name[i] = ttk.Frame(bodyResults, padding="10 0 10 0")
            Name[i].pack(fill=tk.BOTH, expand=True)
            ttk.Label(Name[i], text=item.name, font=("Helvetica", 14)).pack(side=tk.LEFT)

            # Increase
            increaseQty[i] = ttk.Entry(Name[i], width=2)
            increase[i] = ttk.Button(Name[i], text="Increase Qty",
                                     command=lambda i=i: cartUp(cartList, cartList.lineItems[i].name,
                                                                cartList.lineItems[i].price,
                                                                increaseQty[i].get()))
            increase[i].pack(side=tk.RIGHT)
            increaseQty[i].pack(side=tk.RIGHT)

            # Price
            price[i] = ttk.Frame(bodyResults, padding="10 0 10 5")
            price[i].pack(fill=tk.BOTH, expand=True)
            Price[i] = ttk.Label(price[i], font=("Helvetica", 12), text="Price: $" + str(item.price))
            Price[i].pack(side=tk.LEFT)

            # Decrease
            decreaseQty[i] = ttk.Entry(price[i], width=2)
            decrease[i] = ttk.Button(price[i], text="Decrease Qty",
                                     command=lambda i=i: cartDown(cartList, cartList.lineItems[i].name,
                                                                decreaseQty[i].get()))
            decrease[i].pack(side=tk.RIGHT)
            decreaseQty[i].pack(side=tk.RIGHT)

            # Quantity
            qty[i] = ttk.Frame(bodyResults, padding="10 0 10 5")
            qty[i].pack(fill=tk.BOTH, expand=True)
            ttk.Label(qty[i], font=("Helvetica", 12), text="Qty: " + str(item.orderQty)).pack(side=tk.LEFT)

    totals = cartList.getTotal()
    subtotal = ttk.Frame(bodyResults, padding="10 0 10 10")
    subtotal.pack(fill=tk.BOTH, expand=True)
    ttk.Label(subtotal, text=("Subtotal: $"+"{:.2f}".format(totals[0])), font=("Helvetica", 12)).pack(side=tk.RIGHT)
    tax = ttk.Frame(bodyResults, padding="10 0 10 10")
    tax.pack(fill=tk.BOTH, expand=True)
    ttk.Label(tax, text=("Tax: $"+"{:.2f}".format(totals[1])), font=("Helvetica", 12)).pack(side=tk.RIGHT)
    total = ttk.Frame(bodyResults, padding="10 0 10 10")
    total.pack(fill=tk.BOTH, expand=True)
    ttk.Label(total, text=("Total: $"+"{:.2f}".format(totals[2])), font=("Helvetica", 12)).pack(side=tk.RIGHT)
    checkout = ttk.Frame(bodyResults, padding="10 0 10 10")
    checkout.pack(fill=tk.BOTH, expand=True)
    ttk.Button(checkout, text="Checkout", command=lambda: Toggler(7)).pack(side=tk.RIGHT)


def Checkout(bodyResults):
    cartList = bs.Cart()
    i = len(cartList.lineItems)
    while 0 < len(cartList.lineItems):
        bs.decrementProd(cartList.lineItems[0].name, cartList.lineItems[0].orderQty)
        cartList.removeItem(cartList.lineItems[0].name, cartList.lineItems[0].orderQty)

    body = ttk.Frame(bodyResults, padding="10 0 10 10")
    body.pack(fill=tk.BOTH, expand=True)
    if i == 0:
        ttk.Label(body, text="Your cart was empty, so no order has been placed."
                             "Try adding some items to your cart!", font=("Helvetica", 20)).pack()
        ttk.Button(body, text="Back to Product List", command=Toggler).pack()
    else:
        ttk.Label(body, text="Thank You! Your order has been placed!", font=("Helvetica", 20)).pack()

def footer():
    # Footer
    footer = ttk.Frame(root, padding="10 10 10 10")
    footer.pack(fill=tk.BOTH, expand=True)
    ttk.Label(footer, text="Thanks for shopping with us!", font=("Comic Sans MS", 12)).pack(
        side=tk.LEFT)
    ttk.Button(footer, text="Exit Store", command=root.destroy).pack(
        side=tk.RIGHT)


if __name__ == "__main__":
    global cartButton, cart, bodyResults

    # Create Window & Title
    root = tk.Tk()
    root.title("The Healthy Food Shopping Cart App")

    # Display Window Components
    header()
    subheader()
    body()
    footer()

    Refresher()         # Refresh window display based on toggle inputs
    root.mainloop()     # Loop
