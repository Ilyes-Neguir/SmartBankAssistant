# 🚀 Déployer sur GitHub - Guide Rapide

## Étape 1: Installer Git

**Télécharger et installer Git:**
1. Aller sur: https://git-scm.com/download/win
2. Télécharger l'installateur
3. Installer avec les paramètres par défaut
4. **Redémarrer** le terminal/Command Prompt après installation

## Étape 2: Ouvrir un nouveau Terminal

Ouvre un **nouveau** Command Prompt (important après installation de Git).

## Étape 3: Copier-Coller ces commandes

Ouvre ton terminal dans le dossier du projet et exécute ces commandes **une par une**:

```cmd
cd "C:\Users\Asus ExpertBook\OneDrive\Desktop\stage 2\smartbanking-app"
```

```cmd
git init
```

```cmd
git remote add origin https://github.com/Ilyes-Neguir/SmartBankAssistant.git
```

```cmd
git add .
```

```cmd
git commit -m "Complete SmartBank Assistant project - Full-stack banking app with AI chatbot, documentation, presentation, and UML diagrams"
```

```cmd
git branch -M main
```

```cmd
git push -u origin main
```

## Étape 4: Authentification

Quand Git demande tes identifiants:
- **Username:** `Ilyes-Neguir`
- **Password:** Utilise un **Personal Access Token** (PAS ton mot de passe GitHub)

### Créer un Personal Access Token:
1. Va sur: https://github.com/settings/tokens
2. Clique sur "Generate new token" → "Generate new token (classic)"
3. Donne un nom: `SmartBank Assistant`
4. Sélectionne la scope: ✅ **`repo`** (full control)
5. Clique "Generate token"
6. **COPIER LE TOKEN** (tu ne le reverras pas!)
7. Utilise ce token comme mot de passe

## ✅ C'est fait!

Une fois le push terminé, ton code sera sur:
**https://github.com/Ilyes-Neguir/SmartBankAssistant**

## Fichiers inclus

✅ Code source complet (backend + frontend)
✅ `PROJECT_REPORT.md`
✅ `presentation.html`
✅ Documentation des 13 semaines
✅ Diagrammes UML
✅ Tous les fichiers de configuration

## Problème?

Si tu rencontres une erreur:
1. Vérifie que Git est bien installé: `git --version`
2. Vérifie que tu es dans le bon dossier
3. Vérifie que le token GitHub est valide
4. Réessaye les commandes

