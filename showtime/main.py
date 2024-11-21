import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json


class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    # Récupère les horaires de projection d'une date donnée
    def GetShowtimeByDate(self, request, context):
        for showtime in self.db:
            if showtime['date'] == request.date:
                print("Showtime found!")
                return showtime_pb2.ShowtimeData(date=showtime['date'], movies=showtime['movies'])
        return showtime_pb2.ShowtimeData(date="", movies=[])

    # Récupère tous les horaires de projection
    def GetShowtimes(self, request, context):
        for showtime in self.db:
            yield showtime_pb2.ShowtimeData(date=showtime['date'], movies=showtime['movies'])

# Démarrage du serveur
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3003')   
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()