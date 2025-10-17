from abc import ABC, abstractmethod
from flask import Flask, render_template, request
import json
import pandas as pd

app = Flask(__name__)

pivoted_items = {
    'mining': {
        'coal': {'points': 1},
        'salt': {'points': 1},
        'stone': {'points': 1},
        'iron': {'points': 2},
        'quartz': {'points': 2},
        'copper': {'points': 2},
        'marble': {'points': 2},
        'mercury': {'points': 3},
        'sulfur': {'points': 3},
        'silver': {'points': 3},
        'manganese': {'points': 3},
        'obsidian': {'points': 4},
        'gold': {'points': 4},
        'soul gem': {'points': 4},
        'spell crystal': {'points': 4}
    },
    'hunting': {
        'bone': {'points': 1},
        'feathers': {'points': 1},
        'honey': {'points': 1, 'expiration': '1 month'},
        'food': {'points': 1, 'expiration': '1 month'},
        'soft pelt': {'points': 2},
        'demon blood': {'points': 2},
        'large hide': {'points': 3},
        'celestial blood': {'points': 3},
        'fae blood': {'points': 4}
    },
    'mercantile': {
        'cloth': {'points': 1},
        '5 postage (domestic)': {'points': 1},
        'paper': {'points': 1},
        'glass': {'points': 2},
        'blood ink': {'points': 2},
        '5 postage (overseas)': {'points': 2},
        'sanctified water': {'points': 3},
        'ritual component': {'points': 4}
    },
    'black_market': {
        'zye scarab': {'points': 3},
        'zye blood parasites': {'points': 4}
    }
}

item_lookup = {item: {**data, 'cat': cat} for cat, items in pivoted_items.items() for item, data in items.items()}

class Display(ABC):  # all classes used to pass info into the HTML must inherit this 
    @abstractmethod
    def format(self):  # used whenever a class will be passing details into HTML
        pass

class Item:
    def __init__(self, item, quantity):
        dic_ref = item_lookup[item]
        item_cost = dic_ref['points']
        if item_cost > 1:
            item_cost *= 1.5
        self.item = item
        self.quantity = quantity
        self.cost = item_cost * quantity
        self.cat = dic_ref['cat']

class Order(Display):
    def __init__(self, order):
        self.order_cost = 0
        self.items = []  # store items for formatting
        for item, quantity in order.items():
            pull = Item(item, quantity)
            self.items.append(pull)
            self.order_cost += pull.cost

    def format(self):
        output = ''
        for item in self.items:
            readout = f'{item.quantity} {item.item} ({item.cost} silver)<br>'
            output += readout
        summary = f'<strong>Total Cost: {self.order_cost}</strong>'
        output += summary
        return output

    def to_dict(self):
        """Serialize the order for JSON"""
        return {
            "order_cost": self.order_cost,
            "items": [{"item": i.item, "quantity": i.quantity} for i in self.items]
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=["GET", "POST"])
def order():
    if request.method == "POST":
        submitted = {}
        for cat, items_in_cat in pivoted_items.items():
            for item in items_in_cat:
                checkbox_name = f"chk_{item}"
                qty_name = f"qty_{item}"
                if checkbox_name in request.form:
                    submitted[item] = int(request.form.get(qty_name, 1))

        order_details = Order(submitted)
        return render_template('confirmation.html', order_details=order_details)

    return render_template('order.html', items=pivoted_items)

@app.route('/order_confirmation', methods=["POST"])
def process_confirmation():
    order_json = request.form['order_json']
    print("Confirmation button clicked!")
    print("Order JSON received:", order_json)
    return render_template("index.html", message="Action completed!")

if __name__ == "__main__":
    app.run(debug=True)
