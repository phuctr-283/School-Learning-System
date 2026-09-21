from uuid import uuid4


class AssignmentIdGenerator:

    def generate(self) -> str:
        return f"ASG-{uuid4().hex[:12].upper()}"