import base64
from io import BytesIO
import io
import math
import os
import random
from threading import Thread
import threading
import time
from datetime import datetime
import json
import carla
import cv2
import numpy as np
from PIL import Image
from flask.json import jsonify
from flask import request, Blueprint, Response
from pymongo import MongoClient

control_routes = Blueprint('control_routes', __name__)
world = None
client = None


# MongoDB connection URI (replace with your own)
mongo_uri = "mongodb://localhost:27017"  # Localhost or remote MongoDB URI
client = MongoClient(mongo_uri)

# Select database and collection
db = client['SSRCP']  # Replace 'my_database' with your DB name
robotCollection = db['robot']  # Replace 'my_collection' with your collection name



# Replace escaped quotes with single quotes
latest_frame = {}

# sensors Obj
sensors = {}
# Load the JSON string
# data = json_string)
frame_lock = threading.Lock()

def image_to_base64(image):
    """Convert a PIL Image object to a base64-encoded string."""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # Save the image to a buffer in JPEG format
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def camera_callback1(image,id, vehicleId,pos):
    array = image.raw_data
    img = Image.frombytes("RGBA", (image.width, image.height), bytes(array))
    img = img.convert("RGB")


    output_file_path = "./images/"+str(id)+"_"+str(vehicleId)+"_"+pos+".png"  # Specify the desired file path and name
    img.save(output_file_path, format="PNG")
    print("CAMERA CALLBACK : ", id, pos, latest_frame)
    if (latest_frame[str(id)][str(vehicleId)] is None):
        latest_frame[str(id)][str(vehicleId)] = {pos : image_to_base64(img)}
    else:
        latest_frame[str(id)][str(vehicleId)][pos] =  image_to_base64(img)
    time.sleep(2)
    
    
def camera_callback2(image,id, vehicleId,pos):
    array = image.raw_data
    img = Image.frombytes("RGBA", (image.width, image.height), bytes(array))
    img = img.convert("RGB")


    output_file_path = "./images/"+str(id)+"_"+str(vehicleId)+"_"+pos+".png"  # Specify the desired file path and name
    img.save(output_file_path, format="PNG")
    print("CAMERA CALLBACK : ", id, pos, latest_frame)
    if (latest_frame[str(id)][str(vehicleId)] is None):
        latest_frame[str(id)][str(vehicleId)] = {pos : image_to_base64(img)}
    else:
        latest_frame[str(id)][str(vehicleId)][pos] =  image_to_base64(img)
    time.sleep(2)
    
    
    

# Function to save JSON object to a file
def save_json_to_file(json_object, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(json_object, json_file, indent=4)  # Write with indentation for readability

def setup_spectator_camera(world, vehicle):
    vehicle_transform = vehicle.get_transform()
    spectator = world.get_spectator()
    # Set the spectator transform relative to the vehicle
    spectator_transform = carla.Transform(
        vehicle_transform.location + carla.Location(x=-6, y=0, z=2),  # Offset the spectator above the vehicle
        vehicle_transform.rotation  # Match the rotation of the vehicle
    )
    print("vehicle_transform.rotation : ", vehicle_transform.rotation)
    spectator.set_transform(spectator_transform)
    # Wait for a short time before updating again


def update_vehicle_stats(userID, mysqlRobotId, vehicle, camTop, camFront, world):
    vehicle_data = {}
    print("Start update vehicle states ....... ")
    try:
        velocity = vehicle.get_velocity()
        location = vehicle.get_location()
        transform = vehicle.get_transform()
        acceleration = vehicle.get_acceleration()
        control = vehicle.get_control()
        
        vehicle_data = {
            "id": vehicle.id,
            "userId": userID,
            "img" : {
                 "top": latest_frame[str(userID)][str(vehicle.id)]["top"] ,
                "front": latest_frame[str(userID)][str(vehicle.id)]["front"] ,
            },
            "mysqlRobotId": mysqlRobotId,
            "cameraId": {
                 "top": camTop ,
                "front": camFront,
            },
            "velocity": math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2),
            "location": {
                "x": location.x,
                "y": location.y,
                "z": location.z
            },
            "acceleration": math.sqrt(acceleration.x**2 + acceleration.y**2 + acceleration.z**2),
            "throttle": control.throttle,
            "steering": control.steer,
            "brake": control.brake,
            "gear": control.gear,
            "orientation": {
                "pitch": transform.rotation.pitch,
                "yaw": transform.rotation.yaw,
                "roll": transform.rotation.roll
            },
             "time": datetime.now(),
        }

        result = robotCollection.insert_one(vehicle_data)
        return result
    except Exception as e:
        print(f"Error updating vehicle stats: {e}")

@control_routes.route("/createVehicle", methods=['GET'])
def creatVehicleGetPoint():
    userId = request.args.get('id', '1')  # Default value is '1' if 'id' is not provided
    mysqlRobotId = request.args.get('robotId', '1')
    car_type = request.args.get('car_model', 'vehicle.audi.a2')  # Default value
    weather = request.args.get('weather', 'ClearNoon')  # Default value
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    world.set_weather(getattr(carla.WeatherParameters, weather))



    blueprint_library = world.get_blueprint_library()
    print("blueprint_library : ", blueprint_library.filter(car_type))
    vehicle_bp = blueprint_library.find(car_type)
    spawn_points = world.get_map().get_spawn_points()
    random_spawn_point = random.choice(spawn_points)
    vehicle = world.try_spawn_actor(vehicle_bp, random_spawn_point)


    latest_frame[str(userId)] = { str(vehicle.id) : {"top" : None} }
    latest_frame[str(userId)] = { str(vehicle.id) : {"front" : None} }



    camera_bp1 = blueprint_library.find('sensor.camera.rgb')
    camera_bp1.set_attribute('image_size_x', '800')
    camera_bp1.set_attribute('image_size_y', '600')
    
    
    camera_bp2 = blueprint_library.find('sensor.camera.rgb')
    camera_bp2.set_attribute('image_size_x', '800')
    camera_bp2.set_attribute('image_size_y', '600')
    
    camera_spawn_pointFront = carla.Transform(
        carla.Location(x=-5.0, y=0.0, z=3.0),
        carla.Rotation(pitch=-15.0)
    )
    cameraFront = world.spawn_actor(camera_bp1, camera_spawn_pointFront, attach_to=vehicle)
    
    camera_spawn_pointTop = carla.Transform(
            carla.Location(x=0.0, y=0.0, z=5.0),
            carla.Rotation(pitch=-90.0)
    )
    cameraTop = world.spawn_actor(camera_bp2, camera_spawn_pointTop, attach_to=vehicle)

    sensors[userId] = {vehicle.id: { "top" : cameraTop}}
    sensors[userId][vehicle.id]["top"].listen(lambda frame: camera_callback1(frame, userId , vehicle.id, "top"))

    sensors[userId] = {vehicle.id: { "front" : cameraFront}}
    sensors[userId][vehicle.id]["front"].listen(lambda frame: camera_callback2(frame, userId , vehicle.id, "front"))

    vehicleData = {"vehicleObj": vehicle, "vehicle": vehicle.id, "vehicle": vehicle.id, "cameraFront": cameraFront.id, 
    "cameraTop": cameraTop.id,
    "car_type": car_type}

    vehicle.set_autopilot(True)
    vehicleObj = vehicleData["vehicleObj"]

    def generate():
        while True:
            stats = update_vehicle_stats(userId,mysqlRobotId, vehicleObj , vehicleData["cameraFront"], 23, world)  # Initialize the vehicle data # vehicleData["cameraTop"]
            setup_spectator_camera(world, vehicleObj)
            time.sleep(2)


    print("Start Threading .....")    
    thread = threading.Thread(target=generate)
    thread.start()

    del vehicleData["vehicleObj"]
    return vehicleData, 200

@control_routes.route('/deleteRobot/<robot>', methods=['GET'])
def delete_robot(robot):
    try:
        print("robot : ", robot)
        # Get the robot's ID from the request
        robot_id = int(robot)
        if robot_id is None:
            return {"error": "robotId is required"}, 400
        
        print("robot : ", robot)
        client = carla.Client('localhost', 2000)
        world = client.get_world()
        # Find the actor in the CARLA world
        actor = world.get_actor(int(robot_id))
        if actor is None:
            return {"error": f"No actor found with ID {robot_id}"}, 404

        print("w00ww0w0w0w", actor)
        # Iterate through the list of sensors associated with the actor
        sensors_to_destroy = []
        for sensor in world.get_actors():
            if sensor.parent and sensor.parent.id == actor.id:
                sensors_to_destroy.append(sensor)

        # Destroy all associated sensors
        for sensor in sensors_to_destroy:
            sensor.destroy()
            print(f"Destroyed sensor with ID: {sensor.id}")

        # Destroy the actor
        actor.destroy()
        return {"message": f"Robot with ID {robot_id} and associated Sensors has been successfully deleted."}, 200

    except Exception as e:
        print(e)

@control_routes.route('/dummyCar', methods = ['GET'])
def dummy():
    return "Mitansh Gor"
