#!/usr/bin/env python3
# line above is called shebang (#!)
# if you have this, and you do the following:
# chmod +x journal.py (to make the file executable)
# then you run the program as follows: ./journal.py


from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('journal.db')


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)  # default calls the function so you dont need parentheses after now

    class Meta:
        database = db


def initialize():
    """Create database and tables if they don't exist yet"""
    db.connect()

    # safe=True checks if db and tables already exist,
    # so don't need to do anything then.
    db.create_tables([Entry], safe=True)


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Here's my journal creator. Add, view, delete journal entries.")
        print('Press q to quit\n')

        for menu_option, function_to_call in menu.items():
            print(f'{menu_option}) {function_to_call.__doc__}')

        choice = input('Choice one of the options above:\n').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


# This is handy to clear the screen, so it's easier to read the screen
# Just call os.system('clear')
# 'clear' is the command you would like to run
def clear():
    """Clear the screen"""
    os.system('clear')


def add_entry():
    """Add an entry"""
    clear()
    print('Type your entry and at the end do CTRL+D to end your entry:')

    data = sys.stdin.read().strip()

    if data:
        if input('\nDo you want to save this? Type y or n\n').lower() == 'y':
            Entry.create(content=data)
            print('\nSaved successfully!\n')
        else:
            print('\nInput not saved!\n')
    else:
        print('\nNo input received!\n')


def view_entries(search_query=None):
    """View all journal entries"""
    clear()
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        clear()
        print(entry.timestamp, '\n', entry.content, '\n')

        next_action = input(
                '\nShow next entry or delete entry? Press Y,d(elete) or q for quit\n'
            ).lower().strip()

        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entry():
    """Search for an entry"""
    clear()
    search_query = input('\nType the word you would like to search for\n')
    view_entries(search_query)


def delete_entry(entry):
    """Delete an entry"""
    if input('Are you sure? [yN]').lower().strip() == 'y':
        entry.delete_instance()
        print('Entry deleted, bye bye!')


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entry),
])


if __name__ == '__main__':
    initialize()
    menu_loop()
