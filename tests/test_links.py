import tempfile
import unittest
from pathlib import Path

from repo_checks import REPO, check_relative_links


def tree(root, files):
    for name, body in files.items():
        p = Path(root) / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")


class RelativeLinks(unittest.TestCase):
    def test_current_repo_passes(self):
        self.assertEqual(check_relative_links(REPO), [])

    def test_link_to_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"README.md": "See [x](docs/gone.md).\n"})
            out = check_relative_links(t)
            self.assertEqual(len(out), 1)
            self.assertIn("README.md:1: broken link 'docs/gone.md'", out[0])

    def test_valid_links_pass(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {
                "README.md": "[a](docs/a.md#top) [b](docs/) [web](https://x.io/y) [m](mailto:a@b.c) [h](#here)\n",
                "docs/a.md": "[up](../README.md) ![img](pic.png)\n",
                "docs/pic.png": "",
            })
            self.assertEqual(check_relative_links(t), [])

    def test_relative_to_the_linking_file(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"README.md": "ok\n", "docs/a.md": "[bad](README.md)\n"})
            self.assertEqual(len(check_relative_links(t)), 1)

    def test_code_is_ignored(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"a.md": "`[x](nope.md)`\n```\n[y](nope.md)\n```\n"})
            self.assertEqual(check_relative_links(t), [])

    def test_missing_image_fails(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"a.md": "![i](missing.png)\n"})
            self.assertEqual(len(check_relative_links(t)), 1)


if __name__ == "__main__":
    unittest.main()
