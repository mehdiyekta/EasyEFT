import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from bidi.algorithm import get_display
import arabic_reshaper
import matplotlib.font_manager as fm
import random




class DoughnutWidget(QtWidgets.QWidget):
    """
    Embeddable doughnut chart widget for PyQt5.
    - Handles Persian/Arabic shaping (requires python-bidi and arabic-reshaper).
    - Use set_data(sizes, labels, colors=None) to update.
    - Optional show_legend (bool) adds a legend to the right.
    """

    def __init__(self, parent=None, font_path=None, figsize=(4,4), show_legend=False):
        super().__init__(parent)
        self.figure = Figure(figsize=figsize)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.show_legend = show_legend

        if font_path:
            self.font_prop = fm.FontProperties(fname=font_path)
        else:
            self.font_prop = None

        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        lay.addWidget(self.canvas)

        self._sizes = []
        self._labels = []
        self._colors = None

    @staticmethod
    def _prepare_persian(text):
        if not text:
            return text
        return get_display(arabic_reshaper.reshape(str(text)))

    def set_data(self, sizes, labels=None, colors=None, hole_size=0.7, autopct_digits=1, fontsize=10):
        """
        Update chart data and redraw.
        - sizes: list of numeric values
        - labels: list of strings (Persian/Arabic supported)
        - colors: list of color specs
        - hole_size: float 0..1 (0.7 means 70% radius hole)
        - autopct_digits: decimals in percent labels
        - fontsize: font size for labels & percent text
        """
        self._sizes = list(sizes)
        self._labels = list(labels) if labels else None
        self._colors = colors

        self.ax.clear()
        # prepare labels for bidi/reshaper & font
        if self._labels:
            disp_labels = [self._prepare_persian(l) for l in self._labels]
        else:
            disp_labels = None

        def autopct(pct):
            s = f"{pct:.{autopct_digits}f}%"
            return self._prepare_persian(s)

        textprops = {}
        if self.font_prop:
            textprops['fontproperties'] = self.font_prop
        textprops['fontsize'] = fontsize

        wedges, texts, autotexts = self.ax.pie(
            self._sizes,
            labels=disp_labels,
            colors=self._colors,
            startangle=90,
            autopct=autopct,
            textprops=textprops
        )

        if self.font_prop:
            for t in texts + autotexts:
                t.set_fontproperties(self.font_prop)

        centre_circle = matplotlib.patches.Circle((0,0), hole_size, color='white')
        self.ax.add_artist(centre_circle)
        self.ax.axis('equal')

        if self.show_legend and self._labels:

            leg_labels = [self._prepare_persian(l) for l in self._labels]
            self.ax.legend(wedges, leg_labels, loc='center left', bbox_to_anchor=(1, 0.5),
                           prop=self.font_prop if self.font_prop else None)

        self.canvas.draw_idle()

    def set_font(self, font_path):
        """Set a TTF font path supporting Persian/Arabic and redraw if data exists."""
        self.font_prop = fm.FontProperties(fname=font_path)
        if self._sizes:
            self.set_data(self._sizes, self._labels, self._colors)

    def clear(self):
        """Clear the chart."""
        self._sizes = []
        self._labels = []
        self._colors = None
        self.ax.clear()
        self.canvas.draw_idle()
    def generate_random_color(self):
        # Generate random values for red, green, and blue
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        
        # Format the color as a hexadecimal string
        random_color = f'#{red:02x}{green:02x}{blue:02x}'
        return random_color
