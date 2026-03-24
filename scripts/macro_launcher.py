import sys
import os
import runpy
import traceback
import json
from PySide2 import QtWidgets
from PySide2.QtCore import QDir
import shlex


debug = 0

# macro_launcher.py
# Works with PySide2 or PyQt5.

'''
to add this macro to FreeCAD's toolbar to launch it easily, do the following:
Open menu Tools -> Customize
Under the "Macros" tab, select our macro_launcher.py macro, 
fill in the details. I picked Airplane icon for its pixmap.

Under the "Toolbars" tab, create a new custom toolbar in the workbench
on the right, select "Global". 
    Click "New Toolbar", name it "My Macros".
    you can also choose an existing custom toolbar if you already have one.
    I couldn't fingure out how to add it to an existing built-in toolbar.
on the left, search for this macro by name,
    select it and click "Add" to add it to the toolbar.
click "Close" to finish.

We need to switch a workbench to see the new toolbar.
'''

debug = 0


'''
to add this macro to FreeCAD's toolbar to launch it easily, do the following:
Open menu Tools -> Customize
Under the "Macros" tab, select our macro_launcher.py macro, 
fill in the details. I picked Airplane icon for its pixmap.

Under the "Toolbars" tab, create a new custom toolbar in the workbench
on the right, select "Global". 
    Click "New Toolbar", name it "My Macros".
    you can also choose an existing custom toolbar if you already have one.
    I couldn't fingure out how to add it to an existing built-in toolbar.
on the left, search for this macro by name,
    select it and click "Add" to add it to the toolbar.
click "Close" to finish.

We need to switch a workbench to see the new toolbar.
'''

class MacroLauncher(QtWidgets.QDialog):
    def __init__(self, config_json, parent=None):
        super().__init__(parent)

        self.progdir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = config_json
        self.setWindowTitle("Macro Launcher")
        self.resize(900, 600)

        # list originally imported modules
        self.original_modules = set(sys.modules.keys())
    
        '''
        json file: macro_launcher_config.json

        {
            "macro_root": "<path_to_macro_root>",
            "extra_pythonpaths": [
                "<path1>",
                "<path2>"
            ],
            "past_cmdlines": [
                "cmd1 arg11 arg12",
                "cmd2 arg21 arg22"
            ],
            "clear_reportview_before_run": true
        }
        '''
        
        # load json config
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
                if debug:
                    print(f"Loaded config from {self.config_path}: {self.config}")
        else:
            self.config = {}

        macro_root = self.config.get("macro_root")
        if not macro_root:
            macro_root = os.path.dirname(os.path.abspath(__file__))
            # save back
            self.config["macro_root"] = macro_root
            self.save_config()
    
        # Left: file tree
        self.model = QtWidgets.QFileSystemModel(self)
        self.model.setNameFilters(["*.py", "*.FCMacro"])
        self.model.setNameFilterDisables(False)
        self.model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        self.model.setRootPath(macro_root)

        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(macro_root))
        self.tree.setColumnWidth(0, 300)
        # hide irrelevant columns
        for c in range(1, self.model.columnCount()):
            self.tree.hideColumn(c)

        self.cmdline = QtWidgets.QLineEdit()
        self.cmdline.setPlaceholderText("Enter command and arguments")

        # right: past commands list
        self.past_cmdlines_widget = QtWidgets.QListWidget()
        self.past_cmdlines_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # load past commands from config
    
        for cmdline in self.config.get("past_cmdlines", []):
            self.past_cmdlines_widget.addItem(cmdline)

        # right: pattern of extra traced files
        self.file_trace_pattern_lineedit = QtWidgets.QLineEdit()
        self.file_trace_pattern_lineedit.setPlaceholderText("Enter regex pattern for extra traced files")
        self.file_trace_pattern_lineedit.setText(self.config.get("file_trace_pattern", ""))
        self.file_trace_pattern_lineedit.textChanged.connect(self.on_file_trace_pattern_changed)

        self.func_trace_pattern_lineedit = QtWidgets.QLineEdit()
        self.func_trace_pattern_lineedit.setPlaceholderText("Enter regex pattern for extra traced functions")
        self.func_trace_pattern_lineedit.setText(self.config.get("func_trace_pattern", ""))
        self.func_trace_pattern_lineedit.textChanged.connect(self.on_func_trace_pattern_changed)

        # Right: PYTHONPATH list + controls
        self.path_list = QtWidgets.QListWidget()
        self.path_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        pypath_add_btn = QtWidgets.QPushButton("Add")
        pypath_remove_btn = QtWidgets.QPushButton("Remove")
        pypath_move_up_btn = QtWidgets.QPushButton("Move up")
        pypath_move_down_btn = QtWidgets.QPushButton("Move down")
        close_btn = QtWidgets.QPushButton("Close")
        pypath_btn_layout = QtWidgets.QHBoxLayout()
        pypath_btn_layout.addWidget(pypath_add_btn)
        pypath_btn_layout.addWidget(pypath_remove_btn)
        pypath_btn_layout.addWidget(pypath_move_up_btn)
        pypath_btn_layout.addWidget(pypath_move_down_btn)
        pypath_btn_layout.addStretch()
        pypath_btn_layout.addWidget(close_btn)

        

        cmd_layout = QtWidgets.QVBoxLayout()
        cmd_layout.addWidget(QtWidgets.QLabel("Past command lines:"))
        cmd_layout.addWidget(self.past_cmdlines_widget)
        cmd_layout.addWidget(QtWidgets.QLabel("Command and arguments:"))
        cmd_layout.addWidget(self.cmdline)

        self.clear_reportview_checkbox = QtWidgets.QCheckBox("Clear Report View")
        self.clear_reportview_checkbox.setChecked(self.config.get("clear_reportview_before_run", False))
        self.clear_reportview_checkbox.stateChanged.connect(self.on_clear_checkbox_changed)

        self.enable_trace_checkbox = QtWidgets.QCheckBox("Enable Trace")
        self.enable_trace_checkbox.setChecked(self.config.get("enable_trace", False))
        self.enable_trace_checkbox.stateChanged.connect(self.on_enable_trace_checkbox_changed)
        
        cmd_run_btn = QtWidgets.QPushButton("Run")
        cmd_run_btn.setEnabled(False)

        cmd_btn_layout = QtWidgets.QHBoxLayout()
        cmd_btn_layout.addWidget(self.clear_reportview_checkbox)
        cmd_btn_layout.addWidget(self.enable_trace_checkbox)
        cmd_btn_layout.addStretch()
        cmd_btn_layout.addWidget(cmd_run_btn)   
        cmd_layout.addLayout(cmd_btn_layout)

        tree_btn_layout = QtWidgets.QHBoxLayout()
        tree_change_root_btn = QtWidgets.QPushButton("Change Root")
        tree_change_root_btn.setAutoDefault(False)
        tree_change_root_btn.setDefault(False)
        
        tree_btn_layout.addWidget(tree_change_root_btn)
        tree_btn_layout.addStretch()
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.tree)
        left_layout.addLayout(tree_btn_layout)
      
        right_layout = QtWidgets.QVBoxLayout()   
        right_layout.addLayout(cmd_layout, 6)
        
        right_layout.addWidget(QtWidgets.QLabel("extra file trace pattern (regex):"))
        right_layout.addWidget(self.file_trace_pattern_lineedit)

        right_layout.addWidget(QtWidgets.QLabel("extra function trace pattern (regex):"))
        right_layout.addWidget(self.func_trace_pattern_lineedit)

        right_layout.addWidget(QtWidgets.QLabel(""))
        right_layout.addWidget(QtWidgets.QLabel("Extra PYTHONPATH entries (applied while running):"))
        extra_paths = self.config.get("extra_pythonpaths", [])
        for p in extra_paths:
            self.path_list.addItem(p)
        right_layout.addWidget(self.path_list,1)
        right_layout.addLayout(pypath_btn_layout,1)
        
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        for btn in [pypath_add_btn, pypath_remove_btn, pypath_move_up_btn, pypath_move_down_btn, close_btn,
                     tree_change_root_btn]:
            # prevent button default behavior, which pops up a file brower dialog when pressing Enter key in a QLineEdit
            btn.setAutoDefault(False)
            btn.setDefault(False)

        # Signals
        self.tree.selectionModel().selectionChanged.connect(self.on_tree_selection_changed)
        self.tree.doubleClicked.connect(self.on_double_click_tree)

        # self.past_cmdlines_widget.selectionModel().selectionChanged.connect(self.on_past_cmdline_selection_changed) # this works too.
        self.past_cmdlines_widget.currentItemChanged.connect(self.on_past_cmdline_selection_changed) # this works too.
        self.past_cmdlines_widget.doubleClicked.connect(self.on_double_click_past_cmdline)

        # if cmdline args change, update selected label if needed
        self.cmdline.textChanged.connect(lambda: self.on_tree_selection_changed(None, None))

        pypath_add_btn.clicked.connect(self.add_path)
        pypath_remove_btn.clicked.connect(self.remove_selected_paths)
        pypath_move_up_btn.clicked.connect(lambda: self.move_selected(-1))
        pypath_move_down_btn.clicked.connect(lambda: self.move_selected(1))
        tree_change_root_btn.clicked.connect(self.change_root)
        cmd_run_btn.clicked.connect(self.run_selected)
        close_btn.clicked.connect(self.close)

        self._run_btn = cmd_run_btn
        self.run_source = None
                
    def save_config(self):     
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def on_clear_checkbox_changed(self, state):
        self.config["clear_reportview_before_run"] = bool(state)
        self.save_config()

    def on_enable_trace_checkbox_changed(self, state):
        self.config["enable_trace"] = bool(state)
        self.save_config()

    def on_tree_selection_changed(self, selected, deselected):
        # find out what kind change it is
        # print(f"on_tree_selection_changed: selected={selected}, deselected={deselected}")
        if selected is None:
            # someone else selected/deselected something. we ignore it
            return

        index = self.tree.currentIndex()
        if not index.isValid():
            print(f"Invalid tree selection index={index}")
            return
        path = self.model.filePath(index)
        print(f"Selected path: {path}")
        if os.path.isfile(path) and (path.lower().endswith(".py") or path.lower().endswith(".fcmacro")):
            self.cmdline.setText(path)
            self._run_btn.setEnabled(True)
            self.run_source = "tree"

    def on_past_cmdline_selection_changed(self, selected, deselected):
        # print(f"on_past_cmdline_selection_changed: selected={selected}, deselected={deselected}")
        if selected is None:
            # someone else selected/deselected something. we ignore it
            return
        index = self.past_cmdlines_widget.currentIndex()
        if not index.isValid():
            print(f"Invalid past cmdline selection index={index}")
            return
        cmdline = self.past_cmdlines_widget.item(index.row()).text()
        # self.selected_label.setText(f"Selected: {cmdline}")
        self.cmdline.setText(cmdline)
        self.run_source = "past_cmdline"
        self._run_btn.setEnabled(True)

    def on_double_click_tree(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path) and (path.lower().endswith(".py") or path.lower().endswith(".fcmacro")):
            # self.run_path(path)
            cmdline = path
            self.run_cmdline(cmdline)

    def on_double_click_past_cmdline(self, index):
        cmdline = self.past_cmdlines_widget.item(index.row()).text()
        self.run_cmdline(cmdline)

    def add_path(self):
        d = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder to add to PYTHONPATH", os.getcwd())
        if d:
            # avoid duplicates
            for i in range(self.path_list.count()):
                if self.path_list.item(i).text() == d:
                    return
            self.path_list.addItem(d)
            self.config["extra_pythonpaths"] = self._gather_extra_paths()
            self.save_config()

    def remove_selected_paths(self):
        for item in list(self.path_list.selectedItems()):
            self.path_list.takeItem(self.path_list.row(item))
        self.config["extra_pythonpaths"] = self._gather_extra_paths()
        self.save_config()

    def move_selected(self, delta):
        sel = self.path_list.selectedItems()
        if not sel:
            return
        items = sel
        rows = sorted(set(self.path_list.row(it) for it in items))
        if delta < 0:
            for r in rows:
                if r + delta < 0:
                    continue
                it = self.path_list.takeItem(r)
                self.path_list.insertItem(r + delta, it)
                it.setSelected(True)
        else:
            for r in reversed(rows):
                if r + delta >= self.path_list.count():
                    continue
                it = self.path_list.takeItem(r)
                self.path_list.insertItem(r + delta, it)
                it.setSelected(True)
        self.config["extra_pythonpaths"] = self._gather_extra_paths()
        self.save_config()

    def on_file_trace_pattern_changed(self, text):
        self.config["file_trace_pattern"] = text
        self.save_config()

    def on_func_trace_pattern_changed(self, text):
        self.config["func_trace_pattern"] = text
        self.save_config()

    def change_root(self):
        d = QtWidgets.QFileDialog.getExistingDirectory(self, "Select macros root folder", self.model.rootPath())
        if d:
            self.model.setRootPath(d)
            self.tree.setRootIndex(self.model.index(d))
            self.config["macro_root"] = d
            self.save_config()

    def run_selected(self):
        # if self.run_source == "past_cmdline":
        #     try:
        #         index = self.past_cmdlines_widget.currentIndex()
        #         cmdline = self.past_cmdlines_widget.item(index.row()).text()
        #     except:
        #         self.run_source = None
        #         self._run_btn.setEnabled(False)
        #         return
        #     self.run_cmdline(cmdline)   
        # elif self.run_source == "tree":
        #     index = self.tree.currentIndex()
        #     path = self.model.filePath(index)
        #     if os.path.isfile(path):
        #         self.run_path(path)

        cmdline = self.cmdline.text().strip()
        if not cmdline:
            return
        self.run_cmdline(cmdline)

    def _gather_extra_paths(self):
        return [self.path_list.item(i).text() for i in range(self.path_list.count())]

    # def run_path(self, path):
    #     extra_command_args = self.cmdline.text().strip()

    #     # split args using shlex
    #     if extra_command_args:
    #         sys.argv = [path] + shlex.split(extra_command_args)
    #         cmdline = path + " " + extra_command_args
    #     else:
    #         sys.argv = [path]
    #         cmdline = path

    #     # save this command to past commands, at the top
    #     self.update_cmdlines(cmdline)

    #     self.run_path_with_sys_argv(path)

    def unimport_modules(self):
        '''
        unimport later imported modules, so that we can pick up changes in modules.

        note: 
            closing this script may not unimport modules, because FreeCAD,
            which is this script's parent, keeps them in memory.

        therefore, we have to close FreeCAD to fully unload modules.
        '''
        to_remove = []
        for modname in sorted(sys.modules.keys()):
            if modname not in self.original_modules:
                to_remove.append(modname)
        if debug:
            print(f"Unimporting modules: {to_remove}")
        for modname in to_remove:
            del sys.modules[modname]
        
    def run_path_with_sys_argv(self, path):
        # clear report view if needed
        if self.config.get("clear_reportview_before_run", False):
            self.clear_report_view()

        trace_enabled = self.config.get("enable_trace", False)

        extra_pythonpaths = self._gather_extra_paths()
        # prepend extras to sys.path
        orig_sys_path = list(sys.path)
        for p in reversed(extra_pythonpaths):
            if p not in sys.path:
                sys.path.insert(0, p)

        # unimport later imported modules, so we can pick up changes in those modules.
        self.unimport_modules()

        try:
            # Execute the file as a script (like running it directly)
            # runpy.run_path(path, run_name="__main__", init_globals={"trace_enabled": trace_enabled})
            # runpy.run_path(path, run_name="__main__")
            from cadcoder.tracetools import trace_file
            # print(f"trace_file path='{path}', enabled={trace_enabled}")
            trace_file(path, 
                       enabled=trace_enabled, 
                       filePattern=self.config.get("file_trace_pattern", ""),
                       funcPattern=self.config.get("func_trace_pattern", ""),
                       )
        except Exception:
            # tb = traceback.format_exc()
            # QtWidgets.QMessageBox.critical(self, "Error while running macro", tb)
            print(f"Error while running macro: {traceback.format_exc()}")
        except SystemExit as e:
            # catch sys.exit() calls; otherwise if called script may exit FreeCAD too.
            print(f"Macro exited with code: {e.code}")
        finally:
            # restore sys.path
            sys.path[:] = orig_sys_path

            # unimport later imported modules
            self.unimport_modules()

    def update_cmdlines(self, cmdline):
        # add the cmdline to the top of the past commands list
        self.config["past_cmdlines"] = [cmdline]
        for i in range(self.past_cmdlines_widget.count()):
            cl = self.past_cmdlines_widget.item(i).text()
            if cl == cmdline:
                continue
            self.config["past_cmdlines"].append(cl)

        # limit entries
        self.config["past_cmdlines"] = self.config["past_cmdlines"][:100]

        # update the list widget
        self.past_cmdlines_widget.clear()
        for cl in self.config["past_cmdlines"]:
            self.past_cmdlines_widget.addItem(cl)

        # save to file
        self.save_config()

    def run_cmdline(self, cmdline):
        parts = shlex.split(cmdline)
        if not parts:
            return
        path = parts[0]
        
        # the rest are args
        sys.argv = parts

        self.update_cmdlines(cmdline)
        self.run_path_with_sys_argv(path)

    def clear_report_view(self):
        """
        Clears the content of the FreeCAD Report View.
        run reportview_clear.py macro in the same folder as this macro.
        """
        reportview_clear_macro = os.path.join(self.progdir, "reportview_clear.py")
        try:
            # Execute the file as a script (like running it directly)
            runpy.run_path(reportview_clear_macro, run_name="__main__")
        except Exception:
            tb = traceback.format_exc()
            QtWidgets.QMessageBox.critical(self, "Error while running macro", tb)


def main():
    # app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    # default macros path hint: current working directory
    # dlg = MacroLauncher(root=os.getcwd())
    progname = os.path.basename(__file__)
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".MyCAD")
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    config_file = progname.replace('.py', '_config.json')
    config_json = os.path.join(config_dir, config_file)

    dlg = MacroLauncher(config_json)

    dlg.show()

    # app.exec_()
    # when running inside FreeCAD, do not call app.exec_(), otherwise we get error
    #    QCoreApplication::exec: The event loop is already running

if __name__ == "__main__":
    main()
