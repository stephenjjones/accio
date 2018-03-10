# https://gist.github.com/svrist/73e2d6175104f7ab4d201280acba049c
import sys
import os
import json

from clint.arguments import Args
from clint.textui import prompt, puts, colored, validators

from commands import start_ec2, stop_ec2, ssh_login, ssh_launch, validate_stack_exists, create_stack, choose_stack, update_stack, delete_stack, upload_keys, attach_volume, list_all_ec2, create_ecr_registry

def main():
    args = Args()

    puts(colored.yellow('Aruments passed in: ') + str(args.all))
    puts(colored.yellow('Flags detected: ') + str(args.flags))

    arg_cmd = args.get(0)
    puts(colored.cyan('Command: ') + str(arg_cmd))

    if arg_cmd == 'start':
        start_ec2()
    elif arg_cmd == 'stop':
        stop_ec2()
    elif arg_cmd == 'ssh':
        ssh_login()
    elif arg_cmd == 'launch':
        ssh_launch()
    elif arg_cmd == 'create-stack':
        arg1 = args.get(1)
        if arg1:
            stack_name = args.get(1)
            stack_exists = validate_stack_exists(stack_name)
        else:
            stack_name = prompt.query("What's the name of your stack?")
            stack_exists = validate_stack_exists(stack_name)

        if (stack_exists):
            puts(colored.red(f'Stack named {stack_name} already exists'))
        else:
            create_stack(stack_name)

    elif arg_cmd == 'update-stack':
        arg1 = args.get(1)
        if arg1:
            stack_name = args.get(1)
            stack_exists = validate_stack_exists(stack_name)
        else:
            stack_name = choose_stack()
            stack_exists = True

        if not stack_exists:
            puts(colored.red(f'Stack named {stack_name} does not exist'))
        else:
            update_stack(stack_name)

    elif arg_cmd == 'check-status':
        list_all_ec2()
    elif arg_cmd == 'create-ecr':
        # Should this be part of the stack?
        create_ecr_registry()
    elif arg_cmd == 'attach-volume':
        attach_volume()
    elif arg_cmd == 'choose-stack':
        choose_stack()
    elif arg_cmd == 'upload-keys':
        upload_keys()
    elif arg_cmd == 'delete-stack':
        arg1 = args.get(1)
        if arg1:
            stack_name = args.get(1)
            stack_exists = validate_stack_exists(stack_name)
        else:
            stack_name = choose_stack()
            stack_exists = True

        if stack_exists:
            delete_stack(stack_name)
        else:
            puts(colored.red(f'Stack {stack_name} does not exist'))

if __name__ == '__main__':
    main()
