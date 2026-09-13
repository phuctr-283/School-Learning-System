from dataclasses import dataclass


@dataclass
class CreateUniversityDTO:
    
    university_id: str
    name: str
    domain: str
    email: str
    phone: str