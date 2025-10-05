from PyQt6.QtWidgets import QLineEdit


#Custom Qline edit class to only allow digits
class DigitOnlyLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self.filter_input)

    def filter_input(self, text):
        # Keep only digit characters
        filtered = ''.join(c for c in text if c.isdigit())
        if text != filtered:
            # Prevent feedback loop by blocking signal
            self.blockSignals(True)
            self.setText(filtered)
            self.blockSignals(False)