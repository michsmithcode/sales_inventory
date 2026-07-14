from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
import logging


from .models import CustomUser


ROLE_GROUP_MAPPING = {
    "super_admin": "SUPPER ADMIN",
    "manager": "MANAGER",
    "sales_rep": "SALES REPRESENTATIVES",
    "store_keeper": "STORE KEEPER",
    "accountant": "ACCOUNTANT",
    "auditor": "AUDITOR"
    
}




@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, **kwargs):
    """
    Keep the user's Django Group in sync with their role.
    """

    role_groups = Group.objects.filter(
        name__in=ROLE_GROUP_MAPPING.values()
    )

    # Remove the user from all managed role groups
    instance.groups.remove(*role_groups)

# This implemented for users promoted to another role, its automatically add the user to the new role
    # Add the user to the correct group
    group_name = ROLE_GROUP_MAPPING.get(instance.role)

    if not group_name:
        return
    
    logger = logging.getLogger(__name__)

    try:
        group = Group.objects.get(name=group_name)
        instance.groups.add(group)
    except Group.DoesNotExist:
        logger.warning(
        "Group '%s' does not exist for user '%s'.",
        group_name,
        instance.email,
    )
        

# @receiver(post_save, sender=CustomUser)
# def assign_user_group(sender, instance, created, **kwargs):

#     if not created:
#         return

#     group_name = ROLE_GROUP_MAPPING.get(instance.role)

#     if not group_name:
#         return

#     group = Group.objects.filter(name=group_name).first()

#     if group:
#         instance.groups.add(group)