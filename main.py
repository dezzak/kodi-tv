#!/usr/bin/env python3

import Database
import fixers

db = Database.db()


def fix():
    shows = db.get_shows(9)
    for show in shows:
        fixers.fix_show(show)


if __name__ == '__main__':
    fix()
