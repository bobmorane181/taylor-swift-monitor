# Déploiement avec GitHub Actions (100% GRATUIT)

GitHub Actions permet d'exécuter votre moniteur dans le cloud gratuitement, mais avec des vérifications périodiques (toutes les 10 minutes) au lieu d'une surveillance continue.

## Avantages

- ✅ 100% gratuit
- ✅ Pas de serveur à maintenir
- ✅ Pas d'ordinateur à laisser allumé
- ✅ 2000 minutes gratuites par mois (largement suffisant)

## Inconvénients

- ⚠️ Vérifications toutes les 10 minutes (au lieu de 30 secondes)
- ⚠️ Peut avoir 5-10 minutes de délai
- ⚠️ Moins réactif qu'un serveur continu

## Configuration

### Étape 1 : Ajouter le secret Discord Webhook

1. Allez sur votre repository GitHub : https://github.com/bobmorane181/taylor-swift-monitor
2. Cliquez sur **Settings** (l'onglet)
3. Dans le menu de gauche, cliquez sur **Secrets and variables** → **Actions**
4. Cliquez sur **New repository secret**
5. Ajoutez :
   - **Name** : `DISCORD_WEBHOOK_URL`
   - **Secret** : (collez votre URL webhook Discord)
6. Cliquez sur **Add secret**

### Étape 2 : Activer GitHub Actions

Le fichier `.github/workflows/monitor.yml` a déjà été créé et poussé sur GitHub.

1. Allez dans l'onglet **Actions** de votre repository
2. Si demandé, cliquez sur **"I understand my workflows, go ahead and enable them"**
3. Vous devriez voir le workflow "Taylor Swift Monitor"

### Étape 3 : Lancer manuellement (test)

1. Dans **Actions**, cliquez sur le workflow "Taylor Swift Monitor"
2. Cliquez sur **Run workflow** → **Run workflow**
3. Attendez quelques secondes
4. Cliquez sur l'exécution en cours
5. Consultez les logs pour vérifier que ça fonctionne

### Étape 4 : Automatique

GitHub exécutera automatiquement le workflow toutes les 10 minutes !

## Comment ça fonctionne

1. GitHub Actions lance un serveur Ubuntu
2. Installe Python et les dépendances
3. Exécute UNE vérification du site Taylor Swift
4. Envoie une notification si nouveau produit
5. Sauvegarde l'état pour la prochaine fois
6. S'arrête jusqu'à la prochaine exécution (10 min plus tard)

## Vérifier que ça fonctionne

1. Allez dans l'onglet **Actions**
2. Vous verrez toutes les exécutions
3. Cliquez sur une exécution pour voir les logs

## Limites

- **Fréquence minimale** : Toutes les 5-10 minutes (limite GitHub)
- **Minutes gratuites** : 2000/mois (largement suffisant pour vérifier toutes les 10 min)
- **Délai possible** : GitHub peut retarder les tâches planifiées de quelques minutes

## Désactiver temporairement

1. Allez dans **Actions**
2. Sélectionnez le workflow
3. Cliquez sur **...** → **Disable workflow**

## Avantages vs. inconvénients

| Aspect | GitHub Actions | Serveur 24/7 | Local |
|--------|---------------|--------------|-------|
| Prix | Gratuit | 5-7$/mois | Gratuit |
| Réactivité | 10 min | 30 sec | 30 sec |
| Maintenance | Aucune | Aucune | Ordinateur allumé |
| Fiabilité | Haute | Haute | Dépend de vous |

## Recommandation

**GitHub Actions est parfait si** :
- Vous ne voulez pas laisser votre PC allumé
- 10 minutes de délai est acceptable
- Vous voulez une solution 100% gratuite et sans maintenance

**Utilisez un serveur/local si** :
- Vous voulez être alerté en moins d'une minute
- Les produits se vendent très vite
- Vous pouvez laisser un PC allumé

## Amélioration possible

Pour aller plus vite, vous pouvez réduire à 5 minutes (minimum GitHub) :

Modifiez `.github/workflows/monitor.yml` :
```yaml
- cron: '*/5 * * * *'  # Toutes les 5 minutes
```

Puis :
```bash
git add .github/workflows/monitor.yml
git commit -m "Monitor every 5 minutes"
git push
```
