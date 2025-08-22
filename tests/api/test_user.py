class TestUser:
    def test_get_user(self, api_manager, authenticated_admin, registered_user):
        response = api_manager.user_api.get_user_info(registered_user["id"])
        response_data = response.json()

        assert response_data["email"] == registered_user["email"], "Email не совпадает"
        assert response_data["id"] == registered_user["id"], "Email не совпадает"

    def test_delete_user(self, api_manager, authenticated_admin, registered_user):
        api_manager.user_api.delete_user(registered_user["id"])

        response = api_manager.user_api.get_user_info(registered_user["id"])
        response_data = response.json()

        assert response_data == {}, "Пользователь не был удален, ответ не пустой"

