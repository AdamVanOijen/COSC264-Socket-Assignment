from datetime import datetime

class TextTime:
    _ENGLISH = 1
    _MAORI = 2
    _GERMAN = 3
    def __init__(self):
        self._months = {
            1: ["January", "Kohitatea", "Januar"],
            2: ["February", "Hui-tanguru", "Februar"],
            3: ["March", "Poutu-te-rangi" "Marz"],
            4: ["April", "Paenga-whawha", "April"],
            5: ["May", "Haratua", "Mai"],
            6: ["June", "Pipiri", "Juni"],
            7: ["July", "Hongongoi", "Juli"],
            8: ["August", "Here-turi-koka", "August"],
            9: ["September", "Mahuru", "September"],
            10: ["October", "Whiringa-a-nuku", "Oktober"],
            11: ["November", "Whiringa-a-rangi", "November"],
            12: ["December", "Hakihea", "Dezember"]
        }
        self._now = datetime.now()

    def _update_time(self):
        self._now = datetime.now()

    def text_time(self, language):
        self._update_time()
        prefix = {
            self._ENGLISH: "The current time is",
            self._MAORI: "Ko te wa o tenei wa",
            self._GERMAN: "Die Uhrzeit ist"
        }

        return "{0} {1}:{2:02d}".format(
            prefix[language],
            self._now.hour,
            self._now.minute
        )

    def text_date(self, language):
        self._update_time()
        format = {
            self._ENGLISH:"Today's date is {month} {day}, {year}",
            self._MAORI: "Ko te ra o tenei ra ko {month} {day}, {year}",
            self._GERMAN: "Heute ist der {day}. {month} {year}"
        }

        output = format[language].format(
            day=self._now.day,
            month=self._months[self._now.month][language-1],
            year=self._now.year
        )

        return output