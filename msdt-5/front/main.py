from PyQt5 import QtWidgets
from loguru import logger

from analyzer import analyze, SemanticData
from front.main_window import Ui_MainWindow
from analyzer.exceptions import SyntaxAnalyzeError, SemanticAnalyzeError


class SyntaxAnalyzerApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.analyzeButton.clicked.connect(self.syntax_analyze)
        self.semanticButton.clicked.connect(self.output_semantic)

    def _mark_err_literal(self, position):
        """ Перемещение курсора к месту возникновения ошибки """

        self.textEdit.setFocus()
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.Start, cursor.KeepAnchor)
        cursor.movePosition(cursor.Right, cursor.KeepAnchor, position)
        cursor.clearSelection()
        self.textEdit.setTextCursor(cursor)

    def syntax_analyze(self):
        """ Обработчик кнопки 'Проанализировать' """

        input_str = self.textEdit.toPlainText()
        logger.info(f'A string was received in the processing. Source: "{input_str}"')
        try:
            analyze(input_str)
        except SyntaxAnalyzeError as ex:
            logger.error(f'Syntax error: {ex}. Source: "{input_str}"')
            self.errorsLabel.setText(f'Синтаксическая ошибка в {ex.position+1} символе. {ex}')
            self.errorsLabel.setStyleSheet('color: red')
            self._mark_err_literal(ex.position)
        except SemanticAnalyzeError as ex:
            logger.error(f'Semantic error: {ex}. Source: "{input_str}"')
            self.errorsLabel.setText(f'Семантическая ошибка в {ex.position+1} символе. {ex}')
            self.errorsLabel.setStyleSheet('color: red')
            self._mark_err_literal(ex.position)
        except Exception as ex:
            logger.critical(f'Unexpected error: {ex}. Source: "{input_str}"')
            raise
        else:
            logger.info(f'Syntax analysis complete. Source: "{input_str}"')
            self.errorsLabel.setText('Строка корректна!')
            self.errorsLabel.setStyleSheet('color: green')

    def output_semantic(self):
        """ Обработчик кнопки 'Вывести семантику' """

        self.identifiersList.clear()
        self.constantsList.clear()
        input_str = self.textEdit.toPlainText()
        logger.info(f'A string was received in the processing. Source: "{input_str}"')
        try:
            semantic_data: SemanticData = analyze(input_str)
        except (SyntaxAnalyzeError, SemanticAnalyzeError):
            logger.error(f'Attempting to derive semantics from an invalid string. Source: "{input_str}"')
        except Exception as ex:
            logger.critical(f'Unexpected error: {ex}. Source: "{input_str}"')
            raise
        else:
            logger.info(f'Source: "{input_str}". Semantic: {semantic_data.identifiers}; {semantic_data.constants}')
            for identifier in semantic_data.identifiers:
                self.identifiersList.addItem(identifier.value)
            for const in semantic_data.constants:
                self.constantsList.addItem(str(const))

