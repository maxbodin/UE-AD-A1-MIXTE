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
            'GetAllShowtimes'
        ]
        
        # Check if the function name is valid
        if functionToCall not in case:
            raise ValueError(f"Invalid function name: {functionToCall}")

        # Call the appropriate gRPC function with the correct request message
        try:
            if functionToCall == 'GetAllBookings':
                print("GET ALL BOOKINGS")
                response = getAllBookings(stubBooking)
                print("response +> ", response)
                
            elif functionToCall == 'GetBookingsOfUser':
                print("GET BOOKINGS OF USER")
                userId = kwargs.get('userId')
                response = getBookingsOfUser(stubBooking, userId)
                
            elif functionToCall == 'GetAllShowtimes':
                response =  getAllShowtimes(stubShowtime)

            return response
        
        except grpc.RpcError as e:
            print(f"gRPC call failed: {e}")
            return None
        
        

        
def getAllShowtimes(stub):
    try:
        return stub.GetShowtimes(common_pb2.Empty(), timeout=10)
    except grpc.RpcError as e:
        print(f"RPC Error: {e}")