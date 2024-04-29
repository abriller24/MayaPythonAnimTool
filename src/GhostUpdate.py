import maya.cmds as mc
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout
from PySide2.QtCore import Qt

class BuildProxyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.setWindowTitle("Build Rig Proxy") 
        self.setGeometry(0, 0, 300, 150)

        # Build Proxy Button
        buildBtn = QPushButton("Build Proxy")
        buildBtn.clicked.connect(self.BuildProxyBtnClicked)

        # Transparency Slider
        self.transparencyLabel = QLabel("Ghost Transparency")
        self.transparencySlider = QSlider(Qt.Horizontal)
        self.transparencySlider.setRange(0, 100)
        self.transparencySlider.setValue(50)
        self.transparencySlider.valueChanged.connect(self.UpdateGhostTransparency)

        # Layout
        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.transparencyLabel)
        sliderLayout.addWidget(self.transparencySlider)

        self.masterLayout.addWidget(buildBtn)
        self.masterLayout.addLayout(sliderLayout)
        self.adjustSize()

        # Builder instance
        self.builder = BuildProxy()

        # Previous Color
        self.previousColor = None

    def BuildProxyBtnClicked(self):
        self.builder.BuildProxyForSelectedmesh()

    def UpdateGhostTransparency(self, value):
        transparency = float(value) / 100.0
        self.builder.SetGhostTransparency(transparency)

        # Update transparency label
        self.transparencyLabel.setText(f"Ghost Transparency: {value}%")

        # Remember transparency for next build
        self.builder.SetPreviousTransparency(value)

class BuildProxy:
    def __init__(self):
        self.skin = ""
        self.model = ""
        self.jnts = []
        self.previousTransparency = 50  # Default transparency

    def BuildProxyForSelectedmesh(self):
        pass

    def SetGhostTransparency(self, transparency):
        # Set transparency for ghost objects
        pass  # Add implementation here

    def SetPreviousTransparency(self, transparency):
        self.previousTransparency = transparency

# Instantiate and show the widget
buildProxyWidget = BuildProxyWidget()
buildProxyWidget.show()

