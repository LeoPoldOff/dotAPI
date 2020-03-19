from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Account:
    number: uuid4
    fio: str
    balance: int
    holds: int
    status: int

    def add(self, addition):
        if isinstance(addition, int) and addition >= 0 and self.status:
            self.balance += addition
        else:
            raise Exception('You can`t make this operation...')

    def substract(self, substraction):
        result = self.balance - self.holds - substraction
        if result < 0 or not self.status or not isinstance(substraction, int) \
                or substraction <= 0:
            raise Exception('You can`t make this operation...')
        else:
            self.holds += substraction

    def refresh_holds(self):
        self.balance -= self.holds
        self.holds = 0
