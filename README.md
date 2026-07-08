#  SecureAuth API — Authentification JWT avec Django REST Framework

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![JWT](https://img.shields.io/badge/JWT-Auth-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![IBM Cloud](https://img.shields.io/badge/IBM%20Cloud-deployed-054ADA?logo=ibmcloud)

Système d'authentification complet avec JWT, gestion des rôles, refresh token et déploiement sur IBM Cloud.

---

##  Fonctionnalités

- ✅ Inscription et connexion avec JWT
- ✅ Refresh token et révocation
- ✅ Gestion des rôles (admin, manager, utilisateur)
- ✅ Réinitialisation de mot de passe par email
- ✅ Profil utilisateur complet
- ✅ Journalisation des connexions
- ✅ **Déployé sur IBM Cloud (IBM Code Engine)**


## Stack technique

| Technologie | Usage |
|---|---|
| Django 4.2 + DRF | Backend API |
| SimpleJWT | Authentification JWT |
| PostgreSQL (IBM Cloud) | Base de données |
| IBM Code Engine | Déploiement serverless |
| IBM Container Registry | Images Docker |
| SendGrid | Envoi d'emails |

---

## Installation locale

```bash
git clone https://github.com/monas-svg/secure-auth-api.git
cd secure-auth-api
python -m venv env && source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

---

## Endpoints

| Méthode | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Créer un compte |
| POST | `/api/auth/login/` | Connexion (retourne JWT) |
| POST | `/api/auth/token/refresh/` | Rafraîchir le token |
| POST | `/api/auth/logout/` | Déconnexion (blacklist token) |
| GET | `/api/auth/profile/` | Profil utilisateur connecté |
| PUT | `/api/auth/profile/update/` | Modifier le profil |
| POST | `/api/auth/password/reset/` | Demande reset mot de passe |
| POST | `/api/auth/password/confirm/` | Confirmer le nouveau mot de passe |

---

## Déploiement IBM Cloud

```bash
# Build et push de l'image
ibmcloud login
ibmcloud cr login
docker build -t us.icr.io/<namespace>/secure-auth-api .
docker push us.icr.io/<namespace>/secure-auth-api

# Déploiement sur Code Engine
ibmcloud ce application create \
  --name secure-auth-api \
  --image us.icr.io/<namespace>/secure-auth-api \
  --port 8000 \
  --env-from-secret app-secrets
```

---

## Exemple d'utilisation

```bash
# Inscription
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@email.com", "password": "SecurePass123!"}'

# Connexion
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "john@email.com", "password": "SecurePass123!"}'
```
