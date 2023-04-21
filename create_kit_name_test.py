import requests
import config
import data


def prepare_kit_headers():
    user = create_new_user()
    assert user.status_code == 201

    user_token = user.json()["authToken"]
    assert user_token != ""

    headers = data.headers.copy()
    headers["Authorization"] = "Bearer " + user_token

    return headers


def prepare_kit_content(name):
    content = data.kit_body.copy()
    content["name"] = name

    return content


def create_new_user():
    return requests.post(
        config.URL_SERVICE + config.CREATE_USER_PATH,
        json=data.user_body,
        headers=data.headers
    )


def create_new_kit(content, headers):
    return requests.post(
        config.URL_SERVICE + config.CREATE_KIT,
        json=content,
        headers=headers
    )


def positive_assert(kit_name):
    kit = create_new_kit(
        prepare_kit_content(kit_name),
        prepare_kit_headers()
    )
    assert kit.status_code == 201
    assert kit.json()["name"] == kit_name


def negative_assert(kit_name):
    kit = create_new_kit(
        prepare_kit_content(kit_name),
        prepare_kit_headers()
    )
    assert kit.status_code == 400
    assert kit.json()["name"] != kit_name


def negative_assert_no_name_kit():
    kit = create_new_kit(
        data.kit_body,
        prepare_kit_headers()
    )

    assert kit.status_code == 400
    assert kit.json()["code"] == 400
    assert kit.json()["message"] == "Не все необходимые параметры были переданы"


# Тест 1.Допустимое количество символов (1)
def test_1_letter_in_name_kit():
    positive_assert("а")


# Тест 2. Допустимое количество символов (511)
def test_511_letter_in_name_kit():
    positive_assert(
        "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")


# Тест 3. Количество символов меньше допустимого (0)
def test_0_letter_in_name_kit():
    negative_assert("")


# Тест 4. Количество символов больше допустимого (512)
def test_512_letter_in_name_kit():
    negative_assert(
        "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")


# Тест 5. Количество символов меньше допустимого (0)
def test_english_letter_in_name_kit():
    positive_assert("QWErty")


# Тест 6. Разрешены русские буквы
def test_russian_letter_in_name_kit():
    positive_assert("Мария")


# Тест 7. Разрешены спецсимволы
def test_has_special_symbol_in_name_kit():
    positive_assert("№%@")


# Тест 8. Разрешены пробелы
def test_has_space_in_name_kit():
    positive_assert("Человек и КО ")


# Тест 9. Разрешены цифры
def test_has_number_in_name_kit():
    positive_assert("123")


# Тест 10. Параметр не передан в запросе
def test_no_name_kit():
    negative_assert_no_name_kit()


# Тест 11. Передан другой тип параметра (число)
def test_number_type_in_name_kit():
    negative_assert(123)
