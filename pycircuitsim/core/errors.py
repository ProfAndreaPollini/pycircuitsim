

class ChipError(Exception):
    """Base class for exceptions in this module."""
    pass


class IncorrectPinNameError(ChipError):
	def __init__(self, pin_name):
		self.pin_name = pin_name


class ChipWiringError(ChipError):
	def __init__(self, message: str):
		self.message = message
