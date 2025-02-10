import grpc
import spaceship_pb2
import spaceship_pb2_grpc
import json
import sys

def run(coordinates):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = spaceship_pb2_grpc.SpaceshipReportingStub(channel)
        response = stub.GetSpaceships(spaceship_pb2.Coordinates(coordinates=coordinates))
        for spaceship in response:
            print(json.dumps({
                "alignment": "Ally" if spaceship.alignment == spaceship_pb2.Spaceship.ALLY else "Enemy",
                "name": spaceship.name,
                "class": spaceship.ship_class,
                "length": spaceship.length,
                "crew_size": spaceship.crew_size,
                "armed": spaceship.armed,
                "officers": [{
                    "first_name": officer.first_name,
                    "last_name": officer.last_name,
                    "rank": officer.rank
                } for officer in spaceship.officers]
            }, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: reporting_client.py <coordinates>")
        sys.exit(1)
    run(sys.argv[1])