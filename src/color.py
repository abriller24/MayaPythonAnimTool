from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QColorDialog
from PySide2.QtGui import QDoubleValidator, QColor, QPainter, QPalette

class ThreeJntChainWiget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Three Joint Chain")
        self.setGeometry(0, 0, 300, 300)
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        hintLabel = QLabel("Please Select the root of the joint chain:")        
        self.masterLayout.addWidget(hintLabel)

        autoFindBtn = QPushButton("Auto Find Jnts")
        self.masterLayout.addWidget(autoFindBtn)        
        autoFindBtn.clicked.connect(self.AutoFindBtnClicked)

        self.selectionDisplay = QLabel()
        self.masterLayout.addWidget(self.selectionDisplay)

        ctrlSettingLayout = QHBoxLayout()
        ctrlSizeLabel = QLabel("Controller Size: ")
        ctrlSettingLayout.addWidget(ctrlSizeLabel)

        self.ctrlSize = QLineEdit()
        self.ctrlSize.setValidator(QDoubleValidator())
        self.ctrlSize.setText("10")
        ctrlSettingLayout.addWidget(self.ctrlSize)

        self.masterLayout.addLayout(ctrlSettingLayout)

        # Color Control
        colorLayout = QHBoxLayout()
        colorLabel = QLabel("Controller Color:")
        colorLayout.addWidget(colorLabel)

        self.colorSwatch = QLabel()
        self.colorSwatch.setFixedSize(50, 20)
        self.colorSwatch.setStyleSheet("background-color: white; border: 1px solid black;")
        colorLayout.addWidget(self.colorSwatch)

        colorBtn = QPushButton("Pick Color")
        colorBtn.clicked.connect(self.pickColor)
        colorLayout.addWidget(colorBtn)

        self.masterLayout.addLayout(colorLayout)

        rigThreeJntChainBtn = QPushButton("Rig Three Jnt Chain")
        self.masterLayout.addWidget(rigThreeJntChainBtn)
        rigThreeJntChainBtn.clicked.connect(self.RigThreeJntChainBtnClicked)

        self.adjustSize()
        self.threeJntChain = ThreeJntChain()

    def pickColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colorSwatch.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
            self.threeJntChain.setControllerColor(color)
 
    def RigThreeJntChainBtnClicked(self):
        self.threeJntChain.RigThreeJntChain()

    def AutoFindBtnClicked(self):
        print("button pressed")
        self.threeJntChain.AutoFindJntsBasedOnSel()
        self.selectionDisplay.setText(f"{self.threeJntChain.root}, {self.threeJntChain.middle}, {self.threeJntChain.end}")
