from PyQt5 import QtWidgets
from doughnut_widget import DoughnutWidget
'''
test for doughnut widget
'''

app = QtWidgets.QApplication([])

w = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout(w)

dw = DoughnutWidget(font_path=r"..\fonts\B Zar.ttf", show_legend=False)
layout.addWidget(dw)

sizes = [45, 25, 20, 10]
labels = ['ثروت', 'روابط', 'سلامتي', 'معنويت']
dw.set_data(sizes, labels, colors=['#4daf4a','#377eb8','#ff7f00','#984ea3'], hole_size=0.5)

w.show()
app.exec_()
