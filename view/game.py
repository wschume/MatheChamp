import asyncio

import flet as ft

from model.game import Game
from model.question import Question, question_factory
from view.question import QuestionDataRow


class GameView(ft.UserControl):

  def __init__(self, game: Game):
    super().__init__()

    self._game = game

    self._game.value_changed.connect(self._on_game_value_change)

    self._progress_bar = ft.ProgressBar(value=0.0, bar_height=20)

    self._header = ft.Text("Auswertung",
                           visible=False,
                           size=20,
                           weight=ft.FontWeight.BOLD)

    self._results_table = ft.DataTable(
      columns=[ft.DataColumn(ft.Text()),
               ft.DataColumn(ft.Text())])

    self._questions_table = ft.DataTable(columns=[
      ft.DataColumn(ft.Text("Nummer"), numeric=True),
      ft.DataColumn(ft.Text("Frage")),
      ft.DataColumn(ft.Text("Antwort")),
      ft.DataColumn(ft.Text("")),
    ])

    self._start_button = ft.ElevatedButton("Los",
                                           on_click=self._on_start_click)

  def build(self):
    return ft.Column([
      self._progress_bar,
      self._header,
      self._results_table,
      self._questions_table,
      self._start_button,
    ])

  async def _on_game_value_change(self, game: Game, _: str):
    row_questions = {row.question for row in self._questions_table.rows}

    question_row: QuestionDataRow | None = None

    for i, question in enumerate(game.questions):
      if question not in row_questions:
        self._questions_table.rows.insert(
          0, question_row := QuestionDataRow(question, i))
        question.value_changed.connect(self._on_question_value_change)

    await self._questions_table.update_async()

    if question_row is not None:
      await question_row.focus_async()

  async def _on_question_value_change(self, _1: Question, _2: str):
    await self._game.add_question_async(question_factory["any"]())

  async def _on_start_click(self, _: ft.ControlEvent):
    self._start_button.visible = False
    await self._game.add_default_question_async()
    await self.update_async()

    for i in range(self._game.duration + 1):
      await asyncio.sleep(1)
      self._progress_bar.value = i / self._game.duration
      await self._progress_bar.update_async()

    self._questions_table.disabled = True
    await self._questions_table.update_async()

    self._header.visible = True

    answered_questions = {q for q in self._game.questions if q.is_answered}
    correct_answers = {q for q in answered_questions if q.is_correct}
    quotient = len(correct_answers) / len(answered_questions) * 100

    self._results_table.rows.extend([
      ft.DataRow([
        ft.DataCell(ft.Text("Anzahl Fragen")),
        ft.DataCell(ft.Text(str(len(answered_questions)))),
      ], ),
      ft.DataRow([
        ft.DataCell(ft.Text("Richtig")),
        ft.DataCell(ft.Text(str(len(correct_answers)))),
      ]),
      ft.DataRow([
        ft.DataCell(ft.Text("Quote")),
        ft.DataCell(ft.Text(f"{quotient:.2f}%")),
      ]),
    ])

    await self.update_async()
