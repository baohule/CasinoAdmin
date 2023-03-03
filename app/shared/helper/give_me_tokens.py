from app.shared.auth.auth_handler import AuthController

phone = input("Enter phone number: ")
print(AuthController.sign_jwt(phone))
