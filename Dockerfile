# Utiliser une image de base officielle Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste de l'application
COPY . .

# Exposer le port que l'application utilise
EXPOSE 5000

# Définir la commande de démarrage par défaut
CMD ["flask", "run", "--host=0.0.0.0"]
