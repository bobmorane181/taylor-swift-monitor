#!/usr/bin/env python3
"""
Script de test pour envoyer une fausse alerte Discord
"""

import requests
import json
from datetime import datetime

def send_test_notification():
    """Envoie une notification de test Discord"""

    # Charge la configuration
    with open('config.json', 'r') as f:
        config = json.load(f)

    webhook_url = config['discord_webhook_url']

    # Produit de test
    test_product = {
        'name': '🎄 TEST - The Eras Tour Exclusive Holiday Ornament Set',
        'url': 'https://storeca.taylorswift.com/products/test-product'
    }

    try:
        embed = {
            "title": "🎵 NOUVEAU PRODUIT DÉTECTÉ! 🎵",
            "description": f"**{test_product['name']}**",
            "url": test_product['url'],
            "color": 0xFF69B4,  # Rose
            "fields": [
                {
                    "name": "Lien direct",
                    "value": f"[Acheter maintenant]({test_product['url']})",
                    "inline": False
                },
                {
                    "name": "⚠️ ALERTE DE TEST",
                    "value": "Ceci est une notification de test pour vérifier que le système fonctionne correctement.",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Taylor Swift Store Monitor - TEST MODE"
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        payload = {
            "content": "@everyone NOUVEAU PRODUIT TAYLOR SWIFT! 🚨",
            "embeds": [embed]
        }

        print("Envoi de la notification de test...")
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Notification de test envoyee avec succes!")
        print(f"Code de reponse: {response.status_code}")

    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification: {e}")


if __name__ == "__main__":
    print("Test de notification Discord")
    print("=" * 50)
    send_test_notification()
