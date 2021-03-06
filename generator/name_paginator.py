# -*- coding: utf-8 -*-
#    Copyright (C) 2014 The Songbook Team
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# adapted from https://djangosnippets.org/snippets/2732/
import string
from django.core.paginator import InvalidPage
from unidecode import unidecode


class NamePaginator(object):
    """Pagination for string-based objects"""

    def __init__(self, queryset, paginate_by=25, **kwargs):
        # We ignore allow_empty_first_page and orphans, just here for compliance
        self.pages = []
        self.object_list = queryset
        self.count = len(self.object_list)

        # chunk up the objects so we don't need to iterate
        # over the whole list for each letter
        chunks = {}
        numbers = "0123456789"
        alphabet = string.ascii_uppercase

        # we sort them by the first model ordering key
        for obj in self.object_list:
            if queryset:
                obj_str = unicode(getattr(obj, obj._meta.ordering[0]))
            else:
                obj_str = unicode(obj)

            try:
                letter = unicode.upper(obj_str[0])
            except:
                # If obj_str is empty, just ignore it.
                continue
            letter = unidecode(letter)

            if letter in numbers:
                letter = "0"
            elif letter not in alphabet:
                letter = "#"

            if letter not in chunks:
                chunks[letter] = []

            chunks[letter].append(obj)

        # the process for assigning objects to each page
        current_page = NamePage(self)

        for letter in alphabet + "#0":
            if letter not in chunks:
                if letter in alphabet:
                    current_page.add([], letter)
                continue

            # the items in object_list starting with this letter
            sub_list = chunks[letter]

            new_page_count = len(sub_list) + current_page.count
            # first, check to see if sub_list will fit or it needs
            # to go onto a new page. If assigning this list will
            # cause the page to overflow... and an underflow is closer
            # to per_page than an overflow... and the page isn't empty
            # (which means len(sub_list) > per_page)...
            if (new_page_count > paginate_by and \
                    abs(paginate_by - current_page.count) < abs(paginate_by - new_page_count) and \
                    current_page.count > 0) or \
                    letter == "#" or \
                    letter == "0":
                # make a new page
                self.pages.append(current_page)
                current_page = NamePage(self)

            current_page.add(sub_list, letter)
            if letter == "0":
                current_page.add([], "9")
                self.pages.append(current_page)
                current_page = NamePage(self)

        # if we finished the for loop with a page that isn't empty, add it
        if current_page.count > 0:
            self.pages.append(current_page)

    def page(self, num):
        """Returns a Page object for the given 1-based page number."""
        if len(self.pages) == 0:
            return None
        elif num > 0 and num <= len(self.pages):
            return self.pages[num - 1]
        else:
            raise InvalidPage

    @property
    def num_pages(self):
        """Returns the total number of pages"""
        return len(self.pages)


class NamePage(object):
    def __init__(self, paginator):
        self.paginator = paginator
        self.object_list = []
        self.letters = []

    @property
    def count(self):
        return len(self.object_list)

    @property
    def start_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[0]
        else:
            return None

    @property
    def end_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[-1]
        else:
            return None

    @property
    def number(self):
        return self.paginator.pages.index(self) + 1

    # just added the methods I needed to use in the templates
    # feel free to add the ones you need too
    def has_other_pages(self):
        return len(self.object_list) > 0

    def has_previous(self):
        return self.paginator.pages.index(self)

    def has_next(self):
        return self.paginator.pages.index(self) + 2

    def next_page_number(self):
        return self.paginator.pages.index(self) + 2

    def previous_page_number(self):
        return self.paginator.pages.index(self)

    def add(self, new_list, letter=None):
        if len(new_list) > 0:
            self.object_list = self.object_list + new_list
        if letter:
            self.letters.append(letter)

    def __repr__(self):
        if self.start_letter == self.end_letter:
            return self.start_letter
        else:
            return '%c-%c' % (self.start_letter, self.end_letter)
