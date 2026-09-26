
# Standards de code et d'expérimentation ML

## 1. Standards de code
- Utiliser des noms de variables et de fonctions explicites.
- Respecter les conventions PEP 8 de Python.
- Organiser le code en fonctions lorsque c'est pertinent.
- Ajouter des commentaires lorsque le code nécessite une explication.
- Éviter les répétitions inutiles.

## 2. Standards d'expérimentation Machine Learning
- Séparer les données d'entraînement et de test.
- Fixer un `random_state` pour rendre les résultats reproductibles.
- Utiliser un modèle de référence (DummyClassifier).
- Évaluer les modèles avec des métriques adaptées au problème.
- Comparer les résultats avant de choisir un modèle.
- Éviter les fuites de données (data leakage).

## 3. Tests et intégration continue
- Écrire des tests automatisés avec pytest.
- Exécuter les tests avant de fusionner une branche.
- Utiliser Git et GitHub pour suivre les modifications.
- Vérifier que le pipeline GitHub Actions passe avec succès.