
def test_lei_de_potencia(a, b):
    potencia_lab = lambda x, a, b: a * lab.pow(x, b)
    potencia_np = lambda x, a, b: a * np.power(x, b)

    ruido = np.random.normal(1, 0.001, 100)
    x_dados = np.linspace(3, 10, 100)
    y_dados = potencia_lab(x_dados, a, b) * ruido
    popt, pcov = curve_fit(potencia_np, x_dados, y_dados, p0=[a, b])  
    a_scipy, b_scipy = popt
    perr = np.sqrt(np.diag(pcov))
    a_scipy = lab.Medida(a_scipy, perr[0], '')
    b_scipy = lab.Medida(b_scipy, perr[1], '')

    x_dados = lab.linspace(3, 10, 100, 0.01, '')
    y_dados = potencia_lab(x_dados, a, b) * ruido
    potencia_lab = lab.lei_de_potencia(x_dados, y_dados)

    assert np.isclose(a_scipy.nominal,potencia_lab.a.nominal,atol=(1e-2)*a)
    assert np.isclose(b_scipy.nominal,potencia_lab.b.nominal,atol=(1e-2))
    assert np.isclose(a,potencia_lab.a.nominal,rtol=1e-2) or np.isclose(a,potencia_lab.a.nominal,atol=1e-2) 
    assert np.isclose(b,potencia_lab.b.nominal,rtol=1e-2) or np.isclose(b,potencia_lab.b.nominal,atol=1e-2)
    assert np.isclose(a_scipy.nominal,exponencial_lab.a.nominal,atol=(1e-2)*a)
