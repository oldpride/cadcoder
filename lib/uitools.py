import os
from PySide2 import QtWidgets, QtCore, QtGui
import FreeCAD as App
import FreeCADGui as Gui
import json

class FormDialog(QtWidgets.QDialog):
    labels: list = []

    def __init__(self, labels: list):
        super(FormDialog, # this is myself
              self).__init__()
        self.setWindowTitle("My Custom Dialog")
        self.labels = labels
        print("hello4")
        self.setup_ui()
        
    def setup_ui(self):
        # Create layout and widgets
        layout = QtWidgets.QVBoxLayout()

        self.user_input_widget = {}

        print(f"labels={self.labels}")

        for label in self.labels:
            lbl = QtWidgets.QLabel(label)
            line_edit = QtWidgets.QLineEdit()
            layout.addWidget(lbl)
            layout.addWidget(line_edit)
            self.user_input_widget[label] = line_edit

            # # Example: Add a line edit for text input
            # self.text_label = QtWidgets.QLabel("From:")
            # self.text_input = QtWidgets.QLineEdit()
            # layout.addWidget(self.text_label)
            # layout.addWidget(self.text_input)

            # ## Example: Add a spin box for numerical input
            # #self.number_label = QtWidgets.QLabel("To:")
            # #self.number_input = QtWidgets.QSpinBox()
            # #self.number_input.setRange(0, 100)
            # #layout.addWidget(self.number_label)
            # #layout.addWidget(self.number_input)

            # # Example: Add a line edit for text input
            # self.text_label = QtWidgets.QLabel("To:")
            # self.text_input = QtWidgets.QLineEdit()
            # layout.addWidget(self.text_label)
            # layout.addWidget(self.text_input)


        # Add OK and Cancel buttons
        self.buttons= QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def get_values(self):
        user_input = {}
        for label, widget in self.user_input_widget.items():
            user_input[label] = widget.text()
        return user_input

class TextDialog:
    """Show a text dialog"""
    config = {}

    def __init__(self):
        # get caller's progname
        import inspect
        caller_path = inspect.stack()[1].filename
        self.progname = os.path.basename(caller_path)
        self.homedir = os.path.expanduser('~')
        self.savedir = os.path.join(self.homedir, '.MyCAD')
        self.hist_file = self.progname.replace('.py', '_hist.json').replace('.FCMacro', '_hist.json')
        self.hist_json = os.path.join(self.savedir, self.hist_file)
        # macro_dir = App.getUserMacroDir(True)
        self.module_dir = os.path.dirname(os.path.abspath(__file__))
        self.ui_file = os.path.join(self.module_dir, 'uitools_TextDialog.xml')
        print(f"ui_file={self.ui_file}")
        self.form = Gui.PySideUic.loadUi(self.ui_file)
        self.form.pushButtonClose.pressed.connect(self.close_callback)
        self.form.show()

        '''
        - save the generated script to a .py file - add both "Save As" and "Save" buttons.
        - allow user to browse to select the output .py file path
        - the dir of the .py file remembered in the same dir as this macro,
        - the file is a json file, macroname_hist.json.
        - config file has
            {
                "last_output_dir": "/home/user/macros/",
                "last_output_file": "mymaco.py",
            }
        '''
        os.makedirs(self.savedir, exist_ok=True)
        if os.path.exists(self.hist_json):
            with open(self.hist_json, 'r') as f:
                try:
                    self.config = json.load(f)
                except:
                    self.config = {}

        self.save_hist_save_button = QtWidgets.QPushButton('Save')
        self.save_hist_save_button.pressed.connect(self.save_script)
        self.form.pushButtonClose.parent().layout().addWidget(self.save_hist_save_button)
        self.save_as_button = QtWidgets.QPushButton('Save As')
        self.save_as_button.pressed.connect(self.save_script_as)
        self.form.pushButtonClose.parent().layout().addWidget(self.save_as_button)

        # show last saved file path label
        self.last_label = QtWidgets.QLabel()
        self.last_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.update_last_saved_label()
        self.form.pushButtonClose.parent().layout().addWidget(self.last_label)

    def close_callback(self):
        # print("Closing ObjectsToPython dialog.")
        self.form.close()

    def save_hist(self):
        with open(self.hist_json, 'w') as f:
            json.dump(self.config, f, indent=4)

    # add Save, Save As buttons to dialog

    def save_script(self):
        if self.config.get('last_output_file', None) is None:
            self.save_script_as()
            return

        script_text = self.form.textEdit.toPlainText()
        full_output_path = os.path.join(self.config['last_output_dir'], self.config['last_output_file'])
        try:
            with open(full_output_path, 'w') as f:
                f.write(script_text)
            App.Console.PrintMessage(f'Script saved to {full_output_path}\n')
        except Exception as e:
            App.Console.PrintError(f'Error saving script to {full_output_path}: {e}\n')


    def save_script_as(self):
        if 'last_output_dir' in self.config:
            full_output_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.form, "Save Script As", self.config['last_output_dir'], "Python Files (*.py *.FCMacro)")
        else:
            full_output_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.form, "Save Script As", "", "Python Files (*.py *.FCMacro)")
        if full_output_path:
            self.config['last_output_file'] = os.path.basename(full_output_path)
            self.config['last_output_dir'] = os.path.dirname(full_output_path)
            self.save_hist()
            self.save_script()
            self.update_last_saved_label()

    def update_last_saved_label(self):
        if 'last_output_dir' not in self.config or 'last_output_file' not in self.config:
            self.last_label.setText("Last saved: none")
            self.last_label.setToolTip("")
            return
        full_output_path = os.path.join(self.config['last_output_dir'], self.config['last_output_file'])
        self.last_label.setText(f"Last saved: {full_output_path}")
        self.last_label.setToolTip(full_output_path)
