from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

item_lookup={
    'coal':{'points':1,'cat':'mining'},
    'salt':{'points':1,'cat':'mining'},
    'stone':{'points':1,'cat':'mining'},
    'iron':{'points':2,'cat':'mining'},
    'quartz':{'points':2,'cat':'mining'},
    'copper':{'points':2,'cat':'mining'},
    'marble':{'points':2,'cat':'mining'},
    'mercury':{'points':3,'cat':'mining'},
    'sulfur':{'points':3,'cat':'mining'},
    'silver':{'points':3,'cat':'mining'},
    'manganese':{'points':3,'cat':'mining'},
    'obsidian':{'points':4,'cat':'mining'},
    'gold':{'points':4,'cat':'mining'},
    'soul gem':{'points':4,'cat':'mining'},
    'spell crystal':{'points':4,'cat':'mining'},
    'bone':{'points':1,'cat':'hunting'},
    'feathers':{'points':1,'cat':'hunting'},
    'honey':{'points':1,'cat':'hunting','expiration':'1 month'},
    'food':{'points':1,'cat':'hunting','expiration':'1 month'},
    'soft pelt':{'points':2,'cat':'hunting'},
    'demon blood':{'points':2,'cat':'hunting'},
    'large hide':{'points':3,'cat':'hunting'},
    'celestial blood':{'points':3,'cat':'hunting'},
    'fae blood':{'points':4,'cat':'hunting'},
    'cloth':{'points':1,'cat':'mercantile'},
    '5 postage (domestic)':{'points':1,'cat':'mercantile'},
    'paper':{'points':1,'cat':'mercantile'},
    'glass':{'points':2,'cat':'mercantile'},
    'blood ink':{'points':2,'cat':'mercantile'},
    '5 postage (overseas)':{'points':2,'cat':'mercantile'},
    'sanctified water':{'points':3,'cat':'mercantile'},
    'ritual component':{'points':4,'cat':'mercantile'},
    'zye scarab':{'points':3,'cat':'black_market'},
    'zye blood parasites':{'points':4,'cat':'black_market'}
}

def categorize_items(items):
    categories={}
    for name,data in items.items():
        cat=data['cat']
        if cat not in categories:
            categories[cat]=[]
        categories[cat].append({'name':name,'points':data['points']})
    # Sort each category by point value
    for cat in categories:
        categories[cat].sort(key=lambda x:x['points'])
    return categories

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order',methods=['GET','POST'])
def order():
    categories=categorize_items(item_lookup)
    if request.method=='POST':
        order_data={}
        for key,value in request.form.items():
            if key.endswith('_qty') and value!='0':
                item=key[:-4]
                order_data[item]=int(value)
        return render_template('confirm.html',order_data=order_data,item_lookup=item_lookup)
    return render_template('order.html',categories=categories)

@app.route('/confirm_order',methods=['POST'])
def confirm_order():
    # In a real app, you'd process the order here (save/email/etc)
    return "Order confirmed! (functionality coming soon)"

if __name__=='__main__':
    app.run(debug=True)
