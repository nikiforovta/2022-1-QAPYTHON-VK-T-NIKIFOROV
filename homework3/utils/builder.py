from dataclasses import dataclass

import faker

fake = faker.Faker()


class Builder:

    @staticmethod
    def segment(name=None):
        @dataclass
        class Segment:
            name: str = ''
            id: int = 0

        if name is None:
            name = fake.lexify(text='??? ?????')

        return Segment(name=name)

    @staticmethod
    def campaign(name=None, title=None, description=None):
        @dataclass
        class Campaign:
            name: str = ''
            title: str = ''
            description: str = ''
            id: int = 0

        if name is None:
            name = fake.lexify(text='???? ??? ??? ?')
        if title is None:
            title = fake.lexify(text='????? ???')
        if description is None:
            description = fake.lexify(text='??? ?????')

        return Campaign(name=name, title=title, description=description)
