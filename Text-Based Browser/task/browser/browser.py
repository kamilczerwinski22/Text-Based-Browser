import sys
import os


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
    """Function for croping website link"""
    return string[:len(string) - 1 - string[::-1].index('.')]

def check_input(string):
    """Function for checking input validity"""
    return string.count('.') == 0

def write_to_file(file_name, catalog_name, file_inside):
    """Function for writing content to file"""
    with open(catalog_name + '\\' + file_name, 'a+') as f:
        f.write(file_inside)


# MAIN LOOP
def main():

    # create folder
    try:
        os.mkdir(catalog_name)
    except FileExistsError:
        print("Directory ", catalog_name, " already exists")


    while True:
        user_input = input()
        if user_input == 'exit':
            exit()
        elif check_input(user_input):
            print(ERROR_TEXT)
        elif user_input == 'bloomberg.com':
            print(bloomberg_com)
            write_to_file(crop_after_last_dot('bloomberg.com'), catalog_name, bloomberg_com)
        elif user_input == 'nytimes.com':
            print(nytimes_com)
            write_to_file(crop_after_last_dot('nytimes.com'), catalog_name, nytimes_com)
        else:
            print(ERROR_TEXT)

main()
prio

