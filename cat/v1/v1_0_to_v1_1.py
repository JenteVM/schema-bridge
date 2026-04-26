from types import SimpleNamespace

REG = True
USER = False

def translate(reg_db_obj):
    translated_reg_db_obj = []
    for entry in reg_db_obj:
        translated_entry = SimpleNamespace(
            db_id=entry.db_id,
            db_secret=entry.db_secret,
            app_name=entry.app_name,
            allowed_origins=entry.allowed_origins,
            temp_allowed_origin=None,
            validation_token=entry.AO_addition_token,
            validation_token_expiration=None,
            user_auth_scheme=entry.user_auth_scheme,
            authorized=entry.authorized
        )
        translated_reg_db_obj.append(translated_entry)
    return translated_reg_db_obj