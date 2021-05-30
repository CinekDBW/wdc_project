
from django.db.models.signals import post_save
from django.dispatch import receiver

GROUPS = ['Admin', 'Moderator', 'Casual']
PERMISSIONS = {
    'Admin': [
        'Can delete every post',
        'Can verify topics',
        'Can view all topics',
        'Can add topics',
        'Can add posts',
        'Can delete own post',
    ],
    'Moderator': [
        'Can verify topics',
        'Can view all topics',
        'Can add topics',
        'Can add posts',
        'Can delete own post',
    ],
    'Casual': [
        'Can add topics',
        'Can add posts',
        'Can delete own post',
    ],
}


def populate_models(sender, **kwargs):
    from django.contrib.auth.models import User, Group, Permission
    for g in GROUPS:
        new_group, created = Group.objects.get_or_create(name=g)
        for perm in PERMISSIONS[g]:
            perm_object = Permission.objects.get(name=perm)
            new_group.permissions.add(perm_object)

    new_user = User.objects.create_user(username='admin',
                                        email='admin@admin.com',
                                        password='admin')
    new_user.is_superuser = True
    new_user.is_staff = True

    for permission in Permission.objects.all():
        new_user.user_permissions.add(permission)

    new_user.save()

    casual = Group.objects.get(name='Casual')
    casual.user_set.remove(new_user)
    my_group = Group.objects.get(name='Admin')
    my_group.user_set.add(new_user)




