# 🔐 Cyberscan Pro+ – Scanner de sécurité réseau local

**Cyberscan Pro+** est un outil avancé de cybersécurité développé en Python. 
Il permet d'analyser en profondeur un domaine en local sans dépendance externe, à l'aide de modules standards uniquement. Ce scanner fournit des diagnostics réseau utiles à des fins d'apprentissage,
de test ou d’audit de base.

---

## 🎯 Objectif

Cyberscan Pro+ effectue automatiquement une série d'analyses sur un nom de domaine :

- Résolution d’IP
- Ping avec taux de réussite
- Détection de système via analyse TTL
- Résolution inverse (reverse DNS)
- Scan de ports critiques : `22`, `80`, `443`, `3306`
- Extraction de bannières si possible
- Simulation de requête HTTP GET
- Vérification du support HTTPS
- Scan de sous-domaines communs (`mail.`, `admin.`, etc.)
- Génération d’un rapport texte complet
- Création d’un historique global
- Affichage ASCII des ports ouverts
- Système de blocage après 3 erreurs

---

## 🧩 Modules utilisés

Aucun module externe requis. Tout est développé à partir des modules Python standards :

```python
socket, subprocess, datetime, time, os
🛠️ Installation
✅ Prérequis
Python 3.9+

🧪 Fonctionnement
L'utilisateur entre un nom de domaine, puis le programme :

Résout l'adresse IP

Ping 3 fois et affiche les résultats

Analyse le TTL pour deviner le système (Windows/Linux)

Tente une résolution DNS inverse

Scanne les ports 22, 80, 443, 3306

Extrait les bannières sur les ports ouverts

Effectue une requête HTTP GET sur port 80

Vérifie si le port 443 est accessible (HTTPS)

Tente de détecter des sous-domaines classiques

Génère un fichier rapport_<domaine>.txt

Ajoute l'analyse à historique.txt avec date et heure

Affiche une carte ASCII des ports ouverts

🛑 Le programme bloque après 3 domaines invalides consécutifs.

📁 Structure du projet
bash
Copier
Modifier
cyberscan-pro/
├── cyberscan.py               # Script principal
├── rapport_<domaine>.txt      # Rapport généré
├── historique.txt             # Historique global
├── README.md                  # Documentation
