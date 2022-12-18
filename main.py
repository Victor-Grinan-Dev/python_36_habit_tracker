import requests
from datetime import datetime
from random import choice

# udemy class

user_params = {
    "token": "TrackingAppGraphicShit001",
    "username": "tomatotimer",
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# constants
USERNAME = user_params["username"]
TOKEN = user_params["token"]
GRAPH_ID = "graph1"

japanese_colors = {
    "green": "shibafu",
    "red": "momiji",
    "blue": "sora",
    "yellow": "ichou",
    "purple": "ajisai",
    "black": "kuro"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

pixela_endpoint = "https://pixe.la/v1/users"
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"


def create_pixela_account(username, password):
    params = {
        "token": password,
        "username": username,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    response = requests.post(url=pixela_endpoint, json=params)
    print(response)


# create a graph frame
def create_pixela_graph_frame(unit: str, unit_type: str, pixels_colors: str, name=user_params["username"],
                              graph_id=GRAPH_ID):
    graph_config = {
        "id": graph_id,
        "name": name,
        "unit": unit,
        "type": unit_type,
        "color": pixels_colors

    }

    return requests.post(url=graph_endpoint, json=graph_config, headers=headers)


def set_date_format(year: int, month: int, day: int):
    """

    :param year: yyyy
    :param month: mm
    :param day: dd
    :return: formated date
    """


def add_pixel(quantity=None, today: bool = True):
    if not quantity:
        quantity = quantity_UI()

    if today:
        date = datetime.now()
        pixel_json = {
            "date": date.strftime("%Y%m%d"),
            "quantity": quantity,
        }

        response = requests.post(url=pixel_creation_endpoint, json=pixel_json, headers=headers)
        print(response)

    else:
        update_pixela(quantity)


# a few more data to enter
def testing_pixels(day=3, month=5, year=2021, choices: list = None):
    """
    this worked but perfectly
    :param day:
    :param month:
    :param year:
    :param choices:
    :return:
    """
    dummy_today = datetime(year=year, month=month, day=day)

    if not choices:
        choices = [20, 40, 60]

    while day > 0:
        pixel_data = {
            "date": str(dummy_today.strftime("%Y%m%d")),
            "quantity": str(choice(choices)),
        }

        test_response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
        print(test_response.text)
        day -= 1


def set_date():
    data_date = ["year", "month", "day"]
    date_dict = {data: int(input(f"{data}: ")) for data in data_date}
    date = datetime(year=date_dict['year'], month=date_dict['month'], day=date_dict['day'])
    return date


def quantity_UI():
    return input("Quantity: ")


# update pixels
def update_pixela(quantity=None, today=True):
    if not today:
        date = set_date()
    else:
        date = datetime.now()

    if not quantity:
        quantity = quantity_UI()

    date = str(date.strftime("%Y%m%d"))

    pixel_data = {
        "quantity": str(quantity),
    }

    update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date}"

    response = requests.put(url=update_endpoint, json=pixel_data, headers=headers)
    print(response.text)


def delete_a_pixel(today=True):
    if not today:
        date = set_date()
    else:
        date = datetime.now()

    date = str(date.strftime("%Y%m%d"))

    delete_pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date}"
    response = requests.delete(url=delete_pixel_endpoint, headers=headers)
    print(response.text)


if __name__ == "__main__":
    actions = {
        1: "create_pixela_account",
        2: "create_pixela_graph_frame",
        3: "update_pixela_today",
        4: "update_pixela",
        5: "delete_a_pixel",
        6: "delete_a_graph",
        7: "delete_a_user",
    }

    [print(key, value) for key, value in actions.items()]
    answer = input("choose your action: ")
    if answer == 4:
        update_pixela(False)
    else:
        eval(f"{actions[int(answer)]}()")


# my app ideas first steps


class TomatoTimerGraph:
    from datetime import datetime
    url_pixela = """https://docs.pixe.la/"""
    COLORS = {
        "green": "shibafu",
        "red": "momiji",
        "blue": "sora",
        "yellow": "ichou",
        "purple": "ajisai",
        "black": "kuro"
    }

    def __init__(self, name=None, password=None):
        if not name:
            self.name = "enter name function"
        else:
            self.name = "name from database"

        if not password:
            self.headers = "enter password function"
        else:
            self.headers = "password from database"

        self.graph_list = []  # read all graph from database

        self.today = datetime.now()

        self.last_update = "log"

    def create_user_account(self):
        """

        :return:
        """
        in_user_params = {
            "token": self.headers,
            "username": self.name,
            "agreeTermsOfService": "yes",
            "notMinor": "yes",
        }
        response = requests.post(url=pixela_endpoint, json=in_user_params)
        return response.text

    def create_graph_frame(self, graph_name=None):

        # if not graph_name:
        #     # Todo import nameless counter numbers
        #     # create a automatic graph name with the username and counter number (username003)
        #     nameless_counter_number = 1
        #     graph_name = f"{self.name}{str(nameless_counter_number):.2d}"
        #     nameless_counter_number += 1  # create/save the counter to be read after
        #
        graph_setup = {
            "id": graph_name,
            "name": self.name,
            "unit": "minutes",
            "type": "int",
            "color": f"{self.COLORS['purple']}"

        }
        # security reason to give the password or token in a jason format
        password = {
            "X-USER-TOKEN": self.headers
        }

        response = requests.post(url=graph_endpoint, json=graph_setup, headers=password)
        # todo: log the graph in the graph database if succeful
        return response.text

    def add_pixel(self, amount):

        create_pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

        pixel_data = {
            "date": self.set_date(),
            "quantity": amount,
        }

        self.last_update = "recreate log"

        response = requests.post(url=create_pixel_endpoint, json=pixel_data, headers=headers)
        return response.text

    # update pixels
    def update_pixela(self, quantity=None, today=True):
        if not today:
            date = set_date()
        else:
            date = self.today

        if not quantity:
            quantity = quantity_UI()

        date = str(date.strftime("%Y%m%d"))

        pixel_data = {
            "quantity": str(quantity),
        }

        update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date}"

        response = requests.put(url=update_endpoint, json=pixel_data, headers=headers)
        print(response.text)

    def delete_a_pixel(self, today=True):
        if not today:
            date = set_date()
        else:
            date = datetime.now()

        date = str(date.strftime("%Y%m%d"))

        delete_pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date}"
        response = requests.delete(url=delete_pixel_endpoint, headers=headers)
        print(response.text)

    @staticmethod
    def delete_graph():
        delete_graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
        response = requests.delete(url=delete_graph_endpoint, headers=headers)
        # Todo: delete the graph from the database
        return response

    def update_graph_details(self):
        update_graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
        graph_id = input("enter new graph name: ")
        for key, value in self.COLORS.items():
            print(enumerate(key))
        color_choice = None
        while color_choice not in self.COLORS.items():
            color_choice = input("type a color:")

        graph_setup = {
            "id": graph_id,
            "name": self.name,
            "unit": "minutes",  # cause this is for the tomato_timer
            "type": "int",
            "color": f"{self.COLORS['purple']}"

        }

    def change_password(self):  # not tested
        update_user_endpoint = f"{pixela_endpoint}/{USERNAME}"
        update_user_data = {
            "new_token": input("enter password")
        }
        response = requests.put(url=update_user_endpoint, json=update_user_data, headers=headers)
        self.headers = update_user_data["new_token"]
        return response

    @staticmethod
    def set_date():
        data_date = ["year", "month", "day"]
        date_dict = {data: int(input(f"{data}: ")) for data in data_date}
        formatted_date = datetime(year=date_dict['year'], month=date_dict['month'], day=date_dict['day'])
        return formatted_date

    def last_update_log(self):
        # Todo: check if there is a log file
        # Todo: if yes read from it last log and update
        # Todo: if not create one and write on it last log
        pass
