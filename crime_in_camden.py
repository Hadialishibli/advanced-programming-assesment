import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QGraphicsView, QStyleFactory, QGraphicsScene, QDesktopWidget, QTabWidget, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image
from data_processor import load_data, get_data_summary
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data1 = None
        self.setWindowTitle("Dataset Analyzer")
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(screen_geometry)
        self.base_scene = QGraphicsScene(self)
        self.plot_scene = QGraphicsScene(self)
        self.baseComponent = QGraphicsView(self.base_scene, self)
        self.header_dropdown = QComboBox(self)
        self.header_dropdown.setMinimumWidth(200)
        self.header_dropdown.addItem("Select Header Field")
        self.header_dropdown.currentIndexChanged.connect(self.header_selected)
        self.tab_widget = QTabWidget(self)

        try:
            data = self.open_file()
            self.tab_widget.addTab(self.dummy_data_tab(data), "Data Preview")
            scatter_tab = ScatterPlotTab(data, "Street ID", "Easting")
            self.tab_widget.addTab(scatter_tab, "Scatter Plot")
            bar_chart_tab = BarChartTab(data, "Category", "Ward Name")
            self.tab_widget.addTab(bar_chart_tab, "Bar Chart")
            line_plot_tab = LinePlotTab(data, "Epoch", "Easting")
            self.tab_widget.addTab(line_plot_tab, "Line Plot")
            pie_chart_tab = PieChartTab(data)
            self.tab_widget.addTab(pie_chart_tab, "Pie Chart")
            map_tab = MapTab(data)
            self.tab_widget.addTab(map_tab, "Crime Map")
        except Exception as e:
            error_label = QLabel(f"Failed to load data: {str(e)}")
            error_tab = QWidget()
            layout = QVBoxLayout(error_tab)
            layout.addWidget(error_label)
            error_tab.setLayout(layout)
            self.tab_widget.addTab(error_tab, "Error")

        available_height = self.height() - self.menuBar().height() - 50
        self.baseComponent.setGeometry(10, self.menuBar().height(), 230, available_height)
        self.tab_widget.setGeometry(250, self.menuBar().height(), self.width() - 300, available_height)
        self.header_dropdown.move(20, 10 + self.menuBar().height())

    def header_selected(self, index):
        selected_field = self.header_dropdown.currentText()
        if selected_field != "Select Header Field":
            print(f"Selected header field: {selected_field}")

    def open_file(self):
        file_path = "data/On_Street_Crime_In_Camden.csv"
        if file_path:
            data = pd.read_csv(file_path, low_memory=False)
            print(f"Header: {data.columns}")
            self.header_dropdown.addItems(data.columns)
            print("-------------------------------------------")
            data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
            data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')
            data = data.dropna(subset=['Latitude', 'Longitude'])
            
            print(f"Number of valid entries: {len(data)}")
            print(f"Latitude range: {data['Latitude'].min()} to {data['Latitude'].max()}")
            print(f"Longitude range: {data['Longitude'].min()} to {data['Longitude'].max()}")
            
            return data

    def dummy_data_tab(self, data):
        data_tab = QWidget()
        data_table = QTableWidget(rowCount=20, columnCount=len(data.columns))
        data_table.setHorizontalHeaderLabels(data.columns)
        for i in range(20):
            for j in range(len(data.columns)):
                data_table.setItem(i, j, QTableWidgetItem(str(data.iloc[i, j])))
        data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout = QVBoxLayout(data_tab)
        layout.addWidget(data_table)
        data_tab.setLayout(layout)
        return data_tab

class BarChartTab(QWidget):
    def __init__(self, data, x_column, y_column):
        super().__init__()
        self.data = data
        self.x_column = x_column
        self.y_column = y_column
        self.init_ui()

    def init_ui(self):
        try:
            self.fig, self.ax = plt.subplots()
            sns.barplot(x=self.x_column, y=self.y_column, data=self.data)
            self.ax.set_xlabel(self.x_column)
            self.ax.set_ylabel(self.y_column)
            self.ax.set_title("Bar Chart")
            self.layout = QVBoxLayout(self)
            self.layout.addWidget(FigureCanvas(self.fig))
            self.setLayout(self.layout)
        except Exception as e:
            error_label = QLabel(f"Failed to create bar chart: {str(e)}")
            layout = QVBoxLayout(self)
            layout.addWidget(error_label)
            self.setLayout(layout)

class LinePlotTab(QWidget):
    def __init__(self, data, x_column, y_column):
        super().__init__()
        self.data = data
        self.x_column = x_column
        self.y_column = y_column
        self.init_ui()

    def init_ui(self):
        try:
            self.fig, self.ax = plt.subplots()
            sns.lineplot(x=self.x_column, y=self.y_column, data=self.data)
            self.ax.set_xlabel(self.x_column)
            self.ax.set_ylabel(self.y_column)
            self.ax.set_title("Line Plot")
            self.layout = QVBoxLayout(self)
            self.layout.addWidget(FigureCanvas(self.fig))
            self.setLayout(self.layout)
        except Exception as e:
            error_label = QLabel(f"Failed to create line plot: {str(e)}")
            layout = QVBoxLayout(self)
            layout.addWidget(error_label)
            self.setLayout(layout)

class PieChartTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.init_ui()

    def init_ui(self):
        try:
            self.fig, self.ax = plt.subplots()
            category_counts = self.data['Category'].value_counts()
            self.ax.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')
            self.ax.set_title("Crime Categories")
            self.layout = QVBoxLayout(self)
            self.layout.addWidget(FigureCanvas(self.fig))
            self.setLayout(self.layout)
        except Exception as e:
            error_label = QLabel(f"Failed to create pie chart: {str(e)}")
            layout = QVBoxLayout(self)
            layout.addWidget(error_label)
            self.setLayout(layout)

class ScatterPlotTab(QWidget):
    def __init__(self, data, x_column, y_column):
        super().__init__()
        self.data = data
        self.x_column = x_column
        self.y_column = y_column
        self.init_ui()

    def init_ui(self):
        try:
            self.fig, self.ax = plt.subplots()
            self.ax.scatter(self.data[self.x_column], self.data[self.y_column], marker='o', label=self.x_column)
            plt.title("Scatter Plot")
            plt.grid(True)
            plt.legend()
            self.ax.set_xlabel(self.x_column)
            self.ax.set_ylabel(self.y_column)
            self.ax.set_title("Scatter Plot")
            self.layout = QVBoxLayout(self)
            self.layout.addWidget(FigureCanvas(self.fig))
            self.setLayout(self.layout)
        except Exception as e:
            error_label = QLabel(f"Failed to create scatter plot: {str(e)}")
            layout = QVBoxLayout(self)
            layout.addWidget(error_label)
            self.setLayout(layout)

class MapTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        try:
            self.fig, self.ax = plt.subplots(figsize=(10, 8))
            self.canvas = FigureCanvas(self.fig)
            layout.addWidget(self.canvas)

            img = plt.imread("mytry/A-map-of-the-London-Borough-of-Camden-and-location-in-UK-right-Field-locations-are.png")
            self.ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto')

            lat_min, lat_max = self.data['Latitude'].min(), self.data['Latitude'].max()
            lon_min, lon_max = self.data['Longitude'].min(), self.data['Longitude'].max()

            x_adjust = 0.03
            y_adjust = 1.01
            x_scale = 1.05
            y_scale = -1.1

            x = (self.data['Longitude'] - lon_min) / (lon_max - lon_min)
            y = (self.data['Latitude'] - lat_min) / (lat_max - lat_min)

            x = x * x_scale + x_adjust
            y = y * y_scale + y_adjust
            y = 1 - y

            self.scatter = self.ax.scatter(x, y, c='red', alpha=0.5, s=5)
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.axis('off')

            self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),
                                          textcoords="offset points",
                                          bbox=dict(boxstyle="round", fc="w"),
                                          arrowprops=dict(arrowstyle="->"))
            self.annot.set_visible(False)
            self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        except Exception as e:
            error_label = QLabel(f"Failed to load map: {str(e)}")
            layout.addWidget(error_label)

        self.setLayout(layout)

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.scatter.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()

    def update_annot(self, ind):
        pos = self.scatter.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        text = f"{self.data.iloc[ind['ind'][0]]['Category']}"
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
