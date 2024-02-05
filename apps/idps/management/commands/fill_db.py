from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from openpyxl.reader.excel import load_workbook

from apps.idps.management.commands._import_models import (
    import_comments,
    import_goals,
    import_idps,
    import_tasks,
    import_users,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                input_data = load_workbook("data/input_data.xlsx")
                import_users(input_data["users"])
                import_idps(input_data["idps"])
                import_goals(input_data["goals"])
                import_tasks(input_data["tasks"])
                import_comments(input_data["comments"])

        except Exception as error:
            raise CommandError(f"Сбой при импорте: {error}")

        self.stdout.write(self.style.SUCCESS("Импорт прошел успешно"))
