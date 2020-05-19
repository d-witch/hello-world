from WafLogQuery.UI.UI_Dialog_RuleDetail import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class RuleDetailDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.model = QStandardItemModel(10, 3, self)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableView.horizontalHeader().hide()
        self.ui.tableView.verticalHeader().hide()
        self.ui.tableView.setSpan(0, 0, 5, 1)
        self.ui.tableView.setSpan(5, 0, 4, 1)
        self.ui.tableView.setSpan(9, 1, 1, 2)

        detail_title = ['规则名称', '规则ID', '告警类型', '危险等级', '准确度', '操作系统', 'WEB服务器', '数据库', '编程语言']
        for r in range(len(detail_title)):
            self.model.setItem(r, 1, QStandardItem(detail_title[r]))
        self.model.setItem(0, 0, QStandardItem('规则概述'))
        self.model.setItem(5, 0, QStandardItem('影响范围'))
        self.model.setItem(9, 0, QStandardItem('详细说明'))

    def set_data(self, detail):
        for i in range(9):
            self.model.setItem(i, 2, QStandardItem(detail[i]))
        self.model.setItem(9, 1, QStandardItem(detail[9]))

        head = self.ui.tableView.horizontalHeader()
        head.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        head.setSectionResizeMode(2, QHeaderView.Stretch)

        v_head = self.ui.tableView.verticalHeader()
        v_head.setSectionResizeMode(9, QHeaderView.ResizeToContents)
