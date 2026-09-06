# Reprendre après un redémarrage

Mis en place le 2026-09-05 pour installer le GPU (carte ASUS TUF Gaming RTX à enficher dans
`SI35960` / carte mère ASUS Pro Q570M-C) et reprendre la discussion Claude Code en cours.

## Procédure de redémarrage

1. **Éteindre** la machine.
2. Enficher la carte GPU à fond dans le slot **PCIe x16 du haut**, brancher les **2× 8-pin**.
   Vérifier que le bloc d'alimentation suffit (~750 W).
3. **Rallumer.**
4. À l'ouverture de session **root** sur le terminal : un décompte de 4 s propose la reprise.
   Laisser faire → la discussion Claude Code reprend automatiquement.
   - Ctrl-C pendant le décompte → shell normal.
   - Pour un shell sans reprise : `NO_CLAUDE=1 bash -l` ou taper `reprendre` plus tard.

## Ce qui se passe automatiquement au boot

| Élément | Auto ? | Détail |
|---|---|---|
| Docker | ✅ | `systemctl is-enabled docker` = enabled |
| Stack IA souveraine (7 conteneurs) | ✅ | `restart: unless-stopped` sur tous les services (commit `fc65a48`) |
| Détection GPU | ✅ (si carte enfichée) | driver `nvidia-driver-580` + dkms déjà installés — **rien à installer** |
| Reprise discussion Claude | ✅ | `/root/.bash_profile` → `/opt/claude/reprendre.sh` → `claude --resume dc444ce2-…` |

## Ce qui NE revient PAS tout seul (à refaire dans la discussion reprise)

- Le **moniteur d'approbation T5** (Monitor Claude) — Claude le ré-armera si besoin.
- Les **tâches planifiées** (ScheduleWakeup) — aucune active de toute façon.

## Vérifier le GPU après reboot

```
lspci -nn | grep -i 10de                     # la carte doit apparaître (01:00.0)
nvidia-smi                                     # doit répondre
nvidia-smi -q | grep -E "Product Name|FB Memory Usage|Total|VBIOS|CUDA Version"
docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu24.04 nvidia-smi   # GPU dans Docker
```

Coller la sortie de `nvidia-smi -q | grep -E "Product Name|Total"` dans la discussion →
Claude fige le vrai budget VRAM dans `config/models.yaml` + `CLAUDE.md` et bascule la stack
en mode GPU (`./scripts/switch_mode.sh gpu` si présent, sinon retirer `OLLAMA_CPU_ONLY=1` et
mettre `GPU_DEVICE_COUNT=1` dans `.env`).

## Session Claude Code

- **ID de session :** `dc444ce2-d846-44b5-ae7f-61ba9a3b6fa2`
- **Reprise manuelle :** `cd /opt/claude/sovereign-ai && /opt/claude/bin/claude --resume dc444ce2-d846-44b5-ae7f-61ba9a3b6fa2`
- **Alias :** `reprendre` (dans `/root/.bashrc`)
- **Transcript :** `/root/.claude/projects/-opt-claude-sovereign-ai/dc444ce2-d846-44b5-ae7f-61ba9a3b6fa2.jsonl`
- Si `--resume` échoue : `claude --continue` (dernière conversation du dossier), ou démarrer
  une session neuve — elle lira `docs/DESIGN_REVIEW.md`, `docs/AUTONOMOUS_STATE.md` et ce fichier.

## Modèles Albert déjà pullés (candidats tier juridique/admin)

```
hf.co/mradermacher/guillaumetell-7b-GGUF:Q4_K_M   (4,4 Go)
hf.co/mradermacher/albert-spp-8b-GGUF:Q4_K_M      (4,9 Go)
```
Comparaison à faire (bloquée en attendant le GPU — trop lent en CPU). Voir `config/models.yaml`.
