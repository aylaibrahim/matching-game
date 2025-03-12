import pygame
import random

pygame.init()

gameWidth = 840
gameHeight = 700
picSize = 130
gameColumns = 4
gameRows = 3
padding = 20
leftMargin = (gameWidth - ((picSize + padding) * gameColumns)) // 2
topMargin = 200

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 192, 203)

screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption('Memory Cooking Game')
gameIcon = pygame.image.load('onigiri.png')
pygame.display.set_icon(gameIcon)

bgImage = pygame.image.load('background.png')
bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))
startButton = pygame.image.load('start_button.png')
startButton = pygame.transform.scale(startButton, (gameWidth, gameHeight))
startButtonRect = startButton.get_rect(center=(gameWidth // 2, gameHeight // 2))

fade_surface = pygame.Surface((gameWidth, gameHeight))
fade_surface.fill(WHITE)
fade_speed = 5

memoryPictures = ['rice'] * 6 + ['seaweed'] * 6
random.shuffle(memoryPictures)
memPics = []
memPicsRect = []
for index, item in enumerate(memoryPictures):
    picture = pygame.image.load(f'assets/{item}.png')
    picture = pygame.transform.scale(picture, (picSize, picSize))
    pictureRect = picture.get_rect()
    pictureRect.x = leftMargin + (index % gameColumns) * (picSize + padding)
    pictureRect.y = topMargin + (index // gameColumns) * (picSize + padding)
    memPics.append((picture, item))
    memPicsRect.append(pictureRect)

hiddenImages = [True] * len(memPics)
firstSelection = None
secondSelection = None
matchedPairs = {'rice': 0, 'seaweed': 0}
onigiriCount = 0
objective = "Collect 3 bowls of rice and 3 stacks of seaweed to make a plate of onigiri!"
game_started = False
show_congratulations_screen = False
totalRiceCollected = 0
totalSeaweedCollected = 0
reveal_delay = 500

plate_image = pygame.image.load('plate.png')
plate_image = pygame.transform.scale(plate_image, (300, 300))
cat_image = pygame.image.load('cat.png')
cat_image = pygame.transform.scale(cat_image, (600, 600))

def draw_game_elements():
    font = pygame.font.Font(None, 28)
    objective_text = font.render(objective, True, BLACK)
    screen.blit(objective_text, (20, 20))

    collected_text = font.render(
        f"Total Seaweed collected: {totalSeaweedCollected}  Total Rice collected: {totalRiceCollected}", True, BLACK
    )
    screen.blit(collected_text, (20, 60))

    onigiri_text = font.render(f"Onigiri made: {onigiriCount}", True, BLACK)
    screen.blit(onigiri_text, (20, 100))

    for i in range(len(memPics)):
        if not hiddenImages[i]:
            screen.blit(memPics[i][0], memPicsRect[i])
        else:
            pygame.draw.rect(screen, WHITE, memPicsRect[i])

def fade_in_game_screen():
    for alpha in range(255, -1, -fade_speed):
        fade_surface.set_alpha(alpha)
        screen.blit(bgImage, (0, 0))
        draw_game_elements()
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def fade_out_start_screen():
    for alpha in range(0, 256, fade_speed):
        fade_surface.set_alpha(alpha)
        screen.fill(WHITE)
        screen.blit(startButton, startButtonRect)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def show_congratulations_screen_func():
    global show_congratulations_screen
    while show_congratulations_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(PINK)

        cat_position = (gameWidth // 3, gameHeight // 2)
        image_rect = cat_image.get_rect(center=cat_position)
        screen.blit(cat_image, image_rect)

        plate_position = (2 * gameWidth // 3, gameHeight // 2)
        plate_rect = plate_image.get_rect(center=plate_position)
        screen.blit(plate_image, plate_rect)

        font = pygame.font.Font(None, 54)
        text = font.render("Congratulations!", True, BLACK)
        text_rect = text.get_rect(center=(gameWidth // 2, gameHeight // 4))
        screen.blit(text, text_rect)

        pygame.display.update()

startScreen = True
while startScreen:
    screen.fill(WHITE)
    screen.blit(startButton, startButtonRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if startButtonRect.collidepoint(event.pos):
                fade_out_start_screen()
                startScreen = False
                game_started = True
                fade_in_game_screen()

    pygame.display.update()

gameLoop = True
while gameLoop:
    screen.blit(bgImage, (0, 0))
    draw_game_elements()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for i, rect in enumerate(memPicsRect):
                if rect.collidepoint(pos) and hiddenImages[i]:
                    if firstSelection is None:
                        firstSelection = i
                        hiddenImages[i] = False
                    elif secondSelection is None and i != firstSelection:
                        secondSelection = i
                        hiddenImages[i] = False
                        guess_time = pygame.time.get_ticks()

    if firstSelection is not None and secondSelection is not None:
        if pygame.time.get_ticks() - guess_time > reveal_delay:
            if memPics[firstSelection][1] == memPics[secondSelection][1]:
                item_type = memPics[firstSelection][1]
                matchedPairs[item_type] += 1
                if item_type == 'rice':
                    totalRiceCollected += 1
                else:
                    totalSeaweedCollected += 1

                if matchedPairs['rice'] >= 1 and matchedPairs['seaweed'] >= 1:
                    matchedPairs['rice'] -= 1
                    matchedPairs['seaweed'] -= 1
                    onigiriCount += 1

            else:
                hiddenImages[firstSelection] = True
                hiddenImages[secondSelection] = True

            firstSelection, secondSelection = None, None

    if onigiriCount >= 3 and not show_congratulations_screen:
        show_congratulations_screen = True
        show_congratulations_screen_func()

    pygame.display.update()

pygame.quit()
