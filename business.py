import database as db
from tkinter import messagebox

class Product:
    def __init__(self, name="", price=0.0, quantity=0, discount=0, percentoff=0):
        self.name = name
        self.originalprice = price
        self.quantity = quantity
        self.discount = discount
        self.percentoff = percentoff
        self.finalprice = round(price*(1-percentoff), 2)
        if quantity == 0:
            self.stock = "Sold Out."
        elif quantity < 10:
            self.stock = "Almost Gone!"
        else:
            self.stock = "In Stock."


class LineItem:
    def __init__(self, name=None, price=0, qty=0):
        self.name = name
        self.price = price
        self.orderQty = qty


class Cart:
    def __init__(self):
        self.lineItems = []
        data = db.listCart()
        for product in data:
            item = LineItem(product[0], product[1], product[2])
            self.lineItems.append(item)

    def check(self, name):
        inList = -1
        i = -1
        for lineItem in self.lineItems:
            i += 1
            if name == lineItem.name:
                inList = i
        return inList

    def AddItem(self, name, price, qty=1):
        if qty == "":
            qty = 1
        else:
            qty = int(qty)
        indb = db.getQty(name)
        if indb<0:
            messagebox.showinfo("Cart Message", "Item not found")
        elif indb == 0:
            messagebox.showinfo("Cart Message", "Item is out of stock")
        elif int(indb) < int(qty):
            messagebox.showinfo("Cart Message", "There are only "+str(indb)+" items left.")
        else:
            inCart = db.checkCart(name)
            if inCart > 0:
                db.editCart(name, inCart+qty)
            else:
                db.addtoCart(name, price, qty)
            messagebox.showinfo("Cart Message", "Added to cart")

    def RemoveItem(self, name, qty=1):
        inCart = int(db.checkCart(name))
        if qty == "":
            qty = 1
        else:
            qty = int(qty)
        if inCart > qty:
            db.editCart(name, inCart - qty)
        else:
            db.removeFromCart(name)
        messagebox.showinfo("Cart Message", "Removed from cart")


    def removeItem(self, name, qty=1):
        inList = self.check(name)
        if self.lineItems[inList].orderQty <= qty:
            self.lineItems.pop(inList)
            db.removeFromCart(name)
        else:
            newQty = self.lineItems[inList].orderQty - qty
            self.lineItems[inList].removefromOrder(qty)
            db.editCart(name, newQty)


    def getTotal(self):
        subtotal = 0.00
        for item in self.lineItems:
            subtotal += round(item.price*item.orderQty, 2)
        tax = round(subtotal*0.07, 2)
        total = round(tax + subtotal, 2)
        totals = [subtotal, tax, total]
        return totals

    def getItemCount(self):
        return db.cartCount()

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index == len(self.lineItems)-1:
            raise StopIteration
        self.__index += 1
        lineItem = self.lineItems[self.__index]
        return lineItem


def decrementProd(name, Qty):
    qty = db.getQty(name)
    if qty > 0:
        qty -= Qty
        db.subtractfromProds(name, qty)
