import csv
from PyQt6.QtWidgets import QApplication
from image_downloader import prepare_image
from gui import MainWindow

# variables for the submissions from the google form
submissions = {}
submission_keys = []

with open(input("input submission form csv file: "), newline='') as csvfile:
    rock_reader = csv.reader(csvfile)
    for line in rock_reader:
        submission_keys.append(line[1]) # add key to key library
        submissions[line[1]] = {
            "description": line[2],
            "story": line[3],
            "picture": line[4]
        }
    del submissions[submission_keys[0]] # remove the first key (csv file table key)
    submission_keys.pop(0)

# replace the gdrive link with image dir location
for key in submission_keys:
    submissions[key]["picture"] = prepare_image(submissions[key]["picture"])

app = QApplication([])
window = MainWindow(submissions)

window.show()
app.exec()