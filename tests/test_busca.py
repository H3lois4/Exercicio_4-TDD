import pytest

from busca import Livro, filtrar_livros


@pytest.fixture
def acervo():
    return [
        Livro("978-85-359-0277-5", "Dom Casmurro", "Machado de Assis", 29.90,
              {"Paulista": 3, "Pinheiros": 0}),
        Livro("978-85-7164-114-9", "Memórias Póstumas de Brás Cubas", "Machado de Assis", 34.50,
              {"Paulista": 0}),
        Livro("978-85-359-1464-8", "Grande Sertão: Veredas", "João Guimarães Rosa", 89.00,
              {"Pinheiros": 2}),
        Livro("978-85-01-11477-5", "A Hora da Estrela", "Clarice Lispector", 39.90,
              {"Paulista": 1, "Pinheiros": 5}),
    ]


def isbns(livros):
    return [livro.isbn for livro in livros]


# --- Casos básicos ---

def test_sem_criterios_retorna_todos_os_livros(acervo):
    assert filtrar_livros(acervo) == acervo


def test_lista_vazia_retorna_lista_vazia():
    assert filtrar_livros([], titulo="qualquer") == []


def test_nenhum_resultado_retorna_lista_vazia(acervo):
    assert filtrar_livros(acervo, titulo="Harry Potter") == []


# --- Título e autor ---

def test_filtra_por_titulo_parcial_sem_diferenciar_maiusculas(acervo):
    resultado = filtrar_livros(acervo, titulo="casmurro")
    assert isbns(resultado) == ["978-85-359-0277-5"]


def test_filtro_de_titulo_ignora_acentos(acervo):
    resultado = filtrar_livros(acervo, titulo="memorias postumas")
    assert isbns(resultado) == ["978-85-7164-114-9"]


def test_filtra_por_autor(acervo):
    resultado = filtrar_livros(acervo, autor="machado")
    assert isbns(resultado) == ["978-85-359-0277-5", "978-85-7164-114-9"]


def test_filtro_de_autor_ignora_acentos(acervo):
    resultado = filtrar_livros(acervo, autor="joao guimaraes")
    assert isbns(resultado) == ["978-85-359-1464-8"]


# --- ISBN ---

def test_filtra_por_isbn_exato(acervo):
    resultado = filtrar_livros(acervo, isbn="978-85-01-11477-5")
    assert isbns(resultado) == ["978-85-01-11477-5"]


def test_filtro_de_isbn_ignora_hifens(acervo):
    resultado = filtrar_livros(acervo, isbn="9788501114775")
    assert isbns(resultado) == ["978-85-01-11477-5"]


# --- Preço ---

def test_filtra_por_preco_maximo_inclusivo(acervo):
    resultado = filtrar_livros(acervo, preco_maximo=34.50)
    assert isbns(resultado) == ["978-85-359-0277-5", "978-85-7164-114-9"]


def test_preco_maximo_negativo_lanca_erro(acervo):
    with pytest.raises(ValueError):
        filtrar_livros(acervo, preco_maximo=-1)


# --- Loja e estoque ---

def test_filtra_livros_que_a_loja_trabalha(acervo):
    resultado = filtrar_livros(acervo, loja="Pinheiros")
    assert isbns(resultado) == [
        "978-85-359-0277-5", "978-85-359-1464-8", "978-85-01-11477-5",
    ]


def test_apenas_disponiveis_em_qualquer_loja(acervo):
    resultado = filtrar_livros(acervo, apenas_disponiveis=True)
    assert "978-85-7164-114-9" not in isbns(resultado)
    assert len(resultado) == 3


def test_apenas_disponiveis_na_loja_informada(acervo):
    resultado = filtrar_livros(acervo, loja="Pinheiros", apenas_disponiveis=True)
    assert isbns(resultado) == ["978-85-359-1464-8", "978-85-01-11477-5"]


# --- Combinação e integridade ---

def test_criterios_sao_combinados_com_e(acervo):
    resultado = filtrar_livros(
        acervo, autor="machado", loja="Paulista", apenas_disponiveis=True
    )
    assert isbns(resultado) == ["978-85-359-0277-5"]


def test_nao_altera_a_lista_original(acervo):
    copia = list(acervo)
    filtrar_livros(acervo, titulo="dom")
    assert acervo == copia