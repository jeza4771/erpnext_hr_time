import sys
from unittest.mock import MagicMock

"""
Utility file to define mocked (fake) classses and methods of the framework for running tests.
"""


class FakeLogger:
    @staticmethod
    def info(message):
        return

    def set_log_level(self, level):
        return

    @staticmethod
    def error(message, args=None):
        return


class FakeDB:
    @staticmethod
    def commit():
        FakeLogger.info("DB Commit")

    @staticmethod
    def rollback():
        FakeLogger.error("DB Rollback")


class FakeUtils:
    logger = FakeLogger()


class FakeDocument:
    def __init__(self, name, employee=None, task_desc=None, task=None):
        self.name = name
        self.employee = employee
        self.task_desc = task_desc
        self.task = task

    def save(self):
        # Simulate saving the document (do nothing or add custom logic if needed)
        return


class FakeDocumentModel:
    @staticmethod
    def get_doc(doctype, docname):
        # Return a mock document based on doctype and docname
        if doctype == "ToDo":
            return FakeDocument(name=docname, task_desc="Sample Todo Task")
        elif doctype == "Worklog":
            return FakeDocument(name=docname, employee="EMP001", task_desc="Sample Worklog Task")
        raise ValueError(f"Unknown document: {doctype}, {docname}")


class FakeModel:
    document = FakeDocumentModel  # Add document class to simulate frappe.model.document


class FakeFrappe(object):
    utils = FakeUtils()
    db = FakeDB()
    model = FakeModel()

    class User:
        def __init__(self, email):
            self.doc = MagicMock()
            self.doc.email = email

    @staticmethod
    def get_user():
        return FakeFrappe.User(email='test.user@example.com')

    @staticmethod
    def throw(message, error_type):
        raise error_type(message)

    @staticmethod
    def get_current():
        # Mock get_user to return a user object with an email
        mock_user = MagicMock()
        mock_user.doc.email = 'test.user@example.com'
        # Set return value for frappe.get_user()
        return mock_user

    @staticmethod
    def logger(level, allow_site, file_count):
        return FakeLogger()

    # Simulating frappe whitelist function
    @staticmethod
    def whitelist():
        # Return a no-op decorator that simply returns the function passed to it
        return lambda func: func

    @staticmethod
    def _(text):
        # A simple translation function for mock
        return text

    @staticmethod
    def get_all(doctype, fields=None, filters=None):
        if doctype == "Worklog":
            if filters:
                if filters.get('employee_id') == "001":
                    return [
                        FakeDocument(name="Test Employee", employee="001",
                                     task_desc="test description", task="Task A"),
                        FakeDocument(name="Test Employee", employee="001",
                                     task_desc="test description", task="Task B"),
                    ]
                elif filters.get('employee_id') == "002":
                    return []
            else:
                return []
        return []

    @staticmethod
    def new_doc(doctype):
        if doctype == "Worklog":
            return FakeDocument(name="NEW_WORKLOG", employee=None, task_desc=None, task=None)
        raise AttributeError(f"Unknown doctype: {doctype}")

    @staticmethod
    def get_doc(doctype: dict[str: str]):
        if doctype['doctype'] == "Worklog":
            return FakeDocument(name="NEW_WORKLOG", employee=None, task_desc=None, task=None)
        raise AttributeError(f"Unknown doctype: {doctype}")

    @staticmethod
    def get_hooks(hook_name):
        # Return a mock response for hooks
        # You can customize the return value based on the tests you're running
        return {
            # This simulates the behavior of the actual `frappe.get_hooks`
            "persistent_cache_keys": []
        }.get(hook_name, [])

    class DoesNotExistError(Exception):
        pass

    class ValidationError(Exception):
        pass


# noinspection PyTypeChecker
sys.modules["frappe"] = FakeFrappe
