# Sauvegarde Confluence — espace SI (Support informatique)

But : pouvoir reconstruire l'espace Confluence si son contenu était perdu (suppression,
incident, changement d'outillage) — dans Confluence lui-même, ou dans un autre outil
(Obsidian, tout système lisant du Markdown en dossiers).

**État au 2026-09-20** — 101 pages recensées dans l'espace SI, 100 avec du contenu réel
(la 101ᵉ, la page d'accueil de l'espace, n'a jamais été remplie : modèle Confluence par
défaut, non reproduite ici). Le Hub de FAQ (espace HDF) ne contient que des pages modèles
vides et n'a pas été sauvegardé.

## Format

- `SI/` — miroir de la hiérarchie réelle des pages Confluence : chaque page avec des
  enfants devient un dossier (nommé d'après son titre), son propre contenu restant un
  fichier `.md` à l'intérieur de ce dossier, à côté de ses enfants.
- Chaque fichier commence par deux lignes de métadonnées :
  ```
  <!-- confluence: SI / page <ID> — <URL de la page> -->
  <!-- parent_id: <ID parent> · parent: <titre du parent> -->
  ```
- `manifest.json` — table complète page_id → {title, parent_id, file}. C'est la source
  de vérité sur la hiérarchie ; les dossiers sont une projection lisible de ce fichier,
  pas l'inverse. En cas de doute sur l'arborescence exacte, se fier au manifeste.
- Le contenu est du Markdown standard (tableaux, titres, gras) — directement lisible
  par Obsidian (ouvrir `SI/` comme coffre) ou par tout éditeur de texte.

## Reconstruire dans Confluence

Pas de script d'automatisation pour l'instant (choix délibéré — voir historique de
conversation du 2026-09-20 : la priorité était le contenu portable, pas l'automatisation).
Pour recréer une page :

1. Repérer son entrée dans `manifest.json` pour connaître son titre et son `parent_id`.
2. Reconstruire les pages **dans l'ordre de la hiérarchie** (parent avant enfants) —
   trier `manifest.json` par profondeur, ou reconstruire récursivement à partir de la
   racine (`parent_id: null`).
3. Créer la page dans Confluence (API `createConfluencePage` avec `contentFormat:
   "markdown"`, ou copier-coller manuel dans l'éditeur — les tableaux Markdown sont
   reconnus nativement) avec le titre du manifeste et sous le bon parent.
4. Le contenu du fichier `.md` (sans les 2 lignes de métadonnées) est le corps de la page.

## Reconstruire dans Obsidian

Ouvrir directement `confluence-backup/SI/` comme coffre (vault) Obsidian — la hiérarchie
de dossiers existante sert de structure de navigation. Les liens internes entre fiches
(ex. « voir PROC-ATL-H01 ») sont en texte simple, pas en wikilinks `[[...]]` : à convertir
si l'on veut le graphe de liens d'Obsidian, pas nécessaire pour la lecture.

## Tenir à jour

Cette sauvegarde est un instantané du 2026-09-20. Elle ne se met pas à jour toute seule :
si des pages Confluence changent, il faut relire les pages modifiées et régénérer les
fichiers concernés (voir `scripts/build_confluence_backup.py` pour le mécanisme utilisé
pour la première extraction, qui réutilise ce qui est déjà dans `corpus/` plutôt que de
re-télécharger).

## Persistance

Décision opérateur (2026-09-20) : sauvegarde **locale d'abord**, mise en miroir sur
GitHub dans un second temps (pas encore fait à cette date). Tant qu'elle n'est pas
committée, cette sauvegarde ne protège que contre une suppression côté Confluence — pas
contre une perte du disque local.
