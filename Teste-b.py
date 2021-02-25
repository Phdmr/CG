import pygame,sys,time

altura = 16
largura = 16
# Cria um array 2d, ou seja, uma lista de listas
grid = []
for row in range(largura):
        # Add an empty array that will hold each cell
        # in this row
    grid.append([])
    for column in range(altura):
        grid[row].append(0)  # Append a cell

pygame.init()
font = pygame.font.SysFont('Arial', 15)
# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

    # "Grossura" das linhas da matriz
MARGIN = 1
# WIDTH e HEIGHT são, respectivamente, comprimento
# e altura
WIDTH = 24  # x
HEIGHT = 24  # y
WINDOW_SIZE = [400, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
# Go ahead and update the screen with what we've drawn.

def typehere():
    #screen = pygame.display.set_mode((640, 480))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(int(text))
                        d = int(text)
                        text = ''
                        done = True
                        return(d)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode


        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)



#Set title of screen
#pygame.display.set_caption("Grid")

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    global word_height
    words = [word.split(' ') for word in text.splitlines()]  # Array 2d com a "Lista" das palavras.
    space = font.size(' ')[0]  # A distância do espaço.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def drawgrid():
    for row in range(largura):
        for column in range(altura):
            color = WHITE
            pygame.draw.rect(screen, color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    pygame.display.flip()

def drawnit(x,y,col):
    print("Valor de x des ", x)
    print("Valor de y des ",y)
    x = 16 -x
    pygame.draw.rect(screen, col,
                             [(MARGIN + WIDTH) * y + MARGIN,
                              (MARGIN + HEIGHT) * x + MARGIN,
                              WIDTH,
                              HEIGHT])
    pygame.display.flip()

def perguntarPonto(nome):
    x = typehere()
    y = typehere()
    #while x > largura - 1 or x < 0:
    #    x = int(input('X_' + str(nome) + ': '))
    #while y > altura - 1 or y < 0:
    #    y = int(input('Y_' + str(nome) + ': '))
    p = {'x': x, 'y': y}
    return p

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

# Definição do Besenham
def bresenham(p1=None, p2=None):
    drawgrid()
    if p1 is None:
        p1 = perguntarPonto('p1')
    if p2 is None:
        p2 = perguntarPonto('p2')
    drawgrid()
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
        x = i['x']
        y = i['y']
        drawnit(x,y,GREEN)

    pygame.display.flip()
    time.sleep(5)


# -------- Main Program Loop -----------
text = "Digite a opção: \n 1: Bresenham \n 2: Circulo \n 0: Sair"

text2 = font.render('GeeksForGeeks', True,GREEN)
texta = font.render('Voce digitou uma tecla invalida, aguarde',True, RED)
tra = [pygame.K_1, pygame.K_2,pygame.K_0]


# on exit.
while True:
        for event in pygame.event.get():
            screen.fill(WHITE)
            blit_text(screen, text, (20, 20), font)
            pygame.display.flip()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print(event.key)
                    screen.fill(WHITE)
                    bresenham()
                if event.key == pygame.K_0:
                    print("Tecla 0")
                    quit()
                if event.type == pygame.KEYUP:
                    print("Nada acontece")
                if event.key not in tra:
                    print("Errou deu ruim")
                    screen.fill(WHITE)
                    screen.blit(texta, (0, 0))
                    pygame.display.flip()
                    time.sleep(3)
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYUP:
                print("Nada acontece")
        #if event.type == pygame.QUIT: sys.exit()
