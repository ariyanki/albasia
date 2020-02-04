from . import reset_database

class TestUser:

    def test_user(self):
        reset_database()

        # global login_data
        # try:
        #     login_data
        # except NameError:
        #     login_data = create_token()

        # token = login_data['data']['access_token']

        # os.environ['MEOWTH_TEST_CASE'] = 'valid'
        # os.environ['PIGGYBANK_TEST_CASE'] = 'valid'

        # # Test add new success
        # data = {
        #     "username": "081234325256",
        #     "password": "123456",
        #     "fullname": "Super Admin",
        #     "phonenumber": "08123456789",
        #     "email": "Adminin@yapulsa.com",
        #     "longitude": "-6.1753924",
        #     "latitude": "106.8249641",
        #     "area_id": 2,
        #     "cluster_id": 2,
        #     "upline_user_id": 1,
        #     "use_pin": 1,
        #     "is_password_changed": 1,
        #     "photo_filename": "http://www.yapulsa.com/file/photo/image123.jpg",
        #     "kredit": 1000,
        #     "is_loggedin": 1
        # }
        # res = user.post(
        #     '/api/v1/user/',
        #     data=json.dumps(data),
        #     headers={'Authorization': 'Bearer ' + token},
        #     content_type='application/json'
        # )
        # res_json = json.loads(res.data)
        # app.logger.info('ADD NEW USER', {'result': res_json})
        # assert res.status_code == 200
        # user_id = res_json['data']['id']