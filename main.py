import logging

import flet as ft

from model.game import Game, QuestionBase
from model.question import question_factory
from view.game import GameView


class Application:
  page: ft.Page

  def __init__(self, title: str, width: int = 640, height: int = 480):
    self._title = title
    self._width = width
    self._height = height

  async def main(self, page: ft.Page):
    print("Start of main")
    self._initialize_page(page)

    game = Game(60, [QuestionBase(question_factory["any"])])
    game_view = GameView(game)
    #game_view = GameView(None)

    print("Adding text")
    await self.page.add_async(game_view)
    print("End of main")

  def _initialize_page(self, page: ft.Page):
    self.page = page
    self.page.title = self._title
    # self.page.window_max_width = self._width
    # self.page.window_max_height = self._height
    page.scroll = ft.ScrollMode.AUTO


def main():
  print("1")
  logging.basicConfig(level=logging.DEBUG)
  logging.getLogger().setLevel(logging.DEBUG)
  application = Application("MatheChamp")

  ft.app(target=application.main, view=ft.WEB_BROWSER)


if __name__ == "__main__":
  print("main")
  main()
