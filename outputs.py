from abc import ABC, abstractmethod
from prettytable import PrettyTable


class AssistantOutput(ABC):
    @abstractmethod
    def create_table(self, data):
        raise NotImplementedError

    @abstractmethod
    def create_row(self, data):
        raise NotImplementedError


class AddressbookOutput(AssistantOutput):
    def create_table(self, data):
        output = PrettyTable()
        output.field_names = ['Name', 'Birthday', 'Email', 'Address', 'Phones']
        for i in data:
            output.add_row(i)
        return output

    def create_row(self, data):
        output = PrettyTable()
        output.field_names = ['Name', 'Birthday', 'Email', 'Address', 'Phones']
        output.add_row(data)
        return output


class NotebookOutput(AssistantOutput):
    def create_table(self, data):
        output = PrettyTable()
        output.field_names = ['Index', 'Tags', 'Note']
        for i in data:
            output.add_row(i)
        return output

    def create_row(self, data):
        output = PrettyTable()
        output.field_names = ['Index', 'Tags', 'Note']
        output.add_row(data)
        return output


class SortDirOutput(AssistantOutput):
    def create_table(self, data):
        pass

    def create_row(self, data):
        output = PrettyTable()
        output.field_names = ['Known_extensions', "Unknown_extensions"]
        output.add_row(data)
        return output