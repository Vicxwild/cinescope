class TestUser:
    def test_create_user(self, creation_user_data, super_admin):
        resp_data = super_admin.api_manager.user_api.create_user(creation_user_data).json()

        assert resp_data.get('id') and resp_data['id'] != '', "ID должен быть не пустым"
        assert resp_data.get('email') == creation_user_data['email']
        assert resp_data.get('fullName') == creation_user_data['fullName']
        assert resp_data.get('roles', []) == creation_user_data['roles']
        assert resp_data.get('verified') is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_resp = super_admin.api_manager.user_api.create_user(creation_user_data).json()
        resp_by_id = super_admin.api_manager.user_api.get_user(created_user_resp["id"]).json()
        resp_by_email = super_admin.api_manager.user_api.get_user(created_user_resp["email"]).json()

        assert resp_by_id == resp_by_email
        assert resp_by_id.get('id') and resp_by_id['id'] != '', "ID должен быть не пустым"
        assert resp_by_id.get('email') == creation_user_data['email']
        assert resp_by_id.get('fullName') == creation_user_data['fullName']
        assert resp_by_id.get('roles', []) == creation_user_data['roles']
        assert resp_by_id.get('verified') is True

    # админ не может удалить юзера
    def test_delete_user(self, super_admin, registered_user):
        del_resp = super_admin.api_manager.user_api.delete_user(registered_user["id"])

        assert del_resp.status_code == 200

        response = super_admin.api_manager.user_api.get_user(registered_user["id"])
        response_data = response.json()

        assert response_data == {}, "Пользователь не был удален, ответ не пустой"

    def test_negative_get_user_by_id_common_user(self, common_user):
        get_resp = common_user.api_manager.user_api.get_user(common_user.email, expected_status=403)

        assert "message" in get_resp.json()
