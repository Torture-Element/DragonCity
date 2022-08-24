import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self, fullscreen = False):
        # general setup
        pygame.init()
        pygame.mouse.set_visible(False)
        self.fullscreen = fullscreen
        self.Full_Screen()

        pygame.display.set_caption('load always') # game title
        pygame.display.set_icon(pygame.image.load(resource_path('assets/graphics/icon/icon.png')))
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.display.set_mode(REAL_RES, pygame.DOUBLEBUF|pygame.OPENGL)
        from crt_shader import Graphic_engine
        self.crt_shader = Graphic_engine(screen)
        
        # level
        self.level = Level(self.crt_shader.render)
        self.level.title_screen()
        self.level.menu_state = 'title'

        # sound
        self.mute_music = True
        self.main_sound = pygame.mixer.Sound(resource_path('assets/audio/main.ogg'))
        self.main_sound.set_volume(0.03)
        if self.mute_music:
            self.main_sound.set_volume(0)
        self.main_sound.play(loops = -1)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        self.level.upgrade_menu()
                    elif event.key == pygame.K_p:
                        self.level.toggle_menu()
                    elif event.key == pygame.K_m:
                        if not(self.mute_music):
                            self.mute_music = True
                            self.main_sound.set_volume(0)
                        else:self.main_sound.set_volume(0.01)
                    elif event.key == pygame.K_0:
                        self.crt_shader.__init__(self.crt_shader.screen, (self.crt_shader.style + 1) % 3)
                    elif event.key == pygame.K_f:
                        self.fullscreen = not(self.fullscreen)
                        self.Full_Screen()
                    elif event.key == pygame.K_ESCAPE:
                        self.level.title_screen()
                if event.type == pygame.MOUSEWHEEL:
                    self.level.visible_sprites.zoom_scale += event.y * 0.03

            screen.fill(WATER_COLOR)
            self.level.run()
            self.crt_shader.render()
            self.clock.tick(FPS)
            pygame.display.set_caption('load always' + ' ' + str(round(self.clock.get_fps())))

    def Full_Screen(self):
        if self.fullscreen:
            pygame.display.set_mode(REAL_RES, pygame.DOUBLEBUF|pygame.OPENGL|pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(REAL_RES, pygame.DOUBLEBUF|pygame.OPENGL)

    def quit_game(self):
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
    # multithread
    # from gui_helper import Helper_window_run
    # from threading import Thread
    # thread1 = Thread(target=Helper_window_run)
    # thread1.setDaemon(True)
    # thread1.start()
    # thread2 = Thread(target=main())
    # thread2.setDaemon(True)
    # thread2.start()

    # multiprogressing
    # import multiprocessing
    # multiprocessing.freeze_support()
    # for _ in range(2):
    #     multiprocessing.Process(target=main).start()