import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

BOOKING_PORT = 3002


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetAllBookings(self, request, context):
        for booking in self.db:
            datesList = []

            for dateEntry in booking["dates"]:
                moviesList = []

                for movieEntry in dateEntry["movies"]:
                    movie_data = booking_pb2.MovieData(
                        movieId=movieEntry["movieid"],
                        seatsBooked=movieEntry["seatsBooked"]
                    )
                    moviesList.append(movie_data)

                date_data = booking_pb2.DateData(
                    date=dateEntry["date"],
                    moviesData=moviesList
                )
                datesList.append(date_data)

            yield booking_pb2.BookingData(
                userId=booking["userid"],
                dates=datesList
            )

    def GetBookingsOfUser(self, request, context):
        for booking in self.db:
            if booking["userid"] == request.id:
                datesList = []

                for dateEntry in booking["dates"]:
                    moviesList = []

                    for movieEntry in dateEntry["movies"]:
                        movie_data = booking_pb2.MovieData(
                            movieId=movieEntry["movieid"],
                            seatsBooked=movieEntry["seatsBooked"]
                        )
                        moviesList.append(movie_data)

                    date_data = booking_pb2.DateData(
                        date=dateEntry["date"],
                        moviesData=moviesList
                    )
                    datesList.append(date_data)

                return booking_pb2.BookingData(
                    userId=booking["userid"],
                    dates=datesList
                )

        return booking_pb2.BookingData(
            userId=request.id,
            dates=[]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port(f'[::]:{BOOKING_PORT}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
