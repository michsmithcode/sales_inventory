from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Create default user groups"

    GROUPS = {
        "Super Admin": "__all__",
        "Manager": [
            "view_product",
            "add_product",
            "change_product",
            "view_sale",
            "view_customer",
            "view_vendor",
            "view_expense",
            "view_report",
        ],
        "Sales Representative": [
            "view_product",
            "view_sale",
            "add_sale",
            "view_customer",
            "add_customer",
        ],
        "Store Keeper": [
            "view_product",
            "add_product",
            "change_product",
        ],
        
        "Accountant": [
            "view_expense",
            "add_expense",
            "change_expense",
            "view_report",
        ],
        "Auditor": [
            "view_product",
            "view_sale",
            "view_customer",
            "view_vendor",
            "view_expense",
            "view_report",
        ]
        
    }

    def handle(self, *args, **kwargs):

        for group_name, permissions in self.GROUPS.items():

            group, created = Group.objects.get_or_create(name=group_name)

            if permissions == "__all__":
                group.permissions.set(Permission.objects.all())

            else:
                group.permissions.clear()

                for codename in permissions:
                    permission = Permission.objects.filter(
                        codename=codename
                    ).first()

                    if permission:
                        group.permissions.add(permission)

            self.stdout.write(
                self.style.SUCCESS(f"{group_name} created successfully.")
            )