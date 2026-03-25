# ZenLog — API de suivi bien-être

ZenLog est une API REST de carnet de santé personnel permettant aux patients de suivre leurs indicateurs de bien-être (sommeil, humeur, énergie, douleur…) et aux coachs d'accompagner leurs patients en lecture seule.

## Besoin métier

Les patients atteints de maladies chroniques ou en parcours de bien-être ont besoin d'un outil simple pour enregistrer quotidiennement leurs indicateurs de santé. Les professionnels de santé (coachs) doivent pouvoir consulter ces données pour adapter leur accompagnement — sans jamais les modifier.

**Public cible** : patients en suivi bien-être, coachs/professionnels de santé, administrateurs de la plateforme.

## Architecture

Le projet suit une **architecture hexagonale** (Ports & Adapters) avec **Domain-Driven Design** (DDD) :

```
ZenLog/
├── domain/                  # Logique métier pure (aucune dépendance Django)
│   ├── entities/            # Entités du domaine (WellnessEntry, Indicator, Assignment, Trend)
│   ├── ports/               # Interfaces abstraites (ABC) — contrats du domaine
│   └── services/            # Services métier (TrackingService, CoachingService)
├── infrastructure/          # Couche technique (Django, DRF, PostgreSQL)
│   ├── models.py            # Modèles Django (ORM)
│   ├── repositories/        # Implémentations des ports (adapters Django)
│   ├── views/               # ViewSets et APIViews (DRF)
│   ├── serializers/         # Validation et sérialisation (Serializer purs)
│   └── permissions/         # Permissions par rôle (IsPatient, IsCoach, IsAdmin)
├── config/                  # Configuration Django (settings, urls, wsgi)
├── tests/
│   ├── domain/              # Tests unitaires du domaine (mocks, pas de BDD)
│   └── infrastructure/      # Tests d'intégration API (factories, BDD test)
└── zenlog_doc/              # Documentation projet (JUSTIFICATION_PROJET.md)
```

**Deux Bounded Contexts** :
- **Wellness Tracking** (contexte cœur) : CRUD des entrées bien-être par le patient
- **Coaching** (contexte support) : lecture seule des données patient par le coach assigné

## Stack technique

| Composant | Technologie | Justification |
|---|---|---|
| Langage | Python 3.12+ | Écosystème data/santé, typage natif |
| Framework | Django 6 + DRF 3.17 | Robuste, sécurisé, ORM mature |
| BDD | PostgreSQL 15+ | Contraintes avancées, UUID natif |
| Auth | JWT (SimpleJWT) | Stateless, adapté mobile/SPA |
| Doc API | drf-spectacular (OpenAPI 3.0) | Swagger UI auto-généré |
| Doc code | pdoc | Documentation Python depuis les docstrings PEP 257 |
| Qualité | ruff, pre-commit, pytest | Lint + format + tests automatisés |
| CORS | django-cors-headers | Sécurisation cross-origin |
| BDD prod | Neon (PostgreSQL serverless) | Free tier, compatible Django ORM, SSL natif |
| Hébergement | Azure App Service (F1) | PaaS managé, CI/CD via GitHub Actions |
| Serveur WSGI | Gunicorn + WhiteNoise | Production-ready, fichiers statiques intégrés |

## Prérequis

- Python 3.12+
- PostgreSQL 15+
- Git

## Installation rapide

```bash
# 1. Cloner le repo
git clone https://github.com/<votre-repo>/ZenLog.git
cd ZenLog

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos valeurs (SECRET_KEY, DB_PASSWORD, etc.)

# 5. Créer la base de données PostgreSQL
# psql -U postgres
# CREATE DATABASE zenlog;
# CREATE USER zenlog WITH PASSWORD 'votre-mot-de-passe';
# GRANT ALL PRIVILEGES ON DATABASE zenlog TO zenlog;

# 6. Appliquer les migrations
python manage.py migrate

# 7. Lancer le serveur
python manage.py runserver
```

L'API est accessible sur `https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/`.
La documentation Swagger est sur `https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/docs/`.

## API en production

L'API est déployée sur Azure App Service avec une base PostgreSQL hébergée sur Neon :

**Swagger UI** : [https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/docs/](https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/docs/)

**Base URL** : `https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/`

Le déploiement est automatisé via GitHub Actions : chaque push sur `main` déclenche un build + deploy sur Azure.

## Documentation du code

La documentation du code source est générée automatiquement depuis les docstrings (PEP 257) avec **pdoc**.

**En production** : [`/api/code-docs/`](https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/code-docs/)

**En local** :

```bash
# Générer le HTML statique dans docs/api/
python docs/generate.py

# Serveur live avec rechargement automatique (http://localhost:8080)
python docs/generate.py --live
```

La documentation couvre les entités du domaine, les ports (interfaces), les services métier et la configuration infrastructure.

## Lancer les tests

```bash
# Tous les tests (60 tests)
pytest -v

# Tests du domaine uniquement (24 tests, pas de BDD)
pytest tests/domain/ -v

# Tests d'intégration API (36 tests, nécessite PostgreSQL)
pytest tests/infrastructure/ -v

# Avec couverture
pytest --cov=domain --cov=infrastructure --cov-report=term-missing
```

## Guide de test rapide de l'API

Voici comment tester tous les endpoints en quelques minutes avec `curl` (ou depuis Swagger UI sur `/api/docs/`).

> **URL de base** :
> - **Production** : `https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net`
> - **Local** : `https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net`
>
> Les exemples ci-dessous utilisent l'URL de production. Pour tester en local, remplacez l'URL de base.

### 1. Créer un compte patient

```bash
curl -X POST https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "patient@test.com", "username": "patient1", "password": "SecurePass123!", "role": "patient"}'
```

### 2. Obtenir un token JWT

```bash
curl -X POST https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "patient@test.com", "password": "SecurePass123!"}'
```

Réponse : `{"access": "<TOKEN>", "refresh": "<REFRESH>"}`.
Utilisez le token `access` dans les requêtes suivantes.

### 3. Créer un indicateur (en tant qu'admin)

```bash
# D'abord créer un admin
curl -X POST https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "username": "admin1", "password": "SecurePass123!", "role": "admin"}'

# Obtenir son token
curl -X POST https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "SecurePass123!"}'

# Créer l'indicateur (remplacer <ADMIN_TOKEN>)
curl -X POST https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/wellness/indicators/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -d '{"name": "Sommeil", "unit": "/10", "min_value": 1, "max_value": 10}'
```

### 4. Enregistrer une entrée bien-être (en tant que patient)

```bash
curl -X POST https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/wellness/entries/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <PATIENT_TOKEN>" \
  -d '{"indicator_id": "<UUID_INDICATEUR>", "date": "2026-03-23", "value": 7.5, "note": "Bonne nuit"}'
```

### 5. Lister mes entrées

```bash
curl -H "Authorization: Bearer <PATIENT_TOKEN>" \
  "https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/wellness/entries/"
```

Filtres disponibles : `?indicator_id=<UUID>&date_from=2026-03-01&date_to=2026-03-31`

### 6. Consulter les tendances

```bash
curl -H "Authorization: Bearer <PATIENT_TOKEN>" \
  "https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/wellness/trends/?indicator_id=<UUID>&days=7"
```

### 7. Tester le coaching (coach lit les données patient)

```bash
# Créer un coach
curl -X POST https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "coach@test.com", "username": "coach1", "password": "SecurePass123!", "role": "coach"}'

# Obtenir son token
curl -X POST https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "coach@test.com", "password": "SecurePass123!"}'

# Lister les patients assignés (nécessite une assignation en BDD)
curl -H "Authorization: Bearer <COACH_TOKEN>" \
  "https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/coaching/patients/"

# Lire les entrées d'un patient assigné
curl -H "Authorization: Bearer <COACH_TOKEN>" \
  "https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/coaching/patients/<PATIENT_UUID>/entries/"
```

### 8. Tester la sécurité

```bash
# Sans token → 401
curl https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/wellness/entries/

# Patient essaie de créer un indicateur → 403
curl -X POST https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/wellness/indicators/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <PATIENT_TOKEN>" \
  -d '{"name": "hack", "unit": "x", "min_value": 0, "max_value": 10}'

# Injection SQL dans les dates → 200 (ignoré) ou 400
curl -H "Authorization: Bearer <PATIENT_TOKEN>" \
  "https://zenlog-fpbmd5badufda0ep.francecentral-01.azurewebsites.net/api/wellness/entries/?date_from='; DROP TABLE--"
```

## Endpoints API

| Méthode | Endpoint | Rôle requis | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | Aucun | Inscription |
| POST | `/api/auth/token/` | Aucun | Obtenir JWT (access + refresh) |
| POST | `/api/auth/token/refresh/` | Aucun | Rafraîchir le token |
| GET | `/api/wellness/entries/` | Patient | Lister mes entrées |
| POST | `/api/wellness/entries/` | Patient | Créer une entrée |
| GET | `/api/wellness/entries/{id}/` | Patient | Détail d'une entrée |
| PATCH | `/api/wellness/entries/{id}/` | Patient | Modifier une entrée |
| GET | `/api/wellness/indicators/` | Authentifié | Lister les indicateurs |
| POST | `/api/wellness/indicators/` | Admin | Créer un indicateur |
| GET | `/api/wellness/trends/` | Patient | Tendances sur N jours |
| GET | `/api/coaching/patients/` | Coach | Lister mes patients assignés |
| GET | `/api/coaching/patients/{id}/entries/` | Coach | Entrées d'un patient assigné |
| GET | `/api/docs/` | Aucun | Swagger UI |
| GET | `/api/code-docs/` | Aucun | Documentation code (pdoc) |
| GET | `/api/schema/` | Aucun | Schéma OpenAPI JSON |

## Sécurité

- **Authentification** : JWT (access 15min, refresh 24h, rotation automatique)
- **Autorisation** : permissions par rôle (Patient, Coach, Admin) sur chaque endpoint
- **Rate limiting** : 5 req/min sur `/auth/`, 60 req/min sur `/wellness/`
- **CORS** : origines autorisées configurables via `CORS_ALLOWED_ORIGINS`
- **Isolation des données** : un patient ne voit que ses propres entrées
- **Validation** : dates ISO, password validators Django, protection injection SQL
- **Headers** : `X-Content-Type-Options: nosniff`, `X-Frame-Options`

## Design patterns

- **Repository Pattern** : ports abstraits (ABC) dans `domain/ports/`, implémentations Django dans `infrastructure/repositories/`
- **Dependency Injection** : les services métier reçoivent leurs dépendances par constructeur
- **Interface Segregation** : `PatientEntryReader` (read-only coaching) vs `WellnessEntryRepository` (CRUD)
- **Service Pattern** : `TrackingService` et `CoachingService` orchestrent la logique métier
- **Entity Pattern** : objets du domaine avec comportement et identité
- **Guard Clauses** : validation défensive en entrée des services

## Variables d'environnement

| Variable | Description | Défaut |
|---|---|---|
| `SECRET_KEY` | Clé secrète Django | `fallback-dev-key` |
| `DEBUG` | Mode debug | `False` |
| `DATABASE_URL` | URL complète PostgreSQL (prod/Neon) | — |
| `DB_NAME` | Nom BDD PostgreSQL (dev local) | `zenlog` |
| `DB_USER` | Utilisateur BDD (dev local) | `zenlog` |
| `DB_PASSWORD` | Mot de passe BDD (dev local) | — |
| `DB_HOST` | Hôte BDD (dev local) | `localhost` |
| `DB_PORT` | Port BDD (dev local) | `5432` |
| `ALLOWED_HOSTS` | Domaines autorisés | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Origines CORS (séparées par `,`) | — |

> **Note** : en production, `DATABASE_URL` est prioritaire. Si défini, les variables `DB_*` individuelles sont ignorées. En développement local, utilisez les variables `DB_*` via le fichier `.env`.

## Déploiement

### Architecture de production

```
GitHub (push main) → GitHub Actions (CI/CD) → Azure App Service (Python 3.12, Gunicorn)
                                                        ↓
                                               Neon PostgreSQL (serverless, Frankfurt)
```

### Pourquoi Neon plutôt qu'Azure Database for PostgreSQL ?

Azure Database for PostgreSQL Flexible Server coûte minimum ~12€/mois même en tier Burstable. Pour un MVP en phase d'évaluation, Neon offre un PostgreSQL serverless gratuit (0.5 GB, région Frankfurt) entièrement compatible avec Django ORM. La migration vers Azure Database for PostgreSQL est prévue en production avec backups automatiques (7j) et chiffrement AES-256.

### CI/CD

Chaque push sur `main` déclenche automatiquement via GitHub Actions :
1. Installation des dépendances
2. Collecte des fichiers statiques
3. Déploiement sur Azure App Service via publish profile

## Licence

MIT — voir [LICENSE](LICENSE).
