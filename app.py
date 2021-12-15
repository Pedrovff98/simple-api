from flasgger import swag_from, Swagger
from flask import Flask, jsonify, request
from marshmallow.exceptions import ValidationError
from mongoengine import connect
from models import Product, Category
from schemas import ProductSchema, ProductCreateSchema, ErrorSchema,\
                    ErrorEntitySchema, CategorySchema, CategoryEditSchema

app = Flask(__name__)
swagger = Swagger(app)
app.config['JSON_SORT_KEYS'] = False

# products = [{'id': uuid.uuid4().hex, 'name': 'First Product', 'price': 81.54}]

connect(

    db='ecommerce',
    username='db_username',
    password='db_password',
    host='127.0.0.1',
    port=27017,
    authentication_source='admin'
)


@app.route('/category', methods=['POST'])
def categoryPost():

    try:

        data = CategorySchema().load(request.json)
        obj1 = Category(**data)
        obj1.save()
        data = dict(CategorySchema().dump(obj1))

        return jsonify({"data": data}), 200

    except ValidationError as e:

        errors = {'message': 'Unprocessable Entity', 'errors': e.messages}

        return jsonify(errors), 422


@app.route('/category', methods=['GET'])
def categoryGet():
    obj1 = Category.objects
    data = CategorySchema().dump(obj1, many=True)

    return jsonify({"data": data}), 200


@app.route('/category/<string:prod_id>', methods=['PATCH'])
def categoryPatch(prod_id):

    try:
        obj1 = category.objects.get(pk=prod_id)
        data = CategoryEditSchema().load(request.json)
        obj1.update(**data)

        return jsonify({"data": data}), 200

    except ValidationError as e:
        errors = {'message': 'Unprocessable Entity', 'errors': e.messages}

        return jsonify(errors), 422


@app.route('/category/<string:category_id>', methods=['DELETE'])
def category(category_id):
    try:

        obj1 = Category.objects.get(pk=category_id)
        Category.delete(obj1)
        return '', 204

    except Exception:
        return 'Register Not Found', 404


########################################################################################################################

@app.route('/products', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'responses': {
        200: {
            'schema': ProductSchema
        }
    }
})
def listing():
    """
    Listing
    """
    obj1 = Product.objects
    data = ProductSchema().dump(obj1, many=True)

    return jsonify({'data': data}), 200


@app.route('/products', methods=['POST'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': ProductSchema
    }],
    'responses': {
        201: {
            'schema': ProductSchema
        },
        422: {
            'description': 'message: Register Not Found',
            'schema': ErrorEntitySchema
        }

    }
})
def create():
    """
    create
    """
    try:

        data = ProductCreateSchema().load(request.json)

        cat = Category.objects.get(pk=data['category'])  # Valida o id
        print(cat)  # receive the object

        obj1 = Product(name=data['name'], price=data['price'], category=cat)
        obj1.save()

        data = ProductSchema().dump(obj1)

        return jsonify({'data': data}), 201

    except ValidationError as e:
        errors = {'message': 'Unprocessable Entity', 'errors': e.messages}

        return jsonify(errors), 422

    except Exception:
        return 'Register Not Found', 404


@app.route('/products/<string:prod_id>', methods=['PATCH'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': ProductSchema
    }],
    'responses': {
        200: {
            'schema': ProductSchema
        },
        404: {
            'description': 'message: Register Not Found',
            'schema': ErrorSchema
        },
        422: {
            'description': 'Unprocessable Entity',
            'schema': ErrorEntitySchema
        }
    }
})
def edit(prod_id):
    """
    edit
    """
    try:
        obj1 = Product.objects.get(pk=prod_id)
        data = ProductSchema().load(request.json)
        obj1.update(**data)

        return jsonify({'data': data}), 200

    except ValidationError as e:
        errors = {'message': 'Unprocessable Entity', 'errors': e.messages}

        return jsonify(errors), 422

    except Exception:

        return 'Register Not Found', 404


@app.route('/products/<string:prod_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': ProductSchema
    }],
    'responses': {
        204: {

        },
        404: {
            'message': 'Register Not Found',
            'schema': ErrorSchema
        }
    }
})
def delete(prod_id):
    try:
        obj1 = Product.objects.get(pk=prod_id)
        Product.delete(obj1)

        return '', 204

    except Exception:

        return 'Register Not Found', 404
