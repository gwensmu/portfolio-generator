import os
import shutil
import yaml

from PIL import Image
from resizeimage import resizeimage

def get_header():
    with open('header.txt') as h:
        return h.read()

def get_footer():
    with open('footer.txt') as foot:
        return foot.read()

def is_gif(img):
    img.split(".")[1] == "gif"


HEADER = get_header()
FOOTER = get_footer()

def page_name(image_path):
    return image_path.split(".")[0] + ".html"

def generate_page(image_path, desc):
    contents = ""
    with open('page.txt') as f:
        contents = f.read().format(image=image_path, desc=desc)

    with open("site/" + page_name(image_path), 'w') as entry:
        entry.write(HEADER)
        entry.write(contents)
        entry.write(FOOTER)

def standardize_images(images):
    for img in images:
        if "-mov" in img:
            next
        filepath = "site/images/%s" % img
        with open("images/%s" % img, 'r+b') as f:
            try:
                with Image.open(f) as image:
                    banner = resizeimage.resize_height(image, 800)
                    banner.save(filepath, image.format)
            except Exception as e:
                shutil.copyfile("images/%s" % img, filepath)

def generate_thumbnails(images):
    for img in images:
        filepath = "site/images/%s" % img
        with open(filepath, 'r+b') as f:
            with Image.open(f) as image:
                thumb = resizeimage.resize_width(image, 300)
                thumb.save('site/images/thumbnails/%s' % img, image.format)

def generate_index_entry(image_path):
    return "<a href='%s'><img src='images/thumbnails/%s' width='300px'/></a>" % (page_name(image_path), image_path)

def generate_index_entries(images):
    toc = ''.join(map((lambda x: generate_index_entry(x)), images))

    with open("site/index.html", 'w') as p:
        p.write(HEADER)
        p.write(toc)
        p.write(FOOTER)

def manage_alts_db(images):
    alts = {}
    with open('site/meta/alts.yml') as f:
        alts = yaml.load(f)

    for img in images:
        try:
            alts[img]
        except KeyError:
            alts[img] = ''

    with open('site/meta/alts.yml', 'w') as outfile:
        yaml.dump(alts, outfile, default_flow_style=False)

    return alts

def generate_site(images_dir):
    images = os.listdir(images_dir)
    standardize_images(images)
    generate_thumbnails(images)
    generate_index_entries(images)
    alt_texts = manage_alts_db(images)
    for entry in images:
        generate_page(entry, alt_texts[entry])
