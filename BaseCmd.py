from abc import ABC, abstractmethod

from telegram.ext import CommandHandler


class BaseCommand(ABC):
    @abstractmethod
    def command_handlers(self) -> list[CommandHandler]:
        pass
