import math
import time
import random
import winsound  


def estimate_position(distance, angle):
    x = distance * math.cos(angle)  # X-coord
    y = distance * math.sin(angle)  # Y-coord
    return (x, y)


def calculate_speed(prev_position, curr_position, time_elapsed):
    # distance between two positions
    displacement = math.sqrt((curr_position[0] - prev_position[0])**2 + (curr_position[1] - prev_position[1])**2)
    speed = displacement / time_elapsed  


def alert_driver():
    duration = 500  
    frequency = 1000  
    winsound.Beep(frequency, duration)

class Car:
    def __init__(self, plate_number):
        self.plate_number = plate_number
        self.distance = random.uniform(10, 100)  # Random 
        self.angle = random.uniform(0, 2 * math.pi)  
        self.speed = random.uniform(20, 50)  

    def update_position(self):
        self.distance += random.uniform(-2, 2)  
        self.angle += random.uniform(-0.05, 0.05)  
        self.speed += random.uniform(-5, 5)  
        self.speed = max(0, self.speed)  # Ensure speed does not go negative---to check if driving in wrong lane
        return self.distance, self.angle, self.speed

# Stationary sensor 
class StationarySensor:
    def __init__(self, speed_limit):
        self.speed_limit = speed_limit  # Speed limit in km/h for the area

    def receive_signal(self, car_data, prev_car_data):
        distance = car_data["distance"]
        angle = car_data["angle"]
        estimated_position = estimate_position(distance, angle)
        
        # Calculate car speed 
        time_elapsed = 1  
        prev_pos = prev_car_data["position"]
        curr_pos = estimated_position
        speed = calculate_speed(prev_pos, curr_pos, time_elapsed)

        # Detect rapid deceleration
        if prev_car_data["speed"] - speed > 10:  # Threshold for rapid deceleration--can be set
            return f"Rapid deceleration detected for car {car_data['plate_number']}!"
        
        # crash detection based on sudden halt--chk duration
        if speed == 0 and prev_car_data["speed"] > 0:
            return f"Crash detected for car {car_data['plate_number']}!"
        
        # Speed limit warning
        if speed > self.speed_limit:
            return f"Car {car_data['plate_number']} is speeding! Current speed: {speed:.2f} km/h (Limit: {self.speed_limit} km/h)"
        
        # Detect unusual driving behavior (abrupt speed changes for now)
        if abs(prev_car_data["speed"] - speed) > 15:  #---changes needed
            return f"Unusual driving behavior detected for car {car_data['plate_number']}!"

        return {"position": estimated_position, "speed": speed}

# Main control for checking input
def main():
    
    user_input = input("Press '2' to start the simulation: ")
    
    if user_input == '2':
        # Init
        speed_limit = 40  # Speed limit in km/h for the area(to be modified----)
        sensor = StationarySensor(speed_limit)
        
        # Create some cars with random distances & angles 
        cars = [Car(f"Car_{i}") for i in range(5)]
        
        # Previous car data 
        prev_car_data = {car.plate_number: {"position": estimate_position(car.distance, car.angle), "speed": car.speed} for car in cars}
        
        while True:
            for car in cars:
                car_distance, car_angle, car_speed = car.update_position()
                car_data = {"plate_number": car.plate_number, "distance": car_distance, "angle": car_angle, "speed": car_speed}
                result = sensor.receive_signal(car_data, prev_car_data[car.plate_number])
                if isinstance(result, str):
                    print(result)  # alert message -demo
                    alert_driver()  
                else:
                    prev_car_data[car.plate_number] = result
            
            time.sleep(1) 
if __name__ == "__main__":
    main()
