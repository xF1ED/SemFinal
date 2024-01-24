from app import *


@app.route('/product')
def productIndex():  # put application's code here
    return render_template('admin/product/index.html', modul='product')


@app.route('/api/get_all_product')
def getAllProduct():
    category = connection.execute(text("""SELECT * FROM category """))

    result = connection.execute(text(
        """
        SELECT 
            product.*,
            category.name as 'category'
        FROM product 
        join category on product.category_id = category.id
        """
    ))
    connection.commit()
    product_arr = []
    for item in result:
        product_arr.append(
            {
                'id': item.id,
                'name': item.name,
                'category_id': item.category_id,
                'image': item.image,
                'cost': item.cost,
                'price': item.price,
                'category': item.category,
            }
        )
    category_arr = []
    for item_cat in category:
        category_arr.append(
            {
                'id': item_cat.id,
                'name': item_cat.name,
            }
        )
    data = {
        'product': product_arr,
        'category': category_arr
    }
    return data


@app.route('/api/add_product', methods=['POST'])
def addProduct():
    if request.method == 'POST':
        try:
            # Get form data using request.form
            product_name = request.form.get('product_name')
            category_id = request.form.get('category_id')
            cost = request.form.get('product_cost')
            price = request.form.get('product_price')

            # Set a default image filename
            default_image_filename = 'image.png'

            # Insert the new product into the database
            connection.execute(
                text("""
                    INSERT INTO product (name, category_id, image, cost, price)
                    VALUES (:product_name, :category_id, :image, :cost, :price)
                """),
                {
                    "product_name": product_name,
                    "category_id": category_id,
                    "image": 'image.png',
                    "cost": cost,
                    "price": price,
                }
            )
            connection.commit()

            return jsonify({"message": "Product added successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route('/api/delete_product/<int:product_id>', methods=['DELETE'])
def deleteProduct(product_id):
    if request.method == 'DELETE':
        try:
            # Check if the product exists
            product = connection.execute(
                text("""
                    SELECT * FROM product WHERE id = :product_id
                """).bindparams(product_id=product_id)
            ).fetchone()

            if not product:
                return jsonify({"error": "Product not found"}), 404

            # Delete the product from the database
            connection.execute(
                text("""
                    DELETE FROM product WHERE id = :product_id
                """).bindparams(product_id=product_id)
            )
            connection.commit()

            return jsonify({"message": "Product deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route('/api/update_product/<int:product_id>', methods=['PUT'])
def updateProduct(product_id):
    try:
        # Check if the product exists
        product = connection.execute(
            text("""
                SELECT * FROM product WHERE id = :product_id
            """).bindparams(product_id=product_id)
        ).fetchone()

        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Get updated data from the request
        product_name = request.form.get('edit_product_name')
        category_id = request.form.get('edit_category_id')
        cost = request.form.get('edit_product_cost')
        price = request.form.get('edit_product_price')

        # Update the product in the database
        connection.execute(
            text("""
                UPDATE product
                SET name = :product_name,
                    category_id = :category_id,
                    cost = :cost,
                    price = :price
                WHERE id = :product_id
            """).bindparams(
                product_id=product_id,
                product_name=product_name,
                category_id=category_id,
                cost=cost,
                price=price,
            )
        )
        connection.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
