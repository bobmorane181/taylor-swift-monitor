#!/usr/bin/env python3
"""
Script de test complet pour valider le déploiement
"""

import os
import sys
import json

def test_config_file():
    """Test 1: Vérifier que config.json existe et est valide"""
    print("\n=== TEST 1: Configuration locale ===")
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)

            required_keys = ['url', 'discord_webhook_url', 'check_interval_seconds']
            missing = [key for key in required_keys if key not in config]

            if missing:
                print(f"ECHEC: Cles manquantes dans config.json: {missing}")
                return False

            print("OK: config.json est valide")
            print(f"  - URL: {config['url']}")
            print(f"  - Webhook configure: {'Oui' if config['discord_webhook_url'] else 'Non'}")
            print(f"  - Intervalle: {config['check_interval_seconds']}s")
            return True
        else:
            print("AVERTISSEMENT: config.json n'existe pas (OK pour production)")
            return True
    except Exception as e:
        print(f"ECHEC: Erreur lors de la lecture de config.json: {e}")
        return False


def test_dependencies():
    """Test 2: Vérifier que toutes les dépendances sont installées"""
    print("\n=== TEST 2: Dependances Python ===")
    required_modules = ['requests', 'bs4', 'lxml']
    all_ok = True

    for module in required_modules:
        try:
            __import__(module)
            print(f"OK: {module} est installe")
        except ImportError:
            print(f"ECHEC: {module} n'est PAS installe")
            all_ok = False

    return all_ok


def test_deployment_files():
    """Test 3: Vérifier que les fichiers de déploiement existent"""
    print("\n=== TEST 3: Fichiers de deploiement ===")
    required_files = {
        'Procfile': 'Configuration pour Railway',
        'runtime.txt': 'Version Python',
        'requirements.txt': 'Dependances Python',
        'monitor.py': 'Script principal',
        '.gitignore': 'Fichiers a ignorer'
    }

    all_ok = True
    for filename, description in required_files.items():
        if os.path.exists(filename):
            print(f"OK: {filename} existe ({description})")

            # Vérifications spécifiques
            if filename == 'Procfile':
                with open(filename, 'r') as f:
                    content = f.read()
                    if 'worker: python monitor.py' in content:
                        print("   - Commande worker correcte")
                    else:
                        print("   - ATTENTION: Commande worker incorrecte")
                        all_ok = False

            elif filename == 'requirements.txt':
                with open(filename, 'r') as f:
                    deps = f.read()
                    required_deps = ['requests', 'beautifulsoup4', 'lxml']
                    for dep in required_deps:
                        if dep in deps.lower():
                            print(f"   - {dep} present")
                        else:
                            print(f"   - ATTENTION: {dep} manquant")
                            all_ok = False
        else:
            print(f"ECHEC: {filename} n'existe pas")
            all_ok = False

    return all_ok


def test_monitor_import():
    """Test 4: Vérifier que monitor.py peut être importé"""
    print("\n=== TEST 4: Import du moniteur ===")
    try:
        # Essaie d'importer le module
        import monitor
        print("OK: monitor.py peut etre importe")

        # Vérifie que la classe existe
        if hasattr(monitor, 'TaylorSwiftMonitor'):
            print("OK: Classe TaylorSwiftMonitor trouvee")
            return True
        else:
            print("ECHEC: Classe TaylorSwiftMonitor introuvable")
            return False
    except Exception as e:
        print(f"ECHEC: Impossible d'importer monitor.py: {e}")
        return False


def test_env_variable_mode():
    """Test 5: Simuler le mode variables d'environnement"""
    print("\n=== TEST 5: Mode variables d'environnement ===")

    # Sauvegarde l'état actuel
    original_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

    try:
        # Définit une variable d'environnement de test
        os.environ['DISCORD_WEBHOOK_URL'] = 'https://discord.com/api/webhooks/TEST'

        # Renomme temporairement config.json s'il existe
        config_exists = os.path.exists('config.json')
        if config_exists:
            os.rename('config.json', 'config.json.backup')

        try:
            import monitor
            # Force le rechargement du module
            import importlib
            importlib.reload(monitor)

            # Essaie d'instancier le moniteur
            test_monitor = monitor.TaylorSwiftMonitor()

            if test_monitor.webhook_url == 'https://discord.com/api/webhooks/TEST':
                print("OK: Le moniteur utilise bien les variables d'environnement")
                result = True
            else:
                print("ECHEC: Le moniteur n'utilise pas les variables d'environnement")
                result = False

        except Exception as e:
            print(f"ECHEC: Erreur lors de l'instanciation: {e}")
            result = False
        finally:
            # Restaure config.json
            if config_exists:
                os.rename('config.json.backup', 'config.json')

    finally:
        # Restaure la variable d'environnement
        if original_webhook:
            os.environ['DISCORD_WEBHOOK_URL'] = original_webhook
        elif 'DISCORD_WEBHOOK_URL' in os.environ:
            del os.environ['DISCORD_WEBHOOK_URL']

    return result


def test_gitignore():
    """Test 6: Vérifier que .gitignore protège les fichiers sensibles"""
    print("\n=== TEST 6: Protection .gitignore ===")

    if not os.path.exists('.gitignore'):
        print("ECHEC: .gitignore n'existe pas")
        return False

    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()

    sensitive_files = ['config.json', '*.log', 'state.json']
    all_ok = True

    for filename in sensitive_files:
        if filename in gitignore_content:
            print(f"OK: {filename} est ignore par git")
        else:
            print(f"ATTENTION: {filename} n'est PAS ignore par git")
            all_ok = False

    return all_ok


def run_all_tests():
    """Exécute tous les tests"""
    print("=" * 60)
    print("TEST DE PREPARATION AU DEPLOIEMENT RAILWAY")
    print("=" * 60)

    tests = [
        ("Configuration locale", test_config_file),
        ("Dependances Python", test_dependencies),
        ("Fichiers de deploiement", test_deployment_files),
        ("Import du moniteur", test_monitor_import),
        ("Mode environnement", test_env_variable_mode),
        ("Protection .gitignore", test_gitignore),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\nERREUR CRITIQUE dans {test_name}: {e}")
            results.append((test_name, False))

    # Résumé
    print("\n" + "=" * 60)
    print("RESUME DES TESTS")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "REUSSI" if result else "ECHEC"
        symbol = "[OK]" if result else "[X]"
        print(f"{symbol} {test_name}: {status}")

    print(f"\nScore: {passed}/{total} tests reussis")

    if passed == total:
        print("\nFELICITATIONS! Votre application est prete pour le deploiement.")
        print("\nProchaines etapes:")
        print("1. git add .")
        print("2. git commit -m 'Prepare for Railway deployment'")
        print("3. git push origin main")
        print("4. Deployer sur Railway (voir DEPLOYMENT.md)")
        return 0
    else:
        print("\nATTENTION: Certains tests ont echoue.")
        print("Corrigez les problemes avant de deployer.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
