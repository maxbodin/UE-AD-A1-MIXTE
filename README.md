# UE-AD-A1-MIXTE

**UE AD FIL A1**

[Tutoriel sur GraphQL de Helene Coullon - helene.coullon@imt-atlantique.fr](https://helene-coullon.fr/pages/ue-ad-fil-24-25/tuto-graphql/)

[TP sur GraphQL et gRPC de Helene Coullon - helene.coullon@imt-atlantique.fr](https://helene-coullon.fr/pages/ue-ad-fil-24-25/tp-mixte/)


## Objectifs

- Développer une application de 4 micro-services pour la gestion d’une salle de cinéma.
- Comprendre les concepts de développements de micro-services et apprendre à utiliser trois types d’API.


# Installer les dépendances 
```bash
source venv/bin/activate
pip install -r requirements.txt
```

# Lancer la web app (front-end)
```bash
cd web
python3 manage.py runserver
```

# Actualiser les contrats gRPC
Ajouter les fichiers .proto dans `web/cinemaApp/clients/protos`
```bash
cd web/cinemaApp/clients
pip install -r requirements.txt # IF NECESSARY
python3 -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. common.proto
python3 -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. booking.proto
python3 -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. showtime.proto
```
# Description des services
3004 -> USER
3003 -> SHOWTIME
3002 -> BOOKING
3001 -> MOVIE