import json
import re
from groq import Groq
from datetime import datetime

from products_dao import insert_new_product, delete_product, get_product_id_by_name
from order_dao import insert_order, get_all_orders, delete_order
from uom_dao import get_uoms

client = Groq(api_key="") # Add your own groq key

def call_groq_agent(prompt, connection):
    try:
        print(f"[Agent] Received prompt: {prompt}")
        system_prompt = (
            "You are an assistant to a grocery store manager. "
            "You receive prompts and must return a JSON command. "
            "Valid actions are: 'add_product', 'delete_product', 'add_order', 'view_orders', 'delete_order'.\n"
            "For 'add_product': return {action, product_name, price_per_unit, uom_name}\n"
            "For 'delete_product': return {action, product_id}\n"
            "For 'add_order': return {action, customer_name, items: [{product_id, quantity}]}\n"
            "For 'view_orders': return {action}\n"
            "For 'delete_order': return {action, order_id}\n"
            "Output only the JSON. No explanation.\n"
            "You must be able to handle commands like 'add tomato in products in 50 per kg', 'add sugar at 110 rupees per kg', 'add product rice, price 80, uom kg', etc. "
            "If you are unsure, try to infer the intent and fill the JSON as best as possible."
        )

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        ai_output = response.choices[0].message.content.strip()
        print(f"[Agent] AI raw output: {ai_output}")

        match = re.search(r'\{.*\}', ai_output, re.DOTALL)
        if not match:
            print("[Agent] Failed to extract valid JSON command from AI response.")
            return "❌ Failed to extract valid JSON command from AI response."

        command = json.loads(match.group(0))
        action = command.get("action")
        print(f"[Agent] Parsed command: {command}")

        if action == "add_product":
            uoms = get_uoms(connection)
            uom_id = next((u['uom_id'] for u in uoms if u['uom_name'].lower() == command['uom_name'].lower()), None)
            if uom_id is None:
                print(f"[Agent] Invalid UOM: {command['uom_name']}")
                return f"❌ Invalid UOM: {command['uom_name']}"

            product = {
                'product_name': command['product_name'],
                'uom_id': uom_id,
                'price_per_unit': float(command['price_per_unit']),
            }
            insert_new_product(connection, product)
            print(f"[Agent] Product added: {product}")
            return f"✅ Product '{product['product_name']}' added successfully."

        elif action == "delete_product":
            product_id = command.get('product_id')
            try:
                product_id_int = int(product_id)
            except (ValueError, TypeError):
                # Try to look up by name
                product_id_int = get_product_id_by_name(connection, str(product_id))
                if product_id_int is None:
                    print(f"[Agent] Product not found: {product_id}")
                    return f"❌ Product '{product_id}' not found."
            try:
                delete_product(connection, product_id_int)
                print(f"[Agent] Product deleted: {product_id_int}")
                return f"🗑️ Product with ID {product_id_int} deleted."
            except Exception as e:
                if 'foreign key constraint fails' in str(e).lower():
                    # Look up product name for a friendlier message
                    cursor = connection.cursor()
                    cursor.execute("SELECT name FROM grocerystoreschema.products WHERE product_id = %s", (product_id_int,))
                    result = cursor.fetchone()
                    product_name = result[0] if result else f"ID {product_id_int}"
                    return f"❌ Cannot delete '{product_name}' because it is used in existing orders."
                return f"❌ Error occurred: {str(e)}"

        elif action == "add_order":
            grand_total = 0
            order_details = []
            for item in command["items"]:
                qty = int(item["quantity"])
                product_id = int(item["product_id"])
                total = qty * 0  # Optionally fetch price per unit
                order_details.append({
                    "product_id": product_id,
                    "quantity": qty,
                    "total": total
                })
                grand_total += total

            order_data = {
                "customer_name": command["customer_name"],
                "grand_total": grand_total,
                "order_details": order_details
            }

            insert_order(connection, order_data)
            print(f"[Agent] Order added: {order_data}")
            return f"🛒 Order for {command['customer_name']} added."

        elif action == "view_orders":
            orders = get_all_orders(connection)
            print(f"[Agent] Orders viewed.")
            return json.dumps(orders, indent=2, default=str)

        elif action == "delete_order":
            order_id = command.get('order_id')
            try:
                order_id_int = int(order_id)
                delete_order(connection, order_id_int)
                return f"🗑️ Order with ID {order_id_int} deleted."
            except Exception as e:
                return f"❌ Error occurred: {str(e)}"

        else:
            print(f"[Agent] Unknown action in command: {action}")
            return "❌ Unknown action in command."

    except Exception as e:
        import traceback
        print(f"[Agent] Error occurred: {str(e)}\n{traceback.format_exc()}")
        return f"❌ Error occurred: {str(e)}"
