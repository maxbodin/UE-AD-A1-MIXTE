#!/bin/bash

# Définir les chemins des services
REST_SERVICE_PATH="./user"
GRAPHQL_SERVICE_PATH="/chemin/vers/service/graphql"
GRPC_SERVICE1_PATH="/chemin/vers/service/grpc1"
GRPC_SERVICE2_PATH="/chemin/vers/service/grpc2"

# Fonction pour démarrer un service
start_service() {
  local path=$1
  local name=$2
  echo "Démarrage du service $name..."
  cd "$path" || exit
  # Remplacez `go run main.go` par la commande appropriée pour démarrer le service
  python3 main.py &
}

# Démarrage des services
start_service "$REST_SERVICE_PATH" "REST"
start_service "$GRAPHQL_SERVICE_PATH" "GraphQL"
start_service "$GRPC_SERVICE1_PATH" "gRPC 1"
start_service "$GRPC_SERVICE2_PATH" "gRPC 2"

# Attente pour que les services démarrent (facultatif)
sleep 2

echo "Tous les services ont été démarrés."
