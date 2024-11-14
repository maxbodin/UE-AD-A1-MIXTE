import grpc
import showtime_pb2
import showtime_pb2_grpc   
import booking_pb2
import booking_pb2_grpc 
import common_pb2
import common_pb2_grpc


def get_showtime_by_date(stub, date):
    try:
        showtime = stub.GetShowtimeByDate(date)
        if showtime.date:
            print(f"Showtime on {showtime.date}:")
            for movie in showtime.movies:
                print(f"- {movie})")
        else:
            print("No showtime found for the specified date.")
    except grpc.RpcError as e:
        print(f"RPC Error: {e}")


def get_showtimes(stub):
    try:
        all_showtimes = stub.GetShowtimes(common_pb2.Empty())
        for showtime in all_showtimes:
            print(f"Showtime on {showtime.date}:")
            for movie in showtime.movies:
                print(f"- {movie}")
    except grpc.RpcError as e:
        print(f"RPC Error: {e}")
        
def get_bookings(stub):
    try:
        all_bookings = stub.GetAllBookings(common_pb2.Empty())
        for booking in all_bookings:
            print(f"Booking for user {booking.userId}:")
            for date in booking.dates:
                print(f"- {date.date}:")
                for movie in date.moviesData:
                    print(f"  - {movie.movieId}: {movie.seatsBooked}")
    except grpc.RpcError as e:
        print(f"RPC Error: {e}")



def run():
    with grpc.insecure_channel(f'localhost:3003') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetShowtimeByDate --------------")
        showtime_date = showtime_pb2.ShowtimeDate(date="20151130")
        get_showtime_by_date(stub, showtime_date)

        print("-------------- GetShowtimes --------------")
        get_showtimes(stub)
        
    with grpc.insecure_channel(f'localhost:3005') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        print("-------------- GetAllBookings --------------")
        get_bookings(stub)


if __name__ == '__main__':
    run()
