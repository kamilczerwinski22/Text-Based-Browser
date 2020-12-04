import sys
import os
from collections import deque
import requests

catalog_name = sys.argv[1]
ERROR_TEXT = 'FFS, Error again!'


def crop_after_last_dot(string: str) -> str:
    """Function for croping website link from last dot. If string doesn't containg dot, return input string"""
    try:
        return string[:len(string) - 1 - string[::-1].index('.')]
    except ValueError:
        return string

def check_input(string: str) -> bool:
    """Function for checking input validity"""
    return string.count('.') == 0

def write_to_file(file_name: str, catalog_name: str, file_inside: str):
    """Function for writing content to file"""
    with open(os.path.join(catalog_name, file_name), 'a+', encoding='UTF-8') as f:
        f.write(file_inside)


# MAIN LOOP
def main():

    #create stack
    stack = deque()

    # create folder
    try:
        os.mkdir(catalog_name)
    except FileExistsError:
        print("Directory ", catalog_name, " already exists")


    while True:
        user_input = input()
        user_input_cropped = crop_after_last_dot(user_input.replace('https://', '')
                                                           .replace('http://', '')
                                                           .replace('www.', ''))
        user_input_request = user_input if user_input.startswith('https://') else ('https://' + user_input)

        print('file', os.path.join(catalog_name, user_input_cropped))
        print('file if true', os.path.isfile(os.path.join(catalog_name, user_input_cropped)))
        if user_input == 'exit':  # exit
            exit()

        elif user_input == 'back':  # back for getting to second last read argument, e.q. if first we read A and then B,
                                    # after typing 'back' we will see content of A again.
            try:
                # first pop arguments to read
                first_arg = stack.pop()
                second_arg = stack.pop()

                # read content of second to last argument
                with open(os.path.join(catalog_name, second_arg), 'r+') as f:
                    for line in f.readlines():
                        print(line.strip())

                # get them back in
                stack.append(second_arg)
                stack.append(first_arg)

            except IndexError:
                pass

        elif check_input(user_input):  # check input validity
            print(ERROR_TEXT)

        elif os.path.isfile(os.path.join(catalog_name, user_input_cropped)):  # second read of content
            stack.append(user_input_cropped)
            with open(os.path.join(catalog_name, user_input_cropped), 'r+', encoding='UTF-8') as f:
                for line in f.readlines():
                    print(line.strip())

        else:
            request = requests.get(user_input_request)
            print(request.text)
            write_to_file(file_name=user_input_cropped,
                          catalog_name=catalog_name,
                          file_inside=request.text)
            stack.append(user_input_cropped)


        # elif user_input == 'bloomberg.com':  # first occurence of bloomberg
        #     print(bloomberg_com)
        #     write_to_file(crop_after_last_dot('bloomberg.com'),
        #                   catalog_name,
        #                   bloomberg_com)
        #     stack.append(crop_after_last_dot('bloomberg.com'))
        #
        # elif user_input == 'nytimes.com':  # first occurence of nytimes
        #     print(nytimes_com)
        #     write_to_file(crop_after_last_dot('nytimes.com'),
        #                   catalog_name,
        #                   nytimes_com)
        #     stack.append(crop_after_last_dot('nytimes.com'))
        #
        # else:  # error else
        #     print(ERROR_TEXT)

main()
