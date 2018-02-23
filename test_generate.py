import pytest
import generate

def test_generate_page():
    image = "hey.jpg"
    desc = "this is a hey"
    
    generate.generate_page(image, desc)
    
def test_generate_index():
    generate.generate_index_entries(["one.jpg", "two.jpg"])
    
def test_generate_site():
    generate.generate_site('site/images')
    
    