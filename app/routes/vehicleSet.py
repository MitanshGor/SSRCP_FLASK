# from flask import Blueprint, request, jsonify
# import carla
# import random

# vehicle_routes = Blueprint('vehicle_routes', __name__)

# # Carla client setup
# client = carla.Client('localhost', 2000)
# client.set_timeout(10.0)
# world = client.get_world()

# @vehicle_routes.route('/create', methods=['POST'])
# def create_vehicle():
#     try:
#         blueprint_library = world.get_blueprint_library()
#         spawn_points = world.get_map().get_spawn_points()

#         vehicle_bp = blueprint_library.filter('vehicle.*')[0]
#         if 'model' in request.json:
#             model = request.json['model']
#             vehicle_bp = blueprint_library.find(f'vehicle.{model}')

#         spawn_point = random.choice(spawn_points)
#         vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)

#         if vehicle:
#             return jsonify({'message': 'Vehicle created', 'id': vehicle.id}), 200
#         else:
#             return jsonify({'error': 'Failed to spawn vehicle'}), 500
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
