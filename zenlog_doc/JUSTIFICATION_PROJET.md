# ZenLog — Carnet de suivi bien-être

## 1. Introduction et besoin métier

### Le problème

De nombreux particuliers souhaitent suivre au quotidien leurs indicateurs de bien-être — humeur, qualité du sommeil, activité physique, hydratation — afin de mieux comprendre leurs habitudes et améliorer leur santé globale. Aujourd'hui, ces suivis se font souvent sur des carnets papier, des fichiers Excel partagés par email, ou des applications grand public qui monétisent les données personnelles de santé.

Ces approches posent plusieurs problèmes concrets :

- **Perte de données** : un carnet papier se perd, un fichier Excel se corrompt ou est supprimé accidentellement.
- **Absence de confidentialité** : les fichiers Excel circulent par email sans chiffrement. Les applications gratuites revendent fréquemment les données à des tiers.
- **Pas de collaboration sécurisée** : lorsqu'un coach bien-être ou un professionnel de santé souhaite consulter les données de son client pour adapter ses recommandations, il n'existe pas de canal sécurisé et structuré. Les échanges se font par messages, captures d'écran ou documents non protégés.
- **Aucune vision d'ensemble** : sans agrégation ni historique structuré, il est difficile de détecter des tendances (dégradation du sommeil sur plusieurs semaines, corrélation humeur/activité physique, etc.).

### La solution proposée

**ZenLog** est une API back-end sécurisée permettant :

- À un **utilisateur** de saisir quotidiennement ses indicateurs de bien-être et de consulter son historique personnel.
- À un **coach** référent d'accéder en lecture seule aux données de ses clients affectés, afin d'adapter ses recommandations de manière éclairée.
- À un **administrateur** de gérer les comptes, les affectations coach/client et les types d'indicateurs.

L'objectif est de fournir un module back-end autonome, sécurisé et documenté, prêt à être consommé par une application mobile ou web.

### Public cible

- **Utilisateurs finaux** : particuliers souhaitant suivre leur bien-être au quotidien (25-55 ans, sensibilisés à la santé préventive).
- **Coachs bien-être** : professionnels indépendants (nutritionnistes, coachs sportifs, sophrologues) qui accompagnent des clients et ont besoin de données fiables pour personnaliser leurs conseils.
- **Administrateurs** : gestionnaires de la plateforme, responsables de la cohérence des données et de la gestion des comptes.

### Valeur ajoutée

- **Confidentialité garantie** : les données de santé sont protégées par une authentification forte (JWT), un contrôle d'accès strict par rôle, et un transport chiffré (HTTPS). Cela répond aux exigences du RGPD concernant les données de santé (catégorie spéciale, article 9).
- **Collaboration structurée** : le lien coach/client est formalisé et contrôlé — un coach ne voit que les données de ses clients affectés, jamais celles d'autres utilisateurs.
- **Historique fiable** : les données sont stockées en base relationnelle avec intégrité référentielle, sauvegardes et migrations versionnées. Fini les fichiers perdus.
- **Extensibilité** : les types d'indicateurs sont paramétrables (on peut ajouter "stress", "douleur", "alimentation" sans modifier le code), et l'API documentée (OpenAPI/Swagger) permet de brancher n'importe quel front-end.

---

## 2. Périmètre fonctionnel

### Ce que couvre le MVP (Minimum Viable Product)

| Fonctionnalité | Cas d'usage | Rôle concerné |
|---|---|---|
| Inscription et connexion | Un utilisateur crée son compte et se connecte de manière sécurisée | Tous |
| Gestion du profil | L'utilisateur peut consulter et modifier ses informations personnelles | Tous |
| Saisie quotidienne | L'utilisateur enregistre ses indicateurs du jour (humeur, sommeil, activité, hydratation) | Utilisateur |
| Consultation de l'historique | L'utilisateur consulte ses entrées passées avec filtrage par date et par type d'indicateur | Utilisateur |
| Agrégation et tendances | L'utilisateur consulte ses moyennes sur 7 et 30 jours pour détecter des tendances | Utilisateur |
| Consultation coach | Le coach consulte les données de ses clients affectés (lecture seule) | Coach |
| Affectation coach/client | L'administrateur affecte un coach à un ou plusieurs clients | Administrateur |
| Gestion des indicateurs | L'administrateur ajoute ou modifie les types d'indicateurs disponibles | Administrateur |
| Documentation API | Tous les endpoints sont documentés via Swagger/OpenAPI avec exemples d'appels | Technique |

### Ce qui est hors périmètre (v1)

- Front-end (web ou mobile) — ZenLog est un module back-end API-only.
- Notifications push ou email.
- Système de messagerie intégrée entre coach et client.
- Gestion de paiements ou d'abonnements.
- Export PDF des données.
- Fonctionnalités sociales (partage entre utilisateurs, communauté).

Ce périmètre est volontairement restreint pour respecter le principe **KISS** (Keep It Simple, Stupid) et livrer un MVP fonctionnel, sécurisé et documenté en 3 jours.

---

## 3. Choix techniques et justifications

Chaque choix technique ci-dessous est motivé par un besoin métier ou un contexte d'usage identifié.

### 3.1 Langage : Python 3.12+

| Besoin métier | Justification technique |
|---|---|
| Développement rapide en solo (3 jours) | Python offre une syntaxe concise et un écosystème riche de bibliothèques, permettant un prototypage rapide sans sacrifier la lisibilité. |
| Maintenabilité à long terme | Le typage progressif (type hints) et les outils de linting (flake8, mypy) facilitent la relecture et la reprise du code par un tiers. |
| Compétence disponible | Maîtrisé dans le cadre de la formation, ce qui minimise le temps d'apprentissage et les risques de blocage. |

### 3.2 Framework : Django 5.x + Django REST Framework (DRF)

| Besoin métier | Justification technique |
|---|---|
| Authentification et gestion des rôles (3 profils distincts) | Django intègre nativement un système d'authentification robuste et extensible (modèle User, groupes, permissions). Couplé à SimpleJWT, il fournit une auth JWT sans dépendance tierce fragile. |
| Modélisation de données relationnelles (patients, coachs, entrées, indicateurs) | L'ORM Django gère nativement les relations (ForeignKey, ManyToMany), les contraintes d'intégrité, et génère les migrations de schéma automatiquement. Cela évite d'écrire du SQL brut pour le DDL et garantit la cohérence du schéma en production. |
| API REST documentée (exigence du cahier des charges) | DRF fournit des serializers, des viewsets, une pagination et un filtrage intégrés. Couplé à drf-spectacular, il génère automatiquement une documentation OpenAPI 3.0 / Swagger UI à jour. |
| Admin et monitoring basique | L'interface d'administration Django permet aux administrateurs de gérer les comptes, les affectations et les indicateurs sans développement front-end spécifique. |
| Délai court (3 jours, solo) | L'approche "batteries included" de Django réduit considérablement le boilerplate par rapport à Flask où il faudrait configurer manuellement l'ORM (SQLAlchemy), les migrations (Alembic), l'auth, la sérialisation et la documentation. |

**Pourquoi pas Flask ?** Flask aurait offert plus de flexibilité architecturale, mais au prix d'un temps de configuration significatif. Sur un projet solo de 3 jours où la sécurité et la documentation sont des exigences fortes, la productivité de Django + DRF est un avantage décisif. Le compromis flexibilité/productivité penche clairement vers Django dans ce contexte.

### 3.3 Base de données : PostgreSQL 15+

| Besoin métier | Justification technique |
|---|---|
| Données de santé sensibles nécessitant intégrité et fiabilité | PostgreSQL est conforme ACID, garantissant que chaque saisie est soit complètement enregistrée, soit pas du tout (pas de données corrompues en cas de crash). |
| Requêtes d'agrégation (moyennes, tendances sur 7/30 jours) | PostgreSQL excelle sur les fonctions d'agrégation et les window functions, essentielles pour calculer des tendances sans surcharger le serveur applicatif. |
| Contraintes d'accès au niveau base | PostgreSQL supporte le Row-Level Security (RLS), permettant d'ajouter une couche de sécurité supplémentaire directement en base si nécessaire (défense en profondeur). |
| Déploiement cloud (Azure) | Azure Database for PostgreSQL est un service managé disponible en free tier, avec sauvegardes automatiques, chiffrement au repos et haute disponibilité configurable. Cela répond aux exigences de disponibilité et de résilience du cahier des charges. |
| Évolutivité | Si le nombre d'utilisateurs croît, PostgreSQL supporte la réplication, le partitionnement et l'indexation avancée, contrairement à SQLite qui est limité à un seul writer. |

**Pourquoi pas SQLite ?** SQLite est pratique en développement local mais ne supporte pas les accès concurrents en écriture, n'offre pas de chiffrement au repos natif, et n'est pas adapté à un déploiement cloud multi-utilisateurs. Pour une application manipulant des données de santé en production, PostgreSQL est le choix responsable.

### 3.4 Authentification : JWT via djangorestframework-simplejwt

| Besoin métier | Justification technique |
|---|---|
| Trois rôles distincts avec des droits différents | JWT embarque les claims du rôle dans le token, permettant une vérification stateless côté API sans requête BDD à chaque appel. |
| API stateless consommable par un futur front mobile | JWT est le standard de facto pour l'authentification d'API REST consommées par des clients mobiles ou SPA, contrairement aux sessions côté serveur qui nécessitent la gestion de cookies. |
| Sécurité des sessions | Les tokens ont une durée de vie courte (access : 15 min, refresh : 24h), limitant la fenêtre d'exploitation en cas de fuite. La rotation des refresh tokens ajoute une couche supplémentaire. |

### 3.5 Documentation API : drf-spectacular (OpenAPI 3.0)

| Besoin métier | Justification technique |
|---|---|
| Exigence de documentation API dans le cahier des charges | drf-spectacular génère automatiquement un schéma OpenAPI 3.0 à partir des serializers et viewsets DRF, garantissant que la doc est toujours synchronisée avec le code. |
| Faciliter l'intégration par un futur front-end | Swagger UI (inclus) permet à un développeur front de tester les endpoints directement depuis le navigateur, avec des exemples de requêtes et de réponses. |

### 3.6 Déploiement : Azure App Service + Azure Database for PostgreSQL

| Besoin métier | Justification technique |
|---|---|
| Disponibilité et redondance (exigence cahier des charges) | Azure App Service offre un SLA de 99.95% avec redondance de zone configurable. Azure Database for PostgreSQL inclut des sauvegardes automatiques (rétention 7 jours en free tier). |
| Données de santé : chiffrement au repos et en transit | Azure chiffre les données au repos par défaut (AES-256) et force TLS 1.2 pour le transit. Cela répond aux exigences RGPD sans configuration supplémentaire. |
| Monitoring et logging | Azure Application Insights s'intègre nativement avec Django pour collecter métriques, traces et logs applicatifs. |
| Compte étudiant disponible | Le free tier Azure (200$ de crédits) permet un déploiement réel sans coût, conformément à la recommandation du cahier des charges. |

### 3.7 Gestion de code : Git + GitHub Flow (PR) simplifié

| Besoin métier | Justification technique |
|---|---|
| Traçabilité des décisions (exigence cahier des charges) | Commits atomiques et signés, messages expliquant le "pourquoi" de chaque changement. |
| Qualité du code en solo | Branches feature avec auto-review via Pull Request avant merge dans main. Cela force la relecture même en solo. |
| CI minimale | GitHub Actions pour lancer les tests automatiquement à chaque push (cycle TDD visible). |

**Pourquoi GitHub Flow (PR) plutôt que trunk-based development ?**

Le trunk-based development consiste à pousser directement sur la branche principale, sans passer par des branches feature ni des pull requests. C'est une approche adaptée aux équipes expérimentées disposant d'un pipeline CI/CD mature avec feature flags et déploiement continu. Dans le contexte de ZenLog, trois raisons justifient le choix de GitHub Flow avec PR :

1. **Traçabilité pour l'évaluation** : chaque PR crée un historique documenté des décisions techniques. Le formateur peut voir exactement ce qui a été fait, quand, et pourquoi — avec le contexte de relecture. Un push direct sur main ne laisse qu'une liste de commits sans ce niveau de documentation.

2. **CI comme filet de sécurité** : GitHub Actions lance les tests automatiquement sur chaque PR avant le merge. La branche main reste donc toujours dans un état stable et déployable. En trunk-based, un push cassé irait directement en production sans validation préalable — risqué sans feature flags ni rollback automatisé.

3. **Cohérence avec la méthodologie TDD** : une PR par user story rend visible le cycle red-green-refactor. Les tests apparaissent dans les premiers commits de la branche (red), le code d'implémentation suit (green), puis le refactor. Cette progression est évaluable et démontre la rigueur de la démarche.

**Le compromis accepté** : les PR ajoutent une étape de cérémonie (créer la branche, ouvrir la PR, merger). En solo, cette cérémonie est minimale (pas de reviewer à attendre) et le bénéfice en traçabilité, en qualité et en démonstration de la démarche professionnelle compense largement le coût.

**Workflow concret** :

```
main (toujours stable, déployable)
  └── feature/US-1-create-wellness-entry   ← branche feature
        ├── commit: test: add test for create_entry()        [RED]
        ├── commit: feat: implement create_entry()            [GREEN]
        ├── commit: refactor: extract validation logic        [REFACTOR]
        └── PR → merge into main (après CI verte)
```

### 3.8 Outillage qualité : Linter, Hooks et CI

#### 3.8.1 Linter et formatter : Ruff

| Besoin métier | Justification technique |
|---|---|
| Code lisible et maintenable (critère d'évaluation) | Un linter garantit le respect des conventions de style (PEP 8) et détecte les erreurs courantes avant même l'exécution. |
| Cohérence du code en solo | Sans linter, le style dérive au fil du temps. Ruff impose une norme uniforme sur tout le projet. |
| Productivité (3 jours) | Ruff remplace à lui seul flake8 (lint), isort (tri des imports) et black (formatage) en un seul outil, avec des performances 10 à 100 fois plus rapides. Moins d'outils à configurer = plus de temps sur le code métier. |

**Pourquoi Ruff plutôt que flake8 + black ?** Dans un projet avec un délai de 3 jours, chaque minute de configuration compte. Ruff est un outil unique écrit en Rust qui combine lint, formatage et tri des imports. Il se configure dans un seul fichier (`ruff.toml`) au lieu de trois (`setup.cfg`, `pyproject.toml`, `.isort.cfg`). De plus, Ruff est en train de devenir le standard de facto dans l'écosystème Python — l'adopter montre une veille technologique active.

**Règles activées** :

- `E/W` : conventions PEP 8 (erreurs et warnings)
- `F` : détection d'erreurs logiques (variables non utilisées, imports manquants)
- `I` : tri automatique des imports (stdlib → third-party → first-party)
- `N` : conventions de nommage PEP 8 (classes en PascalCase, fonctions en snake_case)
- `UP` : modernisation automatique du code vers Python 3.12+
- `B` : détection de bugs courants (flake8-bugbear)
- `SIM` : simplification du code (conditions inutilement complexes, etc.)

#### 3.8.2 Conventional Commits

| Besoin métier | Justification technique |
|---|---|
| Historique Git lisible pour l'évaluation | Chaque commit suit un format normé `type(scope): description` qui permet de comprendre immédiatement la nature du changement. |
| Cohérence avec le TDD | Les types `test:`, `feat:`, `refactor:` rendent le cycle red-green-refactor visible directement dans le log Git. |
| Automatisation possible | Le format normé permet de générer automatiquement un changelog et de versionner sémantiquement (même si non utilisé en MVP). |

**Types de commits utilisés dans ZenLog** :

- `feat` : nouvelle fonctionnalité métier (ex: `feat(domain): add Indicator entity`)
- `test` : ajout ou modification de tests (ex: `test(domain): add validation tests for WellnessEntry`)
- `fix` : correction de bug
- `refactor` : restructuration du code sans changement fonctionnel
- `chore` : outillage, config, dépendances (ex: `chore: configure Ruff linter`)
- `docs` : documentation

**Outil** : Commitizen vérifie automatiquement le format du message à chaque commit via un hook Git. Un commit avec un message mal formaté est rejeté avant d'être enregistré.

#### 3.8.3 Pre-commit hooks

| Besoin métier | Justification technique |
|---|---|
| Qualité garantie à chaque commit | Les hooks s'exécutent automatiquement avant chaque commit. Impossible de pousser du code non conforme par oubli. |
| Détecter les problèmes au plus tôt | Un problème détecté au commit coûte 0 minute à corriger. Le même problème détecté en CI coûte un cycle push-wait-fix-push. Sur 3 jours, chaque cycle économisé compte. |

**Hooks configurés** :

1. `ruff` (lint) : vérifie et corrige automatiquement les erreurs de style
2. `ruff-format` : formate le code automatiquement
3. `commitizen` (commit-msg) : valide le format du message de commit

**Pourquoi des hooks locaux en plus de la CI ?** La CI (GitHub Actions) est le filet de sécurité final, mais elle intervient après le push — il faut attendre le retour. Les hooks locaux donnent un feedback immédiat, avant même que le commit soit créé. Les deux sont complémentaires : les hooks préviennent les erreurs, la CI les garantit.

#### 3.8.4 CI — GitHub Actions

| Besoin métier | Justification technique |
|---|---|
| Branche main toujours stable (exigence du workflow PR) | La CI bloque le merge d'une PR si le lint ou les tests échouent. Impossible de casser main par accident. |
| TDD vérifiable | La CI exécute les tests automatiquement sur chaque PR. Le formateur peut voir que les tests passent à chaque étape du développement. |
| Déploiement en confiance | Quand viendra le déploiement Azure (jour 3), la CI aura déjà validé que le code est stable. |

**Pipeline CI configuré** :

```
PR ouverte / push sur main
    ├── Job: lint
    │   ├── ruff check .
    │   └── ruff format --check .
    │
    └── Job: test
        ├── Service PostgreSQL (conteneur)
        ├── pytest tests/domain/ -v        (tests domaine, rapides)
        └── pytest tests/infrastructure/ -v (tests intégration, avec BDD)
```

**Pourquoi deux jobs séparés (lint + test) ?** Si le lint échoue, inutile de lancer les tests — c'est du temps de CI économisé. Les deux jobs tournent en parallèle : le feedback est plus rapide.

### 3.9 Structure du projet : architecture hexagonale en pratique

La structure de fichiers du projet reflète directement l'architecture hexagonale documentée en section 4.6. Le point clé : le dossier `domain/` est un package Python **indépendant**, au même niveau que l'app Django `infrastructure/`, jamais à l'intérieur.

```
ZenLog/                            # Racine du repo
├── config/                        # Configuration Django
│   ├── settings.py                # Paramètres (BDD, DRF, JWT, Swagger)
│   ├── urls.py                    # Routage racine
│   └── wsgi.py
│
├── domain/                        # DOMAINE — pure Python, 0 import Django
│   ├── entities/                  # Entités et value objects
│   ├── services/                  # Services métier (use cases)
│   └── ports/                     # Interfaces abstraites (ABC)
│       ├── wellness_entry_repository.py
│       ├── indicator_repository.py
│       ├── assignment_repository.py
│       └── patient_entry_reader.py   # Port read-only (BC Coaching)
│
├── infrastructure/                # INFRASTRUCTURE — app Django
│   ├── models.py                  # ORM models (implémentation BDD)
│   ├── repositories/              # Implémentation des ports
│   ├── serializers/               # Sérialisation API (DRF)
│   ├── views/                     # Contrôleurs HTTP (DRF viewsets)
│   ├── permissions/               # Permissions par rôle
│   ├── urls.py                    # Routage API
│   ├── admin.py                   # Interface admin Django
│   └── apps.py                    # Configuration app Django
│
├── tests/
│   ├── domain/                    # Tests domaine (pytest pur, pas de BDD)
│   └── infrastructure/            # Tests intégration (pytest-django + BDD)
│
├── .github/workflows/ci.yml       # Pipeline CI
├── .pre-commit-config.yaml        # Hooks pre-commit
├── ruff.toml                      # Configuration linter
├── .cz.toml                       # Configuration conventional commits
├── pytest.ini                     # Configuration pytest
├── requirements.txt               # Dépendances Python
├── .env                           # Variables d'environnement (non versionné)
└── .gitignore
```

**Justification de la séparation `domain/` hors de `infrastructure/`** :

Le dossier `domain/` ne doit contenir aucun `import django`. C'est la preuve concrète de l'architecture hexagonale : si on supprimait Django demain pour le remplacer par FastAPI, seul le dossier `infrastructure/` serait impacté. Le domaine resterait intact. Cette séparation est vérifiable : les tests dans `tests/domain/` s'exécutent sans `django.setup()` — c'est du pytest pur.

---

## 4. Approche DDD — Bounded Contexts et modèle du domaine

L'approche DDD (Domain-Driven Design) impose de penser le domaine métier **avant** toute considération technique. Le code métier doit pouvoir exister indépendamment du framework (Django, Flask, ou autre). C'est le principe de l'architecture hexagonale : le domaine est au centre, la technique (API, BDD, framework) est en périphérie et s'y adapte.

### 4.1 Langage ubiquitaire (Ubiquitous Language)

Avant de découper en bounded contexts, voici les termes que tout membre de l'équipe (développeur, coach, product owner) doit utiliser de manière uniforme. La colonne "Nom dans le code" indique le terme anglais utilisé dans les classes, variables et fichiers — convention standard pour un code maintenable à l'international.

| Terme métier (FR) | Nom dans le code (EN) | Définition |
|---|---|---|
| **Patient** | `Patient` | Personne qui suit quotidiennement son bien-être. C'est l'utilisateur principal du système. |
| **Coach** | `Coach` | Professionnel du bien-être qui accompagne un ou plusieurs patients. Il consulte leurs données pour adapter ses recommandations. |
| **Indicateur** | `Indicator` | Dimension de bien-être mesurable (humeur, sommeil, activité physique, hydratation). Chaque indicateur a un nom, une unité et une plage de valeurs acceptables. |
| **Entrée bien-être** | `WellnessEntry` | Enregistrement quotidien d'un patient pour un indicateur donné. Contient une valeur numérique, une note libre optionnelle et une date. |
| **Affectation** | `Assignment` | Relation formelle entre un coach et un patient. Tant que l'affectation est active, le coach peut consulter les données du patient. |
| **Tendance** | `Trend` | Agrégation des entrées d'un patient sur une période (7 jours, 30 jours) permettant de détecter des évolutions. |

### 4.2 Bounded Contexts

Le domaine ZenLog se décompose en **deux bounded contexts métier** et un **contexte support technique** :

```
┌──────────────────────────────────────────────────────────────────┐
│                      ZenLog — Domain Map                          │
│                                                                   │
│   DOMAINE MÉTIER (pure Python, 0 dépendance framework)            │
│  ┌───────────────────────┐     ┌────────────────────────────┐    │
│  │  BC 1 : Wellness       │     │  BC 2 : Coaching            │    │
│  │  Tracking              │     │                             │    │
│  │                        │     │  - Assignment               │    │
│  │  - WellnessEntry       │     │  - PatientView              │    │
│  │  - Indicator           │◄───►│  - check_access()           │    │
│  │  - Trend               │     │  - read-only access         │    │
│  │  - Patient (owner)     │     │  - Coach (reader)           │    │
│  └────────────────────────┘     └─────────────────────────────┘   │
│                                                                   │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│                                                                   │
│   INFRASTRUCTURE (Django)                                         │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  django.contrib.auth + SimpleJWT                          │    │
│  │  (User model, authentication, roles, permissions)         │    │
│  │  → Fournit user_id + role au domaine métier               │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

---

### 4.3 BC 1 : Suivi Bien-Être (contexte cœur)

**Responsabilité** : Permettre à un patient de saisir, consulter et analyser ses données de bien-être au quotidien.

**Pourquoi c'est le cœur** : Sans ce contexte, l'application n'a aucune raison d'exister. C'est la brique qui crée de la valeur pour le patient.

**Entités et objets de valeur :**

- **Entrée bien-être / `WellnessEntry`** (entité, agrégat root) : identifiée par (patient_id, indicator_id, date). Contient une valeur numérique et une note optionnelle.
- **Indicateur / `Indicator`** (entité) : identifié par son nom unique. Définit la plage de valeurs acceptables (min_value/max_value) et l'unité (unit).
- **Tendance / `Trend`** (objet de valeur) : calculée à la volée à partir des entrées. N'est pas persistée, c'est un résultat de calcul métier.

**Invariants (règles métier) :**

1. **Unicité quotidienne** : Un patient ne peut saisir qu'une seule entrée par indicateur et par jour. Si une entrée existe déjà, elle doit être modifiée, pas dupliquée.
2. **Validation de la plage** : La valeur d'une entrée doit être comprise dans [indicateur.valeur_min, indicateur.valeur_max]. Cette règle est du domaine pur — elle ne dépend d'aucun framework.
3. **Propriété des données** : Un patient ne peut consulter et modifier que ses propres entrées. Jamais celles d'un autre patient.
4. **Calcul de tendance** : La moyenne sur N jours exclut les jours sans saisie (pas de valeur 0 par défaut — ce serait un biais).

**Cas d'usage métier (indépendants de toute technique) :**

| # | Cas d'usage | Acteur | Règle métier appliquée |
|---|---|---|---|
| US-1 | Saisir mon bien-être du jour | Patient | Unicité quotidienne + validation plage |
| US-2 | Modifier ma saisie du jour | Patient | Propriété des données |
| US-3 | Consulter mon historique | Patient | Propriété des données |
| US-4 | Voir mes tendances sur 7/30 jours | Patient | Calcul de tendance |
| US-5 | Ajouter un nouveau type d'indicateur | Admin | Indicateur avec plage valide |

---

### 4.4 BC 2 : Accompagnement Coach (contexte de support métier)

**Responsabilité** : Permettre à un coach d'accéder aux données de ses patients affectés, en lecture seule, pour adapter son accompagnement.

**Pourquoi c'est séparé du BC 1** : La logique d'accès coach est une préoccupation différente de la saisie patient. Un patient peut utiliser ZenLog sans jamais avoir de coach. Le coach n'ajoute, ne modifie et ne supprime aucune donnée de bien-être — il les consulte.

**Entités et objets de valeur :**

- **Affectation / `Assignment`** (entité, agrégat root) : identifiée par (coach_id, patient_id). Possède un statut actif/inactif (is_active) et des dates de début/fin (start_date/end_date).
- **Vue patient / `PatientView`** (objet de valeur) : projection en lecture seule des données du BC 1, filtrée par l'affectation active.

**Invariants (règles métier) :**

1. **Accès conditionné à l'affectation** : Un coach ne peut consulter les données d'un patient que si une affectation active les lie. C'est la règle de sécurité centrale du domaine.
2. **Lecture seule stricte** : Le coach ne peut jamais créer, modifier ou supprimer une entrée bien-être. Cet invariant est du domaine, pas juste une permission technique.
3. **Gestion des affectations par l'admin** : Seul un administrateur peut créer, activer ou désactiver une affectation. Ni le coach ni le patient ne peuvent le faire eux-mêmes.

**Cas d'usage métier :**

| # | Cas d'usage | Acteur | Règle métier appliquée |
|---|---|---|---|
| US-6 | Consulter les données d'un patient | Coach | Accès conditionné + lecture seule |
| US-7 | Voir la liste de mes patients | Coach | Filtrage par affectations actives |
| US-8 | Affecter un coach à un patient | Admin | Gestion des affectations |
| US-9 | Désactiver une affectation | Admin | Révocation d'accès |

**Relation entre BC 1 et BC 2** : Le BC 2 consomme les données du BC 1 via un **contrat d'interface read-only** (`PatientEntryReader`). Il ne dépend jamais directement des entités internes ni du repository complet du BC 1 — il utilise un port de lecture seule dédié, garantissant par le type que le coach ne peut jamais écrire de données (voir §5.2 pour le détail du refactoring ayant isolé ce contrat).

---

### 4.5 Identité & Accès — Délégation à Django (décision d'architecture)

**Responsabilité** : Gérer les comptes utilisateurs, l'authentification et l'attribution des rôles.

**Décision** : Ce contexte n'est **pas** un bounded context métier. Il est entièrement délégué à `django.contrib.auth` + `djangorestframework-simplejwt`.

**Justification** :

1. **Django `auth` est déjà découplé** : le module `django.contrib.auth` est un composant indépendant du reste de l'application. Il gère les utilisateurs, les groupes et les permissions dans ses propres tables (`auth_user`, `auth_group`, `auth_permission`), sans couplage avec le code métier.
2. **RGPD-friendly nativement** : les mots de passe sont hashés avec PBKDF2/bcrypt, les sessions sont sécurisées, et Django fournit des mécanismes d'anonymisation et de suppression de compte. Pas besoin de réimplémenter cette logique sensible.
3. **Éprouvé en production** : le système d'authentification Django est utilisé par des milliers d'applications en production. Le réécrire dans une couche domaine serait du sur-engineering pour un projet de cette taille, et potentiellement moins sécurisé.
4. **Cohérence avec l'architecture hexagonale** : dans une archi hexagonale, les préoccupations transverses (auth, logging, etc.) sont légitimement gérées par l'infrastructure. Le domaine métier (BC 1 et BC 2) reçoit simplement un `user_id` et un `role` — il n'a pas besoin de savoir comment l'utilisateur s'est authentifié.

**Implémentation technique** :

- **Modèle utilisateur** : extension du `AbstractUser` de Django avec un champ `role` (choix : `patient`, `coach`, `admin`).
- **Authentification API** : `djangorestframework-simplejwt` pour l'émission et la validation des tokens JWT (access token 15 min, refresh token 24h).
- **Permissions** : classes DRF custom (`IsPatient`, `IsCoach`, `IsAdmin`) qui lisent le rôle de l'utilisateur authentifié.
- **Admin** : gestion des comptes et rôles via l'interface d'administration Django, sans développement spécifique.

**Tâches techniques associées** (ce ne sont pas des user stories métier) :

| # | Tâche | Détail |
|---|---|---|
| TECH-AUTH-1 | Configurer le modèle User custom | Étendre `AbstractUser`, ajouter le champ `role` |
| TECH-AUTH-2 | Configurer JWT (SimpleJWT) | Endpoints `/api/auth/register/`, `/api/auth/token/`, `/api/auth/token/refresh/` |
| TECH-AUTH-3 | Créer les classes de permissions DRF | `IsPatient`, `IsCoach`, `IsAdmin` |

---

### 4.6 Architecture hexagonale — Séparation domaine / technique

Le principe fondamental : **le domaine métier ne connaît pas Django**. Les cas d'usage métier sont implémentés en Python pur, sans import Django, sans ORM, sans HTTP. Le framework s'adapte au domaine, pas l'inverse.

```
                    ┌───────────────────────────────┐
                    │     Input Ports                 │
                    │  (driving adapters)             │
                    │                                 │
                    │  • REST API (DRF adapter)       │
                    │  • CLI (future)                 │
                    │  • Tests                        │
                    └──────────────┬──────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                             │
│                  (pure Python, zero dependencies)              │
│                                                               │
│  ┌────────────────┐  ┌─────────────┐  ┌───────────────────┐  │
│  │  Entities       │  │  Value       │  │  Domain Services   │  │
│  │                 │  │  Objects     │  │                    │  │
│  │  - WellnessEntry│  │  - Trend    │  │  - create_entry()  │  │
│  │  - Indicator    │  │             │  │  - get_history()   │  │
│  │  - Assignment   │  │             │  │  - compute_trend() │  │
│  └────────────────┘  └─────────────┘  │  - check_access()  │  │
│                                        └───────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  Output Ports (abstract interfaces)                   │     │
│  │  • WellnessEntryRepository (ABC)  — BC Tracking       │     │
│  │  • IndicatorRepository (ABC)      — BC Tracking       │     │
│  │  • AssignmentRepository (ABC)     — BC Coaching        │     │
│  │  • PatientEntryReader (ABC)       — BC Coaching (R/O)  │     │
│  └──────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                    ┌───────────────────────────────┐
                    │     Output Adapters             │
                    │  (driven adapters)              │
                    │                                 │
                    │  • Django ORM (PostgreSQL)      │
                    │  • Cache (future)               │
                    │  • External service (future)    │
                    └───────────────────────────────┘
```

**En pratique, cela donne cette structure de fichiers :**

```
zenlog/
├── domain/                        # DOMAIN LAYER — pure Python, no framework dependency
│   ├── entities/                  # Entities & value objects
│   │   ├── wellness_entry.py      # WellnessEntry class (pure Python)
│   │   ├── indicator.py           # Indicator class (pure Python)
│   │   └── assignment.py          # Assignment class (pure Python)
│   ├── services/                  # Domain services (use cases)
│   │   ├── tracking_service.py    # create_entry(), get_history(), compute_trend()
│   │   └── coaching_service.py    # check_access(), get_patient_data()
│   └── ports/                     # Abstract interfaces (contracts)
│       ├── wellness_entry_repository.py  # ABC: save, find, filter entries
│       ├── indicator_repository.py
│       ├── assignment_repository.py
│       └── patient_entry_reader.py       # ABC: read-only (BC Coaching)
│
├── infrastructure/                # ADAPTERS — framework-dependent
│   ├── django_models/             # Django ORM models (DB mapping)
│   ├── repositories/              # Port implementations using Django ORM
│   ├── serializers/               # API serialization (DRF)
│   ├── views/                     # HTTP controllers (DRF viewsets)
│   ├── permissions/               # DRF permissions (roles)
│   └── urls/                      # URL routing
│
├── tests/
│   ├── domain/                    # Domain tests (pure Python, no DB)
│   └── infrastructure/            # Integration tests (with Django/DB)
```

**Le bénéfice clé** : les tests du domaine (`tests/domain/`) ne nécessitent ni Django, ni base de données. On teste la logique métier pure avec des mocks simples des repositories. C'est exactement ce qu'attend le cahier des charges quand il demande de "bien séparer le code métier du code de dépendance".

**Convention de nommage** : toute la documentation métier est rédigée en français, mais le code (classes, méthodes, variables, noms de fichiers) est systématiquement en anglais. La table du langage ubiquitaire (§4.1) fait le lien entre les deux.

---

## 5. Stratégie de refactoring

Le refactoring est une étape essentielle du cycle TDD (Red-Green-**Refactor**). Dans ZenLog, chaque refactoring est traité comme un changement de premier ordre : branche dédiée, commits atomiques, tests au vert avant merge. Cette section documente les refactorings réalisés, leur motivation et leur impact sur l'architecture.

### 5.1 Refactoring 1 — Docstrings et extraction de `_validate_value`

**Branche** : `refactor/docstrings-extract-validate`

**Problème identifié** :

1. **Absence de docstrings** : les entités, services et ports du domaine ne contenaient aucune documentation inline. Pour un projet évalué sur sa qualité et sa maintenabilité, c'est un manque — un développeur découvrant le code ne peut pas comprendre l'intention de chaque classe ou méthode sans lire l'implémentation.
2. **Duplication de la logique de validation** : la validation de la plage de valeurs (vérifier qu'une valeur est comprise entre `min_value` et `max_value` de l'indicateur) était dupliquée entre `create_entry()` et `update_entry()` dans `TrackingService`. Toute modification de la règle de validation impliquait de modifier deux endroits — source classique de bugs par oubli.

**Solution** :

- **Ajout de docstrings** sur toutes les entités (`WellnessEntry`, `Indicator`, `Assignment`, `Trend`), tous les services (`TrackingService`, `CoachingService`) et tous les ports (`WellnessEntryRepository`, `IndicatorRepository`, `AssignmentRepository`). Les docstrings documentent la responsabilité de la classe et le contrat de chaque méthode publique.
- **Extraction de `_validate_value()`** : la logique de validation dupliquée est extraite dans une méthode privée `_validate_value(value, indicator)` du `TrackingService`. Les méthodes `create_entry()` et `update_entry()` appellent désormais cette méthode unique.

**Principes appliqués** :

- **DRY (Don't Repeat Yourself)** : l'extraction élimine la duplication. Un seul point de modification pour la règle de validation.
- **Lisibilité** : les docstrings rendent le code auto-documenté. Chaque port expose son contrat explicitement, ce qui facilite l'implémentation future des adapters Django.

**Impact** : aucun changement fonctionnel — les 24 tests existants passent sans modification. C'est un refactoring pur : le comportement observable est strictement identique, seule la structure interne s'améliore.

---

### 5.2 Refactoring 2 — Isolation du BC Coaching avec un port read-only (`PatientEntryReader`)

**Branche** : `refactor/isolate-coaching-bc-read-port`

#### Le problème

`CoachingService` (BC Coaching) dépendait directement de `WellnessEntryRepository`, une interface du BC Wellness Tracking. Ce repository expose des méthodes d'écriture (`save()`, `exists()`, `find_by_id()`) alors que la règle métier est claire : **un coach ne fait que lire**. Le contrat de lecture seule n'existait que par convention dans le code — rien n'empêchait un développeur futur d'appeler `entry_repo.save()` depuis `CoachingService`.

Ce couplage posait trois problèmes concrets :

1. **Violation du principe de moindre privilège** : le service Coaching avait accès à des opérations qu'il ne devrait jamais utiliser. C'est l'équivalent de donner les clés de l'écriture à un rôle en lecture seule.
2. **Couplage inter-BC non explicite** : le BC Coaching importait directement un port du BC Wellness Tracking, créant une dépendance structurelle invisible. Si le `WellnessEntryRepository` évoluait (ajout d'une méthode `delete()`), le BC Coaching y aurait accès implicitement.
3. **Tests trompeurs** : les mocks injectés dans les tests exposaient `save()`, `exists()`, etc. — un développeur lisant les tests pouvait croire que le coach écrit des données.

#### Le principe SOLID appliqué : Interface Segregation (ISP)

Le **Interface Segregation Principle** (le « I » de SOLID) stipule qu'un client ne devrait pas être forcé de dépendre d'interfaces qu'il n'utilise pas. Ici, `CoachingService` n'utilise que `find_by_patient()` — il est donc forcé de dépendre d'une interface trop large. La solution est de créer une interface restreinte, taillée pour le besoin exact du client.

#### Stratégie de refactoring pas-à-pas

Le refactoring est découpé en **3 commits atomiques**, chacun isolé pour garder la traçabilité du raisonnement :

**Commit 1 — Créer le nouveau port avant de toucher au code existant**

On ajoute `PatientEntryReader` dans `domain/ports/` : une interface ABC exposant uniquement `find_by_patient()`. Aucun fichier existant n'est modifié. À ce stade, le port existe mais n'est pas encore utilisé.

```python
class PatientEntryReader(ABC):
    """Port read-only pour le BC Coaching.

    Expose uniquement la lecture des entrées d'un patient.
    Aucune méthode d'écriture n'est disponible.
    """

    @abstractmethod
    def find_by_patient(self, patient_id: str) -> list[WellnessEntry]:
        pass
```

**Pourquoi un commit séparé ?** Ajouter sans modifier permet de valider l'interface en isolation. Si le port est mal conçu, on le corrige avant qu'il ne soit utilisé. Le risque est nul à cette étape.

**Commit 2 — Basculer le service sur le nouveau port**

On remplace la dépendance dans `CoachingService` :

| Avant | Après |
|---|---|
| `entry_repo: WellnessEntryRepository` | `entry_reader: PatientEntryReader` |
| Accès à `save()`, `exists()`, `find_by_id()`, `find_by_patient()` | Accès uniquement à `find_by_patient()` |

Les tests cassent volontairement à cette étape — les fixtures utilisent encore l'ancien nom `entry_repo`. C'est assumé et documenté : on modifie le contrat du service sans toucher aux tests, pour garder un commit focalisé sur un seul changement.

**Pourquoi laisser les tests casser ?** Un commit qui casse les tests peut sembler contre-intuitif. Mais ici, c'est un choix délibéré de traçabilité : le commit 2 montre exactement ce qui change dans le code de production. Le commit 3, immédiatement après, répare les tests. Cette séparation rend le diff lisible et le raisonnement auditable.

**Commit 3 — Adapter les tests pour restaurer le vert**

Mise à jour des fixtures (`entry_repo` → `entry_reader`) et des assertions dans `test_coaching_service.py`. Résultat : **24/24 tests passent, zéro régression**.

#### Pourquoi cette approche pas-à-pas plutôt qu'un seul commit ?

- **Chaque commit compile ou échoue de manière prévisible** — pas de gros commit « je change tout d'un coup » où on ne sait plus ce qui a cassé quoi.
- **Le commit 2 casse les tests intentionnellement** — c'est documenté et attendu. Le commit 3 les répare immédiatement. Ça montre que le refactoring est maîtrisé, pas subi.
- **On peut revert chirurgicalement** — si le port s'avère mal dimensionné, on revert les commits 2+3 et le port reste disponible sans impact sur le code existant.

#### Ce que ça change concrètement

| Avant | Après |
|---|---|
| `CoachingService` voit `save()`, `exists()`, `find_by_id()` | Ne voit que `find_by_patient()` |
| La lecture seule est une convention d'équipe | La lecture seule est **garantie par le type** |
| Couplage direct BC Coaching → port du BC Wellness Tracking | BC Coaching a son propre port, le contrat inter-BC est explicite |

#### Impact sur l'architecture

Le diagramme des ports du domaine évolue :

```
domain/ports/
├── wellness_entry_repository.py   # BC Wellness Tracking — lecture + écriture
├── indicator_repository.py        # BC Wellness Tracking — gestion des indicateurs
├── assignment_repository.py       # BC Coaching — gestion des affectations
└── patient_entry_reader.py        # BC Coaching — lecture seule des entrées (NEW)
```

**Impact côté infrastructure (futur)** : quand les repositories Django seront implémentés, l'adapter pourra satisfaire les deux interfaces avec une seule classe grâce à l'héritage multiple de Python :

```python
class DjangoWellnessEntryRepository(WellnessEntryRepository, PatientEntryReader):
    """Implémente les deux ports avec le même ORM Django."""

    def save(self, entry): ...
    def find_by_patient(self, patient_id): ...
    def find_by_id(self, entry_id): ...
    def exists(self, patient_id, indicator_id, date): ...
```

Une seule classe, deux contrats : le `TrackingService` reçoit l'instance typée `WellnessEntryRepository`, le `CoachingService` reçoit la même instance typée `PatientEntryReader`. Chacun ne voit que ce que son type autorise.

---

### 5.3 Synthèse — Principes de refactoring appliqués dans ZenLog

| Principe | Refactoring 1 | Refactoring 2 |
|---|---|---|
| **DRY** | Extraction de `_validate_value()` | — |
| **Interface Segregation (SOLID)** | — | Création de `PatientEntryReader` |
| **Moindre privilège** | — | Le coach ne voit que `find_by_patient()` |
| **Commits atomiques** | 1 commit ciblé | 3 commits traçables |
| **Zéro régression** | 24/24 tests ✅ | 24/24 tests ✅ |
| **Séparation des préoccupations** | Docstrings vs. logique | Contrat inter-BC explicite |

**Méthodologie commune** : chaque refactoring suit le même protocole — branche dédiée, commits atomiques avec messages conventionnels (`refactor(scope): description`), exécution complète des tests avant merge, et PR documentée. Le refactoring n'est jamais un « bonus » — c'est la troisième étape du cycle TDD, traitée avec la même rigueur que le Red et le Green.

---

## 6. Design patterns identifiés et justifications

Cette section recense les design patterns mis en œuvre dans ZenLog, leur localisation dans le code, et la justification métier ou architecturale de chacun. Chaque pattern répond à un besoin concret — aucun n'est utilisé « pour faire joli ».

### 6.1 Repository Pattern

**Catégorie** : Pattern structurel (accès aux données)

**Localisation** : `domain/ports/wellness_entry_repository.py`, `domain/ports/indicator_repository.py`, `domain/ports/assignment_repository.py`, `domain/ports/patient_entry_reader.py`

**Implémentation** : chaque repository est défini comme une classe abstraite (ABC) dans `domain/ports/`. L'interface expose les opérations de persistance (`save()`, `find_by_id()`, `find_by_patient()`, `exists()`) sans révéler le mécanisme de stockage sous-jacent.

```python
# domain/ports/wellness_entry_repository.py
class WellnessEntryRepository(ABC):
    @abstractmethod
    def save(self, entry: WellnessEntry) -> WellnessEntry:
        pass

    @abstractmethod
    def find_by_id(self, entry_id: str) -> WellnessEntry | None:
        pass

    @abstractmethod
    def find_by_patient(self, patient_id: str, ...) -> list[WellnessEntry]:
        pass

    @abstractmethod
    def exists(self, patient_id: str, indicator_id: str, date: date) -> bool:
        pass
```

**Justification** :

1. **Découplage domaine/persistance** : les services métier (`TrackingService`, `CoachingService`) n'importent jamais Django, SQLAlchemy ou PostgreSQL. Ils appellent des méthodes abstraites dont l'implémentation concrète est injectée à l'exécution. Si demain on remplace PostgreSQL par MongoDB, seul le dossier `infrastructure/repositories/` change — le domaine reste intact.
2. **Testabilité** : en tests unitaires, on injecte des `MagicMock()` à la place des repositories réels. Les 24 tests du domaine s'exécutent sans base de données, sans `django.setup()`, en pur pytest. Le temps d'exécution des tests reste minimal même si la base de données de production est lente ou indisponible.
3. **Contrat explicite** : chaque repository définit précisément les opérations disponibles. Un développeur implémentant l'adapter Django sait exactement quelles méthodes fournir — le compilateur (ou mypy) vérifie la conformité.

---

### 6.2 Dependency Injection (injection de dépendances par constructeur)

**Catégorie** : Pattern de création / inversion de contrôle

**Localisation** : `domain/services/tracking_service.py` (lignes 18-24), `domain/services/coaching_service.py` (lignes 13-19)

**Implémentation** : les services reçoivent leurs dépendances via le constructeur (`__init__`), typées par les interfaces abstraites. Aucun service n'instancie lui-même ses repositories.

```python
# domain/services/tracking_service.py
class TrackingService:
    def __init__(
        self,
        entry_repo: WellnessEntryRepository,
        indicator_repo: IndicatorRepository,
    ):
        self.entry_repo = entry_repo
        self.indicator_repo = indicator_repo
```

```python
# domain/services/coaching_service.py
class CoachingService:
    def __init__(
        self,
        assignment_repo: AssignmentRepository,
        entry_reader: PatientEntryReader,
    ):
        self.assignment_repo = assignment_repo
        self.entry_reader = entry_reader
```

**Justification** :

1. **Principe d'inversion des dépendances (DIP — SOLID)** : les modules de haut niveau (services) dépendent d'abstractions (ports ABC), pas de modules de bas niveau (Django ORM). La direction de la dépendance est inversée : c'est l'infrastructure qui s'adapte au domaine, pas l'inverse.
2. **Testabilité maximale** : en test, on passe des mocks ; en production, on passera les repositories Django. Le service ne sait pas — et n'a pas besoin de savoir — à qui il parle.
3. **Flexibilité de composition** : on peut recombiner les services avec des implémentations différentes (cache, API externe, repository en mémoire) sans modifier une seule ligne du domaine.

```python
# Exemple en test : injection de mocks
@pytest.fixture
def service(entry_repo, indicator_repo):
    return TrackingService(
        entry_repo=entry_repo,         # MagicMock
        indicator_repo=indicator_repo,  # MagicMock
    )
```

---

### 6.3 Service Pattern (Domain Service)

**Catégorie** : Pattern DDD (Domain-Driven Design)

**Localisation** : `domain/services/tracking_service.py`, `domain/services/coaching_service.py`

**Implémentation** : la logique métier qui ne relève pas d'une seule entité est encapsulée dans des services dédiés. Chaque service a une responsabilité unique (Single Responsibility Principle) :

- **`TrackingService`** : orchestration des opérations de suivi bien-être — création d'entrée (avec vérification d'unicité et validation de plage), mise à jour (avec vérification de propriété), calcul de tendance.
- **`CoachingService`** : contrôle d'accès coach → patient — vérification d'affectation active, récupération de la liste de patients, lecture des données patient en mode read-only.

**Justification** :

1. **Séparation des préoccupations** : la règle « un patient ne peut saisir qu'une entrée par indicateur et par jour » implique une coordination entre le repository d'entrées et celui des indicateurs. Cette logique n'appartient ni à `WellnessEntry` ni à `Indicator` — elle appartient au service qui orchestre les deux.

```python
# TrackingService.create_entry() — coordination de deux repositories
def create_entry(self, patient_id, indicator_id, entry_date, value, note=None):
    if self.entry_repo.exists(patient_id, indicator_id, entry_date):
        raise ValueError("Entry already exists...")
    indicator = self.indicator_repo.find_by_id(indicator_id)
    self._validate_value(value, indicator)
    entry = WellnessEntry(id=str(uuid.uuid4()), ...)
    return self.entry_repo.save(entry)
```

2. **Indépendance du framework** : les services sont du Python pur. Ils ne connaissent ni Django, ni DRF, ni HTTP. Les contrôleurs futurs (viewsets DRF) se contenteront d'appeler les méthodes du service et de sérialiser le résultat. Cette séparation est vérifiable : les tests dans `tests/domain/` s'exécutent sans `django.setup()`.
3. **Testabilité** : chaque service est testable en isolation avec des mocks simples. Les 24 tests couvrent les chemins nominaux et les cas d'erreur (valeur hors plage, doublon, accès non autorisé).

---

### 6.4 Entity Pattern

**Catégorie** : Pattern DDD

**Localisation** : `domain/entities/wellness_entry.py`, `domain/entities/indicator.py`, `domain/entities/assignment.py`

**Implémentation** : les entités sont des `@dataclass` Python possédant une identité (`id`) et des méthodes métier encapsulant les règles propres à l'entité.

```python
# domain/entities/wellness_entry.py
@dataclass
class WellnessEntry:
    id: str
    patient_id: str
    indicator_id: str
    date: date
    value: float
    note: str | None = None

    def is_owned_by(self, patient_id: str) -> bool:
        return self.patient_id == patient_id
```

```python
# domain/entities/indicator.py
@dataclass
class Indicator:
    id: str
    name: str
    unit: str
    min_value: float
    max_value: float
    is_active: bool = True

    def is_value_in_range(self, value: float) -> bool:
        return self.min_value <= value <= self.max_value
```

```python
# domain/entities/assignment.py
@dataclass
class Assignment:
    id: str
    coach_id: str
    patient_id: str
    start_date: date
    is_active: bool = True
    end_date: date | None = None

    def is_currently_active(self) -> bool:
        return self.is_active

    def deactivate(self, end_date: date) -> None:
        self.is_active = False
        self.end_date = end_date
```

**Justification** :

1. **Encapsulation des règles métier** : la vérification de propriété (`is_owned_by`), la validation de plage (`is_value_in_range`) et la gestion du cycle de vie (`deactivate`) sont co-localisées avec les données qu'elles protègent. Un développeur ne peut pas oublier ces règles — elles font partie de l'entité.
2. **Identité vs. valeur** : les entités sont identifiées par un `id` unique et possèdent un cycle de vie (création, modification, désactivation). Cette distinction est fondamentale en DDD pour différencier ce qui est suivi dans le temps (entités) de ce qui est calculé à la volée (value objects, voir §6.5).
3. **Indépendance du framework** : les entités sont de pures `@dataclass` Python sans import Django. Elles ne sont pas des modèles ORM — la correspondance entité ↔ table sera gérée par les repositories dans la couche infrastructure.

---

### 6.5 Value Object Pattern

**Catégorie** : Pattern DDD

**Localisation** : `domain/entities/trend.py`

**Implémentation** : `Trend` est une `@dataclass` sans identité propre (pas de champ `id`), représentant un résultat de calcul agrégé.

```python
# domain/entities/trend.py
@dataclass
class Trend:
    patient_id: str
    indicator_id: str
    period_days: int
    average: float | None
    entry_count: int
```

**Justification** :

1. **Aucune persistance nécessaire** : une tendance est calculée à la volée par `TrackingService.compute_trend()` à partir des entrées existantes. La stocker en base serait de la dénormalisation prématurée — elle se recalcule instantanément.
2. **Immuabilité sémantique** : un `Trend` n'a pas de cycle de vie. Deux tendances avec les mêmes attributs sont interchangeables. Cette propriété distingue clairement les value objects des entités dans le modèle DDD.
3. **Contrat de retour explicite** : plutôt que de renvoyer un dictionnaire ou un tuple anonyme, `compute_trend()` renvoie un objet typé. Le consommateur sait exactement quels champs sont disponibles (`average`, `entry_count`, `period_days`).

---

### 6.6 Ports & Adapters (Architecture Hexagonale)

**Catégorie** : Pattern architectural

**Localisation** : architecture globale du projet — `domain/` (hexagone) vs. `infrastructure/` (adapters)

**Implémentation** : le projet est structuré en deux packages racine au même niveau :

- **`domain/`** : contient les entités, services et ports. Zéro import Django. C'est le cœur applicatif.
- **`infrastructure/`** : contient l'application Django (models, views, serializers, repositories). C'est l'adapter qui traduit les concepts du domaine vers les technologies concrètes (ORM, HTTP, JWT).

**Justification** :

1. **Le domaine dicte, la technique s'adapte** : l'architecture hexagonale inverse la dépendance classique où le code métier est prisonnier du framework. Ici, si Django disparaît demain, seul `infrastructure/` est impacté. La preuve : les tests du domaine s'exécutent en pur pytest, sans `django.setup()`.
2. **Plusieurs adapters possibles** : la même logique métier peut être exposée via une API REST (DRF), une CLI, ou un worker Celery. Chacun est un « driving adapter » qui appelle les services du domaine. Côté persistance, on peut avoir un adapter Django ORM en production et un adapter mock en test — le service ne change pas.
3. **Cohérence avec le cahier des charges** : l'exigence de « bien séparer le code métier du code de dépendance » est directement satisfaite par cette architecture. La séparation est physique (deux packages distincts), pas juste conceptuelle.

---

### 6.7 Interface Segregation Pattern

**Catégorie** : Principe SOLID appliqué comme pattern structurel

**Localisation** : `domain/ports/patient_entry_reader.py` vs. `domain/ports/wellness_entry_repository.py`

**Implémentation** : le port `PatientEntryReader` expose uniquement `find_by_patient()` pour le BC Coaching, tandis que `WellnessEntryRepository` expose l'ensemble des opérations CRUD pour le BC Wellness Tracking.

```python
# domain/ports/patient_entry_reader.py — interface restreinte (BC Coaching)
class PatientEntryReader(ABC):
    @abstractmethod
    def find_by_patient(self, patient_id: str, ...) -> list[WellnessEntry]:
        pass
```

```python
# domain/ports/wellness_entry_repository.py — interface complète (BC Tracking)
class WellnessEntryRepository(ABC):
    @abstractmethod
    def save(self, entry: WellnessEntry) -> WellnessEntry: ...
    @abstractmethod
    def find_by_id(self, entry_id: str) -> WellnessEntry | None: ...
    @abstractmethod
    def find_by_patient(self, patient_id: str, ...) -> list[WellnessEntry]: ...
    @abstractmethod
    def exists(self, patient_id: str, indicator_id: str, date: date) -> bool: ...
```

**Justification** :

1. **Moindre privilège garanti par le type** : `CoachingService` reçoit un `PatientEntryReader` — il lui est structurellement impossible d'appeler `save()` ou `exists()`. La règle « un coach ne fait que lire » n'est plus une convention d'équipe, c'est une contrainte du système de types.
2. **Découplage inter-BC** : le BC Coaching ne dépend plus d'un port du BC Wellness Tracking. Il possède son propre port (`PatientEntryReader`), ce qui rend le contrat inter-bounded contexts explicite et versionnable indépendamment.
3. **Implémentation unique côté infrastructure** : grâce à l'héritage multiple Python, un seul adapter Django pourra implémenter les deux interfaces (`WellnessEntryRepository` + `PatientEntryReader`). Pas de duplication de code côté infrastructure.

---

### 6.8 Guard Clauses Pattern (validation défensive)

**Catégorie** : Pattern de programmation défensive

**Localisation** : `domain/services/tracking_service.py` (`create_entry`, `update_entry`), `domain/services/coaching_service.py` (`get_patient_data`)

**Implémentation** : chaque méthode de service valide ses préconditions en début d'exécution et échoue immédiatement (fail fast) avec une exception explicite si une règle métier est violée.

```python
# TrackingService — chaîne de guard clauses
def create_entry(self, patient_id, indicator_id, entry_date, value, note=None):
    # Guard 1 : unicité quotidienne
    if self.entry_repo.exists(patient_id, indicator_id, entry_date):
        raise ValueError("Entry already exists...")

    # Guard 2 : validation de la plage de valeurs
    indicator = self.indicator_repo.find_by_id(indicator_id)
    self._validate_value(value, indicator)

    # Happy path : création de l'entrée
    entry = WellnessEntry(id=str(uuid.uuid4()), ...)
    return self.entry_repo.save(entry)
```

```python
# CoachingService — guard clause d'autorisation
def get_patient_data(self, coach_id, patient_id):
    if not self.check_access(coach_id, patient_id):
        raise PermissionError("Coach has no active assignment...")
    return self.entry_reader.find_by_patient(patient_id)
```

**Justification** :

1. **Défense en profondeur** : les règles métier sont appliquées au niveau du domaine, indépendamment des validations qui seront ajoutées au niveau API (serializers DRF). Même si un contrôleur oublie une validation, le service la rattrape.
2. **Fail fast** : en échouant dès la première violation, on évite les états incohérents (entrée créée avec une valeur hors plage, données coach sans affectation active).
3. **Lisibilité** : les guard clauses séparent clairement les préconditions du chemin nominal. Un lecteur du code identifie immédiatement les règles métier en début de méthode, sans devoir lire toute l'implémentation.

---

### 6.9 Test Doubles Pattern (Mock Objects)

**Catégorie** : Pattern de test

**Localisation** : `tests/domain/test_tracking_service.py`, `tests/domain/test_coaching_service.py`

**Implémentation** : les tests utilisent `unittest.mock.MagicMock` pour simuler les repositories. Les fixtures pytest assemblent les mocks et les injectent dans les services via le constructeur.

```python
# tests/domain/test_tracking_service.py
@pytest.fixture
def entry_repo():
    return MagicMock()

@pytest.fixture
def indicator_repo(mood_indicator):
    repo = MagicMock()
    repo.find_by_id.return_value = mood_indicator
    return repo

@pytest.fixture
def service(entry_repo, indicator_repo):
    return TrackingService(entry_repo=entry_repo, indicator_repo=indicator_repo)
```

**Justification** :

1. **Isolation totale** : les tests du domaine ne dépendent ni de Django ni de PostgreSQL. Ils s'exécutent en millisecondes, sans infrastructure. C'est la conséquence directe des patterns Repository + Dependency Injection — sans eux, on serait obligé de monter une base de données pour chaque test.
2. **Contrôle fin du comportement** : `MagicMock` permet de simuler précisément chaque scénario — `entry_repo.exists.return_value = True` simule un doublon, `entry_repo.save.side_effect = lambda e: e` simule un save transparent. Chaque test configure exactement le contexte nécessaire.
3. **Vérification des interactions** : `entry_repo.save.assert_called_once()` vérifie que le service a bien appelé la bonne méthode du repository. On teste non seulement le résultat mais aussi le comportement interne du service.

---

### 6.10 Synthèse des design patterns

| Pattern | Localisation | Besoin adressé | Principe SOLID |
|---|---|---|---|
| **Repository** | `domain/ports/*.py` | Découplage domaine / persistance | DIP (Dependency Inversion) |
| **Dependency Injection** | Constructeurs des services | Testabilité, flexibilité de composition | DIP |
| **Domain Service** | `domain/services/*.py` | Orchestration de la logique métier | SRP (Single Responsibility) |
| **Entity** | `domain/entities/*.py` | Encapsulation des règles métier avec identité | SRP |
| **Value Object** | `domain/entities/trend.py` | Résultat de calcul typé, sans cycle de vie | — |
| **Ports & Adapters** | Architecture globale `domain/` vs `infrastructure/` | Indépendance du framework | DIP, OCP |
| **Interface Segregation** | `PatientEntryReader` vs `WellnessEntryRepository` | Moindre privilège, découplage inter-BC | ISP |
| **Guard Clauses** | Méthodes des services | Validation défensive, fail fast | — |
| **Test Doubles (Mocks)** | `tests/domain/*.py` | Tests rapides et isolés | — |

**Cohérence globale** : ces patterns ne sont pas utilisés individuellement — ils forment un système cohérent. Le Repository Pattern n'a de sens que parce que l'injection de dépendances permet de le substituer en test. L'injection de dépendances n'a de sens que parce que les ports définissent des contrats abstraits. Les ports abstraits n'ont de sens que dans une architecture hexagonale qui sépare domaine et infrastructure. Chaque pattern renforce les autres et contribue à l'objectif central du projet : un domaine métier testable, maintenable et indépendant du framework.

---

## 7. Stratégie API — Conception, justification et plan d'implémentation

### 7.1 Choix du style d'API : REST, GraphQL ou RPC ?

ZenLog est une API back-end destinée à être consommée par un front-end mobile ou web. Ce type de client influence fortement le choix du style d'API. Trois options ont été évaluées :

#### Option 1 — REST (resource-oriented)

L'approche classique : chaque ressource (entrées, indicateurs, affectations) est exposée via un endpoint dédié avec les verbes HTTP standards (GET, POST, PATCH, DELETE).

| Avantage | Inconvénient |
|---|---|
| Standard universel, très bien outillé (DRF, Swagger) | Over-fetching : le client reçoit tous les champs même s'il n'en utilise que deux |
| Cache HTTP natif (ETag, Cache-Control) | Under-fetching : pour un écran mobile complexe, il faut souvent 2-3 appels séparés |
| Documentation auto-générée (drf-spectacular) | Pas de typage fort côté client sans génération de code |
| Écosystème Django/DRF mature et éprouvé | Évolution des endpoints = gestion du versioning |

#### Option 2 — GraphQL (query-oriented)

Le client décrit exactement les données dont il a besoin dans une requête unique. Particulièrement adapté aux applications mobiles où la bande passante et le nombre de requêtes comptent.

| Avantage | Inconvénient |
|---|---|
| Pas d'over-fetching ni d'under-fetching | Complexité accrue côté serveur (résolveurs, N+1, sécurité) |
| Un seul endpoint, le client compose ses requêtes | Pas de cache HTTP natif (tout passe par POST) |
| Idéal pour les apps mobiles multi-écrans | Écosystème Django/GraphQL moins mature que DRF |
| Typage fort via le schéma GraphQL | Courbe d'apprentissage + surcoût d'implémentation |

#### Option 3 — gRPC / RPC (action-oriented)

Appels de procédure à distance avec contrats Protobuf. Ultra-performant, adapté au server-to-server.

| Avantage | Inconvénient |
|---|---|
| Très performant (binaire, HTTP/2, streaming) | Pas adapté aux navigateurs web (nécessite gRPC-Web) |
| Contrat fort via Protobuf | Outillage Django quasi inexistant |
| Idéal pour microservices internes | Pas de documentation interactive (pas de Swagger) |

#### Décision : REST maintenant, architecture prête pour GraphQL

**Pour le MVP (3 jours, solo, cahier des charges évaluable)** : REST avec DRF est le choix rationnel.

**Justification** :

1. **Contrainte du cahier des charges** : l'exigence de documentation API (Swagger/OpenAPI) et d'endpoints sécurisés pointe explicitement vers REST. Le formateur s'attend à voir des endpoints HTTP classiques avec des contrats entrée/sortie documentés.
2. **Productivité** : DRF est déjà configuré dans le projet (settings, simplejwt, drf-spectacular). Basculer sur GraphQL (Strawberry ou Graphene) impliquerait de reconfigurer l'authentification, la documentation et les permissions — du temps investi dans la plomberie plutôt que dans la valeur métier.
3. **Testabilité** : DRF fournit `APIClient` pour les tests d'intégration. Le plan de tests (section 3 du PLAN_DE_TESTS.md) est déjà rédigé avec des endpoints REST. Le conserver évite de réécrire 21 tests d'intégration + 10 tests de sécurité.
4. **Évaluation** : REST est le standard attendu dans un contexte de formation back-end. Démontrer la maîtrise de REST (pagination, filtrage, permissions, gestion d'erreurs, versioning) est plus démonstratif qu'un GraphQL partiel.

**Cependant**, l'observation est pertinente : pour une application mobile de suivi bien-être, GraphQL serait un meilleur choix en production. L'écran "dashboard patient" nécessiterait en REST 3 appels (entrées récentes + tendance 7j + tendance 30j), tandis qu'en GraphQL une seule requête suffirait.

#### Préparation pour une couche GraphQL future

L'architecture hexagonale de ZenLog rend l'ajout futur d'un gateway GraphQL trivial, car les services domaine sont déjà découplés de la couche de transport :

```
                    ┌─────────────────────────────────────┐
                    │     Driving Adapters (input ports)    │
                    │                                       │
                    │  ┌─────────────┐  ┌───────────────┐  │
                    │  │  REST / DRF  │  │  GraphQL       │  │
                    │  │  (MVP, v1)   │  │  (futur, v2)   │  │
                    │  └──────┬───────┘  └──────┬────────┘  │
                    └─────────┼─────────────────┼───────────┘
                              │                 │
                              ▼                 ▼
                    ┌─────────────────────────────────────┐
                    │         Domain Services               │
                    │  TrackingService · CoachingService     │
                    │  (inchangés, framework-agnostic)       │
                    └─────────────────────────────────────┘
```

Concrètement, un futur adapter GraphQL (avec Strawberry-Django par exemple) appellerait les mêmes méthodes de service que les viewsets DRF :

```python
# Futur : strawberry resolver (v2)
@strawberry.type
class Query:
    @strawberry.field
    def my_entries(self, info) -> list[WellnessEntryType]:
        service = TrackingService(entry_repo=..., indicator_repo=...)
        return service.get_history(patient_id=info.context.user.id)
```

**Ce qui ne change pas** : les entités, les services, les ports, les repositories. Seule une nouvelle couche de « transport » s'ajoute. C'est le bénéfice concret de l'architecture hexagonale documentée en §4.6.

---

### 7.2 Contrats d'API — Endpoints, verbes et réponses

Les endpoints suivent les conventions REST standards. Chaque endpoint est rattaché à une user story du cahier des charges (§3 du CDC).

#### 7.2.1 Authentification (`/api/auth/`)

| Méthode | Endpoint | US | Description | Auth requise |
|---|---|---|---|---|
| POST | `/api/auth/register/` | AUTH-1 | Inscription (email + password + role) | Non |
| POST | `/api/auth/token/` | AUTH-2 | Connexion → access + refresh tokens | Non |
| POST | `/api/auth/token/refresh/` | AUTH-2 | Renouveler l'access token | Non (refresh token dans le body) |

#### 7.2.2 Wellness Tracking (`/api/wellness/`)

| Méthode | Endpoint | US | Description | Auth | Rôle |
|---|---|---|---|---|---|
| GET | `/api/wellness/indicators/` | US-5 | Lister les indicateurs actifs | Oui | Tous |
| POST | `/api/wellness/indicators/` | US-5 | Créer un indicateur | Oui | Admin |
| GET | `/api/wellness/entries/` | US-3 | Lister mes entrées (filtrage, pagination) | Oui | Patient |
| POST | `/api/wellness/entries/` | US-1 | Saisir une entrée du jour | Oui | Patient |
| GET | `/api/wellness/entries/{id}/` | US-3 | Détail d'une entrée (propriétaire uniquement) | Oui | Patient |
| PATCH | `/api/wellness/entries/{id}/` | US-2 | Modifier une entrée (propriétaire uniquement) | Oui | Patient |
| GET | `/api/wellness/trends/` | US-4 | Tendances 7j/30j (query param `?period=7`) | Oui | Patient |

#### 7.2.3 Coaching (`/api/coaching/`)

| Méthode | Endpoint | US | Description | Auth | Rôle |
|---|---|---|---|---|---|
| GET | `/api/coaching/patients/` | US-7 | Mes patients (affectations actives) | Oui | Coach |
| GET | `/api/coaching/patients/{id}/entries/` | US-6 | Entrées d'un patient (lecture seule) | Oui | Coach |
| GET | `/api/coaching/assignments/` | US-8 | Lister les affectations | Oui | Admin |
| POST | `/api/coaching/assignments/` | US-8 | Créer une affectation | Oui | Admin |
| PATCH | `/api/coaching/assignments/{id}/` | US-9 | Désactiver une affectation | Oui | Admin |

#### 7.2.4 Conventions transversales

**Pagination** : `PageNumberPagination` (DRF), 20 résultats par page (configurable via `?page_size=`).

```json
{
  "count": 142,
  "next": "https://api.zenlog.app/api/wellness/entries/?page=2",
  "previous": null,
  "results": [...]
}
```

**Filtrage** : query parameters standards sur les endpoints de liste.

- `/api/wellness/entries/?indicator_id=<uuid>&date_from=2026-03-01&date_to=2026-03-20`
- `/api/wellness/trends/?period=7&indicator_id=<uuid>`

**Gestion des erreurs** : réponses JSON structurées avec codes HTTP sémantiques.

| Code | Usage |
|---|---|
| 200 | Succès (GET, PATCH) |
| 201 | Création réussie (POST) |
| 400 | Erreur de validation (valeur hors plage, doublon, champs manquants) |
| 401 | Non authentifié (token absent ou expiré) |
| 403 | Non autorisé (rôle insuffisant, pas d'affectation active) |
| 404 | Ressource inexistante (ou accès interdit déguisé pour ne pas révéler l'existence) |
| 429 | Rate limiting (tentatives de login excessives) |

**Sécurité des réponses** : le mot de passe hashé n'apparaît jamais dans les réponses JSON. Les données d'un patient ne sont jamais exposées à un autre patient (même en 404 plutôt que 403, pour ne pas révéler l'existence d'une ressource).

---

### 7.3 Architecture de la couche infrastructure — Du domaine à l'API

Le câblage infrastructure suit le flux suivant :

```
HTTP Request
    │
    ▼
┌──────────────────┐
│  DRF Router/URLs  │  config/urls.py + infrastructure/urls.py
└────────┬─────────┘
         ▼
┌──────────────────┐
│  DRF ViewSet      │  infrastructure/views/
│                   │  - Authentifie (JWT)
│                   │  - Vérifie les permissions (IsPatient, IsCoach, IsAdmin)
│                   │  - Désérialise l'input (serializer)
│                   │  - Instancie le repository Django
│                   │  - Appelle le service domaine
│                   │  - Sérialise l'output
└────────┬─────────┘
         ▼
┌──────────────────┐
│  Domain Service   │  domain/services/
│                   │  - Applique les guard clauses
│                   │  - Orchestre la logique métier
│                   │  - Appelle les ports abstraits
└────────┬─────────┘
         ▼
┌──────────────────┐
│  Django Repository│  infrastructure/repositories/
│  (adapter)        │  - Traduit les appels ports → ORM Django
│                   │  - Convertit Model ↔ Entity (mapping)
└────────┬─────────┘
         ▼
┌──────────────────┐
│  PostgreSQL       │
└──────────────────┘
```

**Point clé — l'injection de dépendances dans les views** : la view est le point de composition où les repositories concrets sont instanciés et injectés dans les services. C'est le seul endroit du code qui connaît à la fois le domaine et l'infrastructure :

```python
# infrastructure/views/wellness_views.py (pattern d'injection)
class WellnessEntryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsPatient]

    def get_service(self) -> TrackingService:
        return TrackingService(
            entry_repo=DjangoWellnessEntryRepository(),
            indicator_repo=DjangoIndicatorRepository(),
        )

    def create(self, request):
        service = self.get_service()
        serializer = CreateEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        entry = service.create_entry(
            patient_id=str(request.user.id),
            **serializer.validated_data,
        )
        return Response(EntrySerializer(entry).data, status=201)
```

---

### 7.4 Plan d'implémentation — Branches, commits et tests

L'implémentation suit une progression **de l'intérieur vers l'extérieur** de l'hexagone, en 6 branches feature. Chaque branche suit le cycle TDD : tests d'abord (RED), implémentation (GREEN), refactor si nécessaire.

#### Phase 1 — Modèles et persistance

**Branche `feature/django-models`**

Objectif : traduire le MCD en modèles Django, créer le User custom, générer les migrations.

| # | Commit | Type | Contenu |
|---|---|---|---|
| 1 | `feat(infra): add custom User model with role field` | feat | Modèle `User` étendant `AbstractUser`, champ `role` (choices: patient/coach/admin), `AUTH_USER_MODEL` dans settings |
| 2 | `feat(infra): add Indicator model` | feat | Modèle Django `Indicator` (uuid pk, name, unit, min_value, max_value, is_active, created_at), contrainte `unique` sur name |
| 3 | `feat(infra): add WellnessEntry model` | feat | Modèle Django `WellnessEntry` (uuid pk, FK patient→User, FK indicator→Indicator, date, value, note, timestamps), contrainte `unique_together` sur (patient, indicator, date) |
| 4 | `feat(infra): add Assignment model` | feat | Modèle Django `Assignment` (uuid pk, FK coach→User, FK patient→User, start_date, end_date, is_active, created_at) |
| 5 | `chore(infra): generate initial migrations` | chore | `makemigrations` + vérification du SQL généré |

Tests associés : aucun test unitaire à ce stade (les modèles sont de la plomberie ORM). Les modèles seront testés indirectement via les tests d'intégration des branches suivantes.

---

**Branche `feature/django-repositories`**

Objectif : implémenter les adapters ORM qui satisfont les ports du domaine. C'est ici que l'architecture hexagonale se concrétise.

| # | Commit | Type | Contenu |
|---|---|---|---|
| 1 | `test(infra): add repository integration tests` | test | Tests avec `pytest-django` et `TransactionTestCase` pour chaque repository : save, find_by_id, find_by_patient (avec filtres), exists. Utilise `factory-boy` pour générer les données. |
| 2 | `feat(infra): implement DjangoWellnessEntryRepository` | feat | Classe implémentant `WellnessEntryRepository` + `PatientEntryReader`. Mapping Model ↔ Entity (méthodes `_to_entity()` / `_to_model()`). |
| 3 | `feat(infra): implement DjangoIndicatorRepository` | feat | Implémente `IndicatorRepository`. |
| 4 | `feat(infra): implement DjangoAssignmentRepository` | feat | Implémente `AssignmentRepository`. |

Tests associés (RED avant chaque implémentation) :

| ID test | Cible | Vérifie |
|---|---|---|
| T-R-01 | `DjangoWellnessEntryRepository.save()` | Entrée persistée et récupérable par `find_by_id()` |
| T-R-02 | `DjangoWellnessEntryRepository.find_by_patient()` | Filtrage par patient_id, indicator_id, date_from, date_to |
| T-R-03 | `DjangoWellnessEntryRepository.exists()` | True si triplet (patient, indicator, date) existe |
| T-R-04 | `DjangoIndicatorRepository.find_all_active()` | Ne retourne que les indicateurs actifs |
| T-R-05 | `DjangoAssignmentRepository.exists_active()` | True si affectation active coach↔patient |
| T-R-06 | `DjangoAssignmentRepository.find_active_by_coach()` | Ne retourne que les affectations actives |

---

#### Phase 2 — Authentification et permissions

**Branche `feature/auth-endpoints`**

Objectif : endpoints d'inscription, connexion et refresh token. Permissions DRF par rôle.

| # | Commit | Type | Contenu |
|---|---|---|---|
| 1 | `test(infra): add auth integration tests (T-I-01 to T-I-06)` | test | Tests d'intégration pour inscription, connexion, refresh, accès sans token |
| 2 | `feat(infra): add registration endpoint` | feat | Vue `RegisterView` + serializer (email, password, role). Validation : email unique, mot de passe robuste (Django validators). |
| 3 | `feat(infra): configure JWT endpoints` | feat | Routes SimpleJWT (`TokenObtainPairView`, `TokenRefreshView`) dans `infrastructure/urls.py`. |
| 4 | `feat(infra): add role-based permissions` | feat | Classes `IsPatient`, `IsCoach`, `IsAdmin` dans `infrastructure/permissions/`. Chaque classe lit `request.user.role`. |
| 5 | `test(infra): add security tests (T-S-01, T-S-02)` | test | Token absent → 401, token expiré → 401. |

Tests associés : T-I-01 à T-I-06 + T-S-01, T-S-02 du plan de tests.

---

#### Phase 3 — Endpoints Wellness (cœur métier API)

**Branche `feature/wellness-api`**

Objectif : exposer les cas d'usage US-1 à US-5 via l'API REST. C'est la branche la plus importante — elle connecte le domaine à l'extérieur.

| # | Commit | Type | Contenu |
|---|---|---|---|
| 1 | `test(infra): add wellness API integration tests (T-I-07 to T-I-13)` | test | Tests d'intégration pour création, doublon, liste, détail, modification, tendances, indicateurs. |
| 2 | `feat(infra): add wellness serializers` | feat | `CreateEntrySerializer` (input), `EntrySerializer` (output), `TrendSerializer`, `IndicatorSerializer`. Validation DRF en complément des guard clauses domaine. |
| 3 | `feat(infra): add WellnessEntryViewSet` | feat | ViewSet connectant les serializers aux services domaine. Injection des repositories Django. Permissions `IsPatient`. Filtrage par query params. |
| 4 | `feat(infra): add TrendView` | feat | Vue dédiée pour `GET /api/wellness/trends/?period=7`. Appelle `TrackingService.compute_trend()`. |
| 5 | `feat(infra): add IndicatorViewSet` | feat | ViewSet pour les indicateurs. GET = tous rôles, POST = `IsAdmin`. |
| 6 | `feat(infra): wire wellness URLs` | feat | Routage DRF (`DefaultRouter`) dans `infrastructure/urls.py`, include dans `config/urls.py`. |
| 7 | `test(infra): add security tests (T-S-03 to T-S-05, T-S-08)` | test | Escalade patient→admin, accès données autre patient, injection SQL. |

Tests associés : T-I-07 à T-I-13 + T-S-03, T-S-04, T-S-05, T-S-08 du plan de tests.

---

#### Phase 4 — Endpoints Coaching

**Branche `feature/coaching-api`**

Objectif : exposer les cas d'usage US-6 à US-9 via l'API REST.

| # | Commit | Type | Contenu |
|---|---|---|---|
| 1 | `test(infra): add coaching API integration tests (T-I-14 to T-I-21)` | test | Tests pour liste patients, données patient, accès refusé, coach tente d'écrire, CRUD admin affectations. |
| 2 | `feat(infra): add coaching serializers` | feat | `AssignmentSerializer`, `PatientListSerializer`, `PatientEntrySerializer`. |
| 3 | `feat(infra): add CoachingViewSet` | feat | ViewSet coach : liste patients (appelle `CoachingService.get_patient_list()`), données patient (appelle `get_patient_data()`). Permissions `IsCoach`. |
| 4 | `feat(infra): add AssignmentViewSet` | feat | ViewSet admin : CRUD affectations. Permissions `IsAdmin`. Désactivation via PATCH (appelle `Assignment.deactivate()`). |
| 5 | `feat(infra): wire coaching URLs` | feat | Routage DRF, include dans `config/urls.py`. |
| 6 | `test(infra): add security tests (T-S-04, T-S-06, T-S-07)` | test | Coach tente d'écrire, coach sans affectation, affectation inactive. |

Tests associés : T-I-14 à T-I-21 + T-S-04, T-S-06, T-S-07 du plan de tests.

---

#### Phase 5 — Sécurité et hardening

**Branche `feature/security-hardening`**

Objectif : rate limiting, logging des accès, protection RGPD, tests de sécurité finaux.

| # | Commit | Type | Contenu |
|---|---|---|---|
| 1 | `feat(infra): add rate limiting on auth endpoints` | feat | `django-ratelimit` ou throttle DRF sur `/api/auth/token/` (10 tentatives/min). |
| 2 | `feat(infra): add access logging middleware` | feat | Middleware Django loguant les accès aux données de santé (qui, quoi, quand). |
| 3 | `feat(infra): mask sensitive fields in API responses` | feat | Vérification que `password_hash` n'apparaît jamais. Serializer User sans champs sensibles. |
| 4 | `test(infra): add final security tests (T-S-09, T-S-10)` | test | Mot de passe non exposé, rate limiting effectif. |

Tests associés : T-S-09, T-S-10 du plan de tests.

---

#### Phase 6 — Documentation et Swagger

**Branche `feature/api-documentation`**

Objectif : documentation OpenAPI complète et fonctionnelle.

| # | Commit | Type | Contenu |
|---|---|---|---|
| 1 | `feat(infra): configure Swagger UI and ReDoc routes` | feat | Routes `/api/docs/` (Swagger UI) et `/api/redoc/` (ReDoc) via drf-spectacular. |
| 2 | `docs(infra): add OpenAPI annotations to all views` | docs | `@extend_schema()` sur chaque vue : descriptions, exemples de requêtes/réponses, tags par BC. |
| 3 | `docs: update README with API quickstart` | docs | Instructions de lancement, exemples curl pour les endpoints principaux. |

---

### 7.5 Synthèse — Vue d'ensemble des branches

```
main (stable, déployable)
│
├── feature/django-models              ← Phase 1 : BDD
│   └── 5 commits (models + migrations)
│   └── PR → merge
│
├── feature/django-repositories        ← Phase 1 : Adapters ORM
│   └── 4 commits (TDD : tests puis implémentation)
│   └── PR → merge
│
├── feature/auth-endpoints             ← Phase 2 : Auth + Permissions
│   └── 5 commits (TDD : T-I-01→T-I-06, T-S-01, T-S-02)
│   └── PR → merge
│
├── feature/wellness-api               ← Phase 3 : Cœur API
│   └── 7 commits (TDD : T-I-07→T-I-13, T-S-03→T-S-05, T-S-08)
│   └── PR → merge
│
├── feature/coaching-api               ← Phase 4 : API Coaching
│   └── 6 commits (TDD : T-I-14→T-I-21, T-S-04, T-S-06, T-S-07)
│   └── PR → merge
│
├── feature/security-hardening         ← Phase 5 : Sécurité
│   └── 4 commits (T-S-09, T-S-10)
│   └── PR → merge
│
└── feature/api-documentation          ← Phase 6 : Swagger + README
    └── 3 commits
    └── PR → merge
```

**Total** : 6 branches, 34 commits, 31 tests d'intégration alignés sur le plan de tests existant (T-I-01 à T-I-21 + T-S-01 à T-S-10).

### 7.6 Couverture des tests — Mapping plan de tests ↔ branches

| Phase | Branche | Tests unitaires domaine | Tests intégration API | Tests sécurité |
|---|---|---|---|---|
| Phase 1a | `feature/django-models` | — | — | — |
| Phase 1b | `feature/django-repositories` | — | T-R-01 à T-R-06 (nouveaux) | — |
| Phase 2 | `feature/auth-endpoints` | — | T-I-01 à T-I-06 | T-S-01, T-S-02 |
| Phase 3 | `feature/wellness-api` | existants (24) | T-I-07 à T-I-13 | T-S-03, T-S-04, T-S-05, T-S-08 |
| Phase 4 | `feature/coaching-api` | existants (24) | T-I-14 à T-I-21 | T-S-04, T-S-06, T-S-07 |
| Phase 5 | `feature/security-hardening` | — | — | T-S-09, T-S-10 |
| Phase 6 | `feature/api-documentation` | — | — | — |

**Bilan final attendu** : 24 tests domaine (existants) + 6 tests repository + 21 tests intégration API + 10 tests sécurité = **61 tests au total**.
