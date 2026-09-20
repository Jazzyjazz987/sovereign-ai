#!/usr/bin/env python3
"""Construit confluence-backup/SI/ en miroir de la hiérarchie réelle Confluence,
à partir du contenu déjà récupéré dans corpus/ (aucun re-fetch réseau).

Ne régénère PAS les 8 pages sans équivalent dans corpus/ (Conformité et RGPD, Vues par
rôle et ses 6 vues) — écrites à la main le 2026-09-20, voir confluence-backup/manifest.json.
Si ces pages changent sur Confluence, les relire et mettre à jour leur fichier directement.

Usage : python3 scripts/build_confluence_backup.py
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path("/opt/claude/sovereign-ai")
OUT = ROOT / "confluence-backup" / "SI"
CORPUS_DIRS = [
    ROOT / "corpus" / "01-procedures-legacy",
    ROOT / "corpus" / "01-procedures-legacy-archive",
    ROOT / "corpus" / "02-procedures-hybride",
    ROOT / "corpus" / "03-procedures-cible",
]

# id -> (title, parentId) — extrait de getPagesInConfluenceSpace (SI, 101 pages, 2026-09-20)
PAGES = {
    "65813": ("Support informatique", None),
    "65918": ("🏠 Accueil CPA — DSI Polynésie française", "65813"),
    "65942": ("👤 EntraID / Exchange", "65813"),
    "65958": ("PROC-STOCK-001 — Réception et contrôle livraison", "98313"),
    "65975": ("PROC-STOCK-002 — Étiquetage et injection GLPI", "98313"),
    "65994": ("PROC-STOCK-005 — Retour matériel", "98313"),
    "66015": ("PROC-ATL-001 — Préparation poste via MDT", "98329"),
    "66032": ("PROC-ATL-004 — Maintenance de l'image MDT", "98329"),
    "66051": ("PROC-TER-001 — Planification et priorisation des interventions", "229575"),
    "66070": ("PROC-TER-006 — Récupération matériel et retour stock", "229575"),
    "66089": ("PROC-INT-004 — Gestion des profils et groupes Intune", "98345"),
    "66108": ("Vue : Chef de cellule CPA", "98567"),
    "66127": ("⚠️ Conformité et RGPD", "65813"),
    "66143": ("🔴 Registre RGPD — Procédures à contrainte", "66127"),
    "66162": ("📊 Synthèse du projet de formalisation CPA", "65813"),
    "98313": ("📦 Gestion du stock", "65813"),
    "98329": ("🔧 Atelier", "65813"),
    "98345": ("🖥️ Console Intune", "65813"),
    "98361": ("PROC-STOCK-004 — Dotation matériel", "98313"),
    "98378": ("PROC-ATL-003 — SAV et incidents N2 atelier", "98329"),
    "98395": ("PROC-ATL-005 — Organisation physique de l'atelier et KPI", "98329"),
    "98415": ("PROC-TER-003 — Dépannage N1 sur site", "229575"),
    "98432": ("PROC-TER-005 — Interventions dans les îles éloignées", "229575"),
    "98455": ("PROC-INT-003 — Packaging et déploiement d'application", "98345"),
    "98475": ("PROC-INT-006 — SecOps — Remontée et traitement des alertes", "98345"),
    "98495": ("PROC-ID-002 — Modification de compte utilisateur", "65942"),
    "98516": ("PROC-ID-005 — Création et gestion des BALP", "65942"),
    "98533": ("PROC-ID-006 — Gestion des ressources Exchange (salles, équipements)", "65942"),
    "98550": ("PROC-ID-007 — Attribution et suivi des licences M365", "65942"),
    "98567": ("👁️ Vues par rôle", "65813"),
    "98585": ("Vue : Agent de proximité terrain", "98567"),
    "98602": ("Vue : Gestionnaire de comptes", "98567"),
    "98624": ("🎯 Matrice RACI — Responsabilités par procédure", "65813"),
    "131189": ("PROC-STOCK-006 — Réforme et destruction de données", "98313"),
    "131206": ("PROC-STOCK-007 — Marchés publics et achats informatiques", "98313"),
    "131226": ("PROC-ATL-002 — Préparation poste via Intune/Autopilot", "98329"),
    "131248": ("PROC-TER-002 — Dotation sur site", "229575"),
    "131270": ("PROC-TER-004 — Téléassistance et escalade atelier", "229575"),
    "131289": ("PROC-INT-001 — Enrôlement Autopilot Windows 11", "98345"),
    "131309": ("PROC-INT-005 — Retrait et désinscription appareil Intune", "98345"),
    "131333": ("PROC-ID-001 — Création de compte utilisateur", "65942"),
    "131350": ("PROC-ID-003 — Désactivation et suppression de compte", "65942"),
    "131367": ("PROC-ID-004 — Déblocage et réinitialisation MFA", "65942"),
    "131390": ("Vue : Gestionnaire de stock", "98567"),
    "131407": ("🎓 Onboarding — Parcours nouvel agent CPA", "65813"),
    "229575": ("🚗 Agents de proximité terrain", "65813"),
    "229602": ("PROC-STOCK-003 — Inventaire périodique", "98313"),
    "229626": ("PROC-INT-002 — Enrôlement Android Enterprise", "98345"),
    "229647": ("Vue : Agent atelier", "98567"),
    "229666": ("Vue : Agent téléassistance", "98567"),
    "1703937": ("🎯 Corpus cible CPA — après migration Intune et externalisation", "65813"),
    "1703958": ("📦 Gestion du stock — cible", "1703937"),
    "1703978": ("PROC-STOCK-C01 — Réception et injection du matériel", "1703958"),
    "1703998": ("PROC-STOCK-C02 — Dotation de matériel", "1703958"),
    "1704018": ("PROC-STOCK-C04 — Réforme et destruction des données", "1703958"),
    "1704038": ("PROC-TER-C02 — Dotation sur site", "1769473"),
    "1704058": ("PROC-INT-C05 — Retrait et désinscription d'un appareil", "1802241"),
    "1704078": ("PROC-ID-C01 — Vérification et suivi des comptes provisionnés", "1736726"),
    "1704098": ("PROC-ID-C02 — Création d'un compte hors SIRH", "1736726"),
    "1704118": ("PROC-ID-C03 — Gestion des boîtes aux lettres partagées et ressources Exchange", "1736726"),
    "1704138": ("PROC-STOCK-H01 — Réception et enregistrement du matériel", "1736806"),
    "1704158": ("PROC-ATL-H01 — Préparation ou contrôle d'un poste avant dotation", "1736826"),
    "1704178": ("PROC-ID-H01 — Cycle de vie d'un compte d'agent", "1802396"),
    "1736705": ("🔧 Atelier — cible", "1703937"),
    "1736726": ("👤 EntraID / Exchange — cible", "1703937"),
    "1736746": ("PROC-ATL-C02 — Contrôle de conformité du matériel à réception", "1736705"),
    "1736766": ("PROC-INT-C02 — Enrôlement et gestion des tablettes Android Enterprise", "1802241"),
    "1736786": ("PROC-ID-C04 — Déblocage et réinitialisation MFA", "1736726"),
    "1736806": ("📦 Gestion du stock — hybride", "1802375"),
    "1736826": ("🔧 Atelier — hybride", "1802375"),
    "1736847": ("🚗 Agents de proximité terrain — hybride", "1802375"),
    "1736867": ("🖥️ Console Intune — hybride", "1802375"),
    "1736887": ("PROC-STOCK-H02 — Dotation de matériel", "1736806"),
    "1736907": ("PROC-STOCK-H04 — Réforme et destruction des données", "1736806"),
    "1736927": ("PROC-ATL-H02 — SAV et incidents de niveau 2", "1736826"),
    "1736947": ("PROC-ATL-H03 — Maintenance de l'image MDT", "1736826"),
    "1736967": ("PROC-TER-H03 — Dépannage de niveau 1 sur site", "1736847"),
    "1736987": ("PROC-TER-H04 — Télé-assistance et interventions aux îles", "1736847"),
    "1737007": ("PROC-INT-H01 — Enrôlement et attribution d'un appareil", "1736867"),
    "1737027": ("PROC-ID-H03 — Déblocage MFA et gestion des licences", "1802396"),
    "1769473": ("🚗 Agents de proximité terrain — cible", "1703937"),
    "1769493": ("PROC-STOCK-C03 — Retour de matériel", "1703958"),
    "1769513": ("PROC-TER-C01 — Planification et priorisation des interventions", "1769473"),
    "1769533": ("PROC-INT-C01 — Attribution d'un appareil enrôlé", "1802241"),
    "1769553": ("PROC-INT-C03 — Packaging et déploiement d'une application", "1802241"),
    "1769573": ("PROC-ID-C05 — Attribution et suivi des licences M365", "1736726"),
    "1769593": ("🎯 Matrice RACI cible", "1703937"),
    "1769613": ("PROC-INT-H03 — Retrait et désinscription d'un appareil", "1736867"),
    "1802241": ("🖥️ Console Intune — cible", "1703937"),
    "1802261": ("PROC-ATL-C01 — SAV et incidents de niveau 2", "1736705"),
    "1802281": ("PROC-TER-C03 — Dépannage de niveau 1 sur site", "1769473"),
    "1802301": ("PROC-TER-C04 — Télé-assistance et interventions aux îles", "1769473"),
    "1802321": ("PROC-INT-C04 — Gestion des profils et groupes dynamiques", "1802241"),
    "1802341": ("🔄 Correspondance des trois corpus", "65813"),
    "1802375": ("⚙️ Procédures hybrides CPA — pendant la migration", "65813"),
    "1802396": ("👤 EntraID / Exchange — hybride", "1802375"),
    "1802416": ("PROC-STOCK-H03 — Retour de matériel", "1736806"),
    "1802437": ("PROC-TER-H01 — Planification et priorisation des interventions", "1736847"),
    "1802458": ("PROC-TER-H02 — Dotation sur site", "1736847"),
    "1802478": ("PROC-INT-H02 — Packaging et déploiement d'une application", "1736867"),
    "1802499": ("PROC-ID-H02 — Comptes hors SIRH, boîtes partagées et ressources", "1802396"),
}

SOURCE_RE = re.compile(r"<!--\s*source:.*?page\s+(\d+)")


def slugify(title: str) -> str:
    t = "".join(c for c in title if not (0x1F300 <= ord(c) <= 0x1FAFF or 0x2600 <= ord(c) <= 0x27BF))
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^\w\s-]", "", t).strip().lower()
    t = re.sub(r"[\s_]+", "-", t)
    return t.strip("-") or "page"


def build_file_index() -> dict[str, Path]:
    idx = {}
    for d in CORPUS_DIRS:
        for f in d.glob("*.md"):
            head = f.read_text(encoding="utf-8")[:400]
            m = SOURCE_RE.search(head)
            if m:
                idx[m.group(1)] = f
    return idx


def dir_for(page_id: str, cache: dict[str, Path]) -> Path:
    if page_id in cache:
        return cache[page_id]
    title, parent = PAGES[page_id]
    base = OUT if parent is None else dir_for(parent, cache) / slugify(PAGES[parent][0])
    cache[page_id] = base
    return base


def main():
    file_idx = build_file_index()
    print(f"{len(file_idx)} pages retrouvées dans corpus/ sur {len(PAGES)} pages Confluence")
    missing = [pid for pid in PAGES if pid not in file_idx and pid != "65813"]
    if missing:
        print("Sans équivalent corpus/ (écrites à la main, non régénérées ici) :", missing)

    dir_cache: dict[str, Path] = {}
    manifest = {}
    for page_id, (title, parent_id) in PAGES.items():
        target_dir = dir_for(page_id, dir_cache)
        target_dir.mkdir(parents=True, exist_ok=True)
        if page_id == "65813":
            manifest[page_id] = {"title": title, "parent_id": parent_id, "file": None,
                                 "note": "page d'accueil d'espace, jamais éditée (modèle par défaut)"}
            continue
        src = file_idx.get(page_id)
        if src is None:
            continue
        slug = slugify(title)
        dest = target_dir / f"{slug}.md"
        body = src.read_text(encoding="utf-8")
        # Retire l'ancien en-tête RAG (3 lignes de commentaire) : le manifeste porte
        # désormais ces métadonnées, pas besoin de les dupliquer dans chaque fichier.
        body = re.sub(r"^(<!--.*?-->\n)+\n?", "", body, count=1, flags=re.S)
        parent_title = PAGES[parent_id][0] if parent_id else None
        header = (
            f"<!-- confluence: SI / page {page_id} — "
            f"https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/{page_id} -->\n"
            f"<!-- parent_id: {parent_id or ''} · parent: {parent_title or ''} -->\n\n"
        )
        dest.write_text(header + body, encoding="utf-8")
        manifest[page_id] = {
            "title": title, "parent_id": parent_id,
            "file": str(dest.relative_to(OUT.parent)),
        }

    (OUT.parent / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    n_files = sum(1 for v in manifest.values() if v.get("file"))
    print(f"{n_files} fichiers écrits sous {OUT}")


if __name__ == "__main__":
    main()
