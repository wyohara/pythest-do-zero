
def quadrado(x):
    return x **2


def test_quadrado():
    assert quadrado(2) == 4

def test_quadrado_falha():
    assert quadrado(3) == 5


class TestQuadrado():
    def test_quadrado(self):
        assert quadrado(2) == 4

    def test_quadrado_erro(self):
        assert quadrado(3) == 2
        


