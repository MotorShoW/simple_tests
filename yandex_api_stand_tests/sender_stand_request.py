import configuration
import requests
import data


def get_docs():
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)

response = get_docs()
print(response.status_code)

def get_logs():
    return requests.get(configuration.URL_SERVICE + configuration.LOG_MAIN_PATH, params={'count': 20})

response_log = get_logs()
print(response_log.status_code, response_log.headers)

def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)

response_db = get_users_table()
print(response_db.status_code)

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

response_user = post_new_user(data.user_body)

print(response_user.json())

def post_products_kits(body):
    return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
                         json=body,
                         headers=data.headers)

response_kits = post_products_kits(data.products_ids)

print(response_kits.status_code)
print(response_kits.json())
