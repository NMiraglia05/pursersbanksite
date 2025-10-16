from flask import Flask, render_template, request  # <- add request

app = Flask(__name__)

def categorize_items(items):
    # Minimal placeholder, just returns empty dict for now
    return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    categories = categorize_items(item_lookup)
    if request.method == 'POST':
        order_data = request.form.to_dict()
        print("Received order:", order_data)
        return "Order submitted (not functional yet)"
    return render_template('order.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
