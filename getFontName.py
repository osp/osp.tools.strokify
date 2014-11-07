#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import fontforge


def main():
    FILE_NAME = sys.argv[1]
    font = fontforge.open(FILE_NAME)
    print font.fontname


if __name__ == "__main__":
        main()
