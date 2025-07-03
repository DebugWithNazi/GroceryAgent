from sql_connection import get_sql_connection

def get_all_products(cnx):

    cursor = cnx.cursor()
    query = ("SELECT products.product_id,products.name,products.price_per_unit,uom.uom_name "
    "FROM grocerystoreschema.products inner join grocerystoreschema.uom on products.uom_id = uom.uom_id")

    cursor.execute(query)
    response = []
    for (product_id, name, price_per_unit,uom_name) in cursor:
        response.append({
            "product_id": product_id,
            "name": name,
            "price_per_unit": price_per_unit,
            "uom_name": uom_name
        })
    return response

def insert_new_product(cnx, product):
    cursor = cnx.cursor()
    query = ("insert into grocerystoreschema.products (name, uom_id, price_per_unit) values "
             "(%s, %s,%s)")
    data = (product["product_name"], product["uom_id"], product["price_per_unit"])
    cursor.execute(query, data)
    cnx.commit()
    return cursor.lastrowid

def delete_product(cnx, product_id):
    cursor = cnx.cursor()
    query = ("delete from grocerystoreschema.products where product_id=" + str(product_id))
    cursor.execute(query)
    cnx.commit()

def get_product_id_by_name(cnx, product_name):
    cursor = cnx.cursor()
    query = ("SELECT product_id FROM grocerystoreschema.products WHERE name = %s")
    cursor.execute(query, (product_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

if __name__ == '__main__':
    connection = get_sql_connection()
    # print(get_all_products(connection))
    # print(insert_new_product(connection,{
    #     "name": "cabbage",
    #     "uom_id": 1,
    #     "price_per_unit": 100
    # }))
    print(delete_product(connection,3))