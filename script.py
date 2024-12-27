from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_management.db'
db = SQLAlchemy(app)


# Models
class ServiceCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)


class MaintenanceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    service_center_id = db.Column(db.Integer, db.ForeignKey('service_center.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)


# Routes
@app.route('/service-centers', methods=['GET', 'POST'])
def manage_service_centers():
    if request.method == 'POST':
        data = request.get_json()
        if not data.get('name') or not data.get('city') or not data.get('capacity'):
            return jsonify({'error': 'Invalid input'}), 400

        new_service_center = ServiceCenter(
            name=data['name'],
            city=data['city'],
            capacity=data['capacity']
        )
        db.session.add(new_service_center)
        db.session.commit()
        return jsonify({'message': 'Service center created', 'id': new_service_center.id}), 200

    city_filter = request.args.get('city')
    query = ServiceCenter.query
    if city_filter:
        query = query.filter_by(city=city_filter)

    service_centers = query.all()
    return jsonify([
        {'id': sc.id, 'name': sc.name, 'city': sc.city, 'capacity': sc.capacity} for sc in service_centers
    ]), 200


@app.route('/service-centers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_service_center_by_id(id):
    service_center = ServiceCenter.query.get(id)
    if not service_center:
        return jsonify({'error': 'Service center not found'}), 404

    if request.method == 'GET':
        return jsonify({'id': service_center.id, 'name': service_center.name, 'city': service_center.city,
                        'capacity': service_center.capacity}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data.get('name') or not data.get('city') or not data.get('capacity'):
            return jsonify({'error': 'Invalid input'}), 400
        service_center.name = data['name']
        service_center.city = data['city']
        service_center.capacity = data['capacity']
        db.session.commit()
        return jsonify({'message': 'Service center updated'}), 200

    if request.method == 'DELETE':
        db.session.delete(service_center)
        db.session.commit()
        return jsonify({'message': 'Service center deleted'}), 200


@app.route('/cars', methods=['GET', 'POST'])
def manage_cars():
    if request.method == 'POST':
        data = request.get_json()
        if not data.get('make') or not data.get('model') or not data.get('year'):
            return jsonify({'error': 'Invalid input'}), 400

        new_car = Car(
            make=data['make'],
            model=data['model'],
            year=data['year']
        )
        db.session.add(new_car)
        db.session.commit()
        return jsonify({'message': 'Car created', 'id': new_car.id}), 200

    filters = {
        'make': request.args.get('make'),
        'year_from': request.args.get('year_from'),
        'year_to': request.args.get('year_to')
    }

    query = Car.query
    if filters['make']:
        query = query.filter_by(make=filters['make'])
    if filters['year_from']:
        query = query.filter(Car.year >= int(filters['year_from']))
    if filters['year_to']:
        query = query.filter(Car.year <= int(filters['year_to']))

    cars = query.all()
    return jsonify([
        {'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year} for car in cars
    ]), 200


@app.route('/cars/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_car_by_id(id):
    car = Car.query.get(id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    if request.method == 'GET':
        return jsonify({'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data.get('make') or not data.get('model') or not data.get('year'):
            return jsonify({'error': 'Invalid input'}), 400
        car.make = data['make']
        car.model = data['model']
        car.year = data['year']
        db.session.commit()
        return jsonify({'message': 'Car updated'}), 200

    if request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'Car deleted'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_management.db'
db = SQLAlchemy(app)

# Models
class ServiceCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

class MaintenanceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    service_center_id = db.Column(db.Integer, db.ForeignKey('service_center.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

# Routes
@app.route('/service-centers', methods=['GET', 'POST'])
def manage_service_centers():
    if request.method == 'POST':
        data = request.get_json()
        if not data.get('name') or not data.get('city') or not data.get('capacity'):
            return jsonify({'error': 'Invalid input'}), 400

        new_service_center = ServiceCenter(
            name=data['name'],
            city=data['city'],
            capacity=data['capacity']
        )
        db.session.add(new_service_center)
        db.session.commit()
        return jsonify({'message': 'Service center created', 'id': new_service_center.id}), 200

    city_filter = request.args.get('city')
    query = ServiceCenter.query
    if city_filter:
        query = query.filter_by(city=city_filter)

    service_centers = query.all()
    return jsonify([
        {'id': sc.id, 'name': sc.name, 'city': sc.city, 'capacity': sc.capacity} for sc in service_centers
    ]), 200

@app.route('/service-centers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_service_center_by_id(id):
    service_center = ServiceCenter.query.get(id)
    if not service_center:
        return jsonify({'error': 'Service center not found'}), 404

    if request.method == 'GET':
        return jsonify({'id': service_center.id, 'name': service_center.name, 'city': service_center.city, 'capacity': service_center.capacity}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data.get('name') or not data.get('city') or not data.get('capacity'):
            return jsonify({'error': 'Invalid input'}), 400
        service_center.name = data['name']
        service_center.city = data['city']
        service_center.capacity = data['capacity']
        db.session.commit()
        return jsonify({'message': 'Service center updated'}), 200

    if request.method == 'DELETE':
        db.session.delete(service_center)
        db.session.commit()
        return jsonify({'message': 'Service center deleted'}), 200

@app.route('/cars', methods=['GET', 'POST'])
def manage_cars():
    if request.method == 'POST':
        data = request.get_json()
        if not data.get('make') or not data.get('model') or not data.get('year'):
            return jsonify({'error': 'Invalid input'}), 400

        new_car = Car(
            make=data['make'],
            model=data['model'],
            year=data['year']
        )
        db.session.add(new_car)
        db.session.commit()
        return jsonify({'message': 'Car created', 'id': new_car.id}), 200

    filters = {
        'make': request.args.get('make'),
        'year_from': request.args.get('year_from'),
        'year_to': request.args.get('year_to')
    }

    query = Car.query
    if filters['make']:
        query = query.filter_by(make=filters['make'])
    if filters['year_from']:
        query = query.filter(Car.year >= int(filters['year_from']))
    if filters['year_to']:
        query = query.filter(Car.year <= int(filters['year_to']))

    cars = query.all()
    return jsonify([
        {'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year} for car in cars
    ]), 200

@app.route('/cars/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_car_by_id(id):
    car = Car.query.get(id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    if request.method == 'GET':
        return jsonify({'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data.get('make') or not data.get('model') or not data.get('year'):
            return jsonify({'error': 'Invalid input'}), 400
        car.make = data['make']
        car.model = data['model']
        car.year = data['year']
        db.session.commit()
        return jsonify({'message': 'Car updated'}), 200

    if request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'Car deleted'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
