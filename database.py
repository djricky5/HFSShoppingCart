import sqlite3
from contextlib import closing

conn = sqlite3.connect("shopcart.db")

def listAllProducts(sort = "name", method = "asc"):
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM products'''
        c.execute(query)
        results = c.fetchall()
        if sort == "price":
            if method == "dsc":
                results = sorted(results, key=lambda x: x[1], reverse=True)
            else:
                results = sorted(results, key=lambda x: x[1])
        else:
            if method == "dsc":
                results = sorted(results, reverse=True)
            else:
                results = sorted(results)
    return results


def getQty(name):
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM products WHERE name == ?'''
        c.execute(query, (name,))
        result = c.fetchone()
        if result == []:
            qty = -1
        else:
            qty = result[2]
    return qty


def subtractfromProds(name, qty):
    with closing(conn.cursor()) as c:
        sql = '''UPDATE products SET quantity = ? WHERE name == ?'''
        c.execute(sql, (qty, name))
        conn.commit()


def listSales():
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM products WHERE discount is 1'''
        c.execute(query)
        results = c.fetchall()
        results = sorted(results)
    return results


def userSearch(entry):
    entry = entry.upper()
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM products WHERE name == ?'''
        c.execute(query, (entry,))
        results = c.fetchall()
        results = sorted(results)
    return results


def listCart():
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM cart'''
        c.execute(query)
        results = c.fetchall()
        results = sorted(results)
    return results


def addtoCart(name, price, qty):
    with closing(conn.cursor()) as c:
        sql = '''INSERT INTO cart (prodName, prodPrice, orderQty) VALUES (?, ?, ?)'''
        c.execute(sql, (name, price, qty))
        conn.commit()


def editCart(name, qty):
    with closing(conn.cursor()) as c:
        sql = '''UPDATE cart SET orderQty = ? WHERE prodName = ?'''
        c.execute(sql, (qty, name))
        conn.commit()


def removeFromCart(name):
    with closing(conn.cursor()) as c:
        sql = '''DELETE FROM cart WHERE prodName = ?'''
        c.execute(sql, (name,))
        conn.commit()


def checkCart(name):
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM cart WHERE prodName == ?'''
        c.execute(query, (name,))
        result = c.fetchone()
        if result == None:
            qty = 0
        else:
            qty = result[2]
    return qty


def cartCount():
    count = 0
    results = listCart()
    for item in results:
        count += item[2]
    return count
