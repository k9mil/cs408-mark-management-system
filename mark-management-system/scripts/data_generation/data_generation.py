import typer
import csv

from faker import Faker

from typing import Dict, List, Final
from random import normalvariate
from datetime import datetime
from typing_extensions import Annotated


faker = Faker()

MU: Final[int] = 65
SIGMA: Final[int] = 10
DP: Final[int] = 0


class DataGenerator:
    """This class is responsible for generating the sample data.

    Attributes:
        data: The list containing the data.
    """
    def __init__(self):
        self.LOWER_MARK_BOUND = 0
        self.UPPER_MARK_BOUND = 100
        self.data: List = []

    def generate_data(self, class_code: str, num_students: int) -> None:
        """Generate the data given a class code & numbers of students for that class.

        Args:
            class_code: A string representing the class code.
            num_students: An integer representing the amount of students taking the class.
        """

        for _ in range(num_students):
            generated_mark = int(round(normalvariate(MU, SIGMA), DP))

            self.data.append(
                {
                    "CLASS_CODE": class_code,
                    "REG_NO": f"{faker.random_lowercase_letter()}{faker.random_lowercase_letter()}{faker.random_lowercase_letter()}{faker.random_number(5)}",
                    "MARK": str(generated_mark) if self.LOWER_MARK_BOUND <= generated_mark <= self.UPPER_MARK_BOUND else "100",
                    "STUDENT_NAME": faker.first_name() + " " + faker.last_name(),
                    "DEGREE_LEVEL": "BSc",
                    "DEGREE_NAME": "Computer Science",
                }
            )

class CSVWriter:
    def write_to_csv(self, data: List[Dict[str, str]], file_name: str) -> None:
        """Writes the data generated by `DataGenerator` into a CSV file.

        Args:
            data: A list containing all of the generated data.
            file_name: The file name to be written to (or created and then written to).
        """

        keys = data[0].keys()

        with open(file_name, "w", newline="") as file:
            dict_writer = csv.DictWriter(file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
    
    @staticmethod
    def generate_filename() -> str:
        """Generate a filename of format: mms_data_<timestamp>

        Returns:
            The filename to be used for the CSV file.
        """

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"mms_data_{timestamp}.csv"


def main(class_code: Annotated[str, typer.Argument()] = "CS408", num_students: Annotated[int, typer.Argument()] = 100) -> None:
    data_generator = DataGenerator()
    data_generator.generate_data(class_code, num_students)

    csv_writer = CSVWriter()
    file_name = csv_writer.generate_filename()
    csv_writer.write_to_csv(data_generator.data, file_name)


if __name__ == "__main__":
    typer.run(main)
