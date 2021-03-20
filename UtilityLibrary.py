import os
import pathlib
import shutil
import pandas as pd
import csv


def path_add_slashes(original_path):
    corrected_path = original_path.replace("/", "//")
    return corrected_path


def path_correct(original_path):
    corrected_path = r"{}"
    path_with_corrected_slash = str(pathlib.Path(original_path))
    corrected_path = corrected_path.format(path_with_corrected_slash)
    return corrected_path


def delete_file(file_path):
    result = "No file deleted"
    # Convert the "\\" for windows
    file_path = pathlib.Path(file_path)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            result = "file " + str(file_path) + " deleted"
    except OSError:
        result = "File not found or could not be deleted"
    return result


def find_file(directory, name_substring):
    dir_list = os.listdir(path=pathlib.Path(directory))
    file_name = "No file"
    complete_file_path = directory
    for file in dir_list:
        if name_substring in file:
            file_name = file
            complete_file_path += "//" + file_name
            break
    if file_name == "No file":
        raise Exception("No file found")
    return complete_file_path


def move_file(source_file_path, source_file_name, destination_file_complete_path):

    source_file_complete_path = find_file(source_file_path, source_file_name)

    # Convert the "\\" for windows
    source_file_complete_path = path_correct(source_file_complete_path)
    destination_file_complete_path = path_correct(destination_file_complete_path)

    result = "File " + source_file_path + " Could not be moved"

    if source_file_name == "No file":
        result = "file could not be found"
    else:
        try:
            shutil.move(source_file_complete_path, destination_file_complete_path)
        except OSError:
            print("Error moving the file " + source_file_complete_path)
        else:
            result = source_file_complete_path + " moved to " + destination_file_complete_path
    return result


def xls_to_csv(input_file, output_file):
    file = pd.read_excel(input_file)
    file.to_csv(output_file, index=None, header=True)


def complete_path(path, filename):
    complete_file_path = path + "//" + filename
    corrected_file_path = pathlib.Path(complete_file_path)
    return corrected_file_path


def create_directory(path):
    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the directory %s failed" % path)


def write_file(file_complete_path, content):
    file = open(file_complete_path, "w", encoding="UTF-8")
    file.write(content)
    file.close()


def load_file_content(file_complete_path, encoding="UTF-8"):
    # corrected_path = path_correct(file_complete_path)
    loaded_file = open(file_complete_path, 'r', encoding=encoding)
    file_content = loaded_file.read()
    loaded_file.close()
    return file_content


def import_csv_file(file_path, delimiter):
    # Functionality: Imports a CSV file, and delivers an iterable csv object, were each line is a dictionary.
    # with open(file_path) as imported_file:
    imported_file = open(file_path)
    csv_object = csv.DictReader(imported_file, delimiter=delimiter)
    return csv_object


class LogFile:
    def __init__(self, _log_file_path, _delete_previous_file=False):
        self.log_file_path = _log_file_path
        self.log_file = None

        if _delete_previous_file is True:
            os.remove(_log_file_path)

    def write(self, log_line):
        self.log_file = open(self.log_file_path, "a")
        log_line = log_line + "\n"
        print(log_line)
        self.log_file.write(log_line)
        self.log_file.close()


letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
           "P", "Q", "R", "R", "S", "T", "U", "V", "W", "X", "X", "Z"]


def letter_to_number(_letter):

    letter = str(_letter)
    number = 0

    try:
        number = letters.index(letter)
    except ValueError:
        print("Letter is lower case")
        upper_case_letter = letter.capitalize()
        number = letters.index(upper_case_letter)

    return number
