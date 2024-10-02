import sys, os, platform
from vtkmodules.vtkCommonCore import vtkObject, vtkLogger
import qdarktheme
import logging
from traceback import format_tb

from pulse import USER_PATH
from pulse.interface.application import Application


def custom_exception_hooks(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.exit()

    # Logs unhandled errors for future checks 
    logging.error("Unhandled error", exc_info=(exc_type, exc_value, exc_traceback))
    
    try:
        from pulse.interface.user_input.project.print_message import PrintMessageInput
        PrintMessageInput([
            "Unhandled error",
            f"{exc_type.__name__}: {exc_value}",
            "\n".join(format_tb(exc_traceback, limit=-1))
        ])
    except Exception as e:
        logging.exception(e)

sys.excepthook = custom_exception_hooks


def configure_logs():
    """
    Configures the logging library.
    Format includes time, log level (info, debug, error and so on).

    The main level is set to NOSET, so every handler can select its
    own filters.

    All info logs are saved in the file, but only warnings or error
    are shown to users.
    """
    file_formatter = logging.Formatter("%(asctime)s \t | %(levelname)s \t | %(message)s")
    file_handler = logging.FileHandler(USER_PATH / ".pulse.log", "w+")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    stream_formatter = logging.Formatter(logging.BASIC_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARN)
    stream_handler.setFormatter(stream_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def main():
    """ OpenPulse main
        The main function starts the OpenPulse software.
        This will create the mainWindow and also pass the terminal arguments to it.

        # If are using Windows with HighDPI active, this'll set the scale to 100%
        # But the screen and text'll be blurry

        Example:
            To start the OpenPulse you must first install all requeriments and
            tip this command in the terminal:
            (Python3)

                $ python pulse.py

        Todo:
            Fix the HighDPI part to not blurry the screen. See more by searching "PyQt5 HighDPI".
    """
    configure_logs()

    # disables vtk terrible error handler
    # you may want to enable them while debugging something
    vtkObject.GlobalWarningDisplayOff()
    vtkLogger.SetStderrVerbosity(vtkLogger.VERBOSITY_OFF)

    # Make the window scale evenly for every monitor
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    if platform.system() == "Windows":
        sys.argv.append("--platform")
        sys.argv.append("windows:dpiawareness=0")

    qdarktheme.enable_hi_dpi()
    app = Application(sys.argv)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
