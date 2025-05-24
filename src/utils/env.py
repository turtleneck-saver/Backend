from pathlib import Path
ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


class Dotenv:

    def __init__(self, filename) -> None:
        """
        Reads a .env file and returns a dictionary of variables.
        :param filename: The name of the .env file to read.
        :return: A dictionary of variables if the file is found, otherwise None.
        """

        self.filename = filename
        self.variables = {}
        try:
            with open(filename, encoding='utf-8') as f:
                for line in f:
                    if line.startswith('#') or not line.strip():
                        continue
                    key, value = line.strip().replace("\'", '').replace("\"", '').split('=', 1)
                    self.variables[key] = value
        except FileNotFoundError:
            print(f"Warning: {self.filename} not found. Using default values.")
        except Exception as e:
            print(f"Error reading {self.filename}: {e}")
        else:
            print(f"Successfully read {self.filename}.")

    def load(self) -> dict:
        """
        Loads the variables from the .env file.
        :return: A dictionary of variables.
        """
        return self.variables


ENV = Dotenv(filename=ENV_PATH).load()
