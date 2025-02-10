import grpc
from concurrent import futures
import random
import spaceship_pb2
import spaceship_pb2_grpc

# Списки для генерации имен и фамилий офицеров
first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Chris", "Laura", "Daniel", "Emma"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

# Правила для каждого класса кораблей
ship_rules = {
    'Corvette': {'length': (80, 250), 'crew_size': (4, 10), 'armed': True},
    'Frigate': {'length': (300, 600), 'crew_size': (10, 15), 'armed': True},
    'Cruiser': {'length': (500, 1000), 'crew_size': (15, 30), 'armed': True},
    'Destroyer': {'length': (800, 2000), 'crew_size': (50, 80), 'armed': True},
    'Carrier': {'length': (1000, 4000), 'crew_size': (120, 250), 'armed': False},
    'Dreadnought': {'length': (5000, 20000), 'crew_size': (300, 500), 'armed': True},
}

class SpaceshipReportingServicer(spaceship_pb2_grpc.SpaceshipReportingServicer):
    def GetSpaceships(self, request, context):
        for _ in range(random.randint(1, 10)):
            ship_class = random.choice(list(ship_rules.keys()))
            rules = ship_rules[ship_class]
            alignment = random.choice([spaceship_pb2.Spaceship.ALLY, spaceship_pb2.Spaceship.ENEMY])
            officers = []
            if alignment == spaceship_pb2.Spaceship.ALLY:
                # Генерация офицеров для союзников
                num_officers = random.randint(1, 10)
                officers = [spaceship_pb2.Officer(
                    first_name=random.choice(first_names),
                    last_name=random.choice(last_names),
                    rank=f"Rank_{i}"
                ) for i in range(num_officers)]
            yield spaceship_pb2.Spaceship(
                alignment=alignment,
                name=f"Spaceship_{random.randint(1, 100)}",
                ship_class=ship_class,
                length=random.uniform(rules['length'][0], rules['length'][1]),
                crew_size=random.randint(rules['crew_size'][0], rules['crew_size'][1]),
                armed=rules['armed'],
                officers=officers
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    spaceship_pb2_grpc.add_SpaceshipReportingServicer_to_server(SpaceshipReportingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()