from flask import Flask, render_template, request

app = Flask(__name__)

items=[
    {"name":"Burger","price":8},
    {"name":"Fries","price":4},
    {"name":"Soda","price":3},
    {"name":"Salad","price":7},
]

@app.route("/")
def home():
    return render_template("order.html", items=items)

@app.route("/order", methods=["POST"])
def order():
    order_data={}
    for key,value in request.form.items():
        if key.startswith("qty_"):
            item_name=key.replace("qty_","")
            try:
                qty=int(value)
                if qty>0:
                    order_data[item_name]=qty
            except ValueError:
                continue
    return render_template("confirm.html", order_data=order_data, items=items)

if __name__=="__main__":
    app.run(debug=True)
