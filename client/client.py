import grpc
import showtime_pb2
import showtime_pb2_grpc
from constants import HOST, SHOWTIME_PORT


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
        all_showtimes = stub.GetShowtimes(showtime_pb2.Empty())
        for showtime in all_showtimes:
            print(f"Showtime on {showtime.date}:")
            for movie in showtime.movies:
                print(f"- {movie}")
    except grpc.RpcError as e:
        print(f"RPC Error: {e}")


def run():
    with grpc.insecure_channel(f'{HOST}:{SHOWTIME_PORT}') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetShowtimeByDate --------------")
        showtime_date = showtime_pb2.ShowtimeDate(date="20151130")
        get_showtime_by_date(stub, showtime_date)

        print("-------------- GetShowtimes --------------")
        get_showtimes(stub)


if __name__ == '__main__':
    run()
