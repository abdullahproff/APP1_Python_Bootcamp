import grpc
import json
import sys
from models import Spaceship
import spaceship_pb2
import spaceship_pb2_grpc

def run(coordinates):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = spaceship_pb2_grpc.SpaceshipReportingStub(channel)
        response = stub.GetSpaceships(spaceship_pb2.Coordinates(coordinates=coordinates))
        
        for spaceship in response:
            try:
                # Преобразуем данные в модель Pydantic
                ship_data = {
                    "alignment": "Ally" if spaceship.alignment == spaceship_pb2.Spaceship.ALLY else "Enemy",
                    "name": spaceship.name,
                    "ship_class": spaceship.ship_class,
                    "length": spaceship.length,
                    "crew_size": spaceship.crew_size,
                    "armed": spaceship.armed,
                    "officers": [{
                        "first_name": officer.first_name,
                        "last_name": officer.last_name,
                        "rank": officer.rank
                    } for officer in spaceship.officers]
                }
                # Валидация данных
                validated_ship = Spaceship(**ship_data)
                # Вывод корректных данных
                print(json.dumps(validated_ship.model_dump(), indent=2))
            except Exception as e:
                # Если данные некорректны, пропускаем корабль
                print(f"Skipping invalid ship: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: reporting_client_v2.py <coordinates>")
        sys.exit(1)
    run(sys.argv[1])