DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': "/password/reset/confirm/{uid}/{token}",
    'USERNAME_CONFIRM_URL': "/username/reset/confirm/{uid}/{token}",
    'ACTIVATION_URL': "user/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {},
    'LOGIN_FIELD': 'email',
    "USER_CREATE_PASSWORD_RETYPE": False,
    "CREATE_SESSION_ON_LOGIN": True,
}
