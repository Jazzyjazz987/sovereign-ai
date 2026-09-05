# 💬 Guide Chat IA - Cascade T1→T2→T3

## 🚀 Accès à l'Application

**URL:** http://localhost:5000

L'application web se charge automatiquement. Aucune installation supplémentaire requise!

---

## 🤖 Comment Fonctionne la Cascade

L'application **sélectionne automatiquement le meilleur modèle** selon la **complexité** de votre question:

### **Tier 1 - Mistral 7B (T1)** ⚡
- **Latence:** 3-4 secondes
- **Idéal pour:**
  - Questions simples
  - Réponses rapides
  - Conversations courtes
  - Support français excellent
- **Exemples:**
  - "Bonjour"
  - "Qu'est-ce que le RGPD?"
  - "Explique l'IA en simple"

### **Tier 2 - Llama2 7B (T2)** 📚
- **Latence:** 4-5 secondes
- **Idéal pour:**
  - Code et programmation
  - Analyse approfondie
  - Questions légales/RGPD
  - Explications détaillées
- **Exemples:**
  - "Écris une fonction Python..."
  - "Implémenter OAuth en détail"
  - "Quels sont les défis RGPD?"

---

## 🎮 Interface Web

### **Sidebar Gauche**
- 🔄 **Sélection de modèle:**
  - Auto (recommandé): T1 par défaut, T2 si complexe
  - T1: Force Mistral 7B
  - T2: Force Llama2 7B

### **Zone de Chat Principale**
- Messages utilisateur: **Bleu** (droite)
- Réponses IA: **Gris** (gauche)
- **Indicateur de modèle:** Affiche T1/T2 et pourquoi

### **Zone d'Entrée**
- Tapez votre question
- Appuyez sur **Entrée** ou cliquez **Envoyer**
- Réponse en temps réel (streaming)

---

## 💡 Exemples d'Utilisation

### Exemple 1: Question Simple → T1
```
Vous: Bonjour
IA: [T1] Bonjour! Comment puis-je vous aider?
```

### Exemple 2: Code Complexe → T2
```
Vous: Écris une fonction Python pour valider un email avec regex
IA: [T2] Voici une fonction:
[Code détaillé avec explications...]
```

### Exemple 3: Légal/RGPD → T2
```
Vous: Quels sont les défis RGPD pour un gouvernement?
IA: [T2] Les défis incluent...
[Analyse approfondie...]
```

### Exemple 4: Français Complexe → T2
```
Vous: Comment implémenter un système de cache distribué?
IA: [T2] Un système de cache distribué implique...
[Explication technique détaillée...]
```

---

## 🔍 Indicateurs de Complexité

L'IA détecte automatiquement la complexité avec ces **mots-clés:**

| Mot-Clé | Tier |
|---------|------|
| code, fonction, programme | T2 |
| implémenter, architecture | T2 |
| complexe, algorithme | T2 |
| RGPD, légal, conformité | T2 |
| sécurité, crypto | T2 |
| explique, profond | T2 |
| **Longueur >50 mots** | T2 |
| Défaut | **T1** |

---

## ⚙️ Modes de Fonctionnement

### Mode Auto (Par Défaut)
- L'app choisit T1 ou T2 automatiquement
- **Recommandé pour:**
  - Productivité maximale
  - Utilisation première fois
  - Questions variées

### Mode T1 Forcé
- Toujours Mistral 7B
- **Recommandé pour:**
  - Questions simples
  - Besoin de rapidité
  - Réponses courtes

### Mode T2 Forcé
- Toujours Llama2 7B
- **Recommandé pour:**
  - Analyse approfondie
  - Code et techniques
  - Explications détaillées

---

## 📊 Performance

| Aspect | T1 | T2 |
|--------|----|----|
| Latence | 3-4s | 4-5s |
| Français | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Code | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Analyse | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Légal/RGPD | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🛠️ Intégration Avancée

### Utiliser l'API Directement

**Requête Simple (Non-Streaming):**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Votre question"}'
```

**Forcer T1:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Question","force_model":"t1"}'
```

**Forcer T2:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Question","force_model":"t2"}'
```

### Réponse JSON
```json
{
  "response": "Réponse complète...",
  "model": "t1",
  "tier": 1,
  "reason": "simple_query",
  "complexity": 1.0
}
```

---

## 📱 Accès Depuis d'Autres Machines

Si vous voulez accéder depuis un autre ordinateur:

1. Remplacer `localhost` par l'adresse IP du serveur
2. Exemple: `http://192.168.1.100:5000`
3. Port par défaut: **5000**

---

## 🔄 Redémarrer le Serveur

```bash
# Arrêter
docker stop sovereign-chat

# Redémarrer
docker run --rm -d \
  --name sovereign-chat \
  --network host \
  -v $(pwd):/app \
  -w /app \
  python:3.11-slim \
  bash -c "pip install -q fastapi uvicorn && \
           python -m uvicorn api.chat_app:app --port 5000"
```

---

## 🐛 Dépannage

### "Erreur de connexion"
- Vérifier que le serveur tourne: `curl http://localhost:5000/api/status`
- Si non, redémarrer avec la commande ci-dessus

### "Réponse lente"
- Vérifier la charge Ollama: `docker logs ollama`
- Peut être normal (4-5s pour T2)

### "Modèle pas disponible"
- Vérifier: `curl http://localhost:5000/api/models`
- T1 et T2 doivent être listés

---

## 📚 Architecture

```
Application Chat
    ↓
FastAPI (port 5000)
    ↓
CascadeRouter (Sélection T1/T2)
    ↓
OllamaClient
    ↓
Ollama (port 11434)
    ↓
T1: Mistral 7B (GPU)
T2: Llama2 7B (GPU)
```

---

## 🎯 Cas d'Usage

### DSI Gouvernemental
- Questions RGPD → T2
- Explications rapides → T1
- Code gouvernemental → T2

### Support Utilisateur
- Escalade automatique
- Français natif (T1)
- Analyse profonde quand nécessaire (T2)

### Développement
- Code: T2
- Quick help: T1
- Optimisation: T2

---

## 📞 Besoin d'Aide?

1. Consulter les exemples ci-dessus
2. Vérifier la section "Dépannage"
3. Vérifier les logs: `docker logs sovereign-chat`

**Bon chat! 🚀**
