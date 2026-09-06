"""Test fonctionnel /search — requêtes CPA réalistes, on regarde le top-k."""
import sys
from embed import embed_query
import store

QUERIES = [
    ("un agent a oublié son mot de passe, que faire ?", "PROC-ID-004"),
    ("comment réinitialiser le MFA d'un utilisateur", "PROC-ID-004"),
    ("créer une boîte aux lettres partagée pour un service", "PROC-ID-005"),
    ("procédure de départ d'un agent : compte et matériel", "PROC-ID-003"),
    ("préparer un poste Windows 11 avec Autopilot", "PROC-ATL-002"),
    ("un poste est en panne, réparation impossible sur site", "PROC-TER-003"),
    ("comment détruire les disques durs d'un poste réformé", "PROC-STOCK-006"),
    ("intervention pour un service aux Marquises", "PROC-TER-005"),
    ("réception d'une livraison de matériel du fournisseur", "PROC-STOCK-001"),
    ("attribuer une licence E3 à un agent", "PROC-ID-007"),
    ("quel est le SLA pour une dotation de poste", "PROC-STOCK-004"),
    ("un ordinateur portable a été volé", "PROC-INT-005"),
]

def main():
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    hits_at_1 = hits_at_k = 0
    for q, gold in QUERIES:
        res = store.search(embed_query(q), k=k)
        codes = [r["proc_code"] or r["doc_id"] for r in res]
        at1 = codes[0] == gold
        atk = gold in codes
        hits_at_1 += at1
        hits_at_k += atk
        mark = "✓" if atk else "✗"
        print(f"\n{mark} « {q} »   (attendu {gold})")
        for r in res:
            flag = "→" if (r["proc_code"] == gold or r["doc_id"] == gold) else "  "
            print(f"   {flag} {r['score']:.3f}  {r['proc_code'] or r['doc_id']:16s} §{r['section'][:34]}")
    n = len(QUERIES)
    print(f"\n=== recall@1 = {hits_at_1}/{n} ({hits_at_1/n:.0%})   "
          f"recall@{k} = {hits_at_k}/{n} ({hits_at_k/n:.0%}) ===")

if __name__ == "__main__":
    main()
