"""Containment test: no client term in any tracked file of this public repo.

The banned terms are stored only as SHA-256 digests of their lowercased,
whitespace-normalized word forms, so this file names nothing. A line is scanned
as its 1-gram and 2-gram word sequences; a hit is any gram whose digest is in
DIGESTS. That keeps the check case-insensitive and word-bounded. This is
regression coverage; a manual sweep of tracked files and git history still runs
before any push. To add a term: sha256 of the lowercased, single-spaced words.
"""

import hashlib
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
TOKEN_RE = re.compile(r"[a-z0-9]+")

DIGESTS = {
    "0e7e0346217d32cc7d646ad999a53759a1db05af816acf487e62b186261a714e",
    "0f0f86981e90f9b4bc94ca5c82b5f5746b6fbd0cb3d097accf2931a2419f59c7",
    "2504b9f687adbbb61c22eae5356e8259d6677b0548e347684f843e92cc5ba02c",
    "28e8740f1a5411ccb601eb5d20e1b6ed2e26b10e8cf885de9b3da5ab586683d8",
    "6fb5b65165efca36c029bbfe75218d3694355856584b8a00004f7aa4850e8c1b",
    "b8746e3fc5eb4f3db7a73acbcb68c250d73d998ac6a12933365aff9bcb53028d",
    "cb13bd11612c6c248add41914ff1fc23a1d311bffadce40d3351bdd8c0def1e9",
    "cfb12585da56e4c0e3e189f24a8418f08108e5a40a84d7aafc504c704e21512c",
    "dced23f9deb642d2b33d7e7fcb38f9b1b15809530da0b21362fe925c31b80000",
    "e5a726a3cf969c027e9734910739b05d0109a6cda58f86efe6bc1791384dca65",
}


def digest(term):
    return hashlib.sha256(" ".join(TOKEN_RE.findall(term.lower())).encode()).hexdigest()


def grams(line):
    toks = TOKEN_RE.findall(line.lower())
    for i, t in enumerate(toks):
        yield t
        if i + 1 < len(toks):
            yield t + " " + toks[i + 1]


def scan(paths, digests=DIGESTS):
    """Return (path, line_no, digest_prefix) for every hit in the given files."""
    hits = []
    for p in paths:
        p = Path(p)
        if p.resolve() == SELF or not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for g in grams(line):
                d = hashlib.sha256(g.encode()).hexdigest()
                if d in digests:
                    hits.append((str(p), n, d[:8]))
    return hits


def tracked_files():
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return [REPO / line for line in out.splitlines() if line]


class ContainmentTests(unittest.TestCase):
    def test_repo_has_no_client_terms(self):
        hits = scan(tracked_files())
        self.assertEqual(hits, [], f"client terms found: {hits}")

    def test_scan_catches_a_two_word_term(self):
        probe = {digest("Zebra Widget")}
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("note about zebra widget here\n")
            self.assertEqual(len(scan([f], probe)), 1)

    def test_scan_is_case_insensitive(self):
        probe = {digest("zebrawidget")}
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("ZEBRAWIDGET said so\n")
            self.assertEqual(len(scan([f], probe)), 1)

    def test_scan_respects_word_boundaries(self):
        probe = {digest("zebra")}
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("zebras and zebrawidget\n")
            self.assertEqual(scan([f], probe), [])


if __name__ == "__main__":
    unittest.main()
