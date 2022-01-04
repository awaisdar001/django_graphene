"""
Enums descriptions for scheduler app
"""


class Description:
    """Verbose descriptions for availability fields. """
    availability_from = "Provide iso datetime for the start of the availability e.g. 2022-08-17T09:00:00"
    availability_to = "Provide iso datetime for your availability limit e.g. 2022-08-17T06:00:00"
    time_interval = "Provide a how much time user can book at max. e.g. 15"
