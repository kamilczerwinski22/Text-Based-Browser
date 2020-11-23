import sys
import os
from collections import deque

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

catalog_name = sys.argv[1]
ERROR_TEXT = 'FFS, Error again!'


def crop_after_last_dot(string):
    """Function for croping website link from last dot. If string doesn't containg dot, return input string"""
    try:
        return string[:len(string) - 1 - string[::-1].index('.')]
    except ValueError:
        return string

def check_input(string):
    """Function for checking input validity"""
    return string.count('.') == 0

def write_to_file(file_name, catalog_name, file_inside):
    """Function for writing content to file"""
    with open(catalog_name + '\\' + file_name, 'a+') as f:
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
        user_input_without_last_dot = crop_after_last_dot(user_input)
        if user_input == 'exit':  # exit
            exit()

        elif user_input == 'back':  # back for getting to second last read argument, e.q. if first we read A and then B,
                                    # after typing 'back' we will see content of A again.
            try:
                # first pop arguments to read
                first_arg = stack.pop()
                second_arg = stack.pop()

                # read content of second to last argument
                with open(catalog_name + '\\' + second_arg, 'r+') as f:
                    for line in f.readlines():
                        print(line.strip())

                # get them back in
                stack.append(second_arg)
                stack.append(first_arg)

            except IndexError:
                pass

        elif check_input(user_input):  # check input validity
            print(ERROR_TEXT)

        elif os.path.isfile(catalog_name + '\\' + user_input_without_last_dot):  # second read of content
            stack.append(user_input_without_last_dot)
            with open(catalog_name + '\\' + user_input_without_last_dot, 'r+') as f:
                for line in f.readlines():
                    print(line.strip())

        elif user_input == 'bloomberg.com':  # first occurence of bloomberg
            print(bloomberg_com)
            write_to_file(crop_after_last_dot('bloomberg.com'), catalog_name, bloomberg_com)
            stack.append(crop_after_last_dot('bloomberg.com'))

        elif user_input == 'nytimes.com':  # first occurence of nytimes
            print(nytimes_com)
            write_to_file(crop_after_last_dot('nytimes.com'), catalog_name, nytimes_com)
            stack.append(crop_after_last_dot('nytimes.com'))

        else:  # error else
            print(ERROR_TEXT)

main()
