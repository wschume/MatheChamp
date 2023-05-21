import random
from dataclasses import dataclass, field
from typing import Callable

from model.question import Question
from util.model_base import ValueChangedEmitter
from util.signal import Blocker


@dataclass
class QuestionBase:
    question: Callable[..., Question]
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)


class Game(ValueChangedEmitter):
    def __init__(self, duration: int, question_base: list[QuestionBase]):
        super().__init__()

        self._duration = duration
        self._question_base = question_base

        self._questions: list[Question] = []

    def add_default_question(self):
        qb = random.choice(self._question_base)
        self.add_question(qb.question(*qb.args, **qb.kwargs))

    async def add_default_question_async(self):
        qb = random.choice(self._question_base)
        await self.add_question_async(qb.question(*qb.args, **qb.kwargs))

    def add_question(self, question: Question):
        self._questions.append(question)

        self.value_changed.emit(self, "questions")

    async def add_question_async(self, question: Question):
        with Blocker.from_signal(self.value_changed):
            self.add_question(question)

        await self.value_changed.emit_async(self, "questions")

    def add_questions(self, questions: list[Question]):
        for question in questions:
            self.add_question(question)

    async def add_questions_async(self, questions: list[Question]):
        for question in questions:
            await self.add_question_async(question)

    @property
    def duration(self) -> int:
        return self._duration

    @property
    def questions(self) -> list[Question]:
        return self._questions.copy()
