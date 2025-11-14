# Guide de déploiement sur Railway

Ce guide vous explique comment déployer le moniteur Taylor Swift sur Railway pour qu'il tourne 24/7 gratuitement.

## Étape 1 : Préparer le repository GitHub

1. Assurez-vous que tous vos fichiers sont commités :
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

## Étape 2 : Créer un compte Railway

1. Allez sur [railway.app](https://railway.app)
2. Cliquez sur "Login" puis "Login with GitHub"
3. Autorisez Railway à accéder à votre compte GitHub

## Étape 3 : Créer un nouveau projet

1. Une fois connecté, cliquez sur "New Project"
2. Sélectionnez "Deploy from GitHub repo"
3. Choisissez votre repository `taylor-swift-monitor`
4. Railway détectera automatiquement qu'il s'agit d'un projet Python

## Étape 4 : Configurer les variables d'environnement

⚠️ **IMPORTANT** : Ne mettez jamais votre webhook Discord dans le code !

1. Dans Railway, allez dans l'onglet "Variables"
2. Cliquez sur "New Variable"
3. Ajoutez la variable suivante :
   - **Nom** : `DISCORD_WEBHOOK_URL`
   - **Valeur** : Votre URL de webhook Discord

## Étape 5 : Modifier monitor.py pour utiliser les variables d'environnement

Le code doit être modifié pour lire le webhook depuis les variables d'environnement au lieu de config.json.

Remplacez dans `monitor.py` :
```python
with open(config_path, 'r') as f:
    self.config = json.load(f)

self.url = self.config['url']
self.webhook_url = self.config['discord_webhook_url']
```

Par :
```python
import os

# Charge la config ou utilise les variables d'environnement
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        self.config = json.load(f)
    self.url = self.config.get('url', 'https://storeca.taylorswift.com/collections/the-holiday-collection')
    self.webhook_url = self.config.get('discord_webhook_url', os.getenv('DISCORD_WEBHOOK_URL'))
else:
    # Mode production (Railway)
    self.url = os.getenv('STORE_URL', 'https://storeca.taylorswift.com/collections/the-holiday-collection')
    self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    self.config = {
        'url': self.url,
        'discord_webhook_url': self.webhook_url,
        'check_interval_seconds': int(os.getenv('CHECK_INTERVAL', 30))
    }
```

## Étape 6 : Déploiement automatique

Railway va automatiquement :
1. Détecter le `Procfile` et savoir comment lancer votre app
2. Installer les dépendances depuis `requirements.txt`
3. Utiliser la version Python spécifiée dans `runtime.txt`
4. Démarrer le worker qui exécute `monitor.py`

## Étape 7 : Vérifier que ça fonctionne

1. Dans Railway, allez dans l'onglet "Deployments"
2. Cliquez sur le déploiement en cours
3. Consultez les logs pour voir si le moniteur fonctionne

Vous devriez voir :
```
Moniteur initialisé
URL surveillée: https://storeca.taylorswift.com/collections/the-holiday-collection
Intervalle de vérification: 30 secondes
Démarrage du moniteur Taylor Swift Store
```

## Étape 8 : Déploiement automatique lors des changements

Maintenant, chaque fois que vous faites un `git push` sur GitHub, Railway redéploiera automatiquement votre application !

## Variables d'environnement disponibles

Sur Railway, vous pouvez configurer :
- `DISCORD_WEBHOOK_URL` : Votre webhook Discord (REQUIS)
- `STORE_URL` : URL à surveiller (optionnel, par défaut : la collection holiday)
- `CHECK_INTERVAL` : Intervalle en secondes (optionnel, par défaut : 30)

## Plan gratuit Railway

Le plan gratuit de Railway offre :
- 500 heures d'exécution par mois
- Largement suffisant pour ce moniteur
- Déploiements illimités
- Logs en temps réel

## Tester que Railway fonctionne

### Méthode 1 : Consulter les logs (Simple)

1. Dans Railway, allez dans "Deployments"
2. Cliquez sur le déploiement actif
3. Consultez les logs en temps réel
4. Vous devriez voir :
   ```
   Moniteur initialisé
   URL surveillée: https://storeca.taylorswift.com/...
   --- Vérification en cours ---
   Trouvé 12 produits sur la page
   Aucun nouveau produit détecté
   Prochaine vérification dans 30 secondes
   ```

### Méthode 2 : Envoyer une notification de test depuis Railway

1. Dans Railway, allez dans l'onglet "Settings"
2. Faites défiler jusqu'à "Custom Start Command"
3. Entrez temporairement : `python send_test_notification.py`
4. Redémarrez le déploiement
5. Vérifiez Discord - vous devriez recevoir une notification de test
6. **IMPORTANT** : Rétablissez ensuite la commande normale : `python monitor.py`

Ou utilisez le Railway CLI :
```bash
railway run python send_test_notification.py
```

### Méthode 3 : Simuler un nouveau produit (Avancé)

Sur Railway, dans l'onglet "Variables", ajoutez temporairement :
- `FORCE_NOTIFICATION=true`

Cela forcera l'envoi d'une notification au prochain cycle (nécessite modification du code).

## Dépannage

### Le déploiement échoue
- Vérifiez que `requirements.txt` est correct
- Vérifiez que `Procfile` contient bien `worker: python monitor.py`

### Le moniteur ne démarre pas
- Vérifiez que la variable `DISCORD_WEBHOOK_URL` est bien définie dans Railway
- Consultez les logs dans Railway pour voir l'erreur exacte

### Le moniteur s'arrête
- Vérifiez que vous n'avez pas dépassé les 500h gratuites du mois
- Consultez les logs pour voir s'il y a eu une erreur

## Arrêter le moniteur

Pour arrêter temporairement le moniteur sans le supprimer :
1. Dans Railway, allez dans "Settings"
2. Cliquez sur "Pause Deployment"

Pour le relancer :
1. Cliquez sur "Resume"
