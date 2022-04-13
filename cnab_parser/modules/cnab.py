from datetime import datetime

from cnab_parser.models.transaction import TransactionModel


class CNAB:
    def __init__(self, content: str) -> None:
        self.content_lines = content.strip().split('\n')

    def parser(self):
        self.transactions = list()
        for transaction in self.content_lines:
            self.date = transaction[1:9]
            self.time = transaction[42:48]
            
            self.transactions.append(TransactionModel(
                type = transaction[0:1],
                time = datetime.strptime(f'{self.date} {self.time}', "%Y%m%d %H%M%S")

            ))

        return self