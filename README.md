# IMT-FIL-A1-UE-AD-MIXTE - Cinema Management Microservices

**IMT-FIL-A1-UE-AD-MIXTE** - Application de Gestion de Cinéma

## 📚 Resources Pédagogiques

- [Tutoriel GraphQL par Helene Coullon](https://helene-coullon.fr/pages/ue-ad-fil-24-25/tuto-graphql/) - helene.coullon@imt-atlantique.fr
- [TP GraphQL et gRPC par Helene Coullon](https://helene-coullon.fr/pages/ue-ad-fil-24-25/tp-mixte/) - helene.coullon@imt-atlantique.fr

## 🎯 Objectifs

- Développer une application distribuée basée sur 4 micro-services pour la gestion d'une salle de cinéma.
- Comprendre les concepts de développement de micro-services.
- Maîtriser trois types d'API : REST, GraphQL et gRPC.
- Implémenter la communication inter-services et la persistance des données.

## 🏗️ Architecture

### Vue d'ensemble

L'application suit une architecture microservices avec une web application Django comme frontend. Les services communiquent via REST, GraphQL et gRPC.

```
┌─────────────┐
│   Web App   │ (Django - Port 8000)
│  (Frontend) │
└──────┬──────┘
       │
   ┌───┴────┬────────┬────────┐
   │        │        │        │
   ▼        ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌────────┐ ┌──────┐
│User  │ │Movie │ │Showtime│ │Booking
│(REST)│ │(GQL) │ │(gRPC)  │ │(gRPC) 
│:3004 │ │:3001 │ │:3003   │ │:3002
└──────┘ └──────┘ └────────┘ └──────┘
```

### Description des Services Microservices

| Service      | Port | Type API | Description                                         |
|--------------|------|----------|-----------------------------------------------------|
| **User**     | 3004 | REST     | Gestion des utilisateurs, authentification, profils |
| **Movie**    | 3001 | GraphQL  | Catalogue des films et acteurs, recherches avancées |
| **Showtime** | 3003 | gRPC     | Horaires de projection, gestion des séances         |
| **Booking**  | 3002 | gRPC     | Réservations de places, gestion des bookings        |

### Caractéristiques Clés

- **REST API** : Service utilisateurs pour CRUD simple.
- **GraphQL** : Service film avec requêtes flexibles et résolveurs.
- **gRPC** : Services haute performance (showtime, booking) avec sérialisation Protocol Buffers.
- **Communication Inter-Services** : Services peuvent se faire des requêtes mutuelles.
- **Persistance** : Fichiers JSON pour la base de données.
- **Containerisation** : Dockerfiles pour chaque service.

## 🚀 Guide de Démarrage

### Prérequis

- Python 3.8+
- pip
- virtualenv (optionnel, mais recommandé)

### 1. Installation des Dépendances

```bash
# Créer et activer un environnement virtuel (optionnel)
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances principales.
pip install -r requirements.txt
```

### 2. Lancer le Backend (Microservices)

Lancez tous les services automatiquement :

```bash
python3 start-services.py
```

Ou lancez les services individuellement (dans des terminaux séparés) :

```bash
# Terminal 1 - Service Movie (GraphQL)
cd movie
python3 main.py

# Terminal 2 - Service Showtime (gRPC)
cd showtime
python3 main.py

# Terminal 3 - Service Booking (gRPC)
cd booking
python3 main.py

# Terminal 4 - Service User (REST)
cd user
python3 main.py
```

### 3. Lancer le front (Application web Django)

```bash
cd web
python3 manage.py runserver
```

L'application sera accessible sur : `http://localhost:8000`

### 4. Arrêter les Services

```bash
python3 end-services.py
```

## 📝 Configuration et Utilisation

### Structure des Données

Les données sont stockées en JSON dans chaque dossier `data/` :

- `user/data/users.json` - Profils utilisateurs.
- `movie/data/movies.json` - Catalogue des films.
- `movie/data/actors.json` - Base des acteurs.
- `showtime/data/times.json` - Horaires et séances.
- `booking/data/bookings.json` - Réservations.

### Endpoints Principaux

#### Service User (REST)

```bash
# Récupérer tous les utilisateurs.
curl http://localhost:3004/users

# Récupérer un utilisateur spécifique.
curl http://localhost:3004/users/{id_or_name}

# Ajouter un utilisateur.
curl -X POST http://localhost:3004/adduser/{userid}

# Voir les bookings d'un utilisateur.
curl http://localhost:3004/users/{userid}/bookings
```

#### Service Movie (GraphQL)

```bash
# Endpoint GraphQL.
curl -X POST http://localhost:3001/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ movies { id title director rating } }"}'
```

#### Services Showtime et Booking (gRPC)

## 🔧 Mise à Jour des Contrats gRPC

Si modification des fichiers `.proto`, régénérez les bindings Python :

```bash
cd web/cinemaApp/clients
pip install -r requirements.txt

# Régénérer les fichiers Python pour chaque proto.
python3 -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. common.proto
python3 -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. booking.proto
python3 -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. showtime.proto
```

## 🐳 Déploiement avec Docker

Chaque service dispose d'un Dockerfile.

```bash
# Construire une image (exemple: booking)
docker build -t booking-service ./booking

# Exécuter le conteneur
docker run -p 3002:3002 booking-service
```

## 🔗 Communication Inter-Services

Les services communiquent entre eux via :

- **gRPC** : User → Booking (requêtes de bookings)
- **gRPC** : User → Showtime (requêtes d'horaires)
- **GraphQL/REST** : Booking/Showtime → Movie (requêtes d'infos films)
- **REST** : Frontend Django → tous les services

## 📚 Structure du Projet

```
IMT-FIL-A1-UE-AD-MIXTE/
├── user/                    # Service utilisateurs (REST)
│   ├── main.py
│   ├── clients/            # Clients pour appeler d'autres services
│   ├── data/
│   └── requirements.txt
├── movie/                   # Service films (GraphQL)
│   ├── main.py
│   ├── resolvers.py        # Résolveurs GraphQL
│   ├── movie.graphql       # Schéma GraphQL
│   ├── data/
│   └── requirements.txt
├── showtime/               # Service séances (gRPC)
│   ├── main.py
│   ├── proto/
│   ├── data/
│   └── requirements.txt
├── booking/                # Service réservations (gRPC)
│   ├── main.py
│   ├── proto/
│   ├── data/
│   └── requirements.txt
├── web/                    # Application Django (Frontend)
│   ├── manage.py
│   ├── cinemaApp/
│   └── archiD/            # Configuration Django
├── client/                 # Client de test
├── start-services.py      # Script pour démarrer tous les services
├── end-services.py        # Script pour arrêter tous les services
└── constants.py           # Constantes (ports, hosts)
```

## 📖 Documentation Supplémentaire

Pour plus d'informations sur les technologies utilisées :

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation Ariadne GraphQL](https://ariadnegraphql.org/)
- [Documentation gRPC Python](https://grpc.io/docs/languages/python/)
- [Documentation Django](https://docs.djangoproject.com/)