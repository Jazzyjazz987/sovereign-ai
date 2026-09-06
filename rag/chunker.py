"""Découpage structuré du corpus (voir docs/RAG_REQUIREMENTS.md § méthodo chunking).

Une procédure CPA suit un gabarit constant :
  table méta → ## 🎯 Objet → ## ⚡ Déclencheur → ## 👤 Acteurs → ## 📋 Étapes
  → ## ⚠️ Points de vigilance → [## 🔴 Points de contrôle RGPD] → ## 🔗 Procédures liées
  → ## 📝 Historique (écarté).

Règles :
- 1 chunk = 1 section `##` (la table méta devient un chunk « fiche »).
- chaque chunk est préfixé d'un en-tête de contexte (code, titre, domaine, section).
- les sections courtes (< MERGE_MIN car.) sont fusionnées avec la suivante.
- l'« Historique des modifications » est écarté.
- les tables ne sont jamais coupées (une section = une unité).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

MERGE_MIN = 200          # sous ce nb de caractères, on fusionne la section avec la suivante
DROP_SECTIONS = ("historique", "historique des modifications")

SOURCE_RE = re.compile(r"<!--\s*source:.*?page\s+(\d+)\s*—\s*(\S+)\s*-->")
META_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$")
H1_RE = re.compile(r"^#\s+(.*)$", re.M)
SECTION_RE = re.compile(r"^##\s+(.*)$", re.M)
PROC_CODE_RE = re.compile(r"\b(PROC-[A-Z]+-\d+)\b")


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str                       # texte prêt à embedder (en-tête de contexte + corps)
    section: str
    proc_code: str | None = None
    titre: str | None = None
    domaine: str | None = None
    criticite: str | None = None
    contrainte_rgpd: bool = False
    sla: str | None = None
    roles: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    source_url: str | None = None
    source_file: str | None = None

    def as_row(self) -> dict:
        return asdict(self)


def _strip_html_comments(md: str) -> str:
    return re.sub(r"<!--.*?-->", "", md, flags=re.S)


def _parse_meta_table(body: str) -> dict:
    """Lit la table méta en tête de fiche (lignes `| clé | valeur |`)."""
    meta: dict[str, str] = {}
    for line in body.splitlines():
        if not line.startswith("|"):
            if meta:            # on s'arrête à la fin du bloc table
                break
            continue
        m = META_ROW_RE.match(line)
        if not m:
            continue
        key, val = m.group(1).strip(), m.group(2).strip()
        if key in ("---", ":--", ":-:", "--:") or set(val) <= {"-", ":", " "}:
            continue
        meta[key.lower()] = val.strip("` ")
    return meta


def _split_sections(body: str) -> list[tuple[str, str]]:
    """Retourne [(titre_section, contenu), ...]. Le préambule (avant le 1er ##) est 'préambule'."""
    parts = SECTION_RE.split(body)
    out: list[tuple[str, str]] = []
    preamble = parts[0].strip()
    if preamble:
        out.append(("préambule", preamble))
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        out.append((title, content))
    return out


def _clean_section_title(t: str) -> str:
    """« ## 🎯 Objet » → « Objet »."""
    return re.sub(r"^[^\wÀ-ÿ]+", "", t).strip()


def chunk_document(path: Path) -> list[Chunk]:
    raw = path.read_text(encoding="utf-8")
    m = SOURCE_RE.search(raw)
    source_url = m.group(2) if m else None

    body = _strip_html_comments(raw).strip()
    h1 = H1_RE.search(body)
    titre = h1.group(1).strip() if h1 else path.stem
    if h1:
        body = body[h1.end():].strip()

    # Un fichier n'est une « procédure » que si SON TITRE porte le code. Les pages
    # d'index / transverses citent des PROC-xxx dans leur corps sans en être une.
    proc_code = None
    pm = PROC_CODE_RE.search(titre) or PROC_CODE_RE.match(path.stem)
    if pm:
        proc_code = pm.group(1)

    meta = _parse_meta_table(body)
    domaine = meta.get("domaine")
    criticite = meta.get("criticité") or meta.get("criticite")
    sla = meta.get("sla cible") or meta.get("sla")
    contrainte_rgpd = (meta.get("contrainte rgpd", "").strip().lower() == "oui")
    roles = []
    if meta.get("rôles concernés"):
        roles = [r.strip() for r in re.split(r"[+/,]", meta["rôles concernés"]) if r.strip()]

    doc_id = proc_code or path.stem

    disp = titre if (not proc_code or proc_code in titre) else f"{proc_code} — {titre}"

    def _ctx_header(section_label: str) -> str:
        bits = [f"passage: {disp}"]
        if domaine:
            bits.append(f"Domaine : {domaine}")
        bits.append(f"Section : {section_label}")
        return " · ".join(bits)

    chunks: list[Chunk] = []

    # --- chunk 0 : fiche d'identité (la table méta) --------------------------------
    if meta:
        meta_txt = "\n".join(f"{k.capitalize()} : {v}" for k, v in meta.items())
        chunks.append(Chunk(
            doc_id=doc_id, chunk_id=f"{doc_id}#fiche", section="Fiche",
            text=_ctx_header("Fiche d'identité") + "\n" + meta_txt,
            proc_code=proc_code, titre=titre, domaine=domaine, criticite=criticite,
            contrainte_rgpd=contrainte_rgpd, sla=sla, roles=roles,
            source_url=source_url, source_file=path.name,
        ))

    # --- sections -----------------------------------------------------------------
    sections = _split_sections(body)
    pending_label, pending_text = None, ""
    for title, content in sections:
        label = _clean_section_title(title)
        if label.lower() in DROP_SECTIONS:
            continue
        # on saute le préambule s'il ne contient que la table méta déjà captée
        if label == "préambule":
            leftover = "\n".join(
                l for l in content.splitlines() if not l.strip().startswith("|")
            ).strip()
            leftover = re.sub(r"\*\*Règle invariante CPA.*", "", leftover, flags=re.S).strip()
            if not leftover:
                continue
            content = leftover

        if "procédures liées" in label.lower():
            related = PROC_CODE_RE.findall(content)
            for c in chunks:
                c.related = sorted(set(c.related) | set(related))
            # on garde quand même un petit chunk "liens"
        if pending_label:
            content = f"### {pending_label}\n{pending_text}\n\n### {label}\n{content}"
            label = f"{pending_label} + {label}"
            pending_label, pending_text = None, ""
        if len(content) < MERGE_MIN:
            pending_label, pending_text = label, content
            continue
        chunks.append(Chunk(
            doc_id=doc_id, chunk_id=f"{doc_id}#{len(chunks)}", section=label,
            text=_ctx_header(label) + "\n" + content,
            proc_code=proc_code, titre=titre, domaine=domaine, criticite=criticite,
            contrainte_rgpd=contrainte_rgpd, sla=sla, roles=roles,
            source_url=source_url, source_file=path.name,
        ))
    if pending_label:  # dernière section courte orpheline
        chunks.append(Chunk(
            doc_id=doc_id, chunk_id=f"{doc_id}#{len(chunks)}", section=pending_label,
            text=_ctx_header(pending_label) + "\n" + pending_text,
            proc_code=proc_code, titre=titre, domaine=domaine, criticite=criticite,
            contrainte_rgpd=contrainte_rgpd, sla=sla, roles=roles,
            source_url=source_url, source_file=path.name,
        ))

    # rétro-propage related sur tous les chunks
    all_related = sorted({r for c in chunks for r in c.related})
    for c in chunks:
        c.related = all_related
    return chunks


def chunk_corpus(root: Path) -> list[Chunk]:
    out: list[Chunk] = []
    for p in sorted(root.rglob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        out.extend(chunk_document(p))
    return out


if __name__ == "__main__":
    import sys
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "corpus/01-procedures-legacy")
    cs = chunk_corpus(root)
    print(f"{len(cs)} chunks depuis {root}")
    from collections import Counter
    for doc, n in Counter(c.doc_id for c in cs).most_common():
        print(f"  {n:2d}  {doc}")
    print("\n--- exemple ---")
    ex = next(c for c in cs if c.section.startswith("Étapes"))
    print(ex.text[:600])
