from pydantic import BaseModel, Field, computed_field


class Money(BaseModel):
    cents: int = Field(ge=0)

    @computed_field
    @property
    def amount(self) -> float:
        return self.cents / 100
