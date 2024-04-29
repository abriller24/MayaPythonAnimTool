import maya.cmds as mc
from PySide2.QtWidgets import QCheckBox, QLineEdit, QWidget, QPushButton, QListWidget, QAbstractItemView, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox
from PySide2.QtCore import Signal

class AnimEntryWidget(QWidget):
    deleted = Signal(object)  # Signal to emit when widget is deleted

    def __init__(self, entry: AnimEntry):
        super().__init__()
        self.entry = entry
        self.masterLayout = QHBoxLayout()
        self.setLayout(self.masterLayout)

        enableCheckbox = QCheckBox()
        enableCheckbox.setChecked(self.entry.shouldExport)
        self.masterLayout.addWidget(enableCheckbox)
        enableCheckbox.toggled.connect(self.EnableCheckboxToggled)

        subfixLabel = QLabel("Subfix: ")
        self.masterLayout.addWidget(subfixLabel)
        subfixLineEdit = QLineEdit()
        subfixLineEdit.setText(self.entry.subfix)
        subfixLineEdit.textChanged.connect(self.SubfixTextChanged)
        self.masterLayout.addWidget(subfixLineEdit)

        minFrameLabel = QLabel("Min: ")
        self.masterLayout.addWidget(minFrameLabel)
        self.minFrameLineEdit = QLineEdit()
        self.minFrameLineEdit.setText(str(self.entry.frameMin))
        self.minFrameLineEdit.textChanged.connect(self.MinFrameChanged)
        self.masterLayout.addWidget(self.minFrameLineEdit)

        maxFrameLabel = QLabel("Max: ")  # Fixed typo here
        self.masterLayout.addWidget(maxFrameLabel)
        self.maxFrameLineEdit = QLineEdit()
        self.maxFrameLineEdit.setText(str(self.entry.frameMax))
        self.maxFrameLineEdit.textChanged.connect(self.MaxFrameChanged)
        self.masterLayout.addWidget(self.maxFrameLineEdit)

        setRangeBtn = QPushButton("[-]")
        setRangeBtn.clicked.connect(self.SetRangeBtnClicked)
        self.masterLayout.addWidget(setRangeBtn)

        deleteBtn = QPushButton("X")
        deleteBtn.clicked.connect(self.DeleteBtnClicked)
        self.masterLayout.addWidget(deleteBtn)

    def DeleteBtnClicked(self):
        self.deleted.emit(self)  # Emit the signal with this widget
        self.deleteLater()

    def SetRangeBtnClicked(self):
        # Set the timeline range to min and max of the entry
        mc.playbackOptions(edit=True, min=self.entry.frameMin, max=self.entry.frameMax)

    def MaxFrameChanged(self, newVal):
        self.entry.frameMax = int(newVal)

    def MinFrameChanged(self, newVal):
        self.entry.frameMin = int(newVal)

    def SubfixTextChanged(self, newVal):
        self.entry.subfix = newVal

    def EnableCheckboxToggled(self):
        self.entry.shouldExport = not self.entry.shouldExport


class MayaToUEWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.mayaToUE = MayaToUE()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.rootJntText = QLineEdit()
        self.rootJntText.setEnabled(False)
        self.masterLayout.addWidget(self.rootJntText)

        setSelectionAsRootJntBtn = QPushButton("Set Root Joint")
        setSelectionAsRootJntBtn.clicked.connect(self.SetSelectionAsRootJntBtnClicked)
        self.masterLayout.addWidget(setSelectionAsRootJntBtn)

        addRootJntBtn = QPushButton("Add Root Joint")
        addRootJntBtn.clicked.connect(self.AddRootJntBtnClicked)
        self.masterLayout.addWidget(addRootJntBtn)

        self.meshList = QListWidget()
        self.masterLayout.addWidget(self.meshList)
        addMeshBtn = QPushButton("Add Meshes")
        addMeshBtn.clicked.connect(self.AddMeshBtnClicked)
        self.masterLayout.addWidget(addMeshBtn)

        addNewAnimEntryBtn = QPushButton("Add Animation Clip")
        addNewAnimEntryBtn.clicked.connect(self.AddNewAnimEntryBtnClicked)
        self.masterLayout.addWidget(addNewAnimEntryBtn)

        # List to hold references to AnimEntryWidget instances
        self.animEntryWidgets = []

    def AddNewAnimEntryBtnClicked(self):
        newEntry = self.mayaToUE.AddNewAnimEntry()
        newAnimEntryWidget = AnimEntryWidget(newEntry)
        newAnimEntryWidget.deleted.connect(self.RemoveAnimEntry)  # Connect signal
        self.animEntryWidgets.append(newAnimEntryWidget)
        self.masterLayout.addWidget(newAnimEntryWidget)

    def RemoveAnimEntry(self, widget):
        self.animEntryWidgets.remove(widget)
        # Remove the corresponding entry from MayaToUE class
        # Assuming each entry has a unique identifier (not implemented in provided code)

    def AddMeshBtnClicked(self):
        success, msg = self.mayaToUE.AddSelectedMeshes()
        if not success:
            QMessageBox.warning(self, "Warning", msg)
        else:
            self.meshList.clear()
            self.meshList.addItems(self.mayaToUE.models)

    def AddRootJntBtnClicked(self):
        success, msg = self.mayaToUE.AddRootJnt()
        if not success:
            QMessageBox.warning(self, "Waring", msg)
        else:
            self.rootJntText.setText(self.mayaToUE.rootJnt)

    def SetSelectionAsRootJntBtnClicked(self):
        success, msg = self.mayaToUE.GetSelectionAsRootJnt()
        if not success:
            QMessageBox.warning(self, "Warning", msg)
        else:
            self.rootJntText.setText(self.mayaToUE.rootJnt)


mayaToUEWidget = MayaToUEWidget()
mayaToUEWidget.show()
