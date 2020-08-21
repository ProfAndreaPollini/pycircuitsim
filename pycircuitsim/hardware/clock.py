

class Clock:
	
	def __init__(self):
		super().__init__()
		self.tick_subscribed = []
		self.tok_subscribed = []
		self.value =  0

	def subscribe_to_tick(self, chip):
		self.tick_subscribed.append(chip)

	def subscribe_to_tok(self, chip):
		self.tok_subscribed.append(chip)

	def tick(self):
		self.value += 1
		for subscribed in self.tick_subscribed:
			subscribed.on_tick(self.value)

	def tok(self):
		for subscribed in self.tok_subscribed:
			subscribed.on_tok(self.value)