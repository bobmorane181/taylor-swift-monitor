#!/usr/bin/env python3
"""
Taylor Swift Store Monitor
Surveille la boutique Taylor Swift Canada pour détecter les nouveaux produits
"""

import requests
import json
import time
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TaylorSwiftMonitor:
    def __init__(self, config_path='config.json'):
        """Initialise le moniteur avec la configuration"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.url = self.config['url']
        self.webhook_url = self.config['discord_webhook_url']
        self.check_interval = self.config['check_interval_seconds']
        self.known_products = set()
        self.first_run = True
        
        logger.info("Moniteur initialisé")
        logger.info(f"URL surveillée: {self.url}")
        logger.info(f"Intervalle de vérification: {self.check_interval} secondes")
    
    def get_products(self):
        """Récupère la liste des produits sur la page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Trouve tous les produits (ajuste les sélecteurs si nécessaire)
            products = []
            
            # Cherche les liens de produits
            product_links = soup.find_all('a', class_='product-item__title')
            if not product_links:
                # Alternative: cherche dans les grilles de produits
                product_links = soup.find_all('a', href=lambda x: x and '/products/' in x)
            
            for link in product_links:
                product_name = link.get_text(strip=True)
                product_url = link.get('href', '')
                
                if product_url and product_name:
                    # Construit l'URL complète si nécessaire
                    if product_url.startswith('/'):
                        product_url = f"https://storeca.taylorswift.com{product_url}"
                    
                    # Crée un identifiant unique pour le produit
                    product_id = hashlib.md5(product_url.encode()).hexdigest()
                    
                    products.append({
                        'id': product_id,
                        'name': product_name,
                        'url': product_url
                    })
            
            logger.info(f"Trouvé {len(products)} produits sur la page")
            return products
            
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération de la page: {e}")
            return []
        except Exception as e:
            logger.error(f"Erreur inattendue: {e}")
            return []
    
    def send_discord_notification(self, product):
        """Envoie une notification Discord pour un nouveau produit"""
        try:
            embed = {
                "title": "🎵 NOUVEAU PRODUIT DÉTECTÉ! 🎵",
                "description": f"**{product['name']}**",
                "url": product['url'],
                "color": 0xFF69B4,  # Rose
                "fields": [
                    {
                        "name": "Lien direct",
                        "value": f"[Acheter maintenant]({product['url']})",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Taylor Swift Store Monitor"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
            payload = {
                "content": "@everyone NOUVEAU PRODUIT TAYLOR SWIFT! 🚨",
                "embeds": [embed]
            }
            
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            logger.info(f"Notification Discord envoyée pour: {product['name']}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de la notification Discord: {e}")
    
    def check_for_new_products(self):
        """Vérifie s'il y a de nouveaux produits"""
        products = self.get_products()
        
        if not products:
            logger.warning("Aucun produit trouvé - vérifiez la connexion ou la structure de la page")
            return
        
        current_product_ids = {p['id'] for p in products}
        
        if self.first_run:
            # Premier lancement: enregistre tous les produits existants
            self.known_products = current_product_ids
            self.first_run = False
            logger.info(f"Initialisation: {len(self.known_products)} produits enregistrés")
            
            # Sauvegarde l'état initial
            self.save_state()
        else:
            # Vérifie les nouveaux produits
            new_product_ids = current_product_ids - self.known_products
            
            if new_product_ids:
                logger.info(f"🎉 {len(new_product_ids)} nouveau(x) produit(s) détecté(s)!")
                
                for product in products:
                    if product['id'] in new_product_ids:
                        logger.info(f"Nouveau produit: {product['name']}")
                        self.send_discord_notification(product)
                
                # Met à jour les produits connus
                self.known_products = current_product_ids
                self.save_state()
            else:
                logger.info("Aucun nouveau produit détecté")
    
    def save_state(self):
        """Sauvegarde l'état des produits connus"""
        try:
            state = {
                'known_products': list(self.known_products),
                'last_update': datetime.now().isoformat()
            }
            with open('state.json', 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de l'état: {e}")
    
    def load_state(self):
        """Charge l'état précédent si disponible"""
        try:
            with open('state.json', 'r') as f:
                state = json.load(f)
                self.known_products = set(state.get('known_products', []))
                self.first_run = False
                logger.info(f"État précédent chargé: {len(self.known_products)} produits connus")
        except FileNotFoundError:
            logger.info("Aucun état précédent trouvé - premier lancement")
        except Exception as e:
            logger.error(f"Erreur lors du chargement de l'état: {e}")
    
    def run(self):
        """Lance le moniteur en boucle continue"""
        logger.info("🚀 Démarrage du moniteur Taylor Swift Store")
        
        # Tente de charger l'état précédent
        self.load_state()
        
        try:
            while True:
                logger.info("--- Vérification en cours ---")
                self.check_for_new_products()
                logger.info(f"Prochaine vérification dans {self.check_interval} secondes\n")
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Arrêt du moniteur par l'utilisateur")
            self.save_state()
        except Exception as e:
            logger.error(f"Erreur fatale: {e}")
            self.save_state()


if __name__ == "__main__":
    monitor = TaylorSwiftMonitor()
    monitor.run()
