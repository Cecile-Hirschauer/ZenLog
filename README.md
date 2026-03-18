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
 

### 3.3 Base de données : PostgreSQL 15+

| Besoin métier | Justification technique |
|---|---|
| Données de santé sensibles nécessitant intégrité et fiabilité | PostgreSQL est conforme ACID, garantissant que chaque saisie est soit complètement enregistrée, soit pas du tout (pas de données corrompues en cas de crash). |
| Requêtes d'agrégation (moyennes, tendances sur 7/30 jours) | PostgreSQL excelle sur les fonctions d'agrégation et les window functions, essentielles pour calculer des tendances sans surcharger le serveur applicatif. |
| Contraintes d'accès au niveau base | PostgreSQL supporte le Row-Level Security (RLS), permettant d'ajouter une couche de sécurité supplémentaire directement en base si nécessaire (défense en profondeur). |
| Déploiement cloud (Azure) | Azure Database for PostgreSQL est un service managé disponible en free tier, avec sauvegardes automatiques, chiffrement au repos et haute disponibilité configurable. Cela répond aux exigences de disponibilité et de résilience du cahier des charges. |
| Évolutivité | Si le nombre d'utilisateurs croît, PostgreSQL supporte la réplication, le partitionnement et l'indexation avancée, contrairement à SQLite qui est limité à un seul writer. |


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
