import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class ChartCanvas(FigureCanvas):
    """A canvas for embedding matplotlib charts in PySide6 UI."""
    def __init__(self, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)

    def plot_line_chart(self, df: pd.DataFrame, x_column: str, y_column: str, title: str = "Line Chart"):
        """Plot a line chart with the given data."""
        self.ax.clear()
        self.ax.plot(df[x_column], df[y_column], marker='o')
        self.ax.set_title(title)
        self.ax.set_xlabel(x_column)
        self.ax.set_ylabel(y_column)
        self.draw()

    def plot_bar_chart(self, df: pd.DataFrame, x_column: str, y_column: str, title: str = "Bar Chart"):
        """Plot a bar chart with the given data."""
        self.ax.clear()
        self.ax.bar(df[x_column], df[y_column], color='skyblue')
        self.ax.set_title(title)
        self.ax.set_xlabel(x_column)
        self.ax.set_ylabel(y_column)
        self.draw()

    def plot_pie_chart(self, df: pd.DataFrame, labels_column: str, values_column: str, title: str = "Pie Chart"):
        """Plot a pie chart with the given data."""
        self.ax.clear()
        labels = df[labels_column]
        values = df[values_column]
        self.ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        self.ax.set_title(title)
        self.ax.axis('equal')  # Equal aspect ratio to ensure the pie is drawn as a circle
        self.draw()
