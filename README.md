# 🎵 Taylor Swift Store Monitor

Moniteur automatique pour la boutique en ligne Taylor Swift Canada. Détecte les nouveaux produits et t'envoie une notification Discord instantanée!

## ✨ Fonctionnalités

- ✅ Vérifie la boutique toutes les 30 secondes
- ✅ Détecte automatiquement les nouveaux produits
- ✅ Envoie des notifications Discord avec lien direct
- ✅ Garde un log de toutes les activités
- ✅ Sauvegarde l'état entre les redémarrages
- ✅ Notifications stylées avec embed Discord

## 📋 Prérequis

- Python 3.8 ou plus récent
- Un serveur Discord (privé ou non)
- Un webhook Discord

## 🚀 Installation et Configuration

### Étape 1: Clone le projet

```bash
git clone <ton-repo-github>
cd taylor-swift-monitor
```

### Étape 2: Installe les dépendances Python

```bash
pip install -r requirements.txt
```

Ou avec un environnement virtuel (recommandé):
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Étape 3: Configure ton webhook Discord

1. **Ouvre ton serveur Discord**
2. **Clique sur la roue dentée** ⚙️ à côté d'un channel (ex: #general)
3. **Va dans "Intégrations"** → **"Webhooks"**
4. **Clique sur "Nouveau Webhook"**
5. **Copie l'URL du webhook**

### Étape 4: Configure le fichier config.json

Ouvre `config.json` et remplace `COLLE_TON_URL_WEBHOOK_ICI` par ton URL webhook:

```json
{
  "url": "https://storeca.taylorswift.com/collections/the-holiday-collection",
  "discord_webhook_url": "https://discord.com/api/webhooks/TonWebhookIci",
  "check_interval_seconds": 30
}
```

**Note:** Garde ton URL webhook secrète! Ne la commit pas sur GitHub.

### Étape 5: Lance le moniteur

```bash
python monitor.py
```

## 🎯 Utilisation

Une fois lancé, le script va:

1. **Premier lancement:** Enregistrer tous les produits actuellement sur la page (aucune notification)
2. **Lancements suivants:** Vérifier toutes les 30 secondes et t'alerter dès qu'un nouveau produit apparaît
3. **Sauvegarder son état** dans `state.json` pour se souvenir des produits entre les redémarrages

### Arrêter le moniteur

Appuie sur `Ctrl + C` pour arrêter proprement le script.

### Relancer après un arrêt

Le script se souviendra des produits qu'il connaît déjà grâce au fichier `state.json`. Il ne t'alertera que pour les NOUVEAUX produits ajoutés après le redémarrage.

## 📁 Fichiers du projet

```
taylor-swift-monitor/
├── monitor.py           # Script principal
├── requirements.txt     # Dépendances Python
├── config.json         # Ta configuration (webhook, URL, intervalle)
├── state.json          # État sauvegardé (généré automatiquement)
├── monitor.log         # Log de toutes les activités
└── README.md           # Ce fichier
```

## 📝 Logs

Tous les événements sont enregistrés dans:
- **Console:** Pour voir en temps réel ce qui se passe
- **monitor.log:** Fichier qui garde l'historique complet

Exemple de log:
```
2024-11-14 10:30:15 - INFO - Moniteur initialisé
2024-11-14 10:30:15 - INFO - Trouvé 24 produits sur la page
2024-11-14 10:30:45 - INFO - 🎉 1 nouveau(x) produit(s) détecté(s)!
2024-11-14 10:30:45 - INFO - Nouveau produit: The Eras Tour Hoodie
2024-11-14 10:30:45 - INFO - Notification Discord envoyée
```

## ⚙️ Personnalisation

### Changer l'intervalle de vérification

Dans `config.json`, modifie `check_interval_seconds`:
```json
"check_interval_seconds": 60  // Vérifie toutes les 60 secondes au lieu de 30
```

**Note:** Ne mets pas un intervalle trop court (<10 secondes) pour éviter de surcharger le serveur.

### Surveiller une autre collection

Change l'URL dans `config.json`:
```json
"url": "https://storeca.taylorswift.com/collections/autre-collection"
```

### Réinitialiser les produits connus

Si tu veux que le script oublie tous les produits et recommence:
```bash
rm state.json
```

Au prochain lancement, il considérera tous les produits comme nouveaux.

## 🔧 Dépannage

### "Aucun produit trouvé"

- Vérifie ta connexion Internet
- Le site pourrait avoir changé sa structure HTML
- Essaie d'ouvrir l'URL dans ton navigateur pour confirmer qu'elle fonctionne

### "Erreur lors de l'envoi de la notification Discord"

- Vérifie que ton URL webhook est correcte
- Assure-toi que le webhook n'a pas été supprimé sur Discord
- Vérifie les permissions du webhook sur Discord

### Le script ne détecte pas les nouveaux produits

- Vérifie le fichier `monitor.log` pour voir ce qui est détecté
- Le site utilise peut-être du JavaScript pour charger les produits (le script ne peut voir que le HTML initial)

## 🚨 Recommandations

1. **Laisse le script tourner en continu** pour ne rien manquer
2. **Active les notifications Discord** sur ton téléphone pour être alerté immédiatement
3. **Vérifie régulièrement le log** pour t'assurer que tout fonctionne
4. **Ne partage JAMAIS ton URL webhook** - garde-la secrète!

## 🛠️ Pour les utilisateurs avancés

### Exécuter en arrière-plan (Linux/Mac)

```bash
nohup python monitor.py > output.log 2>&1 &
```

### Créer un service systemd (Linux)

Créer `/etc/systemd/system/taylor-swift-monitor.service`:
```ini
[Unit]
Description=Taylor Swift Store Monitor
After=network.target

[Service]
Type=simple
User=ton-utilisateur
WorkingDirectory=/chemin/vers/taylor-swift-monitor
ExecStart=/usr/bin/python3 /chemin/vers/taylor-swift-monitor/monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Puis:
```bash
sudo systemctl enable taylor-swift-monitor
sudo systemctl start taylor-swift-monitor
```

## 📞 Support

Si tu rencontres des problèmes:
1. Vérifie le fichier `monitor.log`
2. Assure-toi que toutes les dépendances sont installées
3. Vérifie que ton webhook Discord fonctionne

## ⚖️ Avertissement

Ce script est à usage personnel. Respecte les conditions d'utilisation du site Taylor Swift Store. N'abuse pas du système en mettant un intervalle de vérification trop court.

---

**Bon shopping! 🎵✨**
