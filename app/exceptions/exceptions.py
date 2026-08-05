class CityNotFoundException(Exception):
    """Exception raised when a city is not found."""

    def __init__(self, city_name: str):
        self.city_name = city_name
        self.message = f"City '{city_name}' not found."
        super().__init__(self.message)
