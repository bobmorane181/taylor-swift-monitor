# Déploiement sur PythonAnywhere (GRATUIT)

PythonAnywhere offre un compte gratuit permettant de faire tourner des scripts Python en continu.

## Étape 1 : Créer un compte PythonAnywhere

1. Allez sur **https://www.pythonanywhere.com**
2. Cliquez sur **"Start running Python online in less than a minute"**
3. Créez un compte **Beginner** (gratuit)
4. Confirmez votre email

## Étape 2 : Se connecter et accéder à la console

1. Connectez-vous à votre compte PythonAnywhere
2. Allez dans l'onglet **"Consoles"**
3. Cliquez sur **"Bash"** pour ouvrir un terminal

## Étape 3 : Cloner votre repository GitHub

Dans la console Bash, tapez :

```bash
git clone https://github.com/bobmorane181/taylor-swift-monitor.git
cd taylor-swift-monitor
```

## Étape 4 : Installer les dépendances

```bash
pip3 install --user -r requirements.txt
```

## Étape 5 : Configurer les variables d'environnement

Créez un fichier pour vos variables d'environnement :

```bash
nano ~/taylor-swift-monitor/.env
```

Ajoutez cette ligne (remplacez par votre vrai webhook) :
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/VOTRE_WEBHOOK_ICI
```

Sauvegardez avec `Ctrl+O`, puis `Enter`, puis `Ctrl+X` pour quitter.

## Étape 6 : Modifier monitor.py pour charger le .env

On doit ajouter le support du fichier .env. Dans la console :

```bash
nano monitor.py
```

Ajoutez ces lignes **tout en haut** après les imports existants :

```python
# Charge les variables d'environnement depuis .env si présent
from pathlib import Path
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
```

OU plus simple, installez python-dotenv :

```bash
pip3 install --user python-dotenv
```

Et ajoutez au début de monitor.py (après les imports) :
```python
from dotenv import load_dotenv
load_dotenv()
```

## Étape 7 : Tester le script

```bash
python3 monitor.py
```

Vous devriez voir :
```
Moniteur initialisé
URL surveillée: https://storeca.taylorswift.com/...
--- Vérification en cours ---
```

Appuyez sur `Ctrl+C` pour arrêter le test.

## Étape 8 : Créer une tâche planifiée (Always-On)

### Option A : Tâche planifiée (Recommandé pour le plan gratuit)

1. Allez dans l'onglet **"Tasks"**
2. Dans "Scheduled tasks", entrez :
   - **Command** : `cd /home/VOTRE_USERNAME/taylor-swift-monitor && python3 monitor.py`
   - **Hour** : `*` (chaque heure)
   - **Minute** : `*/30` (toutes les 30 minutes)
3. Cliquez sur **"Create"**

**Note** : Le plan gratuit limite les tâches planifiées à une fois par jour. Pour une surveillance continue, passez à l'Option B.

### Option B : Script Always-On (Nécessite compte payant - 5$/mois)

Si vous voulez une vraie surveillance 24/7 :

1. Allez dans l'onglet **"Tasks"**
2. Cherchez **"Always-on tasks"**
3. Ajoutez votre script
4. **Attention** : Nécessite un compte payant

### Option C : Utiliser nohup (Plan gratuit, mais se termine après 24h)

Dans la console Bash :

```bash
cd ~/taylor-swift-monitor
nohup python3 monitor.py > monitor.log 2>&1 &
```

Pour vérifier que ça tourne :
```bash
ps aux | grep monitor.py
```

Pour voir les logs :
```bash
tail -f ~/taylor-swift-monitor/monitor.log
```

Pour arrêter :
```bash
pkill -f monitor.py
```

**Attention** : PythonAnywhere arrête les processus après 24h sur le plan gratuit.

## Étape 9 : Mettre à jour le code

Quand vous modifiez votre code sur GitHub, dans la console Bash :

```bash
cd ~/taylor-swift-monitor
git pull origin main
pkill -f monitor.py  # Arrête l'ancien processus
nohup python3 monitor.py > monitor.log 2>&1 &  # Relance
```

## Limitations du plan gratuit PythonAnywhere

- ❌ Processus arrêtés après 24h (nécessite relance manuelle)
- ❌ Tâches planifiées limitées à 1x/jour
- ✅ Connexion HTTPS autorisée
- ✅ 512 MB de stockage
- ✅ Accès console gratuit

## Alternative recommandée

Pour une vraie surveillance 24/7 **gratuite**, je recommande plutôt **Render.com** (voir RENDER_DEPLOYMENT.md) qui offre un vrai Background Worker gratuit qui ne s'arrête jamais.

## Script de relance automatique

Créez un script qui relance le moniteur tous les jours :

```bash
nano ~/restart_monitor.sh
```

Contenu :
```bash
#!/bin/bash
cd ~/taylor-swift-monitor
git pull origin main
pkill -f monitor.py
sleep 2
nohup python3 monitor.py > monitor.log 2>&1 &
echo "Monitor restarted at $(date)"
```

Rendez-le exécutable :
```bash
chmod +x ~/restart_monitor.sh
```

Ajoutez une tâche planifiée quotidienne dans PythonAnywhere :
- Command : `/home/VOTRE_USERNAME/restart_monitor.sh`
- Hour : `00` (minuit)
- Minute : `00`

## Dépannage

### Le script ne démarre pas
```bash
cd ~/taylor-swift-monitor
python3 monitor.py  # Lancer manuellement pour voir l'erreur
```

### Vérifier les logs
```bash
tail -f ~/taylor-swift-monitor/monitor.log
```

### Le webhook ne fonctionne pas
Vérifiez que le fichier .env contient bien votre webhook :
```bash
cat ~/taylor-swift-monitor/.env
```

## Résumé

PythonAnywhere gratuit fonctionne **MAIS** nécessite une relance manuelle ou quotidienne. Pour du 24/7 vraiment gratuit et sans maintenance, utilisez plutôt **Render.com**.
