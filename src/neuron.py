def neuron_test():
    print("I'm a HH neuron")
    return


def dX_dt(X, t, IappFunc, *IappPars): # Под X понимается вектор (v, m, n, h); здесь будет говнокод, поскольку я не могу передать функцию I с параметрами извне
# def dX_dt(t, X, IappFunc, *IappPars): # для integrate.solve_ivp

  v = X[0]
  m = X[1]
  n = X[2]
  h = X[3]


  def eq_v(m, n, h, v, t, IappFunc, IappPars):  # Выражение для тока задаю вручную
    gNa = 40
    gK = 35
    gL = 0.3
    ENa = 55
    EK = -77
    EL = -65
    C = 1


    if callable(IappFunc):
      return (-(gNa * m**3*h*(v - ENa) + gK* n**4*(v - EK) + gL*(v - EL)) + Iperiod(t, IappPars[0])) * 1/C  # FIXME: внести условие if callable
    else:
      return (-(gNa * m**3*h*(v - ENa) + gK* n**4*(v - EK) + gL*(v - EL)) + IappFunc) * 1/C


  def eq_x(x, ax, bx):
    # return Cx * exp(-(ax + bx) * t) + ax/(ax + bx) Это ж решение с v в качестве параметра! Мне-то нужно исходное уравнение!
    return ax * (1 - x) - bx * x


  def eq_m(v,t):

    def am(v):
      # return 0.1 * (v + 25) * 1/(exp((v + 25)/10) - 1) # По HodgkinHuxley1952
      return 0.182 * (v + 35) * 1/(1 - exp(-(v + 35)/9))

    def bm(v):
      # return 4 * exp(v/18) # По HodgkinHuxley1952
      return -0.124 * (v + 35) * 1/(1 - exp((v + 35)/9))

    return eq_x(m, am(v), bm(v))


  def eq_n(v,t):

    def an(v):
      # return 0.01 * (v + 10) * 1/(exp((v + 10)/10) - 1) # По HodgkinHuxley1952
      return 0.02 * (v - 25) * 1/(1 - exp(-(v - 25)/9))

    def bn(v):
      # return 0.125 * exp(v/80) # По HodgkinHuxley1952
      return -0.002 * (v - 25) * 1/(1 - exp(v - 25)/9)

    return eq_x(n, an(v), bn(v))


  def eq_h(v,t):

    def ah(v):
      # return 0.07 * exp(v/20) # По HodgkinHuxley1952
      return 0.25 * exp(-(v + 90)/12)

    def bh(v):
      # return 1/(exp((v + 30)/10) + 1) # По HodgkinHuxley1952
      return 0.25 * exp((v + 62)/6) / exp((v + 90)/12)

    return eq_x(h, ah(v), bh(v))


  return array([eq_v(m, n, h, v, t, IappFunc, IappPars), eq_m(v,t), eq_n(v,t), eq_h(v,t)])
