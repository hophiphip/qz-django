from django.test import TestCase
from typing import List
from .services import QuizResultService
from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO


class BaseTestCase(TestCase):
    def setUp(self):
        choices: List[ChoiceDTO] = [
            ChoiceDTO(
                "1-1-1",
                "An elephant",
                True
            ),
            ChoiceDTO(
                "1-1-2",
                "A mouse",
                False
            )
        ]

        questions: List[QuestionDTO] = [
            QuestionDTO(
                "1-1",
                "Who is bigger?",
                choices
            )
        ]

        self.quiz_dto = QuizDTO(
            "1",
            "Animals",
            questions
        )

    def test_success_quiz_result(self):
        answers: List[AnswerDTO] = [
            AnswerDTO(
                "1-1",
                ["1-1-1"]
            )
        ]

        answers_dto = AnswersDTO(
            "1",
            answers
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 1.00)

    def test_failure_quiz_result(self):
        answers: List[AnswerDTO] = [
            AnswerDTO(
                "1-1",
                ["1-1-2"]
            )
        ]

        answers_dto = AnswersDTO(
            "1",
            answers
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.00)


class BorderTestCases(TestCase):
    def setUp(self) -> None:
        self.quiz_dto = QuizDTO(
            # uuid
            "1",

            # title
            "Sample quiz",

            # questions
            [
                QuestionDTO(
                    "1-1",
                    "The correct choice is A",
                    [
                        ChoiceDTO("1-1-1", "A", True),
                        ChoiceDTO("1-1-2", "B", False),
                        ChoiceDTO("1-1-3", "C", False),
                        ChoiceDTO("1-1-4", "D", False)
                    ]
                ),

                QuestionDTO(
                    "1-2",
                    "Correct choices are B and C",
                    [
                        ChoiceDTO("1-2-1", "A", False),
                        ChoiceDTO("1-2-2", "B", True),
                        ChoiceDTO("1-2-3", "C", True),
                        ChoiceDTO("1-2-4", "D", False)
                    ]
                ),

                QuestionDTO(
                    "1-3",
                    "The correct choice is D",
                    [
                        ChoiceDTO("1-3-1", "A", False),
                        ChoiceDTO("1-3-2", "B", False),
                        ChoiceDTO("1-3-3", "C", False),
                        ChoiceDTO("1-3-4", "D", True)
                    ]
                )
            ]
        )

    def test_different_quiz_uuid(self):
        answers_dto = AnswersDTO(
            "-1",
            [
                AnswerDTO("1-1", ["1-1-1"]),
                AnswerDTO("1-2", ["1-2-2", "1-2-3"]),
                AnswerDTO("1-3", ["1-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.00)

    def test_extra_correct_choices(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1", "1-1-1"]),
                AnswerDTO("1-2", ["1-2-2", "1-2-3", "1-2-2", "1-2-3"]),
                AnswerDTO("1-3", ["1-3-4", "1-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 1.00)

    def test_extra_incorrect_choices(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1", "2-1-1"]),

                AnswerDTO("1-2", ["1-2-2", "1-2-3", "1--2"]),

                AnswerDTO("1-3", ["-3-4", "-3-4", "1-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.00)

    def test_extra_choices_with_different_choice_uuid(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1", "aaaaaaaaaaaaaaaaaaaaaaaaaa"]),

                AnswerDTO("1-2", ["1-2-2", "1-2-3", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]),

                AnswerDTO("1-3", ["1-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.33)

    def test_extra_correct_answer(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1"]),
                AnswerDTO("1-1", ["1-1-1"]),
                AnswerDTO("1-1", ["1-1-1"]),

                AnswerDTO("1-2", ["1-2-2", "1-2-3"]),

                AnswerDTO("1-3", ["0-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.67)

    def test_extra_incorrect_answer(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1"]),

                AnswerDTO("1-2", ["1-2-2", "1-2-3"]),

                AnswerDTO("1-3", ["1-3-4"]),

                AnswerDTO("1-3", ["2-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.67)

    def test_extra_incorrect_answer_with_random_choice_uuid(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1"]),

                AnswerDTO("1-2", ["1-2-2", "1-2-3"]),

                AnswerDTO("1-3", ["1-3-4"]),

                AnswerDTO("1-3", ["aaaaaaaaaaaaaaaaaaa"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.67)

    def test_extra_incorrect_answer_with_random_uuid(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1"]),

                AnswerDTO("1-2", ["1-2-2", "1-2-3"]),

                AnswerDTO("1-3", ["1-3-4"]),

                AnswerDTO("adasdasdasdas1-3", ["2-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 1.00)

    def test_one_missing_answer(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1"]),

                AnswerDTO("1-2", ["1-2-2", "1-2-3"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.67)

    def test_all_missing_answers(self):
        answers_dto = AnswersDTO(
            "1",
            [
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.00)

    def test_case_1(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1"]),
                AnswerDTO("1-2", ["1-2-2", "1-2-3"]),
                AnswerDTO("1-3", ["1-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 1.00)

    def test_case_2(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1"]),
                AnswerDTO("1-2", ["1-2-2"]),
                AnswerDTO("1-3", ["1-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.67)

    def test_case_3(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1"]),
                AnswerDTO("1-2", ["1-2-1"]),
                AnswerDTO("1-3", ["1-3-1"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.33)

    def test_case_4(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1"]),
                AnswerDTO("1-2", ["1-2-1", "1-2-2", "1-2-3"]),
                AnswerDTO("1-3", ["1-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.67)

    def test_case_5(self):
        answers_dto = AnswersDTO(
            "1",
            [
                AnswerDTO("1-1", ["1-1-1", "1-1-4"]),
                AnswerDTO("1-2", ["1-2-2", "1-2-3"]),
                AnswerDTO("1-3", ["1-3-4"]),
            ]
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.67)