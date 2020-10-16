#!/usr/bin/python

import sys
import os
import concurrent.futures
import argparse
from text_search_task import TextSearchTask


def main():
    """Runs console program"""
    directory_path, text_to_search, file_extensions = _parse_console_input_arguments()
    search(directory_path, text_to_search, file_extensions)


def search(directory_path, text_to_search, file_extensions):
    """Main function to run the searching text with given file extensions
       inside given directory."""

    try:
        _validate_arguments(directory_path, text_to_search, file_extensions)
        file_extensions = [file_extension.lower() for file_extension in file_extensions]

        found_file_paths = _find_files_with_extensions_inside_directory(directory_path, file_extensions)
        if len(found_file_paths) == 0:
            print("No files found inside given directory with these extensions")
            return

        searching_results = _search_text_in_found_files(found_file_paths, text_to_search)
        if len(searching_results) == 0:
            print("Not found searching text in given directory and in files with given extensions")
            return
        else:
            _print_searching_results(searching_results)

    except (ValueError, IndexError) as e:
        print(f"There was an error during application running:\n{e!r}", file=sys.stderr)
        raise


def _find_files_with_extensions_inside_directory(directory_path, files_extensions):
    """Find files with given files extension inside directory."""

    filepaths = list()
    for root, _, files in os.walk(directory_path, topdown=False):
        for name in files:
            file_extension = name.split('.')[-1].lower()
            if file_extension in files_extensions:
                filepath = os.path.join(root, name)
                filepaths.append(filepath)
    return filepaths


def _search_text_in_found_files(found_file_paths, text_to_search):
    """Starts searching text in given files. Uses multi-threading for
       making search quicker"""

    searching_results = list()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for filepath in found_file_paths:
            future = executor.submit(_thread_function, args=(filepath, text_to_search))
            return_value = future.result()
            searching_results.append(return_value)
    return searching_results


def _print_searching_results(searching_results):
    """Print searching result in readable form"""

    searching_results.sort(key=_searching_key, reverse=True)  # reverse cause showing results
    # from max to min number of text occurences

    for searching_result in searching_results:
        text_to_show = f"Inside file {searching_result.filepath()} text occured {searching_result.occurences()}"
        if searching_result.occurences() == 1:
            print(f"{text_to_show} time")
        else:
            print(f"{text_to_show} times")


def _searching_key(searching_result):
    """Returns the value for sorting mechanism. Sort by number of text occurences"""
    return searching_result.occurences()


def _thread_function(args):
    """Searching function invoked for every separate thread"""

    filepath, text_to_search = args
    task = TextSearchTask(filepath, text_to_search)
    task.search()
    return task


def _validate_arguments(directory_path, text_to_search, file_extensions):
    """Validates input arguments"""

    if len(file_extensions) == 0:
        raise ValueError(f"Invalid number of input arguments."
                         "Please provide arguments <directory_to_search> <text_to_search> "
                         "<extensions_separated_by_space>"
                         "Example: text_searcher.py directory \"Text to be searched\" txt csv")

    if not os.path.isdir(directory_path):
        raise ValueError(f"Given directory path '{directory_path}' is not a directory")

    if not text_to_search:
        raise ValueError(f"Given text to be searched: '{text_to_search}' is blank")


def _parse_console_input_arguments():
    """Parse input arguments and return a tuple containing
       directory path, text to search and file extensions"""

    parser = argparse.ArgumentParser(description='List files in given directory containing text. '
                                                 'Program search in files with given extensions (ex. txt, csv)',
                                     fromfile_prefix_chars='@',
                                     epilog='Author: https://github.com/tomaszkyc - checkout my other projects :)')

    parser.add_argument('-d', '--directory', action='store',
                        help='Path to the directory where search will be performed',
                        metavar='"/path/to/directory"', type=str, required=True)
    parser.add_argument('-t', '--text', action='store', help='Text to be searched. It cold be a char, word or sentence',
                        metavar='"Text to be searched"', type=str, required=True)
    parser.add_argument('-e', '--extensions', action='store', help='List of extensions to be searched',
                        metavar="txt csv", nargs='+', required=True)

    args = parser.parse_args()
    return args.directory, args.text, args.extensions


if __name__ == '__main__':
    main()
