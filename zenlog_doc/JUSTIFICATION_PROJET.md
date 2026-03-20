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

**Relation entre BC 1 et BC 2** : Le BC 2 consomme les données du BC 1 via un **contrat d'interface** (port). Il ne dépend jamais directement des entités internes du BC 1 — il utilise une projection (lecture seule) exposée par le BC 1.

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
│  │  • WellnessEntryRepository (ABC)                      │     │
│  │  • IndicatorRepository (ABC)                          │     │
│  │  • AssignmentRepository (ABC)                         │     │
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
│       └── assignment_repository.py
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
