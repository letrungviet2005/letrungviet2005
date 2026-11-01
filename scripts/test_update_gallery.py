"""Regression tests; fixtures live only in automatically removed temp directories."""

from pathlib import Path
import tempfile
import unittest
from urllib.parse import quote

from update_gallery import START, END, caption, image_paths, update


class GalleryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.readme = self.root / "README.md"
        self.before = b"\xef\xbb\xbf# Profile\r\nKeep this exactly.\r\n" + START
        self.after = END + b"\r\n## Connect\r\nUntouched.\r\n"
        self.readme.write_bytes(self.before + b"\r\nold content\r\n" + self.after)

    def image(self, name):
        path = self.root / "assets" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"test fixture")
        return path

    def test_empty_hides_section(self):
        update(self.root)
        self.assertEqual(self.readme.read_bytes(), self.before + b"\r\n" + self.after)

    def test_add_delete_rename_and_idempotence(self):
        path = self.image("01_First.png")
        self.assertTrue(update(self.root))
        self.assertFalse(update(self.root))
        path = path.rename(path.with_name("02_Second.png"))
        update(self.root)
        self.assertNotIn(b"First", self.readme.read_bytes())
        self.assertIn(b"Second", self.readme.read_bytes())
        path.unlink()
        update(self.root)
        self.assertNotIn(b"<img", self.readme.read_bytes())

    def test_outside_markers_preserved_byte_for_byte(self):
        self.image("photo.png")
        update(self.root)
        data = self.readme.read_bytes()
        self.assertTrue(data.startswith(self.before))
        self.assertTrue(data.endswith(self.after))
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))

    def test_unicode_url_and_html_escaping(self):
        name = "Lớp Python/01_Buổi học & 'code' #100%.PNG"
        self.image(name)
        update(self.root)
        data = self.readme.read_text(encoding="utf-8")
        self.assertIn(quote("assets/" + name, safe="/"), data)
        self.assertIn("Buổi học &amp; &#x27;code&#x27; #100%", data)
        self.assertEqual(caption("01_<hello>_&.png"), "<hello> &")

    def test_recursive_extensions_branding_and_natural_sort(self):
        for name in ["10_ten.PNG", "2_two.jpg", "01_one.JPEG", "sub/x.WeBp",
                     "sub/y.GIF", "branding/hidden.png", "branding/sub/hidden.jpg", "skip.svg"]:
            self.image(name)
        paths = image_paths(self.root)
        self.assertEqual(len(paths), 5)
        self.assertEqual([Path(p).name for p in paths[:3]], ["01_one.JPEG", "2_two.jpg", "10_ten.PNG"])
        update(self.root)
        data = self.readme.read_text(encoding="utf-8")
        self.assertIn("More moments (3)", data)
        self.assertEqual(data.count("<img"), 5)
        self.assertNotIn('height=', data)
        self.assertFalse(update(self.root))

    def test_invalid_markers_never_write(self):
        for data in [b"no markers", START, END, END + START,
                     START + START + END, START + END + END]:
            with self.subTest(data=data):
                self.readme.write_bytes(data)
                with self.assertRaises(ValueError):
                    update(self.root)
                self.assertEqual(self.readme.read_bytes(), data)

    def test_lf_and_caption_fallback(self):
        self.readme.write_bytes(START + b"\n" + END)
        self.image("03_my-python_class.png")
        update(self.root)
        self.assertNotIn(b"\r", self.readme.read_bytes())
        self.assertIn(b"my python class", self.readme.read_bytes())
        self.assertEqual(caption("123.png"), "123")


if __name__ == "__main__":
    unittest.main()
