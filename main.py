from gamee import Game

g = Game()

while g.gamerunning:
    g.curr_menu.display_menu()
    g.run()