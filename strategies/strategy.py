class Strategy:
    def __init__(self, data):
        self.data = data
        self.indicators = {}

    def get_indicator_output(self, func, *args):
        result = func(*args)
        self.indicators[func.__name__] = result
        return result

    def precompute(self):
        """Precompute indicators or any setup logic here."""
        raise NotImplementedError("Override 'precompute' in your strategy.")

    def decide(self, row, row_idx):
        """Decision logic for each row."""
        raise NotImplementedError("Override 'decide' in your strategy.")
