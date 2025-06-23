from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator

class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)

class User(BaseModel):
    name: str = Field(..., min_length=2, pattern="^[A-Za-z ]+$")
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode="after")
    def check_age_employment(self) -> 'User':
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError("Employed users must be between 18 and 65 years old.")
        return self

def process_registration(json_data: str) -> str:
    try:
        user = User.model_validate_json(json_data)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return e.json(indent=4)

json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

print(process_registration(json_input))
