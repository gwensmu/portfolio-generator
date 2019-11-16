import os
import shutil
import yaml

from PIL import Image
from resizeimage import resizeimage

def get_static_html(filename):
    with open(filename) as f:
        return f.read()

HEADER = get_static_html('templates/header.txt')
FOOTER = get_static_html('templates/footer.txt')

def page_name(image_path):
    return image_path.split('.')[0] + '.html'

def generate_page(image_path, desc, **kwargs):
    contents = ''
    with open('templates/page.txt') as f:
        contents = f.read().format(image=image_path, desc=desc)

    page_path = kwargs['output_dir'] + '/' + page_name(image_path)

    with open(page_path, 'w+') as entry:
        entry.write(HEADER)
        entry.write(contents)
        entry.write(FOOTER)

    with open(page_path, 'r') as contents:
        return contents.read()

def standardize_images(images, **kwargs):
    for img in images:
        input_img = kwargs['input_dir'] + '/' + img
        output_img = kwargs['output_dir'] + '/images/%s' % img
        with open(input_img, 'r+b') as f:
            try:
                with Image.open(f) as image:
                    print('standardizing %s' % img)
                    banner = resizeimage.resize_height(image, 800)
                    banner.save(output_img, image.format)
            except Exception as e:
                print(e)
                shutil.copyfile(input_img, output_img)

def generate_thumbnails(images, **kwargs):
    for img in images:
        input_img = kwargs['input_dir'] + '/' + img
        thumbnail = kwargs['output_dir'] + '/' + 'images/thumbnails/' + img
        with open(input_img, 'r+b') as f:
            with Image.open(f) as image:
                print('generating thumbnail for %s' % img)
                thumb = resizeimage.resize_height(image, 300)
                thumb.save(thumbnail, image.format)

def thumbnail_link_html(image_path):
    return "<a href='%s'><img src='images/thumbnails/%s' height='300px'/></a>" % (page_name(image_path), image_path)

def generate_homepage(images,  **kwargs):
    toc = ''.join(map((lambda x: thumbnail_link_html(x)), images))
    index = kwargs['output_dir'] + '/index.html'

    with open(index, 'w') as p:
        p.write(HEADER)
        p.write("<div class='main'>")
        p.write(toc)
        p.write("</div>")
        p.write(FOOTER)

    with open(index, 'r') as contents:
        return contents.read()

# put this in a sqlite db or a docdb
def manage_descriptions_db(images, ymlpath='static/descriptions.yml', **kwargs):
    descriptions = {}

    with open(ymlpath, 'r') as f:
        descriptions = yaml.load(f)

    for img in images:
        try:
            descriptions[img]
        except KeyError:
            descriptions[img] = img.split('.')[0]

    with open(ymlpath, 'w') as outfile:
        yaml.dump(descriptions, outfile, default_flow_style=False)

    return descriptions

def setup_site_dirs(output_dir):
    output_images_dir = output_dir + '/images'
    if os.path.isdir(output_images_dir):
        shutil.rmtree(output_images_dir)
    os.makedirs(output_images_dir)
    os.makedirs(output_images_dir + '/thumbnails')
