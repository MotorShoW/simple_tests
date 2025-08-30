import Data
from sender_stand_request import APIClient
from requests.exceptions import HTTPError, RequestException
import pytest


@pytest.fixture(scope="class", autouse=True) # Фикстура для создания пользователя один раз на весь тест-ран
def setup_user():
    client = APIClient(user_body=Data.user_body)
    client.post_new_user()
    return client


class TestAPI:
    def get_kit_body(self, name):
        current_body = Data.kit_body.copy()
        current_body['name'] = name
        return current_body

    def positive_assert(self, kit_body, setup_user):
        try:
            body = self.get_kit_body(kit_body)
            response = setup_user.post_new_client_kit(body)
            assert response is not None
            assert response.status_code == 201, f'Ожидался код ответа 201, получен {response.status_code}'
            assert response.json()['name'] == kit_body, f"Ожидаемое имя: {kit_body}, получено: {response.json()['name']}"
        except HTTPError as http_error:
            pytest.fail(f"HTTP ошибка при создании набора: {http_error}")

        except RequestException as request_error:
            pytest.fail(f"Ошибка запроса: {request_error}")

        except Exception as e:
            pytest.fail(f"Произошла непредвиденная ошибка: {e}")
        

    def negative_assert(self, kit_body, setup_user):
        try:
            body = self.get_kit_body(kit_body)
            response = setup_user.post_new_client_kit(body)
            assert response is not None
            assert response.status_code == 400, f'Ожидался код ответа 400, получен {response.status_code}'
        except HTTPError as http_error:
            pytest.fail(f"HTTP ошибка при создании набора: {http_error}")

        except RequestException as request_error:
            pytest.fail(f"Ошибка запроса: {request_error}")

        except Exception as e:
            pytest.fail(f"Произошла непредвиденная ошибка: {e}")


    def test_create_kit_1_letter_in_name_get_success_response(self, setup_user):
        self.positive_assert('a', setup_user)

    def test_create_kit_511_letters_in_name_get_success_response(self, setup_user):
        self.positive_assert('a' * 511, setup_user)

    def test_create_kit_0_letters_in_name_get_error_response(self, setup_user):
        self.negative_assert('', setup_user)

    def test_create_kit_512_letters_in_name_get_error_response(self, setup_user):
        self.negative_assert('a' * 512, setup_user)

    def test_create_kit_english_letters_permitted_in_name_get_success_response(self, setup_user):
        self.positive_assert('QWErty', setup_user)

    def test_create_kit_russian_letters_permitted_in_name_get_success_response(self, setup_user):
        self.positive_assert('Мария', setup_user)

    def test_create_kit_special_symbols_permitted_in_name_get_success_response(self, setup_user):
        self.positive_assert('"№%@"', setup_user)

    def test_create_kit_spacebar_permitted_in_name_get_success_response(self, setup_user):
        self.positive_assert('Человек и КО', setup_user)

    def test_create_kit_numbers_as_string_permitted_in_name_get_success_response(self, setup_user):
        self.positive_assert('123', setup_user)

    def test_create_kit_empty_body_name_field_get_error_response(self, setup_user):
        empty_name_kit_body = self.get_kit_body('')
        self.negative_assert(empty_name_kit_body, setup_user)

    def test_create_kit_numbers_as_integer_in_name_get_error_response(self, setup_user):
        self.negative_assert(123, setup_user)
