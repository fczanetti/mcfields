import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_home(client):
    """
    Cria uma requisição na home page.
    """
    return client.get(reverse('base:home'))


def test_status_code_home(resp_home):
    """
    Certifica de que a home page foi carregada com sucesso.
    """
    assert resp_home.status_code == 200


def test_title_e_icone_home_page(resp_home):
    """
    Certifica de que o título e o ícone estão presentes na home page.
    """
    assert_contains(resp_home, "<title>McField's - Home</title>")
    assert_contains(resp_home, '<link rel="icon" type="image/png" href="/static/base/img/logo_original_icon.png">')


def test_nav_bar_home_page(resp_home):
    """
    Certifica de que a navbar e seus componentes estão presentes na home page.
    """
    assert_contains(resp_home, f'<a href="{reverse("base:home")}" id="logo-nav-bar"><img '
                               f'src="/static/base/img/logo-red-2.jpg" alt="Logotipo"></a>')
    assert_contains(resp_home, '<button id="toggle-button">')
    assert_contains(resp_home, '<div id="navbar-links">')
    assert_contains(resp_home, f'<li class="navbar-li"><a class="navbar-link" '
                               f'href="{reverse("base:sobre")}">Sobre</a></li>')
    assert_contains(resp_home, f'<li class="navbar-li"><a class="navbar-link" '
                               f'href="{reverse("newsletter:indice_newsletters")}">Newsletter</a></li>')
    assert_contains(resp_home, '<li class="navbar-li"><a class="navbar-link" href="">Artigos</a></li>')
    assert_contains(resp_home, '<li class="navbar-li"><a class="navbar-link" href="">Vídeos</a></li>')


def test_top_image_div_home_page(resp_home):
    """
    Certifica de que os componentes da primeira div (topo da página) estão presentes na home page
    """
    assert_contains(resp_home, '<div id="top-image-div" style="background-image: '
                               'url(/static/base/img/top_picture.jpg)">')
    assert_contains(resp_home, '<div id="top-message">')


def test_about_section_home_page(resp_home):
    """
    Certifica de que os componentes da div "about-consultant" estão presentes na home page.
    """
    assert_contains(resp_home, '<div id="about-consultant">')
    assert_contains(resp_home, '<img id="about-consultant-img" src="/static/base/img/foto_victor_02.png" '
                               'alt="Foto do logotipo">')
    assert_contains(resp_home, '<div id="about-text-div">')
    assert_contains(resp_home, '<h1 id="about-consultant-title">Sobre o consultor</h1>')
    assert_contains(resp_home, '<p id="about-consultant-text">')


def test_our_services_home_page(resp_home):
    """
    Certifica de que os componentes da div 'our-services' estão presentes na home page.
    """
    assert_contains(resp_home, '<div id="our-services">')
    assert_contains(resp_home, '<div id="our-services-div">')
    assert_contains(resp_home, '<h1 id="our-services-title" >Serviços prestados</h1>')
    assert_contains(resp_home, '<p id="our-services-text">')
    assert_contains(resp_home, '<div id="slider">')
    assert_contains(resp_home, '<div class="slide">')
    assert_contains(resp_home, '<img src="/static/base/img/abacate.jpg" alt="Foto relacionada ao serviço prestado">')
    assert_contains(resp_home, '<img src="/static/base/img/colheita.jpg" alt="Foto relacionada ao serviço prestado">')
    assert_contains(resp_home, '<img src="/static/base/img/exportacao.jpg" alt="Foto relacionada ao serviço prestado">')
    assert_contains(resp_home, '<img src="/static/base/img/plantacao.jpg" alt="Foto relacionada ao serviço prestado">')
    assert_contains(resp_home, '<h3 class="slide-title">Título do serviço</h3>')
    assert_contains(resp_home, '<h3 class="slide-title">Título do serviço</h3>')
    assert_contains(resp_home, '<h3 class="slide-title">Título do serviço</h3>')
    assert_contains(resp_home, '<h3 class="slide-title">Título do serviço</h3>')


def test_mais_infos_home_page(resp_home):
    """
    Certifica de que os componentes da div 'mais infos' estão presentes na home page.
    """
    assert_contains(resp_home, '<div id="mais-infos" style="background-image: url(/static/base/img/background03.jpg)">')
    assert_contains(resp_home, '<div id="mais-infos-bg">')
    assert_contains(resp_home, '<div id="mais-infos-text">')


def test_footer_home_page(resp_home):
    """
    Certifica de que os componentes do footer estão presentes.
    """
    assert_contains(resp_home, '<footer id="footer">')
    assert_contains(resp_home, '<div id="logo-div">')
    assert_contains(resp_home, '<img id="logo-footer" src="/static/base/img/logo_branco.png" alt="Logotipo">')
    assert_contains(resp_home, f'<a class="link-div-footer" href="{reverse("base:sobre")}">Sobre</a>')
    assert_contains(resp_home, f'<a class="link-div-footer" '
                               f'href="{reverse("newsletter:indice_newsletters")}">Newsletter</a>')
    assert_contains(resp_home, '<label id="label-email-form" for="id_email">Fique por dentro:</label>')
    assert_contains(resp_home, '<input type="email" name="email" placeholder="example@gmail.com" '
                               'maxlength="128" required id="id_email">')
    assert_contains(resp_home, '<input id="input-button" type="submit" value="Inscrever-se">')


def test_scripts_home_page(resp_home):
    """
    Certifica de que os scripts necessários para algumas funcionalidades da home page estão presentes.
    """
    assert_contains(resp_home, '<script src="/static/base/js/navbar.js" ></script>')
