import os
import sys
import eyed3
import lyricsgenius as lg
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QSizePolicy, QVBoxLayout, QListWidget, QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QColor


TOKEN = 'nkWbkfZE-e1e6ZXD_Iu27Wy141pGCQapbtGOS3mnDJ_R_DNRRgAPRGhSX2LYM2Yn'
EXCLUDED = ['$RECYCLE.BIN', 'System Volume Information', 'Recovery']


class Signal(QObject):

    song_done = pyqtSignal(int)


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.size = app.primaryScreen().size()
        self.setGeometry(int((self.size.width() - 600) / 2), int((self.size.height() - 500) / 2), 600, 500)
        self.setWindowTitle("  Lyricify 0.1")
        self.setWindowIcon(QIcon('icon.png'))
        self.btn_load_files = QPushButton('Select files', self)
        self.btn_load_folder = QPushButton('Select folder', self)
        self.list = QListWidget()
        self.btn_get_lyrics = QPushButton('Get lyrics', self)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.s = Signal()
        self.s.song_done.connect(self.song_done)
        self.init_ui()

    def init_ui(self):
        self.btn_load_files.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.btn_load_files.setFont(QFont('Calibri', 15))
        self.btn_load_files.clicked.connect(self.load_files)
        self.btn_load_folder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.btn_load_folder.setFont(QFont('Calibri', 15))
        self.btn_load_folder.clicked.connect(self.load_folder)
        self.list.setStyleSheet('border : 1px solid gray')
        self.btn_get_lyrics.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.btn_get_lyrics.setFont(QFont('Calibri', 15))
        self.btn_get_lyrics.clicked.connect(self.get_lyrics)
        self.list.setMinimumHeight(400)
        self.hbox.addWidget(self.btn_load_files)
        self.hbox.addWidget(self.btn_load_folder)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.list)
        self.vbox.addWidget(self.btn_get_lyrics)
        self.setLayout(self.vbox)
        self.show()

    def song_done(self, index):
        self.list.item(index).setForeground(QColor('green'))
        self.list.repaint()

    def load_files(self):
        home_dir = str(Path.home())
        path = QFileDialog.getOpenFileNames(self, 'Select files', home_dir, '*.mp3')
        if path[0]:
            self.list.addItems(path[0])

    def load_folder(self):
        home_dir = str(Path.home())
        path = QFileDialog.getExistingDirectory(self, 'Select folder', home_dir)
        if path[0]:
            files = []
            for root, dirs, names in os.walk(path):
                dirs[:] = [d for d in dirs if d not in EXCLUDED]
                for name in names:
                    if name.lower().endswith(".mp3"):
                        files.append(os.path.abspath(os.path.join(root, name)))
            self.list.addItems(files)

    def get_lyrics(self):
        genius = lg.Genius(TOKEN)
        genius.timeout = 10
        genius.retries = 5

        files = [self.list.item(i).text() for i in range(self.list.count())]
        for file in files:
            mp3 = eyed3.load(file)
            artist = mp3.tag.artist
            title = mp3.tag.title
            if '(' in title or '[' in title:
                title = strip_title(title)
            #print(title)

            try:
                song = genius.search_song(title, artist)
                if 'EmbedShare' in song.lyrics:
                    song.lyrics = strip_embedshare(song.lyrics)
                #print(f'\n{song.lyrics}\n')
            except AttributeError:
                print('Not found\n')
            self.s.song_done.emit(files.index(file))

            # try:
            #     mp3.tag.lyrics.set(song.lyrics)
            #     mp3.tag.save()
            # except AttributeError:
            #     continue


def strip_title(title):
    strings_to_remove = ['mix', 'cover', 'live', 'take', 'feat', 'acoustic', 'bonus', 'instrumental', 'demo']
    stripped_title = title
    #print(stripped_title)
    for string_to_remove in strings_to_remove:
        start_index = 0
        end_index = len(stripped_title) - 1
        if string_to_remove in stripped_title:
            #print(string_to_remove)
            string_index = stripped_title.index(string_to_remove)
            #print(string_index)
            for i in range(string_index, 0, -1):
                if stripped_title[i] == '(':
                    start_index = i - 1
                    break
            for i in range(string_index, len(stripped_title)):
                if stripped_title[i] == ')':
                    end_index = i + 1
                    break
            stripped_title = f'{stripped_title[:start_index]}{stripped_title[end_index:]}'
            #print(f"{stripped_title} Start: {start_index} / End: {end_index}")
    return stripped_title


def strip_embedshare(song_lyrics):
    stripped_lyrics = song_lyrics
    start = song_lyrics.find('EmbedShare')
    count = 0
    for i in range(1, 3):
        if song_lyrics[start - i].isdigit():
            count += 1
    stripped_lyrics = stripped_lyrics[:start - count]
    return stripped_lyrics


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    main = Window()
    sys.exit(app.exec())
