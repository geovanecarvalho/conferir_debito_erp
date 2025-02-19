import pytest
from unittest.mock import Mock
from conferir_debito_play import carregar_cpfs, extrair_dados_erp, verificar_status_erp

def test_carregar_cpfs():
    cpfs = carregar_cpfs()
    assert isinstance(cpfs, list)
    assert len(cpfs) > 0

@pytest.fixture
def mock_page(mocker):
    page = Mock()
    page.goto = Mock()
    page.fill = Mock()
    page.click = Mock()
    page.locator = Mock()
    page.locator().input_value = Mock(return_value="mock_value")
    # Ajustar o mock para retornar uma lista com elementos suficientes
    page.query_selector_all = Mock(return_value=[
        Mock(text_content=Mock(return_value="MAN")),
        Mock(text_content=Mock(return_value="01/01/2022")),
        Mock(text_content=Mock(return_value="MAN")),
        Mock(text_content=Mock(return_value="01/01/2022")),
        Mock(text_content=Mock(return_value="MAN")),
        Mock(text_content=Mock(return_value="01/01/2022")),
        Mock(text_content=Mock(return_value="MAN")),
        Mock(text_content=Mock(return_value="01/01/2022")),
        Mock(text_content=Mock(return_value="MAN")),
        Mock(text_content=Mock(return_value="01/01/2022"))
    ])
    return page

def test_extrair_dados_erp(mock_page):
    cpf = "12345678900"
    dados = extrair_dados_erp(mock_page, cpf)
    assert isinstance(dados, dict)
    assert "NOME" in dados
    assert "CIDADE" in dados
    assert "BAIRRO" in dados
    assert "ENDERECO" in dados
    assert "ENTREGA" in dados

def test_verificar_status_erp(mock_page):
    cpf = "12345678900"
    verificar_status_erp(mock_page, cpf)
    assert mock_page.goto.called
    assert mock_page.fill.called
    assert mock_page.click.called