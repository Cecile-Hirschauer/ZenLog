# ZenLog — Cahier des charges (version light)

**Projet** : ZenLog — Carnet de suivi bien-être
**Version** : 1.0 (MVP)
**Auteur** : Cécile Hirschauer
**Date** : 18 mars 2026
**Durée de réalisation** : 3 jours (solo)

---

## 1. Contexte et objectif

ZenLog est une API back-end permettant à des particuliers de suivre quotidiennement leurs indicateurs de bien-être (humeur, sommeil, activité physique, hydratation) et à un coach référent de consulter ces données en lecture seule pour adapter ses recommandations.

Le projet répond à un triple problème identifié chez les particuliers soucieux de leur santé : la perte de données (carnets papier, fichiers Excel), l'absence de confidentialité (applications gratuites monétisant les données), et le manque de collaboration sécurisée entre patient et coach.

---

## 2. Acteurs du système

| Acteur | Description | Droits |
|---|---|---|
| **Patient** | Utilisateur principal. Saisit et consulte ses données de bien-être. | Lecture/écriture sur ses propres données uniquement |
| **Coach** | Professionnel du bien-être. Consulte les données de ses patients affectés. | Lecture seule sur les données de ses patients affectés |
| **Administrateur** | Gestionnaire de la plateforme. Gère les comptes, affectations et indicateurs. | Accès complet en gestion |

---

## 3. Exigences fonctionnelles

### 3.1 BC Wellness Tracking (suivi bien-être)

| ID | User Story | Critères d'acceptation | Priorité |
|---|---|---|---|
| US-1 | En tant que patient, je veux saisir mon bien-être du jour pour un indicateur donné | La valeur est validée dans la plage de l'indicateur. Une seule saisie par indicateur et par jour. | Must have |
| US-2 | En tant que patient, je veux modifier ma saisie du jour | Seul le propriétaire peut modifier. La modification respecte la validation de plage. | Must have |
| US-3 | En tant que patient, je veux consulter mon historique d'entrées | Filtrage par date et par indicateur. Pagination. Seules mes données sont visibles. | Must have |
| US-4 | En tant que patient, je veux voir mes tendances sur 7 et 30 jours | Moyenne calculée en excluant les jours sans saisie. Pas de valeur 0 par défaut. | Should have |
| US-5 | En tant qu'admin, je veux gérer les types d'indicateurs | CRUD indicateurs avec nom, unité, plage min/max. Seul l'admin y a accès. | Must have |

### 3.2 BC Coaching (accompagnement coach)

| ID | User Story | Critères d'acceptation | Priorité |
|---|---|---|---|
| US-6 | En tant que coach, je veux consulter les données d'un patient | Accès conditionné à une affectation active. Lecture seule stricte. | Must have |
| US-7 | En tant que coach, je veux voir la liste de mes patients | Liste filtrée par affectations actives uniquement. | Must have |
| US-8 | En tant qu'admin, je veux affecter un coach à un patient | Création d'une affectation avec date de début et statut actif. | Must have |
| US-9 | En tant qu'admin, je veux désactiver une affectation | Désactivation avec date de fin. Le coach perd immédiatement l'accès. | Should have |

### 3.3 Authentification (délégué à Django)

| ID | Fonctionnalité | Détail |
|---|---|---|
| AUTH-1 | Inscription | Création de compte par email + mot de passe. Validation email unique, mot de passe robuste. |
| AUTH-2 | Connexion | Authentification JWT. Access token (15 min) + refresh token (24h). |
| AUTH-3 | Gestion des rôles | Trois rôles : patient, coach, admin. Attribués par l'administrateur. |

---

## 4. Exigences non-fonctionnelles

### 4.1 Sécurité

| Exigence | Mesure technique |
|---|---|
| Authentification forte | JWT avec rotation des refresh tokens. Durée de vie courte (15 min access). |
| Autorisation par rôle | Permissions DRF par endpoint (`IsPatient`, `IsCoach`, `IsAdmin`). |
| Chiffrement en transit | HTTPS obligatoire (TLS 1.2+) via Azure App Service. |
| Chiffrement au repos | AES-256 natif Azure Database for PostgreSQL. |
| Protection contre les attaques | Rate limiting sur les endpoints sensibles (login, register). |
| Logs d'accès | Journalisation des accès aux données de santé (qui a consulté quoi, quand). |

### 4.2 Conformité RGPD

| Exigence | Mesure |
|---|---|
| Données de santé (art. 9) | Accès strictement limité au propriétaire + coach affecté. Pas de partage à des tiers. |
| Droit à l'effacement (art. 17) | Suppression de compte → anonymisation des entrées (soft delete). |
| Minimisation des données (art. 5) | Seules les données nécessaires au suivi sont collectées. Pas de tracking, pas de profilage. |
| Consentement | Inscription volontaire. L'affectation coach/patient est gérée par un admin avec accord préalable. |

### 4.3 Performance

| Exigence | Cible |
|---|---|
| Temps de réponse API | < 200ms pour les endpoints CRUD, < 500ms pour les agrégations |
| Optimisation ORM | `select_related` / `prefetch_related` pour éviter les requêtes N+1 |
| Pagination | Obligatoire sur les endpoints de liste (défaut : 20 résultats par page) |
| Indexation BDD | Index sur les colonnes fréquemment filtrées (patient_id, indicator_id, date) |

### 4.4 Maintenabilité

| Exigence | Mesure |
|---|---|
| Architecture hexagonale | Domaine pur (Python) découplé de l'infrastructure (Django). |
| TDD | Tests écrits avant le code. Couverture cible > 80% sur le domaine. |
| Documentation API | Swagger/OpenAPI généré automatiquement et toujours synchronisé avec le code. |
| Conventions de code | Linting (flake8), typage (type hints), nommage anglais dans le code. |

---

## 5. Contraintes

| Contrainte | Détail |
|---|---|
| **Délai** | 3 jours, développeuse solo |
| **Stack imposée** | Python / Django + DRF / PostgreSQL |
| **Déploiement** | Azure (App Service + Azure Database for PostgreSQL) |
| **Méthodologie** | Agile (Kanban), TDD, DDD avec architecture hexagonale |
| **Versioning** | Git + GitHub, commits atomiques, branches feature |
| **Périmètre** | API back-end uniquement (pas de front-end) |

---

## 6. Livrables attendus

| # | Livrable | Format |
|---|---|---|
| 1 | Code source | Repository GitHub (public ou privé) |
| 2 | API fonctionnelle déployée | URL Azure accessible |
| 3 | Documentation API | Swagger UI auto-générée |
| 4 | Documentation projet | README (installation, architecture, choix techniques) |
| 5 | Tests | Tests unitaires domaine + tests d'intégration API |
| 6 | Gestion de projet | Board Trello (Kanban) |

---

## 7. Hors périmètre (v1)

Les éléments suivants sont explicitement exclus du MVP pour respecter le délai de 3 jours :

- Front-end (web ou mobile)
- Notifications (push, email, SMS)
- Messagerie coach/patient
- Gestion de paiements ou abonnements
- Export PDF/CSV des données
- Fonctionnalités sociales (communauté, partage)
- Internationalisation (i18n)

Ces fonctionnalités pourront être ajoutées dans une version ultérieure sans impacter l'architecture existante, grâce à la séparation domaine/infrastructure.

---

## 8. Glossaire

Se référer au langage ubiquitaire défini dans le document `JUSTIFICATION_PROJET.md`, section 4.1.
