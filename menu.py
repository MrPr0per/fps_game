import pygame
from settings import *
from resourses import *
from floors import load_floor, level_names, level_nums
from player import Player


class Menu_panel:
    def __init__(self, button_list, name):
        self.button_list = button_list
        self.name = name

    def check_interaction(self, floor, player, menu, current_level_number):
        if self.name == Names_menu_pannels.MAIN_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.button_list:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            if button.text == Button.Names_buttons.NEW_GAME:
                                return GAME_CYCLES.GAMEPLAY, load_floor(100), Player(), menu, 100

                            elif button.text == Button.Names_buttons.CONTINUE:
                                return GAME_CYCLES.GAMEPLAY, floor, player, menu, current_level_number

                            elif button.text == Button.Names_buttons.SETTINGS:
                                print(Button.Names_buttons.SETTINGS)

                            elif button.text == Button.Names_buttons.CHOOSE_LVL:
                                return GAME_CYCLES.MAIN_MENU, floor, player, choose_lvl, current_level_number

                            elif button.text == Button.Names_buttons.EXIT:
                                pygame.quit()
                                quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # exit()
                        return GAME_CYCLES.GAMEPLAY, floor, player, menu, current_level_number

            # return GAME_CYCLES.MAIN_MENU, floor, player, menu, current_level_number

        if self.name == Names_menu_pannels.CHOOSE_LVL:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.button_list:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            n = level_nums[button.text]
                            return GAME_CYCLES.GAMEPLAY, load_floor(n), Player(), main_menu, n

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return GAME_CYCLES.MAIN_MENU, floor, player, main_menu, current_level_number

        return GAME_CYCLES.MAIN_MENU, floor, player, menu, current_level_number

    def draw(self, sc):
        def draw_background():
            background = Main_menu_sprites.background
            scale = WIDTH / background.get_width()
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            sc.blit(background, (0, 0))

            if self.name == Names_menu_pannels.MAIN_MENU:
                logo = Main_menu_sprites.logo
                logo = pygame.transform.scale(logo, (logo.get_width() * scale, logo.get_height() * scale))
                sc.blit(logo, (HALF_WIDTH - logo.get_width() / 2, HEIGHT * 0.07))

        def draw_buttons():
            width_prefix = Button.font_bold.render('- ', True, Button.color_text).get_width()
            for button in self.button_list:
                if button.centered_text:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        render = Button.font_bold.render('- ' + str(button.text) + ' -', True,
                                                         Button.color_text)
                    else:
                        render = Button.font.render(str(button.text), True, Button.color_text)

                    sc.blit(render, (button.rect.x + button.rect.width / 2 - render.get_width() / 2,
                                     button.rect.y + button.rect.height / 2 - render.get_height() / 2))
                else:
                    is_focused = False
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        is_focused = True
                        render = Button.font_bold.render('- ' + str(button.text), True, Button.color_text)
                    else:
                        render = Button.font.render(str(button.text), True, Button.color_text)

                    x_text = button.rect.x
                    if is_focused:
                        x_text -= width_prefix
                    sc.blit(render, (x_text, button.rect.y + button.rect.height / 2 - render.get_height() / 2))

        def draw_cursor():
            pos = pygame.mouse.get_pos()
            image = Main_menu_sprites.cursor
            image = pygame.transform.scale(image, (WIDTH / 35, WIDTH / 35))
            sc.blit(image, pos)

        draw_background()
        draw_buttons()
        draw_cursor()


class Button:
    font_size = WIDTH // 70
    # font = pygame.font.SysFont('Lucida Console', font_size, bold=False)
    # font_bold = pygame.font.SysFont('Lucida Console', font_size, bold=True)
    font = pygame.font.Font('resourses/fonts/font1.ttf', int(font_size * 8 / 5))
    font_bold = pygame.font.Font('resourses/fonts/font1.ttf', int(font_size * 8 / 5 * 1.01))

    color_text = (188, 201, 223)
    width = WIDTH * 0.25

    class Names_buttons:
        NEW_GAME = 'новая игра'
        CONTINUE = 'продолжить'
        SETTINGS = 'настройки'
        CHOOSE_LVL = 'выбрать уровень'
        EXIT = 'выход'

    def __init__(self, rect, text, centered_text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.centered_text = centered_text


class Names_menu_pannels:
    MAIN_MENU = 'MAIN_MENU'
    CHOOSE_LVL = 'CHOOSE_LVL'


names_button = [
    Button.Names_buttons.NEW_GAME,
    Button.Names_buttons.CONTINUE,
    # Button.Names_buttons.SETTINGS,
    Button.Names_buttons.CHOOSE_LVL,
    Button.Names_buttons.EXIT,
]

# menu_pannels_list = {
#     Names_menu_pannels.MAIN_MENU: Menu_panel(button_list=[
#         Button((HALF_WIDTH - Button.width / 2, HEIGHT * 0.39 + Button.font_size * 2 * i, Button.width, Button.font_size * 1.4), names_button[i]) for i in range(len(names_button))
#     ], is_draw_logo=True),
#     Names_menu_pannels.CHOOSE_LVL: Menu_panel(button_list=[
#         Button((WIDTH * 0.1, HEIGHT * 0.1 + Button.font_size * 1.5 * i, Button.width, Button.font_size * 1.3), floors_list[i].name) for i in range(len(floors_list))
#     ])
# }
main_menu = Menu_panel(button_list=[
    Button((HALF_WIDTH - Button.width / 2, HEIGHT * 0.39 + Button.font_size * 2 * i,
            Button.width, Button.font_size * 1.4), names_button[i],
           centered_text=True) for i in range(len(names_button))
], name=Names_menu_pannels.MAIN_MENU)
names = list(level_names.values())
choose_lvl = Menu_panel(button_list=[
    Button((WIDTH * 0.1, HEIGHT * 0.1 + Button.font_size * 1.5 * i,
            Button.width, Button.font_size * 1.3), names[i],
           centered_text=False) for i in range(len((names)))
], name=Names_menu_pannels.CHOOSE_LVL)