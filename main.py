import yaml
import os
import sys
import urwid


class Game:
    def __init__(self, name, path, uid=None):
        self.name = name
        self.path = path

        if uid is None:
            self.uid = name
        else:
            self.uid = uid


    def __repr__(self):
        return "Game({}, {}, {})".format(self.name, self.path, self.uid)


def load_games():

    #Don't hard-code this path in, use XDG.

    games = []

    with open(os.path.expanduser("~/.config/lgm/games.yaml")) as f:
        for game in yaml.safe_load_all(f):
            newgame = Game(**game)
            games.append(newgame)


    return games


games = load_games()

choices = [game.name for game in games]

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for index, c in enumerate(choices):
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, index)
        body.append(urwid.AttrMap(button, None, focus_map='selected'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, index):
    pass

gamelist = menu('Pythons', choices)
gameinfo = urwid.Text("The quick brown fox")
gameinfo = urwid.Filler(gameinfo, valign="top", top=5)
gameinfo = urwid.Padding(gameinfo, left=4)

main = urwid.Columns([("weight", 1, gamelist), ("weight", 3, gameinfo)])

urwid.MainLoop(main, palette=[("selected", "bold", "default")]).run()
