import pytest
from models.base_models import RegisterUserResponse

@pytest.mark.api
class TestUser:
    def test_create_user(self, creation_user_data, super_admin):
        resp_data = super_admin.api_manager.user_api.create_user(creation_user_data).json()
        created_user_resp = RegisterUserResponse(**resp_data)

        assert created_user_resp.email == creation_user_data.email
        assert created_user_resp.fullName == creation_user_data.fullName
        assert created_user_resp.roles == creation_user_data.roles
        assert created_user_resp.verified is True

    def test_get_user_by_locator(self, super_admin, registered_user):
        resp_data_by_id = super_admin.api_manager.user_api.get_user(registered_user.id).json()
        resp_by_id = RegisterUserResponse(**resp_data_by_id)
        resp_data_by_email = super_admin.api_manager.user_api.get_user(registered_user.id).json()
        resp_by_email = RegisterUserResponse(**resp_data_by_email)

        assert resp_by_id == resp_by_email

    # простой админ не может удалить юзера
    def test_delete_user(self, super_admin, registered_user):
        del_resp = super_admin.api_manager.user_api.delete_user(registered_user.id)

        assert del_resp.status_code == 200

        response = super_admin.api_manager.user_api.get_user(registered_user.id)
        response_data = response.json()

        assert response_data == {}, "Пользователь не был удален, ответ не пустой"


    @pytest.mark.slow
    def test_negative_get_user_by_id_common_user(self, common_user):
        get_resp = common_user.api_manager.user_api.get_user(common_user.email, expected_status=403)

        assert "message" in get_resp.json()
