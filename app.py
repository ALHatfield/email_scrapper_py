import datetime


class Client:
    name = None
    time_created = None


def greetings():
    print("\nGreetings " + Client.name + "!\n")
    print(Client.time_created)


def save_user():
    user = open("user.txt", "r+")
    user.truncate(0)
    user.write(Client.name + "\n")
    user.write(str(Client.time_created) + "\n")
    user.close()


def sign_up():
    Client.name = input("Enter your NAME:\n")
    Client.time_created = datetime.datetime.now()
    save_user()


def get_user():
    user = open("user.txt", "r")
    Client.name = user.readline()
    Client.time_created = user.readline()
    user.close()


def log_in():
    get_user()
    if not Client.name:
        sign_up()
    greetings()


log_in()
