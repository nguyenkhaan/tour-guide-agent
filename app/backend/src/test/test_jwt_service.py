import unittest
from uuid import uuid4

from src.api.exceptions.error import UnauthenticatedException
from src.app import app
from src.bases.enums.jwt_token_type import TokenType
from src.models.base_model import UserRole
from src.modules.auth.auth_dto import RegisterRequest, RegisterResponse, TokenResponse
from src.modules.auth.auth_service import AuthService
from src.services.jwt_service import create_jwt_token, verify_jwt_token


class JWTServiceTests(unittest.TestCase):
    def test_auth_dtos_exclude_unneeded_response_fields(self):
        self.assertNotIn("role", RegisterRequest.model_fields)
        self.assertNotIn("token_type", TokenResponse.model_fields)
        self.assertNotIn("user", TokenResponse.model_fields)

    def test_openapi_uses_a_bearer_access_token_scheme(self):
        scheme = app.openapi()["components"]["securitySchemes"]["Access Token"]

        self.assertEqual(scheme["type"], "http")
        self.assertEqual(scheme["scheme"], "bearer")
        self.assertEqual(scheme["bearerFormat"], "JWT")
        self.assertNotIn("flows", scheme)

    def test_access_and_refresh_tokens_have_the_expected_payload(self):
        user_id = str(uuid4())
        access_token = create_jwt_token({"sub": user_id}, TokenType.ACCESS_TOKEN)
        refresh_token = create_jwt_token({"sub": user_id}, TokenType.REFRESH_TOKEN)

        access_payload = verify_jwt_token(access_token, TokenType.ACCESS_TOKEN)
        refresh_payload = verify_jwt_token(refresh_token, TokenType.REFRESH_TOKEN)

        self.assertEqual(access_payload["sub"], user_id)
        self.assertEqual(refresh_payload["sub"], user_id)
        self.assertEqual(access_payload["purpose"], TokenType.ACCESS_TOKEN.value)
        self.assertEqual(refresh_payload["purpose"], TokenType.REFRESH_TOKEN.value)

    def test_token_cannot_be_verified_as_a_different_type(self):
        access_token = create_jwt_token(
            {"sub": str(uuid4())},
            TokenType.ACCESS_TOKEN,
        )

        with self.assertRaises(UnauthenticatedException):
            verify_jwt_token(access_token, TokenType.REFRESH_TOKEN)


class _EmptyResult:
    def scalar_one_or_none(self):
        return None


class _RegistrationSession:
    def __init__(self):
        self.user = None
        self.committed = False

    async def execute(self, _statement):
        return _EmptyResult()

    def add(self, user):
        self.user = user

    async def commit(self):
        self.committed = True


class AuthServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_register_user_always_assigns_the_user_role(self):
        session = _RegistrationSession()
        service = AuthService(session)

        response = await service.register_user(
            RegisterRequest(email="new-user@example.com", password="password123")
        )

        self.assertIsNotNone(session.user)
        self.assertEqual(session.user.role, UserRole.USER)
        self.assertTrue(session.committed)
        self.assertIsInstance(response, RegisterResponse)
        self.assertEqual(response.message, "User registered successfully")
        self.assertEqual(response.path, "/auth/login")
