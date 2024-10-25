import math
import time
import random

def estimate_position(distance, angle):
    x = distance * math.cos(angle)  # X-coord
    y = distance * math.sin(angle)  # Y-coord
    return (x, y)


def calculate_speed(prev_position, curr_position, time_elapsed):
    #
    displacement = math.sqrt((curr_position[0] - prev_position[0])**2 + (curr_position[1] - prev_position[1])**2)
    speed = displacement / time_elapsed  
    return speed


class Car:
    def __init__(self, plate_number):
        self.plate_number = plate_number
        self.distance = random.uniform(10, 100)  
        self.angle = random.uniform(0, 2 * math.pi)  
        self.speed = random.uniform(20, 50)

    def update_position(self):
        self.distance += random.uniform(-2, 2)  
        self.angle += random.uniform(-0.05, 0.05)   
        self.speed += random.uniform(-5, 5)  
        self.speed = max(0, self.speed)  
        return self.distance, self.angle, self.speed

# Simulate a traffic light 
class TrafficLight:
    def __init__(self):
        self.state = 'green'  # Init state 
    
    def toggle_state(self):
        self.state = 'red' if self.state == 'green' else 'green'

# Stationary sensor class ---traffic lights
class TrafficLightSensor:
    def __init__(self, speed_limit):
        self.speed_limit = speed_limit 
        self.traffic_light = TrafficLight()  

    def check_violation(self, car_data):
        distance = car_data["distance"]
        angle = car_data["angle"]
        estimated_position = estimate_position(distance, angle)
        speed = car_data["speed"]
        if speed > self.speed_limit:
            return f"Speeding detected for car {car_data['plate_number']}! Speed: {speed:.2f} km/h (Limit: {self.speed_limit} km/h)"
        if self.traffic_light.state == 'red':
            return f"Car {car_data['plate_number']} jumped a red light!"
        if abs(speed - car_data.get("prev_speed", speed)) > 15: 
            return f"Dangerous driving detected for car {car_data['plate_number']}! Speed: {speed:.2f} km/h"
        return None

# Main control for checking input
def main():
    speed_limit = 40  
    sensor = TrafficLightSensor(speed_limit)
    cars = [Car(f"Car_{i}") for i in range(5)]

    light_change_interval = 10  
    last_light_change = time.time()

    while True:
        for car in cars:
            car_distance, car_angle, car_speed = car.update_position()
            car_data = {"plate_number": car.plate_number, "distance": car_distance, "angle": car_angle, "speed": car_speed, "prev_speed": car_speed}
            violation_message = sensor.check_violation(car_data)
            if violation_message:
                print(violation_message)
            car_data["prev_speed"] = car_speed
        current_time = time.time()
        if current_time - last_light_change > light_change_interval:
            sensor.traffic_light.toggle_state()
            last_light_change = current_time
            print(f"Traffic light changed to {sensor.traffic_light.state}")
        
        time.sleep(1)  

if __name__ == "__main__":
    main()
