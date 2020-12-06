import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from requests import Response
from colorama import Fore, Style, init as colorama_init

catalog_name = sys.argv[1]
ERROR_TEXT = 'FFS, Error again!'

colorama_init(autoreset=True)

def crop_after_last_dot(string: str) -> str:
    """Function for croping website link from last dot. If string doesn't containg dot, return input string"""
    try:
        return string[:len(string) - 1 - string[::-1].index('.')]
    except ValueError:
        return string

def check_input(string: str) -> bool:
    """Function for checking input validity"""
    return string.count('.') == 0

def write_to_file(file_name: str, catalog_name: str, file_inside: Response):
    """Function for writing content to file"""
    with open(os.path.join(catalog_name, file_name), 'a+', encoding='UTF-8') as f:
        soup = BeautifulSoup(file_inside.content, 'html.parser')
        results = soup.find_all(['p', 'a', 'ul', 'ol', 'li'])
        for tag in results:
            if tag.name == 'a':
                f.write(Fore.BLUE + tag.text)
            else:
                f.write(tag.text)

def pretty_print(catalog_name, file_name):
    """Function for printing file."""
    with open(os.path.join(catalog_name, file_name), 'r+', encoding='UTF-8') as f:
        for line in f.readlines():
            print(line.strip())




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

        if user_input == 'exit':  # exit
            exit()

        elif user_input == 'back':  # back for getting to second last read argument, e.q. if first we read A and then B,
                                    # after typing 'back' we will see content of A again.
            try:
                # first pop arguments to read
                first_arg = stack.pop()
                second_arg = stack.pop()

                # read content of second to last argument
                pretty_print(catalog_name, second_arg)

                # get them back in
                stack.append(second_arg)
                stack.append(first_arg)

            except IndexError:
                pass

        elif check_input(user_input):  # check input validity
            print(ERROR_TEXT)

        elif os.path.isfile(os.path.join(catalog_name, user_input_cropped)):  # second read of content
            stack.append(user_input_cropped)
            pretty_print(catalog_name=catalog_name,
                         file_name=user_input_cropped)

        else:
            request = requests.get(user_input_request)
            write_to_file(file_name=user_input_cropped,
                          catalog_name=catalog_name,
                          file_inside=request)
            pretty_print(catalog_name=catalog_name,
                         file_name=user_input_cropped)

            stack.append(user_input_cropped)

if __name__ == '__main__':
    main()
