# BTC Signal Bot

Ce bot analyse le carnet d'ordres de Bitget et envoie des signaux de trading BTC via Telegram.

## Fonctionnalités

- Analyse les 1000 niveaux du carnet d'ordres BTC/USDT sur Bitget
- Détecte les déséquilibres importants (biais Long ou Short)
- Envoie des signaux précis via Telegram
- Optimisé pour levier élevé (jusqu'à x500)

## Variables d'environnement à définir

- `TELEGRAM_TOKEN`: Clé API du bot Telegram
- `TELEGRAM_CHAT_ID`: ID du canal ou utilisateur

## Déploiement

- Héberger sur Render
- Déclencher automatiquement avec Cronjob toutes les heures