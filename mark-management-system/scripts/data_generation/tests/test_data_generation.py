import unittest
import csv
import os
import sys

from typing import List, Dict
from datetime import datetime

sys.path.append("../")

from data_generation import DataGenerator, CSVWriter


class TestDataGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.SAMPLE_CLASS_CODE: str = "CS408"
        self.SAMPLE_NUM_STUDENTS: int = 5

    def test_given_a_valid_class_code_and_num_students_when_generating_data_then_data_is_generated(self) -> None:
        data_generator = DataGenerator()
        data_generator.generate_data(
            self.SAMPLE_CLASS_CODE, self.SAMPLE_NUM_STUDENTS
        )

        self.assertEqual(len(data_generator.data), self.SAMPLE_NUM_STUDENTS)

    def test_given_no_parameters_when_generating_data_then_a_type_error_is_thrown(self) -> None:
        data_generator = DataGenerator()

        with self.assertRaises(TypeError):
            data_generator.generate_data()

class TestCSVWriter(unittest.TestCase):
    def setUp(self) -> None:
        self.SAMPLE_DATA: List[Dict[str, str]] = [
            {
                "CLASS_CODE": "CS408",
                "REG_NO": "qir4079",
                "MARK": "62",
                "STUDENT": "Christopher Rocha",
                "DEGREE_LEVEL": "BSc",
                "DEGREE": "Computer Science",
                "UNIQUE_CODE": "CS2020GX"
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

        self.assertTrue(file_name.startswith("mms_data_"))
        self.assertTrue(file_name.endswith(".csv"))

        last_underscore_index = file_name.rfind("_")
        first_dot_index = file_name.find(".")

        timestamp_from_file_name = file_name[(last_underscore_index + 1):first_dot_index]

        assert datetime.strptime(timestamp_from_file_name, EXPECTED_FORMAT)


if __name__ == "__main__":
    unittest.main()
