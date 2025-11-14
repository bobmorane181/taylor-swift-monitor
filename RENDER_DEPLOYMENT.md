# Déploiement sur Render.com (GRATUIT)

Render.com offre un plan gratuit pour les applications Python qui est parfait pour ce moniteur.

## Étape 1 : Créer un compte Render

1. Allez sur **https://render.com**
2. Cliquez sur **"Get Started"**
3. Connectez-vous avec **GitHub**
4. Autorisez Render à accéder à vos repos

## Étape 2 : Créer un nouveau Web Service

1. Dans le dashboard Render, cliquez sur **"New +"**
2. Sélectionnez **"Background Worker"** (pas Web Service)
3. Connectez votre repository GitHub **taylor-swift-monitor**
4. Cliquez sur **"Connect"**

## Étape 3 : Configuration

Remplissez les champs suivants :

- **Name** : `taylor-swift-monitor` (ou ce que vous voulez)
- **Region** : Choisissez la plus proche (ex: Oregon USA)
- **Branch** : `main`
- **Runtime** : `Python 3`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `python monitor.py`
- **Instance Type** : Sélectionnez **"Free"**

## Étape 4 : Variables d'environnement

Dans la section **"Environment Variables"**, cliquez sur **"Add Environment Variable"** :

- **Key** : `DISCORD_WEBHOOK_URL`
- **Value** : (collez votre URL webhook Discord depuis config.json)

Optionnel :
- **Key** : `CHECK_INTERVAL`
- **Value** : `30` (secondes entre chaque vérification)

## Étape 5 : Déployer

1. Cliquez sur **"Create Background Worker"**
2. Render va automatiquement :
   - Cloner votre repo
   - Installer Python 3.11
   - Installer les dépendances
   - Lancer `python monitor.py`

## Étape 6 : Vérifier que ça fonctionne

1. Une fois le déploiement terminé, allez dans **"Logs"**
2. Vous devriez voir :
   ```
   Moniteur initialisé
   URL surveillée: https://storeca.taylorswift.com/...
   --- Vérification en cours ---
   Trouvé 12 produits sur la page
   ```

## Tester la notification

### Méthode 1 : Via les logs
Consultez les logs en temps réel pour voir le moniteur fonctionner

### Méthode 2 : Envoyer une notification de test
1. Dans Render, allez dans **"Shell"**
2. Exécutez : `python send_test_notification.py`
3. Vérifiez Discord pour la notification

## Limitations du plan gratuit Render

- ✅ 750 heures/mois (largement suffisant)
- ✅ Le service s'endort après 15 min d'inactivité (mais se réveille automatiquement)
- ✅ Redémarrage automatique en cas d'erreur
- ✅ Déploiement automatique à chaque push GitHub

**Note** : Contrairement à un web service, un Background Worker ne s'endort PAS, il tourne en continu !

## Déploiements automatiques

Chaque fois que vous faites `git push` sur GitHub, Render redéploiera automatiquement votre application.

## Dépannage

### Le déploiement échoue
- Vérifiez les logs de build pour voir l'erreur
- Assurez-vous que `requirements.txt` est correct

### Le moniteur ne démarre pas
- Vérifiez que `DISCORD_WEBHOOK_URL` est bien définie
- Consultez les logs d'exécution

### Le moniteur s'arrête
- Vérifiez les logs pour voir s'il y a une erreur
- Render redémarre automatiquement en cas de crash

## Arrêter le moniteur

Pour arrêter temporairement :
1. Allez dans **"Settings"**
2. Cliquez sur **"Suspend Background Worker"**

Pour redémarrer :
1. Cliquez sur **"Resume"**
