from sql_connection import get_sql_connection
from datetime import datetime

def insert_order(connection, order):
     cursor = connection.cursor()
     order_query = ("insert into orders (customer_name, total, datetime)"
                    "values (%s, %s, %s)")
     order_data = (order['customer_name'], order['grand_total'], datetime.now())
     cursor.execute(order_query, order_data)
     order_id = cursor.lastrowid

     order_details_query=("insert into order_details (order_id,product_id,quantity,total) "
                         "values (%s, %s, %s, %s)")
     order_details_data = []
     for order_detail_record in order['order_details']:
         order_details_data.append([
             order_id,
             int(order_detail_record['product_id']),
             float(order_detail_record['quantity']),
             float(order_detail_record['total']),
         ])

     cursor.executemany(order_details_query,order_details_data)
     connection.commit()
     return order_id

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("select * from orders")
    cursor.execute(query)
    response = []
    for (order_id, customer_name, total, datetime) in cursor:
        response.append({
          'order_id': order_id,
          'customer_name': customer_name,
          'total': total,
          'datetime': datetime,
        })
    return response

def delete_order(connection, order_id):
    cursor = connection.cursor()
    # First delete order details
    cursor.execute("DELETE FROM grocerystoreschema.order_details WHERE order_id = %s", (order_id,))
    # Then delete the order itself
    cursor.execute("DELETE FROM grocerystoreschema.orders WHERE order_id = %s", (order_id,))
    connection.commit()

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
    # print(insert_order(connection,{
    #      'customer_name':'Hulk',
    #      'grand_total' : '500',
    #      'order_details':[{
    #          'order_id':1,
    #          'product_id' : '1',
    #          'quantity' : 1,
    #          'total':50
    #      },
    #          {
    #              'order_id':3,
    #              'product_id': '2',
    #              'quantity': 1,
    #              'total': 40
    #          },
    #      ]
    #
    # }))
