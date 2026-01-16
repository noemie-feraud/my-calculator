"""
models/errors.py

But :
- Centraliser les messages d'erreur.
- Comme ça, on ne met pas des "strings" partout dans le code.
"""

from typing import Dict, Optional, Any

ERROR_MESSAGES: Dict[str, str] = {
    # Validation générale
    "EMPTY_EXPR": "Entrez une expression avant de calculer.",
    "MAX_LEN": "Expression trop longue.",
    "UNKNOWN_TOKEN": "Saisie invalide.",
    "INCOMPLETE_EXPR": "Expression incomplète.",
    "PAREN_MISMATCH": "Parenthèses invalides.",
    "DOUBLE_DOT": "Nombre invalide : deux points décimaux.",
    "OP_START": "Impossible de commencer par cet opérateur.",
    "DOUBLE_OPERATOR": "Deux opérateurs d'affilée sont interdits.",
    "DOT_START": "Impossible de commencer par un point.",
    "DOT_AFTER_OPERATOR": "Impossible de mettre un point ici.",
    "LEADING_ZERO": "Zéro inutile au début du nombre (ex : 05).",
    "MISSING_OPERATOR_BEFORE_PAREN": "Il manque un opérateur avant la parenthèse.",
    "CLOSE_PAREN_START": "Impossible de commencer par ')'.",
    "CLOSE_PAREN_AFTER_OPERATOR": "Parenthèse fermante invalide après un opérateur.",
    "OP_AFTER_OPEN_PAREN": "Opérateur invalide juste après '('",
    "MISSING_OPERATOR_BEFORE_FUNCTION": "Il manque un opérateur avant une fonction scientifique.",
    "FACTORIAL_NO_ARG": "Factorielle : aucun argument.",
    "FACTORIAL_BAD_POS": "Factorielle : position invalide.",
    "NO_LAST_RESULT": "Aucun résultat précédent disponible.",

    # Moteur / calcul
    "TOKEN_ERROR": "Erreur de lecture de l'expression.",
    "PARSE_ERROR": "Erreur de parsing (priorités/parenthèses).",
    "EVAL_ERROR": "Erreur lors du calcul.",
    "DIV_ZERO": "Division par zéro impossible.",
    "BAD_BINARY_OP": "Expression invalide (opérateur binaire).",
    "BAD_UNARY_MINUS": "Expression invalide (moins unaire).",

    # Scientifique
    "POW_EXP_NOT_INT": "Puissance : l'exposant doit être un entier.",
    "POW_ZERO_NEG": "Puissance : 0 exposant négatif est impossible.",
    "SQRT_NEGATIVE": "Racine carrée impossible sur un nombre négatif.",
    "SQRT_NO_ARG": "Racine carrée : aucun argument.",
    "ABS_NO_ARG": "Valeur absolue : aucun argument.",
    "INV_NO_ARG": "Inverse : aucun argument.",
    "INV_ZERO": "Inverse impossible : division par zéro.",
    "FACTORIAL_NOT_INT": "Factorielle : entier >= 0 requis.",
    "MOD_ERROR": "Modulo : entiers requis et diviseur non nul.",
}


def get_message(code: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Retourne le message associé à un code.
    context sert si on veut remplacer des variables dans le message.
    """
    msg = ERROR_MESSAGES.get(code, "Erreur inconnue.")
    if context:
        for k, v in context.items():
            msg = msg.replace("{" + str(k) + "}", str(v))
    return msg
