# ZenLog — Plan de tests

**Projet** : ZenLog — Carnet de suivi bien-être
**Méthodologie** : TDD (Test-Driven Development)
**Auteur** : Cécile Hirschauer
**Date** : 18 mars 2026

---

## 1. Stratégie de test

### Approche TDD

Les tests sont écrits **avant** le code d'implémentation. Chaque user story suit le cycle :

1. **RED** : écrire un test qui échoue (le comportement attendu n'existe pas encore)
2. **GREEN** : écrire le minimum de code pour faire passer le test
3. **REFACTOR** : améliorer le code sans casser les tests

Ce cycle est visible dans l'historique Git : les commits de test précèdent les commits d'implémentation dans chaque PR.

### Pyramide de tests

```
        /‾‾‾‾‾‾‾‾‾‾\
       /  E2E / API   \        ← peu (validation finale)
      /  (Postman/curl) \
     /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
    /   Integration tests   \   ← moyen (DRF + BDD)
   /  (Django TestCase + DB) \
  /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
 /     Unit tests (domain)     \ ← beaucoup (coeur metier)
/   (pure Python, no Django)    \
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

| Niveau | Scope | Framework | Base de données | Cible couverture |
|---|---|---|---|---|
| **Unitaire (domaine)** | Entités, services métier, value objects | `pytest` (Python pur) | Non (mocks) | > 80% |
| **Intégration** | API endpoints, permissions, ORM | `pytest-django` + DRF `APIClient` | Oui (PostgreSQL test) | > 60% |
| **Sécurité** | Permissions, accès non autorisé, injection | `pytest-django` + DRF `APIClient` | Oui | 100% des scénarios critiques |

---

## 2. Tests unitaires domaine (TDD, intégrés au développement)

Ces tests vivent dans `tests/domain/` et s'exécutent **sans Django ni base de données**. Ils testent la logique métier pure.

### 2.1 BC Wellness Tracking — TrackingService

| ID | Test | Entrée | Résultat attendu | Règle testée |
|---|---|---|---|---|
| T-D-01 | Créer une entrée valide | patient_id, indicator(min=1, max=10), value=7, date=today | `WellnessEntry` créée avec les bonnes valeurs | Happy path |
| T-D-02 | Rejeter une valeur hors plage (trop haute) | value=11, indicator(max=10) | `ValueError` levée | Validation plage |
| T-D-03 | Rejeter une valeur hors plage (trop basse) | value=0, indicator(min=1) | `ValueError` levée | Validation plage |
| T-D-04 | Rejeter un doublon (même patient, indicateur, date) | Entrée existante pour ce triplet | `DuplicateEntryError` levée | Unicité quotidienne |
| T-D-05 | Modifier une entrée existante | entry_id, new_value=8 | Entrée mise à jour | Modification autorisée |
| T-D-06 | Rejeter la modification par un autre patient | patient_id_A modifie entrée de patient_id_B | `PermissionError` levée | Propriété des données |
| T-D-07 | Calculer la tendance sur 7 jours | 5 entrées sur 7 jours | Moyenne sur 5 (pas 7), entry_count=5 | Calcul tendance (exclure jours vides) |
| T-D-08 | Tendance sans données | 0 entrées sur la période | `Trend` avec average=None, entry_count=0 | Cas limite |
| T-D-09 | Historique filtré par date | date_from, date_to | Seules les entrées dans la plage | Filtrage |
| T-D-10 | Historique filtré par indicateur | indicator_id | Seules les entrées de cet indicateur | Filtrage |

### 2.2 BC Coaching — CoachingService

| ID | Test | Entrée | Résultat attendu | Règle testée |
|---|---|---|---|---|
| T-D-11 | Coach accède aux données d'un patient affecté | coach_id avec affectation active | Données retournées | Accès conditionné |
| T-D-12 | Coach refuse l'accès sans affectation | coach_id sans affectation | `AccessDeniedError` levée | Accès conditionné |
| T-D-13 | Coach refuse l'accès avec affectation inactive | affectation is_active=False | `AccessDeniedError` levée | Affectation active requise |
| T-D-14 | Liste des patients d'un coach | coach_id avec 3 affectations (2 actives, 1 inactive) | 2 patient_ids retournés | Filtrage actif |
| T-D-15 | Désactivation d'une affectation | assignment_id | is_active=False, end_date renseignée | Révocation d'accès |

### 2.3 Entités — Validations internes

| ID | Test | Entrée | Résultat attendu | Règle testée |
|---|---|---|---|---|
| T-D-16 | `Indicator.is_value_in_range()` avec valeur valide | value=5, min=1, max=10 | `True` | Validation entité |
| T-D-17 | `Indicator.is_value_in_range()` avec valeur invalide | value=15, min=1, max=10 | `False` | Validation entité |
| T-D-18 | `WellnessEntry.is_owned_by()` avec bon patient | patient_id correspondant | `True` | Propriété |
| T-D-19 | `WellnessEntry.is_owned_by()` avec mauvais patient | patient_id différent | `False` | Propriété |
| T-D-20 | `Assignment.is_currently_active()` actif | is_active=True, end_date=None | `True` | Statut affectation |
| T-D-21 | `Assignment.is_currently_active()` désactivé | is_active=False | `False` | Statut affectation |

---

## 3. Tests d'intégration API (Phase 4 — Validation)

Ces tests vivent dans `tests/infrastructure/` et utilisent Django TestCase avec une base PostgreSQL de test. Ils vérifient que l'API HTTP fonctionne de bout en bout.

### 3.1 Authentification

| ID | Test | Méthode | Endpoint | Résultat attendu |
|---|---|---|---|---|
| T-I-01 | Inscription réussie | POST | `/api/auth/register/` | 201, user créé, pas de mot de passe en clair dans la réponse |
| T-I-02 | Inscription doublon (email existant) | POST | `/api/auth/register/` | 400, message d'erreur |
| T-I-03 | Connexion réussie | POST | `/api/auth/token/` | 200, access + refresh tokens retournés |
| T-I-04 | Connexion échouée (mauvais mot de passe) | POST | `/api/auth/token/` | 401 |
| T-I-05 | Refresh token | POST | `/api/auth/token/refresh/` | 200, nouveau access token |
| T-I-06 | Accès sans token | GET | `/api/wellness/entries/` | 401 Unauthorized |

### 3.2 Endpoints Wellness (patient)

| ID | Test | Méthode | Endpoint | Auth | Résultat attendu |
|---|---|---|---|---|---|
| T-I-07 | Créer une entrée | POST | `/api/wellness/entries/` | Patient | 201, entrée créée |
| T-I-08 | Créer un doublon | POST | `/api/wellness/entries/` | Patient | 400, erreur unicité |
| T-I-09 | Lister mes entrées | GET | `/api/wellness/entries/` | Patient | 200, uniquement mes entrées |
| T-I-10 | Voir une entrée d'un autre patient | GET | `/api/wellness/entries/{id}/` | Patient A | 404 (pas 403, pour ne pas révéler l'existence) |
| T-I-11 | Modifier mon entrée | PATCH | `/api/wellness/entries/{id}/` | Patient | 200, valeur mise à jour |
| T-I-12 | Tendances 7 jours | GET | `/api/wellness/trends/?period=7` | Patient | 200, moyennes par indicateur |
| T-I-13 | Lister les indicateurs | GET | `/api/wellness/indicators/` | Patient | 200, indicateurs actifs uniquement |

### 3.3 Endpoints Coaching (coach)

| ID | Test | Méthode | Endpoint | Auth | Résultat attendu |
|---|---|---|---|---|---|
| T-I-14 | Liste de mes patients | GET | `/api/coaching/patients/` | Coach | 200, patients affectés actifs |
| T-I-15 | Données d'un patient affecté | GET | `/api/coaching/patients/{id}/entries/` | Coach | 200, entrées du patient |
| T-I-16 | Données d'un patient non affecté | GET | `/api/coaching/patients/{id}/entries/` | Coach | 403 Forbidden |
| T-I-17 | Coach tente de créer une entrée | POST | `/api/wellness/entries/` | Coach | 403 Forbidden |

### 3.4 Endpoints Admin

| ID | Test | Méthode | Endpoint | Auth | Résultat attendu |
|---|---|---|---|---|---|
| T-I-18 | Créer un indicateur | POST | `/api/wellness/indicators/` | Admin | 201 |
| T-I-19 | Créer une affectation | POST | `/api/coaching/assignments/` | Admin | 201 |
| T-I-20 | Désactiver une affectation | PATCH | `/api/coaching/assignments/{id}/` | Admin | 200, is_active=false |
| T-I-21 | Patient tente de créer un indicateur | POST | `/api/wellness/indicators/` | Patient | 403 Forbidden |

---

## 4. Tests de sécurité (Phase 4 — Validation)

Tests spécifiques aux scénarios de sécurité. Chaque test vérifie qu'un accès non autorisé est correctement bloqué.

| ID | Scénario | Action | Résultat attendu |
|---|---|---|---|
| T-S-01 | Accès sans authentification | GET /api/wellness/entries/ sans token | 401 |
| T-S-02 | Token expiré | GET avec access token expiré | 401 |
| T-S-03 | Escalade de rôle (patient → admin) | Patient POST /api/wellness/indicators/ | 403 |
| T-S-04 | Escalade de rôle (coach → écriture) | Coach POST /api/wellness/entries/ | 403 |
| T-S-05 | Accès données d'un autre patient | Patient A GET entrée de Patient B | 404 |
| T-S-06 | Coach accès sans affectation | Coach GET données patient non affecté | 403 |
| T-S-07 | Coach accès affectation inactive | Coach GET données patient, affectation désactivée | 403 |
| T-S-08 | Injection SQL dans les filtres | GET /api/wellness/entries/?date='; DROP TABLE-- | 400 ou résultats normaux (pas d'erreur SQL) |
| T-S-09 | Mot de passe non exposé | GET /api/auth/me/ | password_hash absent de la réponse JSON |
| T-S-10 | Rate limiting sur login | 10x POST /api/auth/token/ avec mauvais mdp | 429 Too Many Requests |

---

## 5. Outils et exécution

| Outil | Usage |
|---|---|
| `pytest` | Runner principal, assertions |
| `pytest-django` | Intégration Django (fixtures, TestCase, DB test) |
| `pytest-cov` | Couverture de code |
| `factory-boy` | Factories pour générer des données de test (User, Indicator, etc.) |
| `unittest.mock` | Mocks des repositories pour les tests domaine |

### Commandes

```bash
# Tests domaine uniquement (rapides, pas de DB)
pytest tests/domain/ -v

# Tests intégration (avec DB)
pytest tests/infrastructure/ -v

# Tous les tests + couverture
pytest --cov=zenlog --cov-report=html

# CI (GitHub Actions)
pytest --tb=short --no-header -q
```

### Critères de validation

| Critère | Seuil |
|---|---|
| Tests domaine passent | 100% |
| Tests intégration passent | 100% |
| Tests sécurité passent | 100% |
| Couverture domaine | > 80% |
| Couverture globale | > 60% |
| Aucune régression sur main | CI verte obligatoire avant merge |
