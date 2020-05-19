from WafLogQuery.UI.UI_Dialog_HttpMsg import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QTextCursor, QFont
from urllib import parse


class HttpMsgDialog(QDialog):
    signal_font_size = pyqtSignal(int)

    def __init__(self, parent=None, font_size=12):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.row_msg = ''
        self.decode_msg = ''

        self.font = QFont()
        self.font.setPointSize(font_size)
        self.ui.spinbox_font_size.setValue(self.font.pointSize())

    def msg(self, text, match_pattern):
        self.row_msg = text
        self.decode_msg = parse.unquote(self.row_msg)

        self.ui.tb_row.setPlainText(self.row_msg)
        self.ui.tb_decoded.setText(self.decode_msg)

        # 33,67,1,4,27,>'"><script>alert(6710)</script>?merchandiseCode=295685493008404483|||||
        # 'None'值
        if match_pattern != 'None':
            pattern_str = match_pattern.split(',')[5].strip('|||||')
            pattern_index = self.decode_msg.find(pattern_str)
            pattern_str_len = int(match_pattern.split(',')[1])

            text_cursor = self.ui.tb_decoded.textCursor()
            text_cursor.setPosition(pattern_index)
            self.ui.tb_decoded.setTextCursor(text_cursor)
            # 通过起始index和锚点选中匹配特征
            text_cursor.setPosition(pattern_index+pattern_str_len, QTextCursor.KeepAnchor)
            self.ui.tb_decoded.setTextCursor(text_cursor)
            self.ui.tb_decoded.setTextColor(Qt.red)
            text_cursor.clearSelection()
            self.ui.tb_decoded.setTextCursor(text_cursor)

    @pyqtSlot(int)
    def on_spinbox_font_size_valueChanged(self, v):
        self.signal_font_size.emit(v)
        self.font.setPointSize(v)
        self.ui.tb_decoded.setFont(self.font)
        self.ui.tb_row.setFont(self.font)

