import os
import tempfile
import unittest
import generate

class GeneratorTest(unittest.TestCase):
    def test_generate_page(self):
        image = "hey.jpg"
        desc = "this is a hey"

        tmpdir = tempfile.mkdtemp()
        directories = {'input_dir': 'images', 'output_dir': tmpdir}

        page = generate.generate_page(image, desc, **directories)
        self.assertIn("<title>Gwen is Weaving</title>", page)
        self.assertIn("<li>\"handweaver and textile generalist\"</li>", page)
        self.assertIn(desc, page)
        self.assertIn(image, page)

    def test_generate_index(self):
        tmpdir = tempfile.mkdtemp()
        directories = {'input_dir': 'images', 'output_dir': tmpdir}
        index_html = generate.generate_homepage(["one.jpg", "two.jpg"], **directories)
        self.assertIn("<title>Gwen is Weaving</title>", index_html)
        self.assertIn("<li>\"handweaver and textile generalist\"</li>", index_html)
        self.assertIn("one.jpg", index_html)
        self.assertIn("two.jpg", index_html)

    def test_thumbnail_link_html(self):
        path = "one.jpg"
        html = "<a href='one.html'><img src='images/thumbnails/one.jpg' height='300px'/></a>"
        self.assertEqual(html, generate.thumbnail_link_html(path))

    def test_generate_thumbnail(self):
        first_image = os.listdir('images')[0]
        images = [first_image]
        tmpdir = tempfile.mkdtemp()
        generate.setup_site_dirs(tmpdir)
        generate.generate_thumbnails(images, **{'input_dir': 'images', 'output_dir': tmpdir})
        self.assertTrue(os.path.isfile(tmpdir + '/images/thumbnails/' + first_image))

    def test_standardize_image(self):
        first_image = os.listdir('images')[0]
        images = [first_image]
        tmpdir = tempfile.mkdtemp()
        generate.setup_site_dirs(tmpdir)
        generate.standardize_images(images, **{'input_dir': 'images', 'output_dir': tmpdir})
        self.assertTrue(os.path.isfile(tmpdir + '/images/' + first_image))

    def test_manage_descriptions_db(self):
        images = ["blanket.jpg", "scarf.jpg"]

        tmpdir = tempfile.mkdtemp()
        tmpyml = tmpdir + '/data.yml'
        with open(tmpyml, 'w') as f:
            f.write('ok: cool')
        directories = {'input_dir': 'images', 'output_dir': tmpdir}

        titles = generate.manage_descriptions_db(images, ymlpath=tmpyml, **directories)
        self.assertEqual(titles["blanket.jpg"], 'blanket')

    def test_setup_site_dirs(self):
        tmpdir = tempfile.mkdtemp()
        generate.setup_site_dirs(tmpdir)
        self.assertTrue(os.path.isdir(tmpdir + '/images/thumbnails'))

if __name__ == "__main__":
    unittest.main()
