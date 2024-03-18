import unittest
import csv
import os
import sys

from typing import List, Dict
from datetime import datetime

sys.path.append("../")

from mark_generator import MarkGenerator, CSVWriter, PSQLInsertGenerator


class TestMarkGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.SAMPLE_CLASS_CODE: str = "CS408"
        self.SAMPLE_NUM_STUDENTS: int = 5

    def test_given_a_valid_class_code_and_num_students_when_generating_data_then_data_is_generated(self) -> None:
        mark_generator = MarkGenerator()
        mark_generator.generate_data(
            self.SAMPLE_CLASS_CODE, self.SAMPLE_NUM_STUDENTS
        )

        self.assertEqual(len(mark_generator.data), self.SAMPLE_NUM_STUDENTS)

    def test_given_no_parameters_when_generating_data_then_a_type_error_is_thrown(self) -> None:
        mark_generator = MarkGenerator()

        with self.assertRaises(TypeError):
            mark_generator.generate_data()

class TestCSVWriter(unittest.TestCase):
    def setUp(self) -> None:
        self.SAMPLE_DATA: List[Dict[str, str]] = [
            {
                "CLASS_CODE": "CS408",
                "REG_NO": "qir4079",
                "MARK": "62",
                "STUDENT_NAME": "Christopher Rocha",
                "DEGREE_LEVEL": "BSc",
                "DEGREE_NAME": "Computer Science",
                "MARK": "71",
                "MARK_CODE": "PM"
            },
        ]

        self.SAMPLE_FILE_NAME = "TEST_CSV_WRITER_FILE.csv"
        self.csv_writer = CSVWriter()

    def tearDown(self) -> None:
        if os.path.exists(self.SAMPLE_FILE_NAME):
            os.remove(self.SAMPLE_FILE_NAME)

    def test_given_a_valid_data_list_when_writing_to_csv_then_data_is_written_to_a_file_correctly(self) -> None:
        self.csv_writer.write_to_csv(self.SAMPLE_DATA, self.SAMPLE_FILE_NAME)

        with open(self.SAMPLE_FILE_NAME, "r") as file:
            dict_reader = csv.DictReader(file)
            DICT_READER_VALUES = [row for row in dict_reader]

        self.assertEqual(self.SAMPLE_DATA, DICT_READER_VALUES)

    def test_given_no_parameters_when_writing_to_csv_then_a_type_error_is_thrown(self) -> None:
        with self.assertRaises(TypeError):
            self.csv_writer.write_to_csv()

    def test_when_generating_a_filename_then_a_filename_is_correctly_generated(self) -> None:
        EXPECTED_FORMAT: str = "%Y%m%d%H%M%S"

        file_name = self.csv_writer.generate_filename()

        self.assertTrue(file_name.startswith("mms_marks_"))
        self.assertTrue(file_name.endswith(".csv"))

        last_underscore_index = file_name.rfind("_")
        first_dot_index = file_name.find(".")

        timestamp_from_file_name = file_name[(last_underscore_index + 1):first_dot_index]

        assert datetime.strptime(timestamp_from_file_name, EXPECTED_FORMAT)

class TestPSQLInsertGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.SAMPLE_DATA: List[Dict[str, str]] = [
            {
                "CLASS_CODE": "CS408",
                "REG_NO": "qir4079",
                "MARK": "62",
                "STUDENT_NAME": "Christopher Rocha",
                "DEGREE_LEVEL": "BSc",
                "DEGREE_NAME": "Computer Science",
                "MARK": "71",
                "MARK_CODE": "PM"
            },
        ]

        self.psql_insert_generator = PSQLInsertGenerator()
    
    def test_given_a_valid_data_list_when_generating_insert_statements_then_inserts_are_generated_correctly(self) -> None:
        insert_statements = self.psql_insert_generator.generate_insert_statements(self.SAMPLE_DATA)

        self.assertIn(self.SAMPLE_DATA[0]["REG_NO"], insert_statements)
        self.assertIn(self.SAMPLE_DATA[0]["STUDENT_NAME"], insert_statements)

    def test_given_no_params_when_calling_generate_insert_statements_then_an_error_is_thrown(self) -> None:
        with self.assertRaises(TypeError):
            self.psql_insert_generator.generate_insert_statements()
    

if __name__ == "__main__":
    unittest.main()
