import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

from constants import BOOKING_PORT


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port(f'[::]:{BOOKING_PORT}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
