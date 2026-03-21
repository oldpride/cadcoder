from PySide import QtGui
import FreeCADGui as Gui

def clear_report_view():
    """Clears the content of the FreeCAD Report View."""
    mw = Gui.getMainWindow()
    report_view = mw.findChild(QtGui.QTextEdit, "Report view")
    if report_view:
        report_view.clear()
    else:
        print("Report View widget not found.")

def main():
    """Main function to clear the Report View."""
    clear_report_view()
if __name__ == "__main__":
    main()
