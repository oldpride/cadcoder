'''
this is a replace tool. it search and replace substring in object labels and properties.
- it starts a dialog
- input for original string; next is a button to search.
- a checkbox below to "case sensitive" or not.
- a checkbox below to "whole word" or not.
- input for new string; next is a button to replace all occurrences.
- a text area below to show search match and replacement result.
- when search or replace properties, if string, easy, if list of strings, replace each element if match, recursively if dict.
- a close button at bottom.
- don't mimic existing replace.FCMacro, or uitools, write from scratch.
'''

import re
from PySide2 import QtWidgets
import PySide2.QtCore as QtCore
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.proptools import propIsReadonly

class ReplaceDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")
        self.resize(400, 600)

        self.oldLabel = QtWidgets.QLabel("From:")
        self.oldInput = QtWidgets.QLineEdit()
        self.newLabel = QtWidgets.QLabel("To:")
        self.newInput = QtWidgets.QLineEdit()
        
        self.caseCheck = QtWidgets.QCheckBox("Case Sensitive")
        self.wholeWordCheck = QtWidgets.QCheckBox("Whole Word")
        self.regexCheck = QtWidgets.QCheckBox("Use RegExp")

        self.findButton = QtWidgets.QPushButton("Find")
        self.findButton.clicked.connect(self.search)

        self.replaceButton = QtWidgets.QPushButton("Replace")
        self.replaceButton.clicked.connect(self.replace)

        self.clearButton = QtWidgets.QPushButton("Clear")
        self.clearButton.clicked.connect(self.clear)

        self.resultArea = QtWidgets.QTextEdit()
        self.resultArea.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout()
        find_row = QtWidgets.QHBoxLayout()
        find_row.addWidget(self.oldLabel)
        find_row.addWidget(self.oldInput)
        find_row.addWidget(self.findButton)
        layout.addLayout(find_row)

        search_row = QtWidgets.QHBoxLayout()
        search_row.addWidget(self.newLabel)
        search_row.addWidget(self.newInput)
        search_row.addWidget(self.replaceButton)
        layout.addLayout(search_row)

        # place the three checkboxes on a single horizontal row
        checks_row = QtWidgets.QHBoxLayout()
        checks_row.addWidget(self.caseCheck)
        checks_row.addWidget(self.wholeWordCheck)
        checks_row.addWidget(self.regexCheck)
        checks_row.addStretch()  # push checkboxes to the left
        layout.addLayout(checks_row)

        # layout.addWidget(self.findButton)
        # layout.addWidget(self.replaceButton)
        layout.addWidget(self.clearButton)
        layout.addWidget(self.resultArea)

        self.setLayout(layout)


    def search_substring(self, 
                         substring: str, # substring or pattern
                         fullstring: str, # full string 
                          case_sensitive: bool, whole_word: bool, use_regex: bool) -> bool:
        if use_regex:
            pattern = substring     
            if whole_word:
                pattern = r'\b' + pattern + r'\b'
            flags = 0 if case_sensitive else re.IGNORECASE
            return re.search(pattern, fullstring, flags) is not None
        else:
            if not case_sensitive:
                fullstring = fullstring.lower() 
                substring = substring.lower()
            if whole_word:
                return fullstring == substring
            else:
                return substring in fullstring

    def search(self):
        self.replace(searchOnly=True)

    def search_old(self):
        old_substring = self.oldInput.text()
        case_sensitive = self.caseCheck.isChecked()
        whole_word = self.wholeWordCheck.isChecked()
        use_regex = self.regexCheck.isChecked()

        if not old_substring:
            self.resultArea.append("Please enter a substring to search.")
            return

        doc = App.ActiveDocument
        if not doc:
            self.resultArea.append("No active document found.")
            return

        flags = 0
        if not case_sensitive:
            flags |= QtCore.Qt.CaseInsensitive

        self.resultArea.append("")
        self.resultArea.append(f"------ Searching for '{old_substring}' ------")

        selection = Gui.Selection.getSelection()
        if not selection:
            selection = doc.Objects

        for obj in sorted(selection, key=lambda o: o.Label):
            if hasattr(obj, 'Label'):
                name = obj.Name
                label = obj.Label
                if self.search_substring(old_substring, name, case_sensitive, whole_word, use_regex):
                    self.resultArea.append(f"Found match in Obj Label='{label}' Name={name}: in name")
            for propName in obj.PropertiesList:
                try:
                    propValue = getattr(obj, propName)
                except Exception:
                    continue
                # search PropName too.
                if self.search_substring(old_substring, propName, case_sensitive, whole_word, use_regex):
                    self.resultArea.append(f"Found match in Obj Label='{label}' Name={name} PropName='{propName}': in PropName")
                matches = self.search_recursively(old_substring, propValue, case_sensitive, whole_word, use_regex)
                if matches:
                    self.resultArea.append(f"Found match in Obj Label='{label}' Name={name} PropName='{propName}': in PropValue: {matches}")
            
        
        self.resultArea.append("------ Search complete ------")

    def search_recursively(self, old_substring, value, case_sensitive, whole_word, use_regex):
        matches = []
        if isinstance(value, str):
            if self.search_substring(old_substring, value, case_sensitive, whole_word, use_regex):
                matches.append(value)
        elif isinstance(value, list) or isinstance(value, tuple):
            for v in value:
                matches.extend(self.search_recursively(old_substring, v, case_sensitive, whole_word, use_regex))
        return matches

    def replace_string(self,
                        old_substring: str, # substring or pattern to replace
                        new_substring: str, # replacement substring
                        fullstring: str, # full string
                        case_sensitive: bool, whole_word: bool, use_regex: bool) -> str:
        if use_regex:
            pattern = old_substring
            if whole_word:
                pattern = r'\b' + pattern + r'\b'
            flags = 0 if case_sensitive else re.IGNORECASE
            if re.search(pattern, fullstring, flags):
                return re.sub(pattern, new_substring, fullstring, flags)
            else:
                return fullstring
        else:
            if not case_sensitive:
                fullstring_lower = fullstring.lower()
                old_substring_lower = old_substring.lower()
            else:
                fullstring_lower = fullstring
                old_substring_lower = old_substring

            if whole_word:
                if fullstring_lower == old_substring_lower:
                    return new_substring
                else:
                    return fullstring
            else:
                if not case_sensitive:
                    # perform case-insensitive replacement
                    pattern = re.compile(re.escape(old_substring), re.IGNORECASE)
                    return pattern.sub(new_substring, fullstring)
                else:
                    return fullstring.replace(old_substring, new_substring)

    def replace(self, searchOnly=False):
        old_substring = self.oldInput.text()
        new_substring = self.newInput.text()
        case_sensitive = self.caseCheck.isChecked()
        whole_word = self.wholeWordCheck.isChecked()
        use_regex = self.regexCheck.isChecked()

        if not old_substring:
            self.resultArea.append("Please enter a substring to replace.")
            return

        doc = App.ActiveDocument
        if not doc:
            self.resultArea.append("No active document found.")
            return

        flags = 0
        if not case_sensitive:
            flags |= QtCore.Qt.CaseInsensitive

        self.resultArea.append("")
        if searchOnly:
            self.resultArea.append(f"------ Searching '{old_substring}' ------")
        else:
            self.resultArea.append(f"------ Replacing '{old_substring}' with '{new_substring}' ------")

        selection = Gui.Selection.getSelection()

        if not selection:
            selection = doc.Objects

        for obj in sorted(selection, key=lambda o: o.Label):
            self.resultArea.append(f"Searching in Obj Label='{obj.Label}' Name={obj.Name}")
            if hasattr(obj, 'Label'):
                name = obj.Name
                label = obj.Label
                if self.search_substring(old_substring, name, case_sensitive, whole_word, use_regex):
                    self.resultArea.append(f"Found match in Obj Label='{label}' Name={name}: in name; cannot change.")
            for propName in sorted(obj.PropertiesList):
                # try:
                #     propValue = getattr(obj, propName)
                # except Exception:
                #     continue
                propValue = getattr(obj, propName)

                has_match = 0
                # search PropName too.
                if self.search_substring(old_substring, propName, case_sensitive, whole_word, use_regex):
                    self.resultArea.append(f"Found match in Obj Label='{label}' Name={name} PropName='{propName}': in PropName")
                    has_match = 1
                matches = self.search_recursively(old_substring, propValue, case_sensitive, whole_word, use_regex)
                if matches:
                    has_match = 1
                    self.resultArea.append(f"Found match in Obj Label='{label}' Name={name} PropName='{propName}': in PropValue: {matches}")
                
                if searchOnly or has_match == 0:
                    continue
           
                oldValue = propValue
                newValue = self.replace_recursively(old_substring, new_substring, oldValue, case_sensitive, whole_word, use_regex)
                if newValue != oldValue:
                    # if the prop is read-only, change it read-write first
                    was_readonly = propIsReadonly(obj, propName)
                    if was_readonly:
                        print(f"Obj Label={label}'s Property '{propName}' is read-only, temporarily making it writable.")
                        saved_statusnums = obj.getPropertyStatus(propName)
                        obj.setEditorMode(propName, 0)  # 0: visible + editable, 1: hidden, 2: read-only 
                    setattr(obj, propName, newValue)
                    if was_readonly:
                        # restore status
                        obj.setPropertyStatus(propName, saved_statusnums)
                    self.resultArea.append(f"Updated obj Label='{label}' Name={name} PropName='{propName}' Value from '{oldValue}' to '{newValue}'")
        doc.recompute()
        self.resultArea.append("------ Replacement complete ------")

    def replace_recursively(self, old_substring, new_substring, value, case_sensitive, whole_word, use_regex):
        if isinstance(value, str):
            return self.replace_string(old_substring, new_substring, value, case_sensitive, whole_word, use_regex)
        elif isinstance(value, list) or isinstance(value, tuple):
            return [self.replace_recursively(old_substring, new_substring, v, case_sensitive, whole_word, use_regex) for v in value]
        return value
    
    def clear(self):
        self.resultArea.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    else:
        print("Using existing QApplication instance.")

    dialog = ReplaceDialog()

    # dialog.exec_()
    # when running inside FreeCAD, do not call app.exec_(), otherwise we get error
    #    QCoreApplication::exec: The event loop is already running
    
    dialog.show()
