from uuid import uuid4


class AssignmentApplicationIdGenerator:

    def generate(self) -> str:

        return f"AAPP-{uuid4().hex[:20].upper()}"