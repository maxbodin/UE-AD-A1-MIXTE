import grpc

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import booking_pb2_grpc
import booking_pb2

import showtime_pb2_grpc
import showtime_pb2

import common_pb2
import common_pb2_grpc

def getAllBookings(stub):
    all_bookings = []
    try:
        all_bookings_grpc = stub.GetAllBookings(common_pb2.Empty())
        for booking in all_bookings_grpc:
            all_bookings.append(booking)
        return all_bookings

    except grpc.RpcError as e:
        print(f"RPC Error: {e}")
        
def getBookingsOfUser(stub, userId):
    all_dates = []
    try:
        booking = stub.GetBookingsOfUser(booking_pb2.UserId(id=userId))
        for date in booking.dates:
            all_movies = []
            for movie in date.moviesData:
                all_movies.append({
                    'movieId': movie.movieId,
                    'seatsBooked': movie.seatsBooked
                })
                
            all_dates.append({
                'date': date.date,
                'movies': all_movies
            })
        return all_dates
    
    except grpc.RpcError as e:
        print(f"RPC Error: {e}")
        
def getShowtimes(stub):
    print("GET SHOWTIMES")
    all_showtimes = []
    try:
        all_showtimes_grpc = stub.GetShowtimes(common_pb2.Empty())
        for showtime in all_showtimes_grpc:
            all_showtimes.append(showtime)
            
            
        return all_showtimes
    except grpc.RpcError as e:
        print(f"RPC Error: {e}")
        

# Fonction permettant d'effectuer des requêtes gRPC
def call_grpc_service(server_address, functionToCall, **kwargs):
    with grpc.insecure_channel(server_address) as channel:
        stubBooking = booking_pb2_grpc.BookingStub(channel)
        stubShowtime = showtime_pb2_grpc.ShowtimeStub(channel)
        
        case = [
            'GetAllBookings',
            'GetBookingsOfUser',
            'GetBookingsOfShowtime',
            'CreateBooking',
            'DeleteBooking',
            'GetShowtimes'
        ]
        
        # Vérification de la validité de la fonction à appeler
        if functionToCall not in case:
            raise ValueError(f"Invalid function name: {functionToCall}")

        # Appel de la fonction correspondante
        try:
            if functionToCall == 'GetAllBookings':
                print("GET ALL BOOKINGS")
                response = getAllBookings(stubBooking)
                print("response +> ", response)
                
            elif functionToCall == 'GetBookingsOfUser':
                print("GET BOOKINGS OF USER")
                userId = kwargs.get('userId')
                response = getBookingsOfUser(stubBooking, userId)
                
            elif functionToCall == 'GetShowtimes':
                print("GET ALL SHOWTIMES")
                response =  getShowtimes(stubShowtime)

            return response
        
        except grpc.RpcError as e:
            print(f"gRPC call failed: {e}")
            return None
        