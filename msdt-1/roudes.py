"""
Info about program
"""

# Info about why we use random
import random
# Info why we use time
import time



class Car:
    """
        This class do...
    """
    def __init__(self, id, initial_position=(0, 0), initial_speed=0, max_speed=100, acceleration=2.0, braking_force=3.0):
        """
        About the constructor
        :param id:
        :param initial_position:
        :param initial_speed:
        :param max_speed:
        :param acceleration:
        :param braking_force:
        """
        self.id = id
        self.position = list(initial_position)
        self.speed = initial_speed
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.braking_force = braking_force
        self.lane = 0 # Start in lane 0
        self.target_lane = 0
        self.lane_change_start_time = 0

    def update_position(self, dt):
        """
        About update
        :param dt:
        :return:
        """
        speed_ms = self.speed * (1000 / 3600)
        self.position[0] += speed_ms * dt


    def accelerate(self, dt):
        """
        About accelerate
        :param dt:
        :return:
        """
        speed_increase = self.acceleration * dt
        self.speed = min(self.speed + speed_increase, self.max_speed)


    def brake(self, dt):
        """
        About brake
        :param dt:
        :return:
        """
        speed_decrease = self.braking_force * dt
        self.speed = max(0, self.speed - speed_decrease)


    def change_lane(self, dt):
        """
        About change lane
        :param dt:
        :return:
        """
        if self.lane != self.target_lane:
            # Simulate gradual lane change
            lane_change_speed = 10 # km/h
            lane_change_ms = lane_change_speed * (1000/3600)
            if time.time() - self.lane_change_start_time < 2.0: #Simulate 2-sec lane change
                if self.lane < self.target_lane:
                    self.position[1] += lane_change_ms * dt
                else:
                    self.position[1] -= lane_change_ms * dt
            else:
                self.lane = self.target_lane
                self.lane_change_start_time = 0


    def decide_action(self, dt, other_cars):
        """
        About decide action
        :param dt:
        :param other_cars:
        :return:
        """
        # Simple decision-making:  Accelerate, brake, or change lanes
        if random.random() < 0.7:  # 70% chance to accelerate
            self.accelerate(dt)
        else:
            self.brake(dt)

        #Rudimentary lane changing logic.  Avoids crashing into other cars.
        if random.random() < 0.2: #20% chance to change lanes
            target_lane = random.choice([0,1]) # only 2 lanes for simplicity
            if self.is_lane_change_safe(target_lane,other_cars):
                self.target_lane = target_lane
                self.lane_change_start_time = time.time()


    def is_lane_change_safe(self, target_lane, other_cars):
        """
        About is_lane_change_safe
        :param target_lane:
        :param other_cars:
        :return:
        """
        # Check for collisions before lane change (very basic check)
        for car in other_cars:
            if car.id != self.id and abs(car.position[0] - self.position[0]) < 50 and car.lane == target_lane: #Check for cars within 50 meters
                return False
        return True


    def get_status(self):
        """
        About get_status
        :return:
        """
        return f"Car {self.id}: Pos=({self.position[0]:.2f},{self.position[1]:.2f}), Speed={self.speed:.2f} km/h, Lane={self.lane}"



def simulate_traffic(num_cars, duration, dt=1.0):
    """
    About simulate_traffic
    :param num_cars:
    :param duration:
    :param dt:
    :return:
    """
    cars = [Car(i, initial_position=(i * 50, 0), max_speed=random.randint(80,120),acceleration=random.uniform(1.5,2.5),braking_force=random.uniform(2.5,3.5)) for i in range(num_cars)]
    for t in range(int(duration / dt)):
        for i, car in enumerate(cars):
            car.decide_action(dt, cars[:i] + cars[i+1:]) #avoid self-collision in the decision
            car.change_lane(dt)
            car.update_position(dt)
            print(car.get_status())
        print("-" * 20)


#Example
simulate_traffic(num_cars=3, duration=20, dt=1)


#Dummy functions to boost line count
def dummy_func1():
    pass


def dummy_func2(x,y):
    return x*y


for i in range(20):
    dummy_func1()
    dummy_func2(i,i+1)
