from rezgui.qt import QtCore, QtGui
from rezgui.objects.App import app
from rezgui.widgets.ToolWidget import ToolWidget


class VariantToolsList(QtGui.QTableWidget):
    def __init__(self, parent=None):
        super(VariantToolsList, self).__init__(0, 1, parent)
        self.variant = None
        self.context = None
        self.tool_widgets = {}

        self.setGridStyle(QtCore.Qt.DotLine)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        hh = self.horizontalHeader()
        hh.setStretchLastSection(True)
        hh.setVisible(False)
        vh = self.verticalHeader()
        vh.setVisible(False)

        app.process_tracker.instanceCountChanged.connect(self._instanceCountChanged)

    def clear(self):
        super(VariantToolsList, self).clear()
        self.setEnabled(False)
        self.tool_widgets = {}

    def refresh(self):
        variant = self.variant
        self.variant = None
        self.set_variant(variant)

    def set_context(self, context):
        self.context = context
        self.variant = None

    def set_variant(self, variant):
        if variant == self.variant:
            return

        if variant is None:
            self.clear()
        else:
            tools = sorted(variant.tools or [])
            self.setRowCount(len(tools))
            self.setEnabled(True)
            self.tool_widgets = {}

            for i, tool in enumerate(tools):
                widget = ToolWidget(self.context, tool, app.process_tracker)
                widget.clicked.connect(self._clear_selection)
                self.setCellWidget(i, 0, widget)
                self.tool_widgets[tool] = widget

            select_mode = QtGui.QAbstractItemView.SingleSelection \
                if self.context else QtGui.QAbstractItemView.NoSelection
            self.setSelectionMode(select_mode)

        self.variant = variant

    def _clear_selection(self):
        self.clearSelection()
        self.setCurrentIndex(QtCore.QModelIndex())

    def _instanceCountChanged(self, context_id, tool_name, num_procs):
        if self.context is None or context_id != id(self.context):
            return

        widget = self.tool_widgets.get(str(tool_name))
        if widget:
            widget.set_instance_count(num_procs)
