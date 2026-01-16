# Pascaline — Calculatrice (Standard + Scientifique) en CustomTkinter

**Pascaline** est une calculatrice GUI en Python avec **CustomTkinter**.  
Objectifs du projet : une appli **simple à expliquer**, robuste côté erreurs, avec un vrai moteur d’évaluation **sans `eval()`** et **sans `math`**.

> Interaction : **clics uniquement** (pas de saisie clavier PC).  
> L’expression est construite bouton par bouton, puis validée et évaluée.

---

## Fonctionnalités

### Standard
- Opérations : `+` `-` `*` `/`
- Parenthèses : `(` `)`
- Décimaux : `.`
- Priorités respectées : parenthèses → `* / %` → `+ -` (+ gestion de `^`)

### Scientifique (bouton **SCI**)
- `sqrt(x)` (affiché `√`) : racine carrée (méthode numérique, sans `math`)
- `abs(x)` (affiché `|x|`) : valeur absolue
- `inv(x)` (affiché `1/x`) : inverse
- `a^b` : puissance (**exposant entier uniquement**)
- `x²`, `x³` : raccourcis (en réalité `^2` / `^3`)
- `%` : modulo (**entiers uniquement**, diviseur non nul)
- `!` : factorielle (**postfix**, entier ≥ 0)


### Historique & mémoire

- Historique en mémoire (pas de base de données)
- Clic sur une ligne = rappel de l’expression
- Mémoire : `MC`, `MR`, `M+`, `M-`


### Gestion d’erreurs

- Validation au clic + validation finale au `=`
- Messages explicites : parenthèses invalides, double opérateur, division par zéro, etc.

---

## Prérequis
- Python **3.10+** recommandé
- Dépendance : `customtkinter`

---

## Installation

```bash
pip install -r requirements.txt
```

## Lancer l’application

```bash
python main.py
```

## Utilisation (boutons importants)

* `=` : calcule l’expression *(après validation finale)*

* `C` : efface uniquement l’expression + les messages *(garde historique + mémoire)*

* `Réinitialiser (AC)` : reset complet *(retour à l’état initial)*

* `⌫` : supprime le dernier caractère

* `SCI` : affiche/masque le clavier scientifique

## Comportement après un résultat

Si tu tapes un **chiffre** après `=` → nouvelle expression

Si tu tapes un **opérateur** après `=` → continue le calcul à partir du dernier résultat


## Règles de validation (ce que l’app empêche)

**Quelques règles (pour éviter les expressions impossibles) :**

* Pas deux opérateurs d’affilée (`+``*`, `-``-` est géré comme moins unaire selon le contexte)

* Parenthèses cohérentes et équilibrées

* Un seul `.` par nombre

* Pas de nombres du type `05` (zéro inutile au début)

* Factorielle `!` seulement après un nombre ou une `)`

* Fonctions `sqrt(` / `abs(` / `inv(` seulement si c’est logique (pas collées à un nombre sans opérateur)


## Comment ça marche (moteur de calcul)

**L’évaluation se fait en 3 étapes (classique et expliquable) :**

1. Tokenize : transforme le texte en tokens (nombres, opérateurs, fonctions…)

2. Shunting-yard : conversion en RPN (notation polonaise inversée)

3. Évaluation RPN : calcul avec une pile

***Tout est fait sans eval() et sans math.***


## Structure du projet

* **main.py**
* **requirements.txt**
* **app_view.py**          # UI (CustomTkinter)
* **app_controller.py**    # handlers clics + pipeline
* **app_state.py**         # état global de l’app
* **engine.py**            # moteur d’évaluation (tokens → RPN → calcul)
* **validation.py**        # validation au clic + validation finale
* **scientific.py**        # fonctions scientifiques (sans math)
* **formatting.py**        # formatage du résultat
* **history.py**           # historique (en mémoire)
* **memory.py**            # mémoire (MC/MR/M+/M-)
* **errors.py**            # messages d’erreur centralisés
* **history_item.py**      # modèle item d’historique
* **test_.py**             # tests unitaires


### Tests

```bash
python -m unittest discover -s . -p "test_*.py"
```

### Limites connues

Pas de saisie clavier (clic uniquement)

* **^** : exposant entier uniquement

* **%** : entiers uniquement

* **sqrt** : approximation numérique (Newton)

---

## Crédits
**Projet étudiant — calculatrice GUI en Python / CustomTkinter.**

## [![Réalisé par](https://img.shields.io/badge/R%C3%89ALIS%C3%89-PAR-orange?style=for-the-badge)](https://forthebadge.com)

**Antuat Abdallah** | **Ahamada Assmine** | **Noémie Feraud**