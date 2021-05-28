import csv


class EpicenterName:
    """A class that can convert epicenter's japanese name to english name."""

    def __init__(self, logger):
        """
        Initializes the instance.

        :param logger: The Flask app logger.
        """
        self.logger = logger
        self._epicenter_eng = {}
        self._epicenter_jpn = {}
        self.logger.debug("Initializing Epicenter library...")
        self._initialize_eng_epicenter()
        self._initialize_jpn_epicenter()

    def _initialize_eng_epicenter(self):
        """
        Initializes the epicenter names in English.
        """
        with open("./modules/stationtoenglish/Epicenter_en.csv", "r", encoding="utf-8") as f:
            fieldnames = ("codename", "name")
            reader = csv.DictReader(f, fieldnames)
            for row in reader:
                self._epicenter_eng[row["codename"]] = row["name"]
            f.close()
        self.logger.debug("Successfully initialized epicenter in English!")

    def _initialize_jpn_epicenter(self):
        """
        Initializes the epicenter names in Japanese.
        """
        with open("./modules/stationtoenglish/Epicenter_ja.csv", "r", encoding="utf-8") as f:
            fieldnames = ("codename", "name")
            reader = csv.DictReader(f, fieldnames)
            for row in reader:
                self._epicenter_eng[row["name"]] = row["codename"]
            f.close()
        self.logger.debug("Successfully initialized epicenter in Japanese!")

    def get_english_epicenter_name(self, epicenter_name):
        """
        Converts the Japanese epicenter name to English.

        :param epicenter_name: The Japanese epicenter name
        :return: The epicenter's English name
        :rtype: str
        """
        epicenter_code = self._epicenter_jpn.get(epicenter_name, default="")
        if epicenter_code != "":
            return self._epicenter_eng.get(epicenter_code, default=epicenter_name)
        else:
            return epicenter_name
