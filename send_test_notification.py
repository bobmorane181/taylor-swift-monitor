#!/usr/bin/env python3
"""
Script de test pour Railway - Envoie une notification de test
Peut être exécuté localement OU sur Railway
"""

import requests
import json
import os
from datetime import datetime


def send_test_notification():
    """Envoie une notification de test Discord"""

    # Récupère le webhook (config.json OU variable d'environnement)
    webhook_url = None

    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
        webhook_url = config.get('discord_webhook_url')

    if not webhook_url:
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    if not webhook_url:
        print("ERREUR: Aucun webhook Discord configure")
        print("- En local: verifiez config.json")
        print("- Sur Railway: verifiez la variable DISCORD_WEBHOOK_URL")
        return False

    # Produit de test
    test_product = {
        'name': 'TEST - The Eras Tour Exclusive Holiday Ornament Set',
        'url': 'https://storeca.taylorswift.com/products/test-product'
    }

    try:
        embed = {
            "title": "NOUVEAU PRODUIT DETECTE! (TEST)",
            "description": f"**{test_product['name']}**",
            "url": test_product['url'],
            "color": 0xFF69B4,
            "fields": [
                {
                    "name": "Lien direct",
                    "value": f"[Acheter maintenant]({test_product['url']})",
                    "inline": False
                },
                {
                    "name": "ALERTE DE TEST",
                    "value": "Ceci est une notification de test pour verifier que le systeme fonctionne correctement.",
                    "inline": False
                },
                {
                    "name": "Source",
                    "value": "Railway" if not os.path.exists('config.json') else "Local",
                    "inline": True
                }
            ],
            "footer": {
                "text": "Taylor Swift Store Monitor - TEST MODE"
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        payload = {
            "content": "@everyone NOUVEAU PRODUIT TAYLOR SWIFT! (TEST)",
            "embeds": [embed]
        }

        print("Envoi de la notification de test...")
        print(f"Webhook: {webhook_url[:50]}...")

        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()

        print("Notification de test envoyee avec succes!")
        print(f"Code de reponse: {response.status_code}")
        return True

    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE NOTIFICATION DISCORD")
    print("=" * 60)
    success = send_test_notification()
    exit(0 if success else 1)
