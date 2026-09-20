#!/usr/bin/env bash
# Lancé par cron à 1h du matin — voir .claude/skills/veille-nocturne/SKILL.md
# Aucune supervision humaine : portée volontairement en lecture seule + rapport,
# jamais de modification du corpus/config/production. Ne pas ajouter de droits
# plus larges ici sans relire le skill.
set -uo pipefail

cd /opt/claude/sovereign-ai || exit 1

LOG_DIR="logs/veille-nocturne"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"

/opt/claude/bin/claude \
  "/veille-nocturne" \
  --print \
  --output-format text \
  --permission-mode acceptEdits \
  --allowedTools "Read,Grep,Glob,WebSearch,WebFetch,Artifact,Bash(docker compose ps),Bash(curl -s http://localhost:*),Bash(git status),Bash(git log*),Bash(git diff*),Bash(git checkout*),Bash(git add*),Bash(git commit*),Bash(git branch*),Edit(docs/veille/*)" \
  --disallowedTools "Bash(git push*),Bash(docker compose build*),Bash(docker compose up*),Bash(docker compose down*),Bash(docker compose restart*),Bash(rm*),Bash(sudo*)" \
  >> "$LOG_FILE" 2>&1

echo "--- fin $(date -Iseconds) ---" >> "$LOG_FILE"
