class QuestionInputMapper:

    SUPPORTED_QUESTION_TYPES = {
        "multiple_choice",
        "ordering",
        "drag_and_drop",
    }

    @classmethod
    def to_parser_format(
        cls,
        raw_questions: list[dict],
    ) -> list[dict]:

        if not isinstance(
            raw_questions,
            list,
        ):
            raise ValueError("questions phải là một danh sách.")

        if not raw_questions:
            raise ValueError("Danh sách câu hỏi không được để trống.")

        result = []

        for index, raw in enumerate(
            raw_questions,
            start=1,
        ):
            if not isinstance(
                raw,
                dict,
            ):
                raise ValueError(f"Câu hỏi {index} không hợp lệ.")

            question_type = str(
                raw.get(
                    "question_type",
                )
                or "",
            ).strip()

            question = str(
                raw.get(
                    "question",
                )
                or "",
            ).strip()

            content = str(
                raw.get(
                    "content",
                )
                or "",
            ).strip()

            answer = str(
                raw.get(
                    "answer",
                )
                or "",
            )

            if question_type not in cls.SUPPORTED_QUESTION_TYPES:
                raise ValueError(f"Câu hỏi {index}: " f"question_type không hợp lệ.")

            if not question:
                raise ValueError(f"Câu hỏi {index}: " f"question không được để trống.")

            if not answer.strip():
                raise ValueError(f"Câu hỏi {index}: " f"answer không được để trống.")

            normalized = {
                "question_type": question_type,
                "question": question,
                "content": content,
                "answer": answer,
            }

            if raw.get("score") is not None and raw.get("score") != "":
                normalized["score"] = raw["score"]

            result.append(
                normalized,
            )

        return result
