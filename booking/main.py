import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

from clients.grpc_service import call_grpc_service


BOOKING_PORT = 3004


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
        print("Server started")

    # Récupère toutes les réservations
    def GetAllBookings(self, request, context):
        print("GET ALL BOOKINGS")
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

    # Récupère les réservations d'un utilisateur 
    def GetBookingsOfUser(self, request, context):
        print("GET BOOKINGS OF USER")
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

    def CreateBooking(self, request, context):
        print("CREATE BOOKING")

        all_showtimes = call_grpc_service("localhost:3003", "GetShowtimes")
        print("ALL SHOWTIMES", all_showtimes)
        
        for date in all_showtimes:
            if date.date == request.date:
                for movie in date.movies:
                    if movie.id == request.movie:
                        print(request)
                        print("MAX SEATS", movie.seatsMax) 
                        print("BOOKED SEATS", movie.seatsBooked)
                        if request.seats >= 0 :
                            print('DONE')
                            createBookingData = {
                                "userid": request.user,
                                "dates": [
                                    {
                                        "date": request.date,
                                        "movies": [
                                            {
                                                "movieid": request.movie,
                                                "seatsBooked": request.seats
                                            }
                                        ]
                                    }
                                ]
                            }
                            print("CREATE BOOKING DATA", createBookingData)
                            self.db.append(createBookingData)
                            with open('{}/data/bookings.json'.format("."), "w") as jsf:
                                json.dump({"bookings": self.db}, jsf)
                            return booking_pb2.CreateBookingResult(success=True, message="Booking created successfully.")
                        else:
                            return booking_pb2.CreateBookingResult(success=False, message="Invalid number of seats. Please enter a number between 0 and {}".format(movie.seatsMax - movie.seatsBooked))
        
        

# Démarre le serveur
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port(f'[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
