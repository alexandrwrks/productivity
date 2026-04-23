import pygame

class Car:
    def __init__(self, color, max_speed, acceleration, handling):
        self.color = color
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.handling = handling
        self.current_speed = 0
        self.position = 0

    def get_stats(self):
        return f"{self.color} машина: {self.max_speed}км/ч, разгон {self.acceleration}, управление {self.handling}"
    
    def race(self):
        pass


class Track:
    def __init__(self, name, grip, length, difficulty):
        self.name = name
        self.grip = grip # Сцепление:
        self.length = length # длина
        self.difficulty = difficulty # Сложность

    def get_track_info(self):
        return f"{self.name}: сцепление {self.grip}, длина {self.length}"
    

class Race:
    def __init__(self, car: Car, track: Track):
        self.car = car
        self.track = track
        self.progress = 0

    def calculate_speed(self):
        """Скорость зависит от характеристик машины И трасы"""
        base_speed = self.car.max_speed

        track_penalty = (1 - self.track.grip) * 0.3

        handling_bonus = self.car.handling * (1 - self.track.difficulty)

        final_speed = base_speed * (1 - track_penalty + handling_bonus)

        return max(0, final_speed)
    
    def start_race(self):
        print(f"Гонка на трассе '{self.track.name}'")
        print(f"Машина: {self.car.color}")
        print(f"Расчетная скорость: {self.calculate_speed():.1f} км/ч")

car = Car(color="blue", max_speed=120, acceleration=0.8, handling=0.7)
track = Track(name="city", grip=0.8, length=2500, difficulty=1.)

race = Race(car, track)
print(race.calculate_speed())
race.start_race()
