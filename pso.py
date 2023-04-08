import random
from copy import deepcopy
import numpy as np


# Функция, которую мы будем минимизировать
def fitness_function(x, y):
    return x ** 2 + 3 * y ** 2 + 2 * x * y


# Другое представление функции
def ff(x):
    return fitness_function(x[0], x[1])


# Копия исходной функции и метод сброса,
# (для возврата к исходной функции после использования кастомной)
backup = deepcopy(fitness_function)


def reset_ff():
    # noinspection PyGlobalUndefined
    global fitness_function
    fitness_function = deepcopy(backup)


# Хранение, сброс и изменения границ
ranges = {'x1': -10, 'x2': 10, 'y1': -10, 'y2': 10}


def reset_ranges():
    ranges['x1'] = -10
    ranges['y1'] = -10
    ranges['x2'] = 10
    ranges['y2'] = 10


def set_ranges(x1, x2, y1, y2):
    ranges['x1'] = x1
    ranges['x2'] = x2
    ranges['y1'] = y1
    ranges['y2'] = y2


args = {'num_of_particles': 100, 'omega': 0.5, 'phi_p': 1, 'phi_g': 1}


# Класс частицы
class Particle:
    def __init__(self):
        self.pos = np.array([random.uniform(ranges['x1'], ranges['x2']), random.uniform(ranges['y1'], ranges['y2'])])
        self.velocity = np.array([random.uniform(-(ranges['x2'] - ranges['x1']), (ranges['x2'] - ranges['x1'])),
                                  random.uniform(-(ranges['y2'] - ranges['y1']), (ranges['y2'] - ranges['y1']))])
        self.best_pos = deepcopy(self.pos)

    def update_velocity(self, swarm_best: np.ndarray):
        for i in range(2):
            r_p = random.random()
            r_g = random.random()
            self.velocity[i] = args['omega'] * self.velocity[i] + args['phi_p'] * r_p * (
                    self.best_pos[i] - self.pos[i]) + args['phi_g'] * r_g * (swarm_best[i] - self.pos[i])

    def update_pos(self):
        self.pos += self.velocity
        if ff(self.pos) < ff(self.best_pos):
            self.best_pos = deepcopy(self.pos)
            return self.best_pos
        else:
            return None


class PSO:
    def __init__(self):
        self.swarm = []
        self.iters = 0
        for _ in range(args['num_of_particles']):
            self.swarm.append(Particle())
        self.global_best = np.array(deepcopy(min(self.swarm, key=lambda x: ff(x.best_pos)).best_pos))
        print('iter:', self.iters, 'best:', self.global_best, 'min:', ff(self.global_best))


    def get_res(self):
        return ff(self.global_best), self.global_best, self.iters
    def pso(self, iterations):
        for _ in range(iterations):
            self.iters += 1
            for particle in self.swarm:
                particle.update_velocity(self.global_best)
                particle_best = particle.update_pos()
                if particle_best is not None and fitness_function(*particle_best) < fitness_function(*self.global_best):
                    self.global_best = deepcopy(particle_best)
            print('iter:', self.iters, 'best:', self.global_best, 'min:', ff(self.global_best))

    def reset(self):
        self.__init__()


def set_args(num_of_particles, omega, phi_p, phi_g):
    if num_of_particles > 1:
        args['num_of_particles'] = num_of_particles
    else:
        raise ValueError('Введите корректное количество частиц')
    if 0 <= omega <= 2:
        args['omega'] = omega
    else:
        raise ValueError('Введите корректный инерционный коэффициент')
    if 0 <= phi_p <= 2:
        args['phi_p'] = phi_p
    else:
        raise ValueError('Введите корректный коэффициент когнитивной компоненты')
    if 0 <= phi_g <= 2:
        args['phi_g'] = phi_g
    else:
        raise ValueError('Введите корректный коэффициент социальной компоненты')