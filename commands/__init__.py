"""Add cmd decorator here for parsing command parameters"""

from config import BOT_PREFIX, TEXT_LANGUAGE
import utils

command_info = utils.common.read_json_file("json/command_info.json")


def get_all_commands():
    return [*command_info.keys()]


def get_command_description(command):
    if command in command_info:
        return command_info[command]["description"][TEXT_LANGUAGE]

    return None


def get_command_exclusive_roles(command):
    if command in command_info:
        return command_info[command]["exclusive_roles"]

    return None


def get_command_required_params(command):
    if command in command_info:
        return command_info[command]["required_params"]

    return []


def get_command_additional_params(command):
    if command in command_info:
        return command_info[command].get("additional_params", [])

    return []


def get_command_usages(command, **kwargs):
    if command in ("fjoin", "fleave"):
        return [f"`{BOT_PREFIX}{command} @user1 @user2 ...`"]

    if command in command_info:
        required_params = get_command_required_params(command)
        additional_params = get_command_additional_params(command)

        command_args_list = []
        command_args = []
        command_args_2 = []

        for param in required_params:
            argv = str(kwargs.get(param, param))
            if argv:
                command_args.append(argv)
                command_args_2.append(f"@user{param[9:]}" if param.startswith("player_id") else argv)

        for param in additional_params:
            argv = str(kwargs.get(param, "[" + param + "]"))
            if argv:
                command_args.append(argv)
                command_args_2.append(f"@user{param[9:]}" if param.startswith("player_id") else argv)

        command_args_list.append(command_args)
        if command_args != command_args_2:
            command_args_list.append(command_args_2)

        # print(command, required_params, additional_params, kwargs, "->", *command_args_list)

        return [
            f"`{BOT_PREFIX}{command} {' '.join(command_args)}`"
            for command_args in command_args_list
        ]

    return []
