# Utiliser une image Python officielle comme image de base
FROM python:3.11-slim

# Désactiver temporairement la vérification des signatures GPG et configurer apt pour ne pas utiliser de cache
RUN echo "Acquire::Check-Valid-Until \"false\";" > /etc/apt/apt.conf.d/10no-check-valid-until \
    && echo "Acquire::AllowInsecureRepositories \"true\";" > /etc/apt/apt.conf.d/10allow-insecure \
    && echo "Acquire::AllowDowngradeToInsecureRepositories \"true\";" >> /etc/apt/apt.conf.d/10allow-insecure \
    && echo "Acquire::http::No-Cache=True;" > /etc/apt/apt.conf.d/10no-cache \
    && echo "Acquire::http::Pipeline-Depth=0;" >> /etc/apt/apt.conf.d/10no-cache

# Mettre à jour, installer postgresql-client, nettoyer, et supprimer les configurations temporaires en une seule couche
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /etc/apt/apt.conf.d/10no-check-valid-until \
    && rm -f /etc/apt/apt.conf.d/10allow-insecure \
    && rm -f /etc/apt/apt.conf.d/10no-cache

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et installer les dépendances
COPY requirements.txt .
COPY wait-for-db.sh .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source de l'application
COPY . .

# Créer le dossier STATIC_ROOT
RUN mkdir -p staticfiles

# Installer psql
RUN apt-get update && apt-get install -y postgresql-client

# Rendre le script d'attente exécutable
RUN chmod +x wait-for-db.sh

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port sur lequel l'application Django s'exécutera
EXPOSE 8001

# Commande pour démarrer l'application
CMD ["./wait-for-db.sh", "db","python", "manage.py", "runserver", "0.0.0.0:8001"]