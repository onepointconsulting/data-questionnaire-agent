class SessionNumberContainer:
    def __init__(self) -> None:
        self.counter = 0

    def current(self):
        return self.counter

    def increment_and_get(self):
        self.counter += 1
        return self.counter

    def __repr__(self) -> str:
        return f"{self.counter}"
