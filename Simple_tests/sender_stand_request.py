import Configuration
import Data
import requests
from requests.exceptions import HTTPError, RequestException
import logging

logging.basicConfig(level=logging.INFO)

class APIClient:
    def __init__(self, user_body, headers=Data.headers):
        self.user_body = user_body
        self.headers = headers
        self.auth_token = None

    def post_new_user(self): # Создание нового пользователя и получение токена
        try:
            create_user = requests.post(
                Configuration.URL_SERVICE + Configuration.URL_CREATE_USER,
                json=self.user_body,
                headers=self.headers
            )
            create_user.raise_for_status()  # Проверка на HTTP ошибки
            response_data = create_user.json()
            if 'authToken' in response_data:   # Проверка наличия токена в ответе
                self.auth_token = response_data['authToken']
                logging.info(f'Токен получен: {self.auth_token}')
            else:
                logging.error('authToken не найден в ответе при создании пользователя')
                return None
        except HTTPError as http_error:
            logging.error(f'HTTP ошибка при создании пользователя: {http_error}')
        except KeyError:
            logging.error('Ошибка при обработке данных ответа при создании пользователя')
        except Exception as error:
            logging.error(f'Ошибка при создании пользователя: {error}')
        return self.auth_token

    def post_new_client_kit(self, kit_body): # Создание набора для авторизованного клиента
        if not self.auth_token:
            logging.error('authToken не найден в ответе. Невозможно создать набор.')
            return None
        
        headers_with_token = self.headers.copy()
        headers_with_token['Authorization'] = f'Bearer {self.auth_token}'
        
        try:
            response = requests.post(
                Configuration.URL_SERVICE + Configuration.URL_CREATE_KIT,
                json=kit_body,
                headers=headers_with_token
            )
            response.raise_for_status()  # Проверка на HTTP ошибки
            logging.info(f'Набор успешно создан. Ответ: {response.status_code}')
            return response
        except HTTPError as http_error:
            logging.error(f'HTTP ошибка при создании набора: {http_error}')
        except RequestException as request_error:
            logging.error(f'Ошибка запроса при создании набора: {request_error}')
        except Exception as error:
            logging.error(f'Непредвиденная ошибка при создании набора: {error}')
        return None
