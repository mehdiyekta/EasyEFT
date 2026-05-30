from PyQt5.QtChart import QChartView, QLineSeries, QChart,QValueAxis,QDateTimeAxis,QCategoryAxis
from PyQt5.QtGui import  QPainter
class HandleChart():
    def __init__ (self,time,dates):
        self.time = time
        self.dates = dates
    def create(self):
        series = QLineSeries()
        series.setName("میزان تمرینات شما")
        x = 0
        for time in self.time:
            series.append(x,time)
            x += 1
        # Append data points (you can use any x values, here we use 1 to 5)
        # series.append(1, 1000)  # 1 Farvardin 1402
        # series.append(2, 1010)  # 2 Farvardin 1402
        # series.append(3, 1015)  # 3 Farvardin 1402
        # series.append(4, 1000)  # 4 Farvardin 1402
        # series.append(5, 800) # 5 Farvardin 1402
        # series.append(6, 1200) # 5 Farvardin 1402
        # series.append(7, 1250) # 5 Farvardin 1402
        # Create a QChart and add the series
        chart = QChart()
        chart.setTheme(QChart.ChartThemeDark)
        chart.setTitle("میزان تمرینات")
        chart.addSeries(series)
        chart.createDefaultAxes()

        # Customize the axes
        axisX = QCategoryAxis()
        axisX.setTitleText("تاریخ")
        y = 0
        for date in self.dates:
            axisX.append(date,y)
            y += 1
        # # Set custom labels for the Jalali dates
        # axisX.append("1403/1/25", 1)
        # axisX.append("1403/2/25", 2)
        # axisX.append("1403/3/25", 3)
        # axisX.append("1403/4/25", 4)
        # axisX.append("1403/5/25", 5)
        # axisX.append("1403/6/25", 6)
        # axisX.append("1403/12/30", 7)

        axisY = QValueAxis()
        axisX.setRange(0, int(len(self.dates)))
        axisY.setRange(0,60)
        axisY.setTitleText("زمان به دقیقه")

        chart.setAxisX(axisX, series)
        chart.setAxisY(axisY, series)
        chart.axisX().setVisible(True)
        chart.axisY().setVisible(True)

        # Create a QChartView and set the chart
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView