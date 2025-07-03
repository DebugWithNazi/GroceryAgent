## GroceryGenie – Version 1.0

### **Description**
Version 1.0 is the initial release of **GroceryAgent**, a web-based Grocery Store Management System with an integrated AI agent assistant. This version provides the foundational features for managing products and orders, as well as a smart agent chat to help automate common tasks.

---

### **Features**
- **Product Management**
  - Add new products with name, unit of measure, and price per unit.
  - View a list of all products.
  - Delete products from the inventory.

- **Order Management**
  - Create new orders for customers.
  - Add multiple products to an order with quantity and price.
  - View all orders placed.

- **Agent Chat Assistant**
  - Floating chatbox UI for interacting with an AI agent.
  - Use natural language to add products, delete products, and manage orders (e.g., “add tomato in products in 50 per kg”).
  - Agent responses and actions are reflected in the main app.

- **User Interface**
  - Clean, responsive HTML/CSS/JS frontend for managing products, orders, and agent chat.
  - Bootstrap-based styling for a modern look.

- **Backend**
  - Python Flask backend with REST API endpoints for products, orders, and agent chat.
  - SQLite/MySQL database support for storing products and orders.

---

### **Tech Stack**
- **Frontend:** HTML, CSS (Bootstrap), JavaScript (jQuery)
- **Backend:** Python (Flask)
- **Database:** MySQL
- **AI Agent:** Integrated via backend and chatbox UI

---

### **How to Use**
1. Start the Flask backend server.
2. Open the frontend in your browser.
3. Add products and create orders using the web interface or the agent chatbox.

---

### **Limitations**
- No authentication or user roles.
- No persistent cloud database (unless configured).
- Agent actions are limited to basic product and order management.

---

### **Commit Message Example**
```
Initial release: GroceryAgent v1.0
- Product CRUD (add, view, delete)
- Order creation and listing
- Integrated agent chat assistant for natural language commands
- Basic HTML/CSS/JS frontend with floating chatbox
- Flask backend with REST API and agent endpoint
- MySQL database support
```

---


