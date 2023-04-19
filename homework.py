"""
Модуль фитнес-трекера, который обрабатывает данные
для трёх видов тренировок: бега, спортивной ходьбы
и плавания.
"""
from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке. Содержит метод"""
    training_type: str   # Тип тренировки
    duration: float      # Продолжительность тренировка в часах.
    distance: float      # Пройденная дистанция в км..
    speed: float         # Средняя скорость км. в час.
    calories: float      # Количество сожженных калорий за тренировку
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вывод сообщения о пройденой тренировке"""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """
    Базовый класс тренировки. Модуль рассчитывает длину дистанции,
    среднюю скорость, вычисляет количество сожженных каллорий. Так же
    модуль возвращает информационное сообщение о результатах
    пройденной тренировки.
    """
    LEN_STEP: float = 0.65         # Коэфицент расчета длины шага.
    M_IN_KM: int = 1000            # М. в км..
    MIN_IN_HOUR: int = 60          # М. в часе.

    def __init__(self,
                 action: int,      # Кол-во раз действий (шагов или гребков)
                 duration: float,  # Продолжительность тренировка в часах
                 weight: float,    # Вес спортсмена в кг.
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км. в ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий вычисляется в
        соответствии с типом тренировки"""
        raise NotImplementedError('Метод get_spent_calories не был '
                                  'переопределен в классе ',
                                  f'{self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """
    Тренировка: бег. Дочерний класс от Training. Модуль рассчитывает
    длину пройденной дистанции, среднюю скорость, вычисляет количество
    сожженных каллорий.
    """
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18      # Множитель средней скорости.
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79       # Коэфицент расхода калорий.

    def get_spent_calories(self) -> float:
        """Получить сожжённые калории."""
        spent_calories = ((
                          self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight
                          / self.M_IN_KM
                          * self.duration
                          * self.MIN_IN_HOUR
                          )
        return spent_calories


class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба. Дочерний класс от Training.
    Модуль рассчитывает длину пройденной дистанции, среднюю скорость,
    вычисляет количество сожженных каллорий.
    """

    COEF_KMH_MS: float = 0.278       # Константа скорости - м/c.
    WEIGHT_COEF1: float = 0.035      # Константа  множителя веса.
    WEIGHT_COEF2: float = 0.029      # 2я константа  множителя веса.
    M_TO_SM: int = 100               # Константа метры в сантиметры.

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить сожжённые калории."""
        si_av_speed: float = self.get_mean_speed() * self.COEF_KMH_MS
        si_height: float = self.height / self.M_TO_SM
        spent_calories = ((self.WEIGHT_COEF1 * self.weight
                           + (si_av_speed ** 2
                               / si_height) * self.WEIGHT_COEF2 * self.weight)
                          * self.duration * self.MIN_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """
    Тренировка: плавание. Дочерний класс от Training. Модуль рассчитывает
    длину пройденной дистанции, среднюю скорость, вычисляет количество
    сожженных каллорий.
    """
    LEN_STEP: float = 1.38        # Коэфицент расчета длины гребка пловца.
    SWIM_CONST1: float = 1.1      # Добавочный коэфицент скорости при плавании.
    SWIM_CONST2: int = 2          # Множитель скорости при плавании.

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость"""
        swim_av_speed = (self.length_pool
                         * self.count_pool
                         / self.M_IN_KM
                         / self.duration)
        return swim_av_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченых калорий"""
        swim_cal = ((self.get_mean_speed() + self.SWIM_CONST1)
                    * self.SWIM_CONST2
                    * self.weight
                    * self.duration)
        return swim_cal


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    """Словарь сопоставляющий коды тренировок с классами для их вызова."""
    workout_dict: Dict[str, Type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking}
    """Инвертируем проверку вхождения ключа в словарь"""
    if workout_type not in workout_dict:
        raise ValueError(f'Неизвестный тип тренировки: {workout_type}')
    return workout_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
