from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO
from typing import List


class QuizResultService:
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        # If quiz uuid is different return 0
        if self.quiz_dto.uuid != self.answers_dto.quiz_uuid:
            return 0

        # Map questions UUIDs to their correct choices
        correct_choices = {
            question.uuid: list(
                # Get question choices UUIDs that are correct
                map(lambda choice: choice.uuid, filter(lambda choice: choice.is_correct, question.choices))
            )
            for question in self.quiz_dto.questions
        }

        provided_choices = {
            answer.question_uuid: answer.choices
            for answer in self.answers_dto.answers
        }

        total_questions = len(correct_choices)
        correct_questions = 0

        # TODO: Could be shortened
        for question_uuid, provided_choice in provided_choices.items():
            if question_uuid in correct_choices:
                # Remove duplicates
                if list(dict.fromkeys(correct_choices[question_uuid])) == list(dict.fromkeys(provided_choice)):
                    correct_questions += 1

        return round(correct_questions / total_questions, 2)
