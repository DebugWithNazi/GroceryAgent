from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
from agent import call_groq_agent
import products_dao
import order_dao
import uom_dao
import json
from flask_cors import CORS
from order_dao import delete_order

app = Flask(__name__)
CORS(app)
connection = get_sql_connection()

@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({'product_id':return_id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['Post'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({'product_id':product_id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['Post'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = order_dao.insert_order(connection, request_payload)
    response = jsonify({'order_id':order_id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = order_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteOrder', methods=['POST'])
def delete_order_endpoint():
    data = request.get_json()
    order_id = data.get('order_id')
    if not order_id:
        return jsonify({'error': 'order_id is required'}), 400
    try:
        delete_order(connection, int(order_id))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/agent", methods=["POST", "OPTIONS"])
def agent():
    if request.method == "OPTIONS":
        # CORS preflight
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    user_prompt = request.json.get("prompt")
    connection = get_sql_connection()
    agent_response = call_groq_agent(user_prompt, connection)
    response = jsonify({"response": agent_response})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("starting python flask server for grocery store management system")
    app.run(port=5000)
