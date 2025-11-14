import pprint
import sys
import json
from pathlib import Path
from time import strftime, localtime

from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QStringListModel, QUrl, QTimer, QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from sportident import SIReaderReadout, SIReaderCardChanged
from fastlog import log
from .utils.grading import get_correctness_of_course, CURRENT_COURSE, InputData

class ReaderThread(QThread):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

    def run(self):
        log.success("running now")
        while True:
            log.info("polling now in loop")
            # TODO: make port an argument or pull from the ui someplace
            reader_port = '/dev/cu.SLAB_USBtoUART'


            try:
                # TODO: retry
                # TODO: do not recreate each loop. cache once
                si = SIReaderReadout(reader_port)

                # wait for poll
                while not si.poll_sicard():
                    pass

                # process output
                card_number = si.sicard
                card_type = si.cardtype

                card_data = si.read_sicard()
                log.info(card_data)
                # input_data = InputData.from_si_result(card_data)
            except SIReaderCardChanged:
                # this exception (card removed too early) can be ignored 
                pass

            # beep
            si.ack_sicard()
            response = { 'id': card_number, 'type': card_type, 'data': card_data }

            # grade response
            # TODO: when multiple courses are available, get_closest_course before grading
            runner_correct = get_correctness_of_course(card_data, CURRENT_COURSE.stations)

            log.debug(pprint.pformat(response))
            log.debug("Correctness: " + pprint.pformat(runner_correct))
            # Put stuff in the UI
            if runner_correct:
                self.engine.rootObjects()[0].setProperty('image_path', './resources/glassy-smiley-good-green.png')
            else:
                self.engine.rootObjects()[0].setProperty('image_path', './resources/glassy-smiley-bad.png')


def main() -> None:
    # Data nonsense we will not keep
    # TODO: Delete
    # get our data
    # url = "http://country.io/names.json"
    # response = urllib.request.urlopen(url)
    # data = json.loads(response.read().decode('utf-8'))
    # # Format and sort the data
    # data_list = sorted(list(data.values()))
    # # Expose the list to the Qml code
    # my_model = QStringListModel()
    # my_model.setStringList(data_list)

    # Set up the application window
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load('./src/easysnec/qml/Main.qml')
    engine.quit.connect(app.quit)


    def update_time():
        # Pass the current time to QML.
        curr_time = strftime("%H:%M:%S", localtime())
        # write state to ui
        engine.rootObjects()[0].setProperty('currTime', curr_time)

    timer = QTimer()
    timer.setInterval(100)  # msecs 100 = 1/10th sec
    timer.timeout.connect(update_time)
    timer.start()
    
    reader_thread = ReaderThread(engine)
    reader_thread.start()

    # execute and cleanup
    app.exec()

if __name__ == '__main__':
    main()