from flask import Flask, jsonify, request

app = Flask(__name__)


garages = {}
cars = {}
maintenances = {}


@app.route('/garages', methods=['POST'])
def create_garage():
    data = request.json
    if not all(key in data for key in ['name', 'location', 'city', 'capacity']):
        return jsonify({"error": "Missing required fields"}), 400

    garage_id = len(garages) + 1
    garages[garage_id] = {
        "id": garage_id,
        "name": data["name"],
        "location": data["location"],
        "city": data["city"],
        "capacity": data["capacity"]
    }
    return jsonify(garages[garage_id]), 200

@app.route('/garages/<int:garage_id>', methods=['GET'])
def get_garage(garage_id):
    garage = garages.get(garage_id)
    if not garage:
        return jsonify({"error": "Garage not found"}), 404
    return jsonify(garage), 200

@app.route('/garages', methods=['GET'])
def get_all_garages():
    city = request.args.get('city')
    filtered_garages = [garage for garage in garages.values() if city is None or garage['city'] == city]
    return jsonify(filtered_garages), 200

@app.route('/garages/<int:garage_id>', methods=['PUT'])
def update_garage(garage_id):
    garage = garages.get(garage_id)
    if not garage:
        return jsonify({"error": "Garage not found"}), 404

    data = request.json
    garage.update({key: data[key] for key in data if key in garage})
    return jsonify(garage), 200

@app.route('/garages/<int:garage_id>', methods=['DELETE'])
def delete_garage(garage_id):
    if garage_id not in garages:
        return jsonify({"error": "Garage not found"}), 404
    del garages[garage_id]
    return jsonify({"message": "Garage deleted"}), 200


@app.route('/cars', methods=['POST'])
def create_car():
    data = request.json
    if not all(key in data for key in ['make', 'model', 'productionYear', 'licensePlate']):
        return jsonify({"error": "Missing required fields"}), 400

    car_id = len(cars) + 1
    cars[car_id] = {
        "id": car_id,
        "make": data["make"],
        "model": data["model"],
        "productionYear": data["productionYear"],
        "licensePlate": data["licensePlate"],
        "garages": data.get("garageIds", [])
    }
    return jsonify(cars[car_id]), 200

@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car = cars.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404
    return jsonify(car), 200

@app.route('/cars', methods=['GET'])
def get_all_cars():
    car_make = request.args.get('carMake')
    garage_id = request.args.get('garageId')
    from_year = request.args.get('fromYear', type=int)
    to_year = request.args.get('toYear', type=int)

    filtered_cars = [
        car for car in cars.values()
        if (car_make is None or car['make'] == car_make) and
           (garage_id is None or int(garage_id) in car['garages']) and
           (from_year is None or car['productionYear'] >= from_year) and
           (to_year is None or car['productionYear'] <= to_year)
    ]
    return jsonify(filtered_cars), 200

@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = cars.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404

    data = request.json
    car.update({key: data[key] for key in data if key in car})
    return jsonify(car), 200

@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    if car_id not in cars:
        return jsonify({"error": "Car not found"}), 404
    del cars[car_id]
    return jsonify({"message": "Car deleted"}), 200


@app.route('/maintenance', methods=['POST'])
def create_maintenance():
    data = request.json
    if not all(key in data for key in ['carId', 'garageId', 'scheduledDate', 'serviceType']):
        return jsonify({"error": "Missing required fields"}), 400

    garage = garages.get(data['garageId'])
    if not garage:
        return jsonify({"error": "Garage not found"}), 404

    maintenance_id = len(maintenances) + 1
    maintenances[maintenance_id] = {
        "id": maintenance_id,
        "carId": data["carId"],
        "garageId": data["garageId"],
        "scheduledDate": data["scheduledDate"],
        "serviceType": data["serviceType"]
    }
    return jsonify(maintenances[maintenance_id]), 200

@app.route('/maintenance/<int:maintenance_id>', methods=['GET'])
def get_maintenance(maintenance_id):
    maintenance = maintenances.get(maintenance_id)
    if not maintenance:
        return jsonify({"error": "Maintenance not found"}), 404
    return jsonify(maintenance), 200

@app.route('/maintenance', methods=['GET'])
def get_all_maintenances():
    car_id = request.args.get('carId', type=int)
    garage_id = request.args.get('garageId', type=int)
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    filtered_maintenances = [
        maintenance for maintenance in maintenances.values()
        if (car_id is None or maintenance['carId'] == car_id) and
           (garage_id is None or maintenance['garageId'] == garage_id) and
           (start_date is None or maintenance['scheduledDate'] >= start_date) and
           (end_date is None or maintenance['scheduledDate'] <= end_date)
    ]
    return jsonify(filtered_maintenances), 200

if __name__ == '__main__':
    app.run(debug=True)
