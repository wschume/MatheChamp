import logging
import random

from util.model_base import ValueChangedEmitter


class Question(ValueChangedEmitter):

  def __init__(self,
               question: str,
               correct_answer: str,
               given_answer: str = ""):
    super().__init__()

    self._question = question
    self._correct_answer = correct_answer
    self._given_answer = given_answer

    logging.debug(f"Createing question {self}.")

  @property
  def question(self) -> str:
    return self._question

  @question.setter
  def question(self, value: str):
    self._setattr("question", value)

  async def set_question_async(self, question: str):
    await self._setattr_async("question", question)

  @property
  def correct_answer(self) -> str:
    return self._correct_answer

  @correct_answer.setter
  def correct_answer(self, value: str):
    self._setattr("correct_answer", value)

  async def set_correct_answer_async(self, correct_answer: str):
    await self._setattr_async("correct_answer", correct_answer)

  @property
  def given_answer(self) -> str:
    return self._given_answer

  @given_answer.setter
  def given_answer(self, value: str):
    self._setattr("given_answer", value)

  async def set_given_answer_async(self, given_answer: str):
    await self._setattr_async("given_answer", given_answer)

  @property
  def is_correct(self) -> bool:
    return self._correct_answer == self._given_answer

  @property
  def is_answered(self) -> bool:
    return self._given_answer != ""


# region Factory


def from_addition(maximum: int = 10) -> Question:
  a = random.randint(0, maximum)
  b = random.randint(0, maximum)
  return Question(f"{a} + {b}", str(a + b))


def from_subtraction(maximum: int = 10) -> Question:
  a = random.randint(0, maximum)
  b = random.randint(0, maximum)

  if a < b:
    a, b = b, a

  return Question(f"{a} - {b}", str(a - b))


def from_multiplication(maximum: int = 10) -> Question:
  a = random.randint(0, maximum)
  b = random.randint(0, maximum)
  return Question(f"{a} x {b}", str(a * b))


def from_any(maximum: int = 10) -> Question:
  return random.choice([
    from_addition(maximum),
    from_subtraction(maximum),
    from_multiplication(maximum),
  ])


# endregion

question_factory = {
  "+": from_addition,
  "-": from_subtraction,
  "x": from_multiplication,
  "any": from_any,
}
