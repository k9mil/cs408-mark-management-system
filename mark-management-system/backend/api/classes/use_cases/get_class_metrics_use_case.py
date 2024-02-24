from statistics import mean, stdev

from typing import Tuple

from api.system.schemas.schemas import MarksMetrics
from api.system.schemas.schemas import ClassBaseMetric

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetClassMetricsUseCase:
    """
    The Use Case containing business logic for retrieving class data & calculating
    metrics from them.
    """
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository) -> None:
        self.mark_repository = mark_repository
        self.user_repository = user_repository
    
    def execute(self, current_user: Tuple[str, bool, bool]) -> MarksMetrics:
        """
        Executes the Use Case to calculate metrics of all classes in the system.

        Args:
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            MarkNotFound: If no marks are found in the system.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            MarksMetrics: A MarksMetrics schema object containing metrics about the classes, i.e. lowest, most and most consistently performing.
        """
        user_email, _, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        marks = self.mark_repository.get_all_student_marks()

        if marks is None:
            raise MarkNotFound("No marks found")

        if marks:
            classes = {}

            for code, name, credit, credit_level, mark in marks:
                if code not in classes:
                    class_base = ClassBaseMetric(
                        name=name,
                        code=code,
                        credit=credit,
                        credit_level=credit_level,
                        mean=-1,
                        stdev=-1,
                    )

                    classes[code] = {"class_base": class_base, "marks": [mark]}
                else:
                    classes[code]["marks"].append(mark)

            for code, data in classes.items():
                class_base = data["class_base"]
                class_base.mean = round(mean(data["marks"]))
                class_base.stdev = round(stdev(data["marks"]))

            sorted_classes_by_mean = sorted(classes.items(), key=lambda class_: class_[1]["class_base"].mean)

            lowest_performing_classes_sorted_list = [data[1]["class_base"] for data in sorted_classes_by_mean[:3]]
            highest_performing_classes_sorted_list = [data[1]["class_base"] for data in sorted_classes_by_mean[-3:]]

            sorted_classes_by_stdev = sorted(classes.items(), key=lambda class_: class_[1]["class_base"].stdev)
            most_consistent_classes_sorted_list = [data[1]["class_base"] for data in sorted_classes_by_stdev[-3:]]


            marks_statistics = MarksMetrics(
                lowest_performing_classes=lowest_performing_classes_sorted_list,
                highest_performing_classes=highest_performing_classes_sorted_list,
                most_consistent_classes=most_consistent_classes_sorted_list,
            )

        return marks_statistics
