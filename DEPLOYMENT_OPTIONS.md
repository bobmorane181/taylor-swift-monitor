# Options de déploiement GRATUITES (2025)

Voici toutes les options vraiment gratuites pour héberger votre moniteur 24/7.

## ✅ Option 1 : Fly.io (RECOMMANDÉ - Vraiment gratuit)

**Avantages** :
- ✅ 100% gratuit (3 machines incluses)
- ✅ Background workers supportés
- ✅ Pas de carte de crédit requise
- ✅ Redémarrage automatique
- ✅ CLI facile à utiliser

**Installation** :
1. Installer Fly CLI : https://fly.io/docs/hands-on/install-flyctl/
2. Créer un compte : `flyctl auth signup`
3. Lancer l'app : `flyctl launch`
4. Définir le webhook : `flyctl secrets set DISCORD_WEBHOOK_URL="votre_webhook"`
5. Déployer : `flyctl deploy`

**Guide complet** : Voir FLY_DEPLOYMENT.md

---

## ✅ Option 2 : Koyeb (Gratuit)

**Avantages** :
- ✅ Gratuit pour toujours
- ✅ Workers supportés
- ✅ Interface web simple
- ✅ Déploiement GitHub automatique

**Étapes** :
1. Allez sur https://www.koyeb.com
2. Connectez-vous avec GitHub
3. Créez un "Worker"
4. Sélectionnez votre repo
5. Ajoutez DISCORD_WEBHOOK_URL dans les variables

---

## ⚠️ Option 3 : PythonAnywhere (Gratuit mais limité)

**Avantages** :
- ✅ Gratuit
- ✅ Console web accessible

**Inconvénients** :
- ❌ Processus arrêtés après 24h
- ❌ Nécessite relance manuelle quotidienne

**Guide** : Voir PYTHONANYWHERE_DEPLOYMENT.md

---

## 🏠 Option 4 : Local (Votre ordinateur)

**Le plus simple !**

**Avantages** :
- ✅ 100% gratuit
- ✅ Contrôle total
- ✅ Déjà configuré et fonctionnel

**Inconvénients** :
- ❌ Ordinateur doit rester allumé
- ❌ Dépend de votre connexion Internet

**Pour le lancer** :
```bash
python monitor.py
```

---

## 💰 Options payantes (Si vraiment besoin)

### Railway
- 5$/mois
- Excellent pour les applications

### Render
- 7$/mois pour Background Workers
- Très simple d'utilisation

### DigitalOcean
- 4$/mois (Droplet le moins cher)
- Plus de contrôle mais plus technique

---

## Ma recommandation finale

### Pour vous :

1. **Essayez Fly.io d'abord** - C'est vraiment gratuit et simple
2. **Alternative : Koyeb** - Si Fly.io ne fonctionne pas
3. **Solution temporaire : Local** - En attendant de configurer le cloud

Je peux vous guider pour déployer sur Fly.io ou Koyeb si vous voulez !
