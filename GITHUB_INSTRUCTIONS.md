# Instructions pour pousser vers GitHub

## Option 1: Utiliser le script automatique

1. **Installer Git** (si pas déjà fait):
   - Télécharger: https://git-scm.com/download/win
   - Installer avec les paramètres par défaut
   - Redémarrer le terminal

2. **Exécuter le script**:
   ```cmd
   PUSH-TO-GITHUB.bat
   ```

3. **Authentification GitHub**:
   - Quand demandé, utilisez un **Personal Access Token** (pas votre mot de passe)
   - Générer un token: https://github.com/settings/tokens
   - Sélectionner scope: `repo` (full control)

## Option 2: Commandes manuelles

Ouvrir un terminal et exécuter:

```cmd
cd "C:\Users\Asus ExpertBook\OneDrive\Desktop\stage 2\smartbanking-app"

REM Initialiser Git (si pas déjà fait)
git init

REM Ajouter le remote
git remote add origin https://github.com/Ilyes-Neguir/SmartBankAssistant.git

REM Ajouter tous les fichiers
git add .

REM Créer un commit
git commit -m "Complete SmartBank Assistant project - Full-stack banking app with AI chatbot"

REM Pousser vers GitHub
git branch -M main
git push -u origin main
```

## Fichiers inclus dans le dépôt

✅ **Code source**:
- Backend (FastAPI/Python)
- Frontend (React/TypeScript)
- Tous les fichiers de configuration

✅ **Documentation**:
- `PROJECT_REPORT.md` - Rapport complet du projet
- `PRESENTATION_SUMMARY.md` - Résumé pour présentation
- `presentation.html` - Présentation HTML interactive
- `UML_DIAGRAMS.md` - Documentation des diagrammes UML
- `README.md` - Documentation principale
- `REQUIREMENTS_COVERAGE_CHECKLIST.md` - Checklist des exigences

✅ **Documentation des 13 semaines**:
- `docs/week1-introduction.md`
- `docs/week2-requirements.md`
- `docs/week3-design.md`
- `docs/week4-coding1.md`
- `docs/week5-coding2.md`
- `docs/week6-testing1.md`
- `docs/week7-testing2.md`
- `docs/week9-devops.md`
- `docs/week10-maintenance.md`
- `docs/week11-project-management.md`
- `docs/week12-ai-products.md`
- `docs/week13-ethics.md`

✅ **Diagrammes UML**:
- `diagrams/01-complete-class-diagram.puml`
- `diagrams/02-system-architecture-diagram.puml`
- `diagrams/03-complete-sequence-diagram.puml`
- `diagrams/04-use-case-diagram.puml`

✅ **Scripts et configuration**:
- Tous les fichiers `.bat` pour démarrer l'application
- `docker-compose.yml`
- `.gitignore`

## Fichiers exclus (dans .gitignore)

❌ `node_modules/` - Dépendances Node.js
❌ `venv/` - Environnement virtuel Python
❌ `*.db` - Fichiers de base de données
❌ `.env` - Variables d'environnement
❌ `__pycache__/` - Cache Python

## Après le push

Votre dépôt sera accessible à:
**https://github.com/Ilyes-Neguir/SmartBankAssistant**

Vous pourrez voir tous les fichiers, l'historique Git, et partager le lien avec votre équipe/professeur.

## Vérification

Après le push, vérifiez sur GitHub:
1. Tous les fichiers sont présents
2. Le README s'affiche correctement
3. La présentation HTML est accessible

## Besoin d'aide?

- Documentation Git: https://git-scm.com/doc
- Aide GitHub: https://docs.github.com
- GitHub Desktop (interface graphique): https://desktop.github.com

