"""tberg's newbie-ish functions, all in one place"""


def sort_list_of_dictionaries(unsorted_list, key_to_sort_by, reverse=False) -> list:
    return sorted(unsorted_list, key=lambda k: k[key_to_sort_by], reverse=reverse)
