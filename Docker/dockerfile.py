# Utilisez une image de base Python
FROM python:3.8-slim
# Définir le répertoire de travail
WORKDIR /app
# Copier les fichiers de dépendances
COPY requirements.txt requirements.txt
# Installer les dépendances
RUN pip install -r requirements.txt
# Copier le reste des fichiers de l'application
COPY . .
# Exposer le port que l'application utilisera
EXPOSE 5000
# Définir la commande par défaut pour exécuter l'application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]