from os import listdir
from os.path import join
from random import choice

import requests

from settings import IMAGES_DIR
from settings.urls import get_url


class Company:
    objects = {}

    def __init__(self, pk, name, cameras=None):
        self.name = name
        self.pk = pk
        self.cameras = cameras
        Company.objects[self.pk] = self

    def __repr__(self):
        return f'{self.pk}: {self.name}'


class Companies:
    active_company = None

    @staticmethod
    def all():
        companies = requests.get(get_url('companies')).json()
        for company in companies:
            Company(company['pk'], company['name'])
        return Company.objects

    @staticmethod
    def select(pk):
        return Company.objects[int(pk)]

    @staticmethod
    def config_camera():
        choices = {str(pos): el for pos, el in enumerate(Companies.all().values())}
        print('Select company to emulate camera working')
        for pos, camera in choices.items():
            print(pos, ':', camera.name)

        choice = input('Which company to emulate? > ')
        while choice not in choices.keys():
            choice = input('Company is not found. Which company to emulate? > ')

        Companies.active_company = choices[choice]

    @staticmethod
    def get_cameras():
        cameras = requests.get(get_url('cameras')).json()
        for company, cams in cameras.items():
            Companies.select(company).cameras = cams

    @staticmethod
    def get_random_camera():
        return choice(Companies.active_company.cameras)

    @staticmethod
    def get_random_photo():
        file_name = choice(listdir(IMAGES_DIR))
        return join(IMAGES_DIR, file_name)

    @staticmethod
    def move():
        Companies.get_cameras()
        photo = Companies.get_random_photo()
        camera = Companies.get_random_camera()
        files = {'photo': open(photo, 'rb')}
        return requests.post(get_url('move'), files=files, data={'camera': camera})


if __name__ == '__main__':
    Companies.config_camera()
    while True:
        try:
            print(Companies.move())
        except (KeyboardInterrupt, SystemExit):
            break
