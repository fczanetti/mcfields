import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp(client):
    """
    Cria uma requisição na home page.
    """
    return client.get(reverse('base:home'))


def test_status_code_home(resp):
    """
    Certifica de que a home page foi carregada com sucesso.
    """
    assert resp.status_code == 200


def test_title_home_page(resp):
    """
    Certifica de que o título está presente na home page.
    """
    assert_contains(resp, "<title>McField's</title>")


def test_nav_bar_home_page(resp):
    """
    Certifica de que a navbar e seus componentes estão presentes na home page.
    """
    assert_contains(resp, '<button class="toggle-button">')
    assert_contains(resp, '<div class="navbar-links">')
    assert_contains(resp, '<li><a href="">Sobre</a></li>')
    assert_contains(resp, '<li><a href="">Newsletter</a></li>')
    assert_contains(resp, '<li><a href="">Artigos</a></li>')
    assert_contains(resp, '<li><a href="">Vídeos</a></li>')


def test_top_image_div_home_page(resp):
    """
    Certifica de que os componentes da primeira div (topo da página) estão presentes na home page
    """
    assert_contains(resp, '<div id="top-message">')


def test_about_section_home_page(resp):
    """
    Certifica de que os componentes da div "about-consultant" estão presentes na home page.
    """
    assert_contains(resp, '<div id="about-consultant">')
    assert_contains(resp, '<img id="about-consultant-img"')
    assert_contains(resp, '<div id="about-text-div">')
    assert_contains(resp, '<h1 id="about-consultant-title">Sobre o consultor</h1>')
    assert_contains(resp, '<p id="about-consultant-text">')


def test_our_services_home_page(resp):
    """
    Certifica de que os componentes da div 'our-services' estão presentes na home page.
    """
    assert_contains(resp, '<div id="our-services">')
    assert_contains(resp, '<div id="our-services-div">')
    assert_contains(resp, '<h1 id="our-services-title"')
    assert_contains(resp, '<p id="our-services-text">')
    assert_contains(resp, '<div id="slider">')
    assert_contains(resp, '<div class="slide">')
    assert_contains(resp, '<h3 class="slide-title">')
    assert_contains(resp, '<p class="text-slide">')


def test_mais_infos_home_page(resp):
    """
    Certifica de que os componentes da div 'mais infos' estão presentes na home page.
    """
    assert_contains(resp, '<div id="mais-infos"')
    assert_contains(resp, '<div id="mais-infos-bg">')
    assert_contains(resp, '<div id="mais-infos-text">')
