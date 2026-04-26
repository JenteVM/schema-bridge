from importlib import import_module
from testing_files.file_reader import load_instance_for_test

def create_version_step_list(start:float, end:float):
    start_major, start_minor = str(start).split(".")
    end_major, end_minor = str(end).split(".")
    start_major, start_minor, end_major, end_minor = int(start_major), int(start_minor), int(end_major), int(end_minor)
    if start_major != end_major:
        raise ValueError("Start and end major versions must be the same.")
    if start_minor >= end_minor:
        raise ValueError("Start minor version must be less than end minor version.")
    version_steps = {}
    steps = end_minor - start_minor
    for step in range(steps):
        version_steps[f"{start_major}.{start_minor + step}"] = f"{start_major}.{start_minor + step + 1}"
    return version_steps, start_major

def translator(reg_db_obj, user_db_obj_list, current_version, target_version):
    version_steps, major = create_version_step_list(current_version, target_version)
    for step in version_steps:
        translator = import_module(f"cat.v{major}.v{step.replace('.', '_')}_to_v{version_steps[step].replace('.', '_')}")
        if translator.REG:
            if reg_db_obj is None:
                raise ValueError("reg_db_obj cannot be None when translator.REG is True.")
            reg_db_obj = translator.translate(reg_db_obj=reg_db_obj)[0]
        if translator.USER:
            if user_db_obj_list is None:
                raise ValueError("user_db_obj_list cannot be None when translator.USER is True.")
            translated_user_db_obj_list = []
            for user_db_obj in user_db_obj_list:
                user_db_obj = translator.translate(user_db_obj=user_db_obj)[0]
                translated_user_db_obj_list.append(user_db_obj)
            user_db_obj_list = translated_user_db_obj_list
    return reg_db_obj, user_db_obj_list