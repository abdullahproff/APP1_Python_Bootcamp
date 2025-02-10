import grpc
from concurrent import futures
import random
import spaceship_pb2
import spaceship_pb2_grpc

class SpaceshipReportingServicer(spaceship_pb2_grpc.SpaceshipReportingServicer):
    def GetSpaceships(self, request, context):
        for _ in range(random.randint(1, 10)):
            alignment = random.choice([spaceship_pb2.Spaceship.ALLY, spaceship_pb2.Spaceship.ENEMY])
            officers = []
            if alignment == spaceship_pb2.Spaceship.ALLY:
                officers = [spaceship_pb2.Officer(
                    first_name=f"Officer_{i}",
                    last_name=f"Lastname_{i}",
                    rank=f"Rank_{i}"
                ) for i in range(random.randint(1, 10))]
            yield spaceship_pb2.Spaceship(
                alignment=alignment,
                name=f"Spaceship_{random.randint(1, 100)}",
                ship_class=random.choice(["Corvette", "Frigate", "Cruiser", "Destroyer", "Dreadnought"]),
                length=random.uniform(100.0, 10000.0),
                crew_size=random.randint(1, 1000),
                armed=random.choice([True, False]),
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