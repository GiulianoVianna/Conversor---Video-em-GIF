from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from moviepy.editor import VideoFileClip
import os

# Classe para representar a janela principal
class ConversorVideoGIFUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("conversor.ui", self)

        # Conectar botões
        self.bt_ad_origem.clicked.connect(self.selecionar_arquivo)
        self.bt_converter.clicked.connect(self.converter_video_para_gif)

        # Desativar os botões de maximizar e minimizar
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.show()

    # Função para selecionar um arquivo
    def selecionar_arquivo(self):
        arquivo, _ = QFileDialog.getOpenFileName(self, " Selecionar vídeo", "", "Videos (*.mp4 *.avi)")
        if arquivo:
            self.txt_origem.setText(arquivo)
            extensao = os.path.splitext(arquivo)[1][1:].upper()
            self.lb_status.setText(f'  Arquivo {extensao} selecionado.')

    # Função para converter arquivo de vídeo em GIF
    def converter_video_para_gif(self):
        arquivo_origem = self.txt_origem.text()
        if not arquivo_origem:
            self.lb_status.setText("  Favor selecionar um arquivo de vídeo (MP4 ou AVI).")
            return

        # Solicitar o segundo inicial e final (inteiros)
        segundo_inicial, ok1 = QInputDialog.getInt(self, "Informação", "Informe o segundo inicial:", min=0)
        segundo_final, ok2 = QInputDialog.getInt(self, "Informação", "Informe o segundo final:", min=0)
        if not (ok1 and ok2):
            self.lb_status.setText("  Favor fornecer o segundo inicial e final.")
            return

        # Solicitar o formato de FTP
        ftp, ok3 = QInputDialog.getItem(self, "Selecionar FTP", "Escolha o formato de FTP:", ["FTP 15", "FTP 24", "FTP 30"], 0, False)
        if not ok3:
            self.lb_status.setText("  Favor selecionar o formato de FTP.")
            return

        ftp_value = int(ftp.split()[1])  # Extrair o valor numérico do FTP selecionado

        if arquivo_origem.endswith(('.mp4', '.avi')):
            arquivo_destino = arquivo_origem.rsplit('.', 1)[0] + '.gif'
        else:
            self.lb_status.setText("  Formato não suportado.")
            return

        clip = VideoFileClip(arquivo_origem).subclip(segundo_inicial, segundo_final).set_fps(ftp_value)
        clip.write_gif(arquivo_destino)

        self.lb_status.setText(f"  Salvo como {arquivo_destino}")

# Função para iniciar a aplicação
def iniciar_aplicacao():
    app = QApplication([])
    janela = ConversorVideoGIFUI()
    app.exec_()

# Iniciar a aplicação
if __name__ == "__main__":
    iniciar_aplicacao()
