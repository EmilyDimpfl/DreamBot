"""
module for keeping track of users' time spent in the server
"""

import json

class UserData:
    """
    class for managing user data, deserializing and serializing
    """
    data = {}
    filepath = None

    def __init__(self, filepath: str = None):
        """
        reads in data to set up our data structure
        """

        try:
            with open(filepath, 'r', encoding='utf-8') as file_desc:
                raw = file_desc.read()
                data = json.loads(raw)

                # validation: todo

                self.data = data
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {} # default to no data if the data file doesn't exist.

        self.filepath = filepath

    def modify_user(self, user_id: int, delta: int):
        """
        adds (or removes) time from a user's recorded time in the server
        """

        time_in_server = self.get_user_time(str(user_id))
        self.data[str(user_id)] = int(time_in_server) + int(delta)

    def get_user_time(self, user_id: int):
        """
        gets the amount of time a user has been in the server
        """

        try:
            if self.data[str(user_id)] is not None:
                return self.data[str(user_id)]
        except KeyError:
            self.data[str(user_id)] = 0

        return 0

    def save_data(self, filepath: str):
        """
        dumps our user data to disk
        """

        with open(filepath, 'w', encoding='utf-8') as file_desc:
            output = json.dumps(self.data)

            file_desc.write(output)

    def pretty_print(self):
        """
        prints out all data, pretty-like
        """

        output = ""
        for key, value in self.data.items():
            if value != 0:
                output += f"{str(key)}: {str(value)}\n"

        return output
