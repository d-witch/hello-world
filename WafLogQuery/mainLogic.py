from WafLogQuery.UI.UI_MainWindow import Ui_MainWindow
from dialog_http_msg import HttpMsgDialog
from dialog_rule_detail import RuleDetailDialog
from PyQt5.QtWidgets import \
    QMainWindow, QAbstractItemView, QFileDialog, QCheckBox, QLineEdit, QComboBox, QDateTimeEdit, QMessageBox, QHeaderView
from PyQt5.QtCore import pyqtSlot, QModelIndex, QDateTime, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from os import getcwd
import pandas as pd
import base64
from math import ceil


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cols = ['告警发生时间', '告警类型', '服务器IP', '客户端IP', '域名', 'URI', '匹配规则',
                     'HTTP请求或者响应信息', '国家名字', '站点ID', '匹配策略', '告警信息', '匹配特征', '浏览器标识']

        self.display_cols = ['告警发生时间', '告警类型', '服务器IP', '客户端IP', '域名', 'URI', '匹配规则',
                             'HTTP请求或者响应信息', '国家名字']

        self.df = None
        self.result_df = None

        self.model = QStandardItemModel(20, 9, self)
        self.model.setHorizontalHeaderLabels(self.display_cols)

        self.ui.tableView.setModel(self.model)

        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.tableView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectItems)

        self.ui.tableView.setAlternatingRowColors(True)
        self.ui.tableView.verticalHeader().setDefaultSectionSize(22)
        # self.ui.tableView.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.ui.tableView.setEnabled(False)

        self.ui.btn_pre.setEnabled(False)
        self.ui.btn_next.setEnabled(False)
        self.ui.btn_go.setEnabled(False)

        self.cur_page = 1
        self.page_amount = 0

        cur_datetime = QDateTime().currentDateTime()
        self.ui.dte_start.setDateTime(cur_datetime)
        self.ui.dte_end.setDateTime(cur_datetime)

        self.ui.frame_condition.setVisible(False)

        temp_rule_detail_df = pd.read_excel('./Crawl/crawl_data/detail.xlsx', usecols=[1, 2])
        self.rule_detail_dict = {str(i): name for i, name in zip(temp_rule_detail_df['rule_id'], temp_rule_detail_df['name'])}

        self.condition_frame()

        self.dialog_msg_font_size = 12

        self.rule_detail_df = pd.read_excel('./Crawl/crawl_data/detail.xlsx')
        self.rule_detail_df['rule_id'] = self.rule_detail_df['rule_id'].astype(str)

    def condition_frame(self):
        # 设置控件属性
        self.set_property()
        # 关联槽函数
        self.multi_connect()

    def set_property(self):
        """
        设置frame_condition内部控件属性，
        frame_condition内部变动时，需修改该方法
        :return:
        """
        buddy_list = [None, 'server_ip', 'server_ip', 'client_ip', 'client_ip', 'event', 'event', 'rule', 'rule',
                      'uri', 'uri', 'datetime', 'datetime', 'datetime', None]
        b = 0
        for i in self.ui.frame_condition.children():
            i.setProperty('buddy', buddy_list[b])
            b += 1

    def multi_connect(self):
        """
        将frame_condition内多个checkbox toggled信号连接到槽函数
        :return:
        """
        for i in self.ui.frame_condition.findChildren(QCheckBox):
            i.toggled.connect(self.do_condition_slot)

    def do_condition_slot(self, check):
        """
        1.将checkbox与含有相同buddy属性的控件相联系，根据checked信号设置相关控件是否enabled
        2.根据checkbox，设置查找按钮是否启用
        :param check:
        :return:
        """
        # 信号发送者
        sender = self.sender()
        for i in self.ui.frame_condition.findChildren((QLineEdit, QComboBox, QDateTimeEdit)):
            if sender.property('buddy') == i.property('buddy'):
                i.setEnabled(check)
        for i in self.ui.frame_condition.findChildren(QCheckBox):
            if i.isChecked():
                self.ui.btn_find.setEnabled(True)
                break
            self.ui.btn_find.setEnabled(False)

    @pyqtSlot()
    def on_btn_condition_clicked(self):
        if self.ui.frame_condition.isVisible():
            self.ui.frame_condition.setVisible(False)
        else:
            self.ui.frame_condition.setVisible(True)

    @pyqtSlot()
    def on_action_open_triggered(self):
        cur_dir = getcwd()
        filename, flt = QFileDialog.getOpenFileName(self, '打开日志文件', cur_dir, '日志文件(*.csv);;所有文件(*.*)')
        if not filename:
            return
        self.init_table(filename)

    def init_table(self, filename):
        # 日志文件中站点名称列编码为utf-8与其他列编码gbk不同，导致解码错误
        with open(filename, errors='ignore') as f:
            self.df = pd.read_csv(f, usecols=self.cols)
        # 调整列的顺序
        self.df = self.df[self.cols]
        # 修改告警发生时间列的数据类型为datetime类型
        self.df['告警发生时间'] = pd.to_datetime(self.df['告警发生时间'])
        # 修改匹配规则列，由rule_id替换为规则名称
        self.df['匹配规则'] = self.df['匹配规则'].apply(lambda s: self.rule_detail_dict.get(s, 'None'))

        self.update_model(self.df, 0, 20 if len(self.df) > 20 else len(self.df))

        self.ui.tableView.setEnabled(True)
        self.ui.btn_next.setEnabled(True)
        self.ui.btn_go.setEnabled(True)

        self.hint_widget_display()

    def update_model(self, df, start_row, end_row):
        """
        更新模型数据
        :param df:
        :param start_row:
        :param end_row:
        :return:
        """
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.display_cols)
        for row in range(start_row, end_row):
            for column in range(9):
                if column == 7:
                    try:
                        http_message = base64.b64decode(df.iloc[row, column]).decode()
                    # 消息存在为"None"的情况
                    except UnicodeDecodeError:
                        http_message = str(df.iloc[row, column])
                    item = QStandardItem(http_message)
                    self.model.setItem(row - start_row, column, item)
                else:
                    item = QStandardItem(str(df.iloc[row, column]))
                    self.model.setItem(row-start_row, column, item)

        # 调整模式需要在model设置后添加
        head = self.ui.tableView.horizontalHeader()
        head.setSectionResizeMode(QHeaderView.ResizeToContents)
        head.setSectionResizeMode(5, QHeaderView.Stretch)
        head.setSectionResizeMode(7, QHeaderView.Stretch)

        v_head = self.ui.tableView.verticalHeader()
        v_head.setSectionResizeMode(QHeaderView.Stretch)

    @pyqtSlot(QModelIndex)
    def on_tableView_clicked(self, index: QModelIndex):
        if index.column() == 6 and index.data() != 'None':
            rule_detail_dialog = RuleDetailDialog(self)

            one_rule_detail_df = self.rule_detail_df[self.rule_detail_df['name'] == index.data()]
            rule_detail_dialog.set_data(one_rule_detail_df.values[0].tolist()[1:])
            rule_detail_dialog.setAttribute(Qt.WA_DeleteOnClose)
            rule_detail_dialog.show()

        if index.column() == 7 and index.data() != 'None':
            # item = self.model.itemFromIndex(index)
            # Matching Pattern  匹配特征

            msg_dialog = HttpMsgDialog(self, self.dialog_msg_font_size)
            b64_matching_pattern = self.df.iloc[index.row() + (self.cur_page-1)*20, 12]
            matching_pattern = base64.b64decode(b64_matching_pattern).decode() if b64_matching_pattern != 'None' else b64_matching_pattern
            msg_dialog.msg(index.data(), matching_pattern)

            msg_dialog.setAttribute(Qt.WA_DeleteOnClose)
            msg_dialog.show()
            msg_dialog.signal_font_size.connect(self.slot_dialog_msg_font_size)

    def slot_dialog_msg_font_size(self, v):
        self.dialog_msg_font_size = v

    @pyqtSlot()
    def on_btn_next_clicked(self):
        self.cur_page += 1
        self.update_model(self.df if self.result_df is None else self.result_df, (self.cur_page-1) * 20, self.cur_page * 20)

        self.hint_widget_display()
        if self.cur_page > 1:
            self.ui.btn_pre.setEnabled(True)

    @pyqtSlot()
    def on_btn_pre_clicked(self):
        self.cur_page -= 1
        self.update_model(self.df if self.result_df is None else self.result_df, (self.cur_page - 1) * 20,
                          self.cur_page * 20)

        self.hint_widget_display()
        if self.cur_page == 1:
            self.ui.btn_pre.setEnabled(False)

    @pyqtSlot()
    def on_btn_go_clicked(self):
        go_page = self.ui.spinbox_page.value()
        self.cur_page = go_page
        self.update_model(self.df if self.result_df is None else self.result_df, (self.cur_page - 1) * 20,
                          self.cur_page * 20)
        self.hint_widget_display()

    @pyqtSlot()
    def on_btn_find_clicked(self):
        self.cur_page = 1
        enabled = {}
        for i in self.ui.frame_condition.findChildren((QLineEdit, QComboBox, QDateTimeEdit),
                                                      options=Qt.FindDirectChildrenOnly):
            if i.isEnabled():
                enabled.update({i.objectName(): i})
        self.condition(enabled)

    def condition(self, enabled_condition):
        self.result_df = None
        if self.df is None:
            QMessageBox.warning(self, '错误', '请打开日志文件后查找')
        else:
            true_series = pd.Series(index=range(len(self.df)), dtype=bool).notna()

            if 'le_server_ip' in enabled_condition:
                c_server_ip = self.df['服务器IP'] == enabled_condition.get('le_server_ip').text()
            else:
                c_server_ip = true_series

            if 'le_client_ip' in enabled_condition:
                c_client_ip = self.df['客户端IP'] == enabled_condition.get('le_client_ip').text()
            else:
                c_client_ip = true_series

            if 'le_rule' in enabled_condition:
                # c_rule = self.df['匹配规则'] == enabled_condition.get('le_rule').text()
                c_rule = self.condition_rule(self.df, enabled_condition.get('le_rule').text())
            else:
                c_rule = true_series

            if 'le_uri' in enabled_condition:
                c_uri = self.df['URI'] == enabled_condition.get('le_uri').text()
            else:
                c_uri = true_series

            if 'dte_start' in enabled_condition and 'dte_end' in enabled_condition:
                c_datetime = (self.df['告警发生时间'] >= enabled_condition.get('dte_start').dateTime().toPyDateTime()) & \
                             (self.df['告警发生时间'] <= enabled_condition.get('dte_end').dateTime().toPyDateTime())
            else:
                c_datetime = true_series

            self.result_df = self.df[c_server_ip & c_client_ip & c_rule & c_uri & c_datetime]

            self.update_model(self.result_df, 0, 20 if len(self.result_df) > 20 else len(self.result_df))

            self.hint_widget_display()

    def condition_rule(self, df, row_condition):
        result = pd.Series(index=range(len(df)), dtype=bool).notna()
        mid_list = []
        # ['xss', 'tag', '!sql']
        condition_list = row_condition.split(';')
        for c in condition_list:
            if '!' in c:
                temp = df['匹配规则'] != c.strip('!')
            else:
                temp = df['匹配规则'] == c
            mid_list.append(temp)

        for c in mid_list:
            result = result & c

        return result

    def hint_widget_display(self):
        if self.result_df is None:
            self.page_amount = ceil(self.df.shape[0] / 20)
        else:
            self.page_amount = ceil(self.result_df.shape[0] / 20)
        self.ui.label_page.setText('{}/{}'.format(self.cur_page, self.page_amount))
        self.ui.spinbox_page.setValue(self.cur_page)


from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
