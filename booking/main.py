import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json


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
        
        showtime_service_url = f'http://localhost:3003/showtimes/{user_id}'

        try:
            response = requests.get(booking_service_url)
            if response.status_code == 200:
                return jsonify(response.json()), 200
            else:
                return jsonify({"error": "Bookings not found for the user"}), 404
        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Booking service is unavailable", "details": str(e)}), 500

        
        new_booking = {
            "userid": request.userId,
            "dates": []
        }

        for dateEntry in request.dates:
            new_date = {
                "date": dateEntry.date,
                "movies": []
            }

            for movieEntry in dateEntry.moviesData:
                new_movie = {
                    "movieid": movieEntry.movieId,
                    "seatsBooked": movieEntry.seatsBooked
                }
                new_date["movies"].append(new_movie)

            new_booking["dates"].append(new_date)

        self.db.append(new_booking)

        with open('{}/data/bookings.json'.format("."), "w") as jsf:
            json.dump({"bookings": self.db}, jsf)

        return booking_pb2.BookingResult(
            success=True,
            message="Booking created successfully"
        )

# Démarre le serveur
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port(f'[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
