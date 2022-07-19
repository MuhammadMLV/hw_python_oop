from dataclasses import dataclass, asdict
from typing import Type, Dict, Tuple, Sequence


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info_message: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.info_message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60
    const_run_1: int = 18
    const_run_2: int = 20
    const_walk_1: float = 0.035
    const_walk_2: float = 0.029
    const_swim: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()

        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__str__()
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        duration: float = self.duration

        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    def __str__(self):
        return 'Running'

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()

        return (self.const_run_1 * mean_speed - self.const_run_2
                ) * self.weight / self.M_IN_KM * (
            self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def __str__(self):
        return 'SportsWalking'

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()

        return (self.const_walk_1 * self.weight + (
                mean_speed ** 2 // self.height) * self.const_walk_2
                * self.weight) * (self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def __str__(self):
        return 'Swimming'

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                ) / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()

        return (mean_speed + self.const_swim) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Sequence[Tuple[str, Sequence[float]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)