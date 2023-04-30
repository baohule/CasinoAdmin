from pydantic import BaseModel, Field


class OTPStartMessage(BaseModel):
    otp: str = Field(default="123456")
    message: str = Field(default=f"Your OTP is {otp}")

    def __init__(self, otp):
        super().__init__()
        self.otp = otp
        self.message = f"Your OTP is {self.otp}"