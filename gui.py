from datetime import datetime
import logging

import json

from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QApplication, QFrame,
    QStackedLayout, QVBoxLayout, QWidget, QLabel,
    QGridLayout, QLineEdit, QHBoxLayout, QDialog,
    QDialogButtonBox, QDoubleSpinBox, QTextEdit, QTextBrowser
)
from PyQt6.QtCore import QSize, Qt, QRect, pyqtSignal


## i know that basically nothing is commented,
## but i had to get this done before the contest and i had no time
## i will probably work on that soon


# testing code (do not use)
testing_data = {
    "contestant 1": {
        "description": "description",
        "story": "story",
        "picture": "image.jpg"
    },
    "contestant 2": {
        "description": "description",
        "story": "story",
        "picture": "image.jpg"
    },
    "contestant 3": {
        "description": "description",
        "story": "story",
        "picture": "image.jpg"
    }
}

# this is where the fun begins

logger = logging.getLogger(__name__)

base_font = QFont("Verdana", 15)
year = int(str(datetime.now().year)[2:])


class MenuFrame(QFrame):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() # vertical box layout with the stuff inside

        # font :p
        font = base_font
        self.setFont(font)

        # title label
        title = QLabel()
        title.setText("Kembl\nRock Judger")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font.setPointSize(30)
        title.setFont(font)
        layout.addWidget(title)

        # buttons
        self.new_save_btn = QPushButton() # new save button
        self.new_save_btn.setText("New Save")
        layout.addWidget(self.new_save_btn)

        self.load_save_btn = QPushButton() # load save button
        self.load_save_btn.setText("Load Last Save")
        layout.addWidget(self.load_save_btn)

        exit_btn = QPushButton()
        exit_btn.setText("Exit Program")
        layout.addWidget(exit_btn)
        exit_btn.clicked.connect(exit)

        container_widget = QWidget(parent=self)
        container_widget.setGeometry(QRect(170, 140, 391, 275))
        container_widget.setLayout(layout)


class NewSaveFrame(QFrame):
    def __init__(self):
        super().__init__()

        page_layout = QVBoxLayout()
        line_layout = QHBoxLayout() # hbox? what is this? evo 2019 melee side event?

        # font :)
        font = base_font
        font.setPointSize(15)
        self.setFont(font)

        # name prompt label
        prompt_label = QLabel()
        prompt_label.setText("Judge Name:")
        line_layout.addWidget(prompt_label)

        # name entry
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("John Smith")
        line_layout.addWidget(self.name_entry)

        page_layout.addLayout(line_layout)

        # start button
        self.start_button = QPushButton()
        self.start_button.setText("Begin Judging")
        page_layout.addWidget(self.start_button)

        container_widget = QWidget(parent=self)
        container_widget.setGeometry(QRect(210, 140, 300, 100))
        container_widget.setLayout(page_layout)


class LoadSaveDialog(QDialog): pass


class ScoreSpinner(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setDecimals(1)
        self.setSingleStep(0.1)
        self.setMinimum(0)
        self.setMaximum(10)


class JudgmentFrame(QFrame):

    last_signal = pyqtSignal()

    def __init__(self, data):
        super().__init__()

        self.submission_sheet = data # data from the google form
        self.judging_data = {} # data to help with saving, such as the current rock

        rsl = QVBoxLayout() # right side layout

        fsl = QHBoxLayout() # full screen layout
        lsl = QVBoxLayout() # left side layout

        # Judging UI

        score_widgets = QGridLayout()

        self.cool_text = QLabel("Cool Score")
        self.cool_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        score_widgets.addWidget(self.cool_text, 0, 0)

        self.color_text = QLabel("Color Score")
        self.color_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        score_widgets.addWidget(self.color_text, 1, 0)

        self.story_text = QLabel("Story Score")
        self.story_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        score_widgets.addWidget(self.story_text, 2, 0)

        self.cool_spinner = ScoreSpinner()
        score_widgets.addWidget(self.cool_spinner, 0, 1)

        self.color_spinner = ScoreSpinner()
        score_widgets.addWidget(self.color_spinner, 1, 1)

        self.story_spinner = ScoreSpinner()
        score_widgets.addWidget(self.story_spinner, 2, 1)

        self.judge_comments = QTextEdit()
        self.judge_comments.setFixedHeight(90)
        self.judge_comments.setPlaceholderText("Judge comments go here...")

        next_prev = QHBoxLayout()

        prev_rock = QPushButton(text="Previous Rock")
        next_prev.addWidget(prev_rock)
        prev_rock.clicked.connect(self.to_prev_rock)
        next_rock = QPushButton(text="Next Rock")
        next_prev.addWidget(next_rock)
        next_rock.clicked.connect(self.to_next_rock)


        # Rock UI

        self.rock_pic = QLabel()
        self.rock_pic.setPixmap(QPixmap("assets/rock_not_found.png"))
        self.rock_pic.setScaledContents(False)

        rock_text = QVBoxLayout()

        rock_description_label = QLabel()
        rock_description_label.setText("Rock Description:")
        rock_text.addWidget(rock_description_label)

        self.rock_description = QTextBrowser()
        rock_text.addWidget(self.rock_description)

        rock_story_label = QLabel()
        rock_story_label.setText("Rock Story:")
        rock_text.addWidget(rock_story_label)

        self.rock_story = QTextBrowser()
        rock_text.addWidget(self.rock_story)

        rsl.addLayout(rock_text)
        rsl.addLayout(score_widgets)
        rsl.addWidget(self.judge_comments)
        rsl.addLayout(next_prev)

        lsl.addWidget(self.rock_pic)

        fsl.addLayout(lsl)
        fsl.addLayout(rsl)

        container_widget = QWidget(self)
        container_widget.setGeometry(QRect(0,0,750,750))
        container_widget.setLayout(fsl)


    def setup_frame(self, save_data=None):
        if save_data is None:
            self.judging_data = {
                "keys": [i for i in iter(self.submission_sheet)],
                "current": 0,
                "length": len(self.submission_sheet) - 1,
                "scores": {i: {"cool": 0., "color": 0., "story": 0., "comments": ""} for i in iter(self.submission_sheet)}
            }
        else:
            self.judging_data = save_data

        self.change_rock(self.judging_data["keys"][self.judging_data["current"]])

    def save_current(self, key):
        self.judging_data["scores"][key]["cool"] = self.cool_spinner.value()
        self.judging_data["scores"][key]["color"] = self.color_spinner.value()
        self.judging_data["scores"][key]["story"] = self.story_spinner.value()
        self.judging_data["scores"][key]["comments"] = self.judge_comments.toPlainText()
        # logger.debug(self.judging_data)

    def change_rock(self, key):
        self.rock_pic.setPixmap(QPixmap(self.submission_sheet[key]["picture"]))
        self.rock_description.setText(self.submission_sheet[key]["description"])
        self.rock_story.setText(self.submission_sheet[key]["story"])

        self.cool_spinner.setValue(self.judging_data["scores"][key]["cool"])
        self.color_spinner.setValue(self.judging_data["scores"][key]["color"])
        self.story_spinner.setValue(self.judging_data["scores"][key]["story"])
        self.judge_comments.setText(self.judging_data["scores"][key]["comments"])

    def to_next_rock(self):
        if self.judging_data["current"] < self.judging_data["length"]:
            self.save_current(self.judging_data["keys"][self.judging_data["current"]])
            self.judging_data["current"] += 1
            self.change_rock(self.judging_data["keys"][self.judging_data["current"]])
        else:
            self.save_current(self.judging_data["keys"][self.judging_data["current"]])
            self.last_signal.emit()

    def to_prev_rock(self):
        if self.judging_data["current"] > 0:
            self.save_current(self.judging_data["keys"][self.judging_data["current"]])
            self.judging_data["current"] -= 1
            self.change_rock(self.judging_data["keys"][self.judging_data["current"]])
        else:
            pass


class EndingFrame(QFrame):
    def __init__(self):
        super().__init__()

        font = self.font()
        font.setPointSize(30)

        layout = QVBoxLayout() # vertical box layout with the stuff inside

        # title label
        gratitude = QLabel()
        gratitude.setText("Thank you for your judgments today")
        gratitude.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gratitude.setWordWrap(True)
        gratitude.setFont(font)
        layout.addWidget(gratitude)

        # buttons
        exit_btn = QPushButton()
        exit_btn.setText("Exit and Save")
        layout.addWidget(exit_btn)
        exit_btn.clicked.connect(exit)

        container_widget = QWidget(parent=self)
        container_widget.setGeometry(QRect(170, 140, 391, 275))
        container_widget.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, data):

        ## EXT VARIABLES

        self.judging_data = data # this is where the scores are stored
        self.judge_name = None # this is where the judges name is stored

        ## GUI STUFF

        # window init
        super().__init__()
        self.setWindowTitle("Kembl Rock Judger")
        self.setFixedSize(QSize(750, 750))

        font = base_font # good news! font is genetic
        self.setFont(font)

        # page frame layout setup
        self.page_stack = QStackedLayout()
        # page_stack.setObjectName("pageStack")

        # menu frame -- index 0
        self.menu_frame = MenuFrame() # create menu frame
        self.menu_frame.setObjectName("menu_frame")
        self.page_stack.addWidget(self.menu_frame) # add menu frame to page stack

        self.menu_frame.new_save_btn.clicked.connect(self.new_save_btn_clicked)
        self.menu_frame.load_save_btn.clicked.connect(self.load_save_btn_clicked)

        # new save frame -- index 1
        self.new_save_frame = NewSaveFrame() # create new save frame
        self.new_save_frame.setObjectName("new_save_frame")
        self.page_stack.addWidget(self.new_save_frame) # add frame to page stack

        self.new_save_frame.start_button.clicked.connect(self.start_judgment)

        # judgment frame -- index 2
        self.judgment_frame = JudgmentFrame(self.judging_data) # im doing the same thing. you can figure it out
        self.judgment_frame.setObjectName("judgment_frame")
        self.page_stack.addWidget(self.judgment_frame)

        self.judgment_frame.last_signal.connect(self.end_frame)

        # ending frame -- index 3
        self.ending_frame = EndingFrame()
        self.ending_frame.setObjectName("ending_frame")
        self.page_stack.addWidget(self.ending_frame)

        container_widget = QWidget()
        container_widget.setLayout(self.page_stack)
        self.setCentralWidget(container_widget)

    def export_data(self):
        with open(f"KRA{year}_judge_form_{self.judge_name}_save1.json", "w") as file:
            json.dump(self.judgment_frame.judging_data["scores"], file)

    def new_save_btn_clicked(self): # start a new save
        self.page_stack.setCurrentIndex(1)
        self.judge_name = self.new_save_frame.name_entry.text()
        return

    def load_save_btn_clicked(self): # load the last save
        pass # todo

    def start_judgment(self): # begin judging rocks
        name = self.new_save_frame.name_entry.text()
        if len(name) == 0: # dialog for if the judge doesn't input a name
            dlg = QDialog(parent=self)
            dlg.setWindowTitle("whoopsies")

            layout = QVBoxLayout()

            button = QDialogButtonBox.StandardButton.Ok
            btnbox = QDialogButtonBox(button)
            message = QLabel("Please input your name.")
            layout.addWidget(message)
            layout.addWidget(btnbox)
            dlg.setLayout(layout)

            btnbox.clicked.connect(dlg.accept)

            dlg.exec()
        else:
            self.judge_name = name
            self.judgment_frame.setup_frame()
            self.page_stack.setCurrentIndex(2)

    def end_frame(self):
        self.export_data()
        self.page_stack.setCurrentIndex(3)


def run_gui():
    app = QApplication([])

    window = MainWindow(testing_data)
    window.show()
    # window.page_stack.setCurrentIndex(2)

    return app, window


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s--[%(levelname)s]: %(message)s')
    logger.debug("debugger started")

    app, window = run_gui()
    app.exec()