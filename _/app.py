from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'store-1',
        'items': [
            {
                'name': 'first-item',
                'price': 15.99
            }
        ]
    }
]


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'not found'})


@app.route('/store')
def get_stores():
    return jsonify({'result': stores})


@app.route('/store/<string:name>/item')
def create_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'not found'})


@app.route('/store/<string:name>/item', methods=['POST'])
def get_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_items = {
                'name': request_data['name'],
                'price': request_data['price']
            }

            store['items'].append(new_items)
            return jsonify(new_items)
    return jsonify({'message': 'store not found'})


app.run(port=5000, debug=True)
