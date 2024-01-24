from app import *


@app.route('/category')
def categoryIndex():  # put application's code here
    return render_template('admin/category/index.html')


@app.route('/get_all_category')
def getAllCategory():
    category = connection.execute(text("""SELECT * FROM category """))
    connection.commit()
    category_arr = []
    for item_cat in category:
        category_arr.append(
            {
                'id': item_cat.id,
                'name': item_cat.name,
                'description': item_cat.description
            }
        )
    return category_arr
