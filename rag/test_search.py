"""Éval /search — requêtes CPA réalistes. Compare vecteur seul vs + reranker.

Usage :  python test_search.py [k]           (défaut k=5, montre les 2 modes)
"""
import sys

from retriever import retrieve

# gold = liste des fiches acceptables (multi-gold : certaines questions couvrent
# légitimement plusieurs procédures).
QUERIES = [
    ("un agent a oublié son mot de passe, que faire ?", ["PROC-ID-004"]),
    ("comment réinitialiser le MFA d'un utilisateur", ["PROC-ID-004"]),
    ("créer une boîte aux lettres partagée pour un service", ["PROC-ID-005"]),
    ("procédure de départ d'un agent : compte et matériel",
     ["PROC-ID-003", "PROC-INT-005", "PROC-STOCK-005", "PROC-TER-006"]),
    ("préparer un poste Windows 11 avec Autopilot", ["PROC-ATL-002", "PROC-INT-001"]),
    ("un poste est en panne, réparation impossible sur site", ["PROC-TER-003", "PROC-ATL-003"]),
    ("comment détruire les disques durs d'un poste réformé", ["PROC-STOCK-006"]),
    ("intervention pour un service aux Marquises", ["PROC-TER-005"]),
    ("réception d'une livraison de matériel du fournisseur", ["PROC-STOCK-001"]),
    ("attribuer une licence E3 à un agent", ["PROC-ID-007"]),
    ("quel est le SLA pour une dotation de poste", ["PROC-STOCK-004"]),
    ("un ordinateur portable a été volé", ["PROC-INT-005"]),
]


def run(k: int, rerank: bool, verbose: bool = False):
    h1 = hk = 0
    for q, gold in QUERIES:
        res = retrieve(q, k=k, rerank=rerank)
        codes = [r["proc_code"] or r["doc_id"] for r in res]
        at1 = codes[0] in gold
        atk = any(c in gold for c in codes)
        h1 += at1
        hk += atk
        if verbose:
            mark = "✓" if atk else "✗"
            print(f"\n{mark} « {q} »   (attendu {'/'.join(gold)})")
            for r in res:
                g = "→" if (r["proc_code"] or r["doc_id"]) in gold else "  "
                sc = r.get("rerank_score")
                sc = f"rr={sc:+.2f}" if sc is not None else f"cos={r['score']:.2f}"
                print(f"   {g} {sc:>10}  {r['proc_code'] or r['doc_id']:16s} §{r['section'][:32]}")
    n = len(QUERIES)
    tag = "vecteur + reranker" if rerank else "vecteur seul     "
    print(f"[{tag}]  recall@1 = {h1}/{n} ({h1/n:.0%})   recall@{k} = {hk}/{n} ({hk/n:.0%})")
    return h1, hk


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    v = "-v" in sys.argv
    run(k, rerank=False, verbose=v)
    print()
    run(k, rerank=True, verbose=v)
