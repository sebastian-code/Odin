from students.models import User


def register_user(cleaned_data):
    email = cleaned_data['email']
    name = cleaned_data['name']
    password = User.generate_password()

    new_user = User.objects.create_user(email, password)
    new_user.set_full_name(name)
    new_user.save()

    return new_user
