import pygame
import matplotlib.pyplot as plt
import numpy as np


pygame.init()
b = pygame.Color("black")
w = pygame.Color("white")
r = pygame.Color("red")
altura = 20
largura = 20


# Cria tabuleiro
def iniciarTabuleiro():
    data = []
    for y in range(altura):
        data.append([])
        for x in range(largura):
            data[y].append(w)
    print('Tabuleiro ', largura, ' x ', altura, 'criado!')
    return data


# Apagar todos os pontos
def limpaTabuleiro(data):
    for y in range(largura):
        for x in range(altura):
            data[y][x] = w
    return data


# Desenha um ponto com uma determinada cor: r, w, ou b
def desenhaPonto(data, ponto, cor):
    for y in range(largura):
        for x in range(altura):
            if y == ponto['y'] and x == ponto['x']:
                data[(altura - y-1)][x] = cor
    return data


# Entrada de usuário pra um ponto
def perguntarPonto(nome):
    x = largura
    y = altura
    while x > largura - 1 or x < 0:
        x = int(input('X_' + str(nome) + ': '))
    while y > altura - 1 or y < 0:
        y = int(input('Y_' + str(nome) + ': '))
    p = {'x': x, 'y': y}
    return p


# Mostra o tabuleiro
def mostrarTabuleiro(data):
    screen = pygame.display.set_mode([500, 500])
    for y, row in enumerate(data):
        for x, colour in enumerate(row):
            rect = pygame.Rect(x*25, y*25, 25, 25)
            screen.fill(colour, rect=rect)
    pygame.display.update()
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
    except SystemExit:
        pygame.quit()


def bresenham(data, p1=None, p2=None):
    if p1 is None:
        p1 = perguntarPonto('p1')
    if p2 is None:
        p2 = perguntarPonto('p2')

    reflx = reflexao(p1, p2)

    if reflx['trocaxy'] is True:
        p1['x'], p1['y'] = p1['y'], p1['x']
        p2['x'], p2['y'] = p2['y'], p2['x']
    if reflx['negativax'] is True:
        p1['x'] = -p1['x']
        p2['x'] = -p2['x']
    if reflx['negativay'] is True:
        p1['y'] = -p1['y']
        p2['y'] = -p2['y']

    delta_x = p2['x'] - p1['x']
    delta_y = p2['y'] - p1['y']

    if delta_x == 0:
        m = 1
    else:
        m = float(delta_y)/float(delta_x)

    e = m - (0.5)

    x = p1['x']
    y = p1['y']

    bufferPontos = []
    p = {'x': x, 'y': y}
    bufferPontos.append(p)
    while(x < p2['x']):
        if e >= 0:
            y += 1
            e -= 1
        x += 1
        e += m
        p = {'x': x, 'y': y}
        bufferPontos.append(p)
    bufferPontos = reflexaoInversa(bufferPontos, reflx)

    for i in bufferPontos:
        if i == p1 or i == p2:
            cor = r
        else:
            cor = b
        data = desenhaPonto(data, i, cor)
    return data


def reflexao(p1, p2):
    delta_x = p2['x'] - p1['x']
    delta_y = p2['y'] - p1['y']

    if delta_x == 0:
        m = 1
    else:
        m = float(delta_y)/float(delta_x)

    if m > 1 or m < -1:
        trocaxy = True
    else:
        trocaxy = False
    if p1['x'] > p2['x']:
        negativax = True
    else:
        negativax = False
    if p1['y'] > p2['y']:
        negativay = True
    else:
        negativay = False
    res = {'trocaxy': trocaxy, 'negativax': negativax, 'negativay': negativay}
    return res


def reflexaoInversa(bufferPontos, reflx):
    if reflx['negativay'] is True:
        for i in range(len(bufferPontos)):
            bufferPontos[i]['y'] = -bufferPontos[i]['y']
    if reflx['negativax'] is True:
        for i in range(len(bufferPontos)):
            bufferPontos[i]['x'] = -bufferPontos[i]['x']
    if reflx['trocaxy'] is True:
        for i in range(len(bufferPontos)):
            bufferPontos[i]['x'], bufferPontos[i]['y'] = bufferPontos[i]['y'], bufferPontos[i]['x']
    return bufferPontos


def polilinhas(data, pontos=None):
    if pontos is None:
        pontos = []
        npontos = int(input('Quantos pontos deseja inserir: '))
        for i in range(npontos):
            pontos.append(perguntarPonto(i + 1))
    for i in range(1, len(pontos)):
        data = bresenham(data, pontos[i-1], pontos[i])
    return data


def desenhaPoligono(data, pontos=None):
    if pontos is None:
        pontos = []
        npontos = int(input('Quantos pontos deseja inserir: '))
        for i in range(npontos):
            pontos.append(perguntarPonto(i + 1))
    pontos.append(pontos[0])
    for i in range(1, len(pontos)):
        data = bresenham(data, pontos[i-1], pontos[i])
    return data


def recorteLinha(data):
    print('Diagonal inferior esquerda da janela:')
    p1 = perguntarPonto("d1")
    print('Diagonal superior direita da janela:')
    p2 = perguntarPonto("d2")
    for y in range(largura):
        for x in range(altura):
            if x < p1['x'] or y < p1['y']:
                p = {'x': x, 'y': y}
                data = desenhaPonto(data, p, r)
            if x > p2['x'] or y > p2['y']:
                p = {'x': x, 'y': y}
                data = desenhaPonto(data, p, r)
    return data

def recortePoligono(data):
    print('Diagonal inferior esquerda da janela:')
    p1 = perguntarPonto("d1")
    print('Diagonal superior direita da janela:')
    p2 = perguntarPonto("d2")
    for y in range(largura):
        for x in range(altura):
            if x < p1['x'] or y < p1['y']:
                p = {'x': x, 'y': y}
                data = desenhaPonto(data, p, r)
            if x > p2['x'] or y > p2['y']:
                p = {'x': x, 'y': y}
                data = desenhaPonto(data, p, r)
    return data


# Inicio Bezier
# Disponível em: https://towardsdatascience.com/b%C3%A9zier-interpolation-8033e9a262c2
# find the a & b points
def get_bezier_coef(points):
    # since the formulas work given that we have n+1 points
    # then n must be this:
    n = len(points) - 1

    # build coefficents matrix
    C = 4 * np.identity(n)
    np.fill_diagonal(C[1:], 1)
    np.fill_diagonal(C[:, 1:], 1)
    C[0, 0] = 2
    C[n - 1, n - 1] = 7
    C[n - 1, n - 2] = 2

    # build points vector
    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
    P[0] = points[0] + 2 * points[1]
    P[n - 1] = 8 * points[n - 1] + points[n]

    # solve system, find a & b
    A = np.linalg.solve(C, P)
    B = [0] * n
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2

    return A, B

# returns the general Bezier cubic formula given 4 control points
def get_cubic(a, b, c, d):
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

# return one cubic curve for each consecutive points
def get_bezier_cubic(points):
    A, B = get_bezier_coef(points)
    return [
        get_cubic(points[i], A[i], B[i], points[i + 1])
        for i in range(len(points) - 1)
    ]

# evalute each cubic curve on the range [0, 1] sliced in n points
def evaluate_bezier(points, n):
    curves = get_bezier_cubic(points)
    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])
# Fim Bezier


def bezier(data):
    # generate 5 (or any number that you want) random points that we want to fit (or set them youreself)

    points = np.random.rand(5, 2)

    # fit the points with Bezier interpolation
    # use 50 points between each consecutive points to draw the curve
    path = evaluate_bezier(points, 50)

    # extract x & y coordinates of points
    x, y = points[:,0], points[:,1]
    px, py = path[:,0], path[:,1]

    # plot
    plt.figure(figsize=(11, 8))
    plt.plot(px, py, 'b-')
    plt.plot(x, y, 'ro')
    plt.show()
    return data


def perspectiva(data):
    pts = []
    npontos = int(input('Quantos pontos deseja inserir: '))
    for i in range(npontos):
        pts.append(perguntarPonto(i + 1))
    p = pts
    data = desenhaPoligono(data, p)
    mostrarTabuleiro(data)
    pontos2 = []
    for i in range(len(pts) - 1):
        if pts[i]['x'] < 0:
            x = -pts[i]['x']
            pts[i]['x'] = -pts[i]['x']
        else:
            x = pts[i]['x']
        if pts[i]['y'] < 0:
            y = -pts[i]['y']
            pts[i]['y'] = -pts[i]['y']
        else:
            y = pts[i]['y']
        pontos2.append({'x': x + 3, 'y': y + 3})

    for i in range(2, len(pontos2)):
        data = bresenham(data, pts[i], pontos2[i])

    pontos3 = []
    for i in range(len(pts) - 1):
        if pts[i]['x'] < 0:
            x = -pts[i]['x']
        else:
            x = pts[i]['x']
        if pts[i]['y'] < 0:
            y = -pts[i]['y']
        else:
            y = pts[i]['y']
        pontos3.append({'x': x + 2, 'y': y + 2})

    for i in range(1, len(pontos2)):
        data = bresenham(data, pontos2[i - 1], pontos2[i])

    return data

def main():
    tabuleiro = iniciarTabuleiro()
    opcao = 99
    while True:
        print('1 - Bresenham')
        print('2 - Polilinhas')
        print('3 - Curva de Bézier')
        print('4 - Recorte de Linha')
        print('5 - Recorte de poligono')
        print('6 - Perspectiva')
        print('0 - Sair')
        opcao = int(input('Opção desejada: '))
        if opcao == 1:
            tabuleiro = bresenham(tabuleiro)
            mostrarTabuleiro(tabuleiro)
            tabuleiro = limpaTabuleiro(tabuleiro)
        if opcao == 2:
            opSec = 0
            while opSec <= 0 or opSec > 2:
                print('Polígono ?')
                print('1 - Sim')
                print('2 - Não')
                opSec = int(input('Resposta: '))
            if opSec == 1:
                tabuleiro = desenhaPoligono(tabuleiro)
            if opSec == 2:
                tabuleiro = polilinhas(tabuleiro)
            mostrarTabuleiro(tabuleiro)
            tabuleiro = limpaTabuleiro(tabuleiro)
        if opcao == 3:
            tabuleiro = bezier(tabuleiro)
            mostrarTabuleiro(tabuleiro)
            tabuleiro = limpaTabuleiro(tabuleiro)
        if opcao == 4:
            tabuleiro = bresenham(tabuleiro)
            mostrarTabuleiro(tabuleiro)
            tabuleiro = recorteLinha(tabuleiro)
            mostrarTabuleiro(tabuleiro)
            tabuleiro = limpaTabuleiro(tabuleiro)
        if opcao == 5:
            tabuleiro = desenhaPoligono(tabuleiro)
            mostrarTabuleiro(tabuleiro)
            tabuleiro = recorteLinha(tabuleiro)
            mostrarTabuleiro(tabuleiro)
            tabuleiro = limpaTabuleiro(tabuleiro)
        if opcao == 6:
            tabuleiro = perspectiva(tabuleiro)
            mostrarTabuleiro(tabuleiro)
            tabuleiro = limpaTabuleiro(tabuleiro)
        elif opcao == 0:
            exit()
        else:
            print('Opção inválida!')


if __name__ == "__main__":
    main()
