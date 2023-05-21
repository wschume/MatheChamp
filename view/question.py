import flet as ft

from model.question import Question


class QuestionDataRow(ft.DataRow):
    def __init__(self, question: Question, index: int):
        super().__init__()

        self._question = question

        self._question.value_changed.connect(self._on_question_value_change)

        self._question_text = ft.Text(self._question.question)
        self._question_answer = ft.TextField(
            value=self._question.given_answer,
            on_blur=self._on_blur_or_submit,
            on_submit=self._on_blur_or_submit,
        )
        self._question_icon = ft.Icon()

        self.cells.extend(
            [
                ft.DataCell(control)
                for control in [
                    ft.Text(f"{index + 1}."),
                    self._question_text,
                    ft.Container(self._question_answer, width=100),
                    self._question_icon,
                ]
            ]
        )

    @property
    def question(self) -> Question:
        return self._question

    async def focus_async(self):
        await self._question_answer.focus_async()

    async def _on_question_value_change(self, question: Question, key: str):
        self.disabled = question.is_answered

        if question.is_correct:
            self._question_icon.name = ft.icons.CHECK
            self._question_icon.color = "green"
        else:
            self._question_icon.name = ft.icons.CLOSE
            self._question_icon.color = "red"

        await self.update_async()

    async def _on_blur_or_submit(self, event: ft.ControlEvent):
        await self._question.set_given_answer_async(event.control.value.strip())
