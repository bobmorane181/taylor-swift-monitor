# Déploiement sur Koyeb (100% GRATUIT - Sans carte de crédit)

Koyeb offre un plan gratuit permanent pour les applications, idéal pour ce moniteur.

## Étape 1 : Créer un compte Koyeb

1. Allez sur **https://www.koyeb.com**
2. Cliquez sur **"Start for Free"** ou **"Sign Up"**
3. Connectez-vous avec **GitHub** (recommandé)
4. Pas de carte de crédit requise !

## Étape 2 : Créer un nouveau service

1. Dans le dashboard Koyeb, cliquez sur **"Create App"**
2. Sélectionnez **"GitHub"** comme source
3. Autorisez Koyeb à accéder à vos repositories
4. Sélectionnez le repository **taylor-swift-monitor**
5. Choisissez la branche **main**

## Étape 3 : Configuration du service

### Builder
- **Builder** : Laissez sur "Buildpack" (détection automatique)

### Configuration
- **Name** : `taylor-swift-monitor`
- **Region** : Choisissez la plus proche (ex: Frankfurt, Paris, ou Washington)
- **Instance type** : Sélectionnez **"Eco"** (gratuit)

### Build and deployment settings
- **Build command** : `pip install -r requirements.txt` (devrait être détecté automatiquement)
- **Run command** : `python monitor.py`

### Port (IMPORTANT)
Koyeb s'attend à une application web par défaut. Il faut indiquer que c'est un worker :
- Décochez **"Expose service"** ou mettez le port sur **8080** (on ne l'utilisera pas)

OU créez un fichier `nixpacks.toml` (voir étape optionnelle ci-dessous)

## Étape 4 : Variables d'environnement

Dans la section **"Environment variables"** :

1. Cliquez sur **"Add variable"**
2. Ajoutez :
   - **Key** : `DISCORD_WEBHOOK_URL`
   - **Value** : (collez votre URL webhook Discord)
   - Laissez **"Secret"** coché pour la sécurité

Optionnel :
   - **Key** : `CHECK_INTERVAL`
   - **Value** : `30`

## Étape 5 : Scaling

Dans **"Scaling"** :
- **Instances** : 1
- **Type** : Eco (gratuit)

## Étape 6 : Déployer

1. Cliquez sur **"Deploy"**
2. Koyeb va :
   - Cloner votre repository
   - Installer les dépendances
   - Lancer votre moniteur

## Étape 7 : Vérifier que ça fonctionne

1. Attendez que le déploiement soit terminé (statut "Healthy" en vert)
2. Allez dans **"Logs"**
3. Vous devriez voir :
   ```
   Moniteur initialisé
   URL surveillée: https://storeca.taylorswift.com/...
   --- Vérification en cours ---
   Trouvé 12 produits sur la page
   ```

## IMPORTANT : Contourner le problème de port

Koyeb s'attend à ce que votre app écoute sur un port (comme une app web). Pour un worker pur, il y a deux solutions :

### Solution 1 : Créer un fichier nixpacks.toml

Créez un fichier `nixpacks.toml` à la racine de votre projet :

```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "python monitor.py"
```

Commitez et poussez :
```bash
git add nixpacks.toml
git commit -m "Add nixpacks config for Koyeb"
git push origin main
```

### Solution 2 : Ajouter un serveur HTTP minimal (Quick fix)

Si Koyeb se plaint du port, on peut ajouter un mini serveur HTTP qui ne fait rien :

Créez `web_wrapper.py` :
```python
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import monitor

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Monitor is running")

    def log_message(self, format, *args):
        pass  # Silence HTTP logs

# Démarre le serveur HTTP en arrière-plan
def run_http_server():
    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Démarre HTTP server dans un thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Lance le moniteur
    mon = monitor.TaylorSwiftMonitor()
    mon.run()
```

Et changez la **Run command** dans Koyeb en : `python web_wrapper.py`

## Déploiements automatiques

Chaque fois que vous faites `git push`, Koyeb redéploie automatiquement !

## Plan gratuit Koyeb

- ✅ 1 service "Eco" gratuit
- ✅ 512 MB RAM
- ✅ Partagé CPU
- ✅ Redémarrage automatique
- ✅ Déploiement automatique GitHub
- ✅ **Pas de limite de temps** (tourne 24/7)

## Tester la notification

Une fois déployé, utilisez la console Koyeb ou attendez qu'un nouveau produit apparaisse !

## Dépannage

### Le service ne démarre pas (problème de port)
- Utilisez la Solution 1 (nixpacks.toml) ou Solution 2 (web_wrapper.py)

### "Unhealthy" status
- Vérifiez les logs
- Assurez-vous que DISCORD_WEBHOOK_URL est définie
- Le service peut être marqué "unhealthy" même s'il fonctionne (car pas de HTTP response)

### Vérifier que ça tourne
- Consultez les logs en temps réel
- Vous devriez voir les vérifications toutes les 30 secondes

## Arrêter/Suspendre le moniteur

1. Allez dans votre app
2. Cliquez sur **"Pause"** ou **"Delete"**

## Résumé

Koyeb est actuellement la meilleure option gratuite sans carte de crédit pour un worker Python 24/7 !
