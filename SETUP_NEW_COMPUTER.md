# Installation sur un nouvel ordinateur

Ce guide explique comment installer et lancer le moniteur Taylor Swift sur un nouvel ordinateur.

## Prérequis

1. **Python 3.11 ou supérieur**
   - Téléchargez depuis https://www.python.org/downloads/
   - ⚠️ IMPORTANT : Cochez "Add Python to PATH" lors de l'installation

2. **Git** (optionnel mais recommandé)
   - Téléchargez depuis https://git-scm.com/downloads/

## Méthode 1 : Cloner depuis GitHub (Recommandé)

### Étape 1 : Cloner le repository

Ouvrez un terminal (Command Prompt ou PowerShell) et tapez :

```bash
cd C:\Users\VOTRE_NOM_UTILISATEUR\
git clone https://github.com/bobmorane181/taylor-swift-monitor.git
cd taylor-swift-monitor
```

### Étape 2 : Installer les dépendances Python

```bash
python -m pip install -r requirements.txt
```

### Étape 3 : Créer le fichier de configuration

Créez le fichier `config.json` dans le dossier :

```json
{
  "url": "https://storeca.taylorswift.com/collections/the-holiday-collection",
  "discord_webhook_url": "VOTRE_WEBHOOK_DISCORD_ICI",
  "check_interval_seconds": 30
}
```

**Remplacez `VOTRE_WEBHOOK_DISCORD_ICI` par votre vrai webhook Discord !**

### Étape 4 : Tester

```bash
python test_deployment.py
```

Vous devriez voir : `Score: 6/6 tests reussis`

### Étape 5 : Lancer le moniteur

```bash
python monitor.py
```

C'est tout ! Le moniteur tourne maintenant.

---

## Méthode 2 : Télécharger en ZIP (Sans Git)

### Étape 1 : Télécharger le projet

1. Allez sur https://github.com/bobmorane181/taylor-swift-monitor
2. Cliquez sur le bouton vert **"Code"**
3. Sélectionnez **"Download ZIP"**
4. Extrayez le ZIP dans un dossier (ex: `C:\Users\VOTRE_NOM\taylor-swift-monitor`)

### Étape 2 : Installer Python

Téléchargez et installez Python depuis https://www.python.org/downloads/

⚠️ **Cochez "Add Python to PATH"**

### Étape 3 : Installer les dépendances

Ouvrez un terminal dans le dossier extrait :

```bash
cd C:\Users\VOTRE_NOM\taylor-swift-monitor
python -m pip install -r requirements.txt
```

### Étape 4 : Créer config.json

Dans le dossier `taylor-swift-monitor`, créez un fichier `config.json` avec :

```json
{
  "url": "https://storeca.taylorswift.com/collections/the-holiday-collection",
  "discord_webhook_url": "VOTRE_WEBHOOK_DISCORD_ICI",
  "check_interval_seconds": 30
}
```

### Étape 5 : Lancer

```bash
python monitor.py
```

---

## Méthode 3 : Transférer depuis l'ancien ordinateur

Si vous voulez copier directement depuis votre ancien PC :

### Fichiers à copier

Copiez **tout le dossier** `taylor-swift-monitor` sur le nouvel ordinateur.

**IMPORTANT** : Ne copiez PAS ces fichiers (ils sont spécifiques à votre ancien PC) :
- `state.json` (sera recréé automatiquement)
- `monitor.log` (sera recréé)
- `__pycache__/` (sera recréé)

### Sur le nouvel ordinateur

1. Installez Python 3.11+
2. Ouvrez un terminal dans le dossier
3. Installez les dépendances :
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Lancez :
   ```bash
   python monitor.py
   ```

---

## Fichiers essentiels nécessaires

Voici les fichiers dont vous avez ABSOLUMENT besoin :

### Fichiers de code (nécessaires)
- ✅ `monitor.py` - Script principal
- ✅ `requirements.txt` - Liste des dépendances
- ✅ `config.example.json` - Exemple de configuration
- ✅ `test_alert.py` - Pour tester les notifications
- ✅ `test_deployment.py` - Pour tester l'installation

### Fichier de configuration (à créer)
- ✅ `config.json` - **VOUS DEVEZ LE CRÉER** avec votre webhook Discord

### Fichiers optionnels
- ⚠️ `state.json` - État des produits connus (sera recréé automatiquement)
- ⚠️ `*.log` - Fichiers de logs (seront recréés)
- ❌ `__pycache__/` - Cache Python (pas besoin)

---

## Vérification rapide

Une fois installé, testez avec :

```bash
# Test 1 : Vérifier l'installation
python test_deployment.py

# Test 2 : Envoyer une notification de test
python send_test_notification.py

# Test 3 : Lancer le moniteur
python monitor.py
```

---

## Démarrage automatique au démarrage de Windows

### Option A : Créer un raccourci dans le dossier Démarrage

1. Créez un fichier `start_monitor.bat` :
   ```batch
   @echo off
   cd C:\Users\VOTRE_NOM\taylor-swift-monitor
   python monitor.py
   pause
   ```

2. Faites un clic droit → **Créer un raccourci**

3. Copiez le raccourci dans :
   ```
   C:\Users\VOTRE_NOM\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
   ```

Le moniteur démarrera automatiquement à chaque démarrage de Windows !

### Option B : Tâche planifiée Windows

1. Ouvrez **Planificateur de tâches** (Task Scheduler)
2. Créez une tâche basique
3. Déclencheur : **Au démarrage**
4. Action : Démarrer un programme
   - Programme : `python`
   - Arguments : `C:\Users\VOTRE_NOM\taylor-swift-monitor\monitor.py`
   - Démarrer dans : `C:\Users\VOTRE_NOM\taylor-swift-monitor`

---

## Dépannage

### "Python n'est pas reconnu..."
- Réinstallez Python en cochant "Add Python to PATH"
- OU ajoutez Python au PATH manuellement

### "pip n'est pas reconnu..."
- Utilisez `python -m pip` au lieu de juste `pip`

### "ModuleNotFoundError: No module named 'requests'"
- Installez les dépendances : `python -m pip install -r requirements.txt`

### Le moniteur ne trouve pas config.json
- Vérifiez que `config.json` est dans le même dossier que `monitor.py`
- Vérifiez que le nom est exactement `config.json` (pas `config.json.txt`)

---

## Récupérer votre webhook Discord

Si vous avez perdu votre webhook Discord :

1. Allez sur votre serveur Discord
2. Paramètres du serveur → Intégrations → Webhooks
3. Créez-en un nouveau ou copiez l'URL d'un existant

---

## Support

Si vous avez des problèmes :

1. Vérifiez que Python est installé : `python --version`
2. Vérifiez que les dépendances sont installées : `python -m pip list`
3. Testez avec : `python test_deployment.py`
4. Consultez les logs : `monitor.log`
