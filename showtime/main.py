import time
import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

from clients.graphql_service import call_graphql_service

import common_pb2

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    # Récupère les horaires de projection d'une date donnée
    def GetShowtimeByDate(self, request, context):
        for showtime in self.db:
            if showtime['date'] == request.date:
                print("Showtime found!")
                return common_pb2.ShowtimeData(date=showtime['date'], movies=showtime['movies'])
        return common_pb2.ShowtimeData(date="", movies=[])

    # Récupère tous les horaires de projection
    def GetShowtimes(self, request, context):
        print("GET ALL SHOWTIMES")
        for showtime in self.db:
            showtime_date = showtime['date']
            showtime_movies = []
            for movie in showtime['movies']:
                movie_graphql = call_graphql_service(3001, f"{{ movie_with_id(_id: \"{movie['id']}\") {{ title }} }}").json()['data']['movie_with_id']
                showtime_movies.append(common_pb2.ShowtimeMovieData(id=movie['id'], title=movie_graphql["title"], seatsMax=movie['seatsMax'], seatsBooked=movie['seatsBooked']))
            
            yield common_pb2.ShowtimeData(date=showtime_date, movies=showtime_movies)
            
    def UpdateSeats(self, request, context):
        for showtime in self.db:
            if showtime['date'] == request.date:
                for movie in showtime['movies']:
                    if movie['id'] == request.movie:
                        if request.number >= 0 and request.number <= movie['seatsMax'] - movie['seatsBooked']:
                            movie['seatsBooked'] = request.number
                            with open('{}/data/times.json'.format("."), "w") as jsf:
                                json.dump({"schedule": self.db}, jsf)
                            return showtime_pb2.UpdateSeatsResult(success=True, message="Seats updated successfully. New number of seats booked: {}".format(movie['seatsBooked']))
                        else:
                            return showtime_pb2.UpdateSeatsResult(success=False, message="Invalid number of seats. Please enter a number between 0 and {}".format(movie['seatsMax'] - movie['seatsBooked']))
            

# Démarrage du serveur
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3003')   
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()