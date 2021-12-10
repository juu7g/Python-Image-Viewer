"""
画像ビューワー
"""

import csv, itertools, re, os, sys
from posixpath import basename, join
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import Frame, Label, PhotoImage, filedialog
from tkinterdnd2 import *
from typing import Tuple                # 関数アノテーション用
from typing import List
from PIL import Image, ImageTk          # Pillow
from PIL.ExifTags import TAGS, GPSTAGS  # Exifタグ情報
import subprocess                       # 外部プログラム起動

class ListView(ttk.Frame):
    """
    画像をリストビューで表示する
    """
    check_str = {"uncheck":"☐", "checked":"☑"}    # ☐☑☒チェックボックス用文字

    def __init__(self, master):
        """
        画面の作成
        上のFrame: 入力用
        下のFrame: 出力用
        """
        super().__init__(master)
        self.image_op = ImageOp()
        self.u_frame = tk.Frame(bg="white")     # 背景色を付けて配置を見る
        self.b_frame = tk.Frame(bg="green")     # 背景色を付けて配置を見る
        self.u_frame.pack(fill=tk.X)
        self.b_frame.pack(fill=tk.BOTH, expand=True)
        self.create_input_frame(self.u_frame)
        self.treeview1 = self.create_tree_frame(self.b_frame)
        # bind
        self.treeview1.bind("<Button 1>", self.togle_checkbox) # マウスを左クリックしたときの動作
        # self.treeview1.bind("<Double 1>", self.preview_image)  # マウスをダブルクリックしたときの動作
        self.treeview1.bind("<Double 3>", self.preview_image)  # マウスを右ダブルクリックしたときの動作
        # マウスのクリックとダブルクリックを併用する場合
        # self.double_click_flag =False
        # self.treeview1.bind("<Button 1>", self.mouse_click)  # マウスを左クリックしたときの動作
        # self.treeview1.bind("<Double 1>", self.double_click) # マウスをダブルクリックしたときの動作

    def fixed_map(self, option):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in self.style.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]

    def create_input_frame(self, parent):
        """
        入力項目の画面の作成
        上段：ファイル選択ボタン、すべて選択、選択解除、プレビューボタン
        下段：メッセージ
        """
        self.btn_f_sel = tk.Button(parent, text="ファイル選択", command=self.select_files)
        self.btn_select_all = tk.Button(parent, text="すべて選択", command=self.select_all)
        self.btn_deselection = tk.Button(parent, text="選択解除", command=self.deselection)
        self.btn_preview = tk.Button(parent, text="プレビュー", command=self.preview_images)
        self.msg = tk.StringVar(value="msg")
        self.lbl_msg = tk.Label(parent
                                , textvariable=self.msg
                                , justify=tk.LEFT
                                , font=("Fixedsys", 11)
                                , relief=tk.RIDGE
                                , anchor=tk.W)
        # pack
        self.lbl_msg.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)    # 先にpackしないと下に配置されない
        self.btn_preview.pack(side=tk.RIGHT, padx=5)
        self.btn_deselection.pack(side=tk.RIGHT, padx=5)
        self.btn_select_all.pack(side=tk.RIGHT, padx=5)
        self.btn_f_sel.pack(side=tk.RIGHT, padx=5)
        # bind

    def create_tree_frame(self, parent:Frame) -> ttk.Treeview:
        """
        Treeviewとスクロールバーを持つframeを作成する。
        frameは、Treeviewとスクロールバーをセットする
        Treeviewは、ツリーと表形式、ツリーに画像、行は縞模様
        Args:
            Frame:          親Frame
        Returns:
            Treeview:       ツリービュー
        """
        # tagを有効にするためstyleを更新 tkinter8.6?以降必要みたい
        # 表の文字色、背景色の設定に必要
        self.style = ttk.Style()
        self.style.map('Treeview', foreground=self.fixed_map('foreground')
                                 , background=self.fixed_map('background'))
        # スタイルの設定
        self.style.configure("Treeview", rowheight = 150)   # 画像を150pxで表示するので初期設定する
        # frameの作成。frameにTreeviewとScrollbarを配置する
        frame4tree = tk.Frame(parent, bg="pink")
        frame4tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        # Treeviewの作成
        treeview1 = ttk.Treeview(frame4tree, style="Treeview")
        # treeview1["show"] = "headings"      # デフォルトは treeとheadingsなので設定しない
        treeview1.tag_configure("odd", background="ivory2")     # 奇数行の背景色を指定するtagを作成
        # 水平スクロールバーの作成
        h_scrollbar = tk.Scrollbar(frame4tree, orient=tk.HORIZONTAL, command=treeview1.xview)
        treeview1.configure(xscrollcommand=h_scrollbar.set)
        # 垂直スクロールバーの作成
        v_scrollbar = tk.Scrollbar(frame4tree, orient=tk.VERTICAL, command=treeview1.yview)
        treeview1.configure(yscrollcommand=v_scrollbar.set)
        # pack expandがある方を後にpackしないと他が見えなくなる
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)          # 先にパックしないと表示されない
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)           # 先にパックしないと表示されない
        treeview1.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        treeview1.column("#0", width=200, stretch=False)    # ツリー列の幅の設定
        return treeview1

    def update_tree_column(self, tree1:ttk.Treeview, columns:list):
        """
        TreeViewの列定義と見出しを設定
        見出しの文字長で列幅を初期設定
        Args:
            Treeview:   treeviewオブジェクト
            list:       列名のリスト
        """
        tree1["columns"] = columns                  # treeviewの列定義を設定
        font1 = tkFont.Font()
        for col_name in columns:
            tree1.heading(col_name, text=col_name)  # 見出しの設定
            width1 = font1.measure(col_name)        # 見出しの文字幅をピクセルで取得
            tree1.column(col_name, width=width1)    # 見出し幅の設定

    def update_tree_by_result(self, tree1:ttk.Treeview, rows:list, images:list):
        """
        rows(表データ)、images(画像のデータ)をTreeViewに設定
        要素の文字幅が見出しの文字幅より長い場合は、列幅を変更する。
        奇数列の背景色を変更
        Args:
            Treeview:   Treeviewインスタンス
            list:       行データ(行リストの列リスト)
            list:       画像データ
        """
        if not rows:    # 要素が無ければ戻る
            return
        font1 = tkFont.Font()
        # 要素の長さにより列幅を修正
        for i, _ in enumerate(rows[0]):     # 列数分回す(1行目の要素数分)
            # 同じ列のデータをリストにし列の値の長さを求め、最大となる列のデータを求める。
            # 値は数字もあるので文字に変換し長さを求める。また、Noneは'None'となるので'    'とする。
            max_str = max([x[i] for x in rows], key=lambda x:len(str(x))) or "    "
            # 求めたものが文字列だったら、改行された状態での最大となるデータを求める。
            # 厳密にはこの状態で最大となるデータを探さなければならないが割愛
            if type(max_str) is str:
                max_str = max(max_str.split("\n"), key=len)
            width1 = font1.measure(max_str)   # 文字幅をピクセルで取得
            curent_width = tree1.column(tree1['columns'][i], width=None) # 現在の幅を取得
            # 設定済みの列幅より列データの幅の方が大きいなら列幅を再設定
            if width1 > curent_width:
                tree1.column(tree1['columns'][i], width=width1)    # 見出し幅の再設定
                # print(f"幅の再設定 幅:{width1}、値:{max_str}")   # debug用
        
        tree1.delete(*tree1.get_children())   # Treeviewをクリア
        # 要素の追加
        for i, row in enumerate(rows):
            tags1 = []              # tag設定値の初期化
            if i & 1:               # 奇数か? i % 2 == 1:
                tags1.append("odd") # 奇数番目(treeviewは0始まりなので偶数行)だけ背景色を変える(oddタグを設定)
            # 要素の追加(image=はツリー列の画像、text=はツリー列の文字(疑似チェックボックス))
            iid = tree1.insert("", tk.END, values=row, tags=tags1, 
                                image=images[i], text=self.check_str["uncheck"])     # Treeviewに1行分のデータを設定

    def open_file_and_get_data(self, event=None):
        """
        self.file_pathsのパスからファイル情報、画像サムネイルを作成
        Treeviewに情報追加
        データの幅でTreeviewの列の幅を設定する
        データの行数でTreeviewの行の高さを設定する(行ごとにはできないので一番高い行に合わせる)
        """
        self.image_op.msg = ""
        # DnD対応
        if event:
            # DnDのファイル情報はevent.dataで取得
            # "{空白を含むパス名1} 空白を含まないパス名1"が返る
            # widget.tk.splitlistでパス名のタプルに変換
            self.file_paths = self.u_frame.tk.splitlist(event.data)
            
        # 取得したパスから拡張子がself.extentiosのkeyに含まれるものだけにする
        file_paths2 = tuple(path for path in self.file_paths if os.path.splitext(path)[1].lower() in self.image_op.extensions)
        if len(file_paths2) == 0:
            self.image_op.msg = "対象のファイルがありません"
            self.msg.set(self.image_op.msg)
            return
        if file_paths2 != self.file_paths:
            self.image_op.msg = "対象外のファイルは除きました"
            self.file_paths = file_paths2

        # 取得したパスから表示データと画像を作成
        columns1, rows1, images1, msg1 = self.image_op.get_images(self.file_paths)
        self.d_images = []  # ダイアログ表示用画像初期化

        self.msg.set(self.image_op.msg)     # エラーメッセージの表示

        # 見出しの文字長で列幅を初期設定、treeviewのカラム幅を文字長に合わせて調整
        self.update_tree_column(self.treeview1, columns1)

        # 列項目を右寄せ
        # self.treeview1.column("#0", anchor=tk.E)         # 列項目を右寄せ(ツリー)#0には働かないみたい
        self.treeview1.column("#2", anchor=tk.E)         # 列項目を右寄せ(幅)
        self.treeview1.column("#3", anchor=tk.E)         # 列項目を右寄せ(高さ)
        self.treeview1.column("#4", anchor=tk.E)         # 列項目を右寄せ(サイズ)

        # rows、画像をTreeViewに設定
        # 要素の文字幅が見出しの文字幅より長い場合は、列幅を変更する。偶数列の背景色を変更
        self.update_tree_by_result(self.treeview1, rows1, images1)

        # 一番行数の多い行に合わせて高さを設定する
        # ２次元のデータを平坦化しstr型だけを抽出する
        cells = [s for s in itertools.chain.from_iterable(rows1) if type(s) is str]
        if cells:
            # 抽出したリストの要素の中で改行の数の最も多い要素を取得
            longest_cell = max(cells, key=lambda x:x.count("\n"))
            max_row_lines = longest_cell.count("\n") + 1             # 改行の数を数える
            # Treeviewの行の高さを変更  # タブごとのスタイルの設定
            if max_row_lines * 18 > 150:
                self.style.configure("Treeview", rowheight = 18 * max_row_lines)
        
    def select_files(self, event=None):
        """
        ファイル選択ダイアログを表示。選択したファイルパスを取得
        ファイル情報や画像を取得して表示
        """
        # 拡張子の辞書からfiletypes用のデータを作成
        # 辞書{".csv":"CSV", ".tsv":"TSV"}、filetypes=[("CSV",".csv"), ("TSV",".tsv")]
        self.file_paths = filedialog.askopenfilenames(
            filetypes=[(value, key) for key, value in self.image_op.extensions.items()])
        self.open_file_and_get_data()		# ファイル情報や画像を取得して表示

    # マウスのクリックとダブルクリックを併用する場合
    # 反応が鈍いので未使用。参考に残す。
    def mouse_click(self, event=None):
        """
        マウスのシングルクリック時の処理
        シングルクリックとダブルクリックイベントは両方発生するので
        シングルクリックイベントでダブルクリックイベントの発生を待ち、
        ダブルクリックが発生してから共通の処理(中身は分ける)を実行する
        """
        self.treeview1.after(200, self.mouse_action, event)

    # マウスのクリックとダブルクリックを併用する場合
    def double_click(self,event=None):
        """
        マウスのダブルクリック時の処理
        ダブルマリックの発生をフラグに設定
        """
        self.double_click_flag = True

    # マウスのクリックとダブルクリックを併用する場合
    def mouse_action(self, event=None):
        """
        マウスクリック時の処理
        ダブルクリック発生フラグを確認して処理を実行
        ダブルクリック用処理実行後はフラグをクリア
        """
        if self.double_click_flag:
            self.preview_image(event)
            self.double_click_flag =False
        else:
            self.togle_checkbox(event)

    def togle_checkbox(self, event=None):
        """
        チェックボックスの状態を反転
        """
        rowid = self.treeview1.identify_row(event.y)    # マウスの座標から対象の行を取得する
        if self.treeview1.item(rowid, text=None) == self.check_str["uncheck"]:
            self.treeview1.item(rowid, text=self.check_str["checked"])
        else:
            self.treeview1.item(rowid, text=self.check_str["uncheck"])

    def preview_image(self, event=None, path=""):
        """
        画像のプレビュー
        ダイアログ表示
		Args:
            string:     ファイルパス(ない場合もある)
        """
        # マウスのクリックとダブルクリックを併用する場合
        # マウスクリックイベントが先に動いているので打ち消す
        # クリックとダブルクリックを左ボタンで実装する時の考慮
        # self.togle_checkbox(event)

        if event:
            rowid = self.treeview1.identify_row(event.y)    # マウスの座標から対象の行を取得する
            path1 = self.treeview1.item(rowid)["values"][0].replace("\n", "")   # ファイル名取得
        else:
            path1 = path

        # ダイアログ表示
        dialog = tk.Toplevel(self)      # モードレスダイアログの作成
        dialog.title("Preview")         # タイトル
        self.d_images.append(ImageTk.PhotoImage(file=path1))    # 複数表示する時のために画像を残す
        label1 = tk.Label(dialog, image=self.d_images[-1])      # 最後のものを表示
        label1.pack()

    def preview_images(self, event=None):
        """
        選択された画像のプレビュー
        """
        self.msg.set("")
        # Treeviewのチェックボックスがオンの行のファイル名列(1列)を取得。改行してあるので除く。
        paths = [self.treeview1.item(x)["values"][0].replace("\n", "") for x in self.treeview1.get_children() if self.treeview1.item(x)["text"] == self.check_str["checked"]]
        for path1 in paths:
            self.preview_image(path=path1)
        if not paths:
            self.msg.set("選択された画像がありません")

    def select_all(self, event=None):
        """
        Treeviewの要素をすべて選択する
        """
        self.set_all_checkbox("checked")

    def deselection(self, event=None):
        """
        Treeviewの要素をすべて選択解除する
        """
        self.set_all_checkbox("uncheck")

    def set_all_checkbox(self, check_stat:str):
        """
        Treeviewのチェックボックスをすべて設定する
		Args:
			str: "checked" または "uncheck"
        """
        for iid in self.treeview1.get_children():
            self.treeview1.item(iid, text=self.check_str[check_stat])

class ImageOp():
    """
    画像データの操作を行う
    """
    def __init__(self):
        self.msg = ""   # メッセージ受渡し用
        # 対象拡張子	辞書(key:拡張子、値:表示文字)
        self.extensions = {".png .jpg .gif .webp":"画像", ".png":"PNG", 
                            ".jpg":"JPEG", ".gif":"GIF", ".webp":"WebP"}

    def get_images(self, file_names:tuple) -> Tuple[list, str]:
        """
        画像ファイルを読みデータを返す
        Args:
            str:    ファイル名
        Returns:
            columns1(list):     列名 
            rows1(list):        行データ(行リストの列リスト)
            self.images(list):  画像データ
            msg1(str):          エラーメッセージ(空文はエラーなし)
        """
        msg1 = ""
        columns1 = ["ファイル名", "幅(px)", "高さ(px)", "サイズ(kB)", "画像情報 EXIF", "位置情報 GPS"]
        try:
            self.images = []    # selfでないとうまくいかない。理由は不明
            rows1 = []
            for file_name in file_names:   # パス名で回す
                # basename = os.path.basename(file_name)
                f = os.path.normpath(file_name)
                wrap_file_name = f.replace("\\", "\\\n")
                # 画像のサイズ
                file_size = os.path.getsize(file_name)
                # 画像の取得
                image1 = Image.open(file_name)
                # ファイルサイズの取得
                image_size = image1.size
                # Exif情報の取得
                exif_dict = image1.getexif()
                exif = [TAGS.get(k, "Unknown")+ f": {str(v)}" for k, v in exif_dict.items()]
                exif_str = "\n".join(exif)
                # GPS情報の取得
                gps_dict = exif_dict.get_ifd(34853)
                gps = [GPSTAGS.get(k, "Unknown") + f": {str(v)}" for k, v in gps_dict.items()]
                gps_str = "\n".join(gps)
                # 縮小
                image1.thumbnail((150, 150), Image.BICUBIC)
                # サムネイルの大きさを統一(そうしないとチェックボックスの位置がまちまちになるため)
                # ベース画像の作成と縮小画像の貼り付け(中央寄せ)
                # base_image = Image.new(image1.mode, (160, 160), "#ffffff")
                base_image = Image.new('RGBA', (160, 160), (255, 0, 0, 0))  # 透明なものにしないとgifの色が変わる
                horizontal = int((base_image.size[0] - image1.size[0]) / 2)
                vertical = int((base_image.size[1] - image1.size[1]) / 2)
                # print(f"size:{image1.size} h,v:{horizontal},{vertical}, base:{base_image.size}")  # debug
                base_image.paste(image1, (horizontal, vertical))
                image1 = base_image
                # PhotoImageへ変換
                image1 = ImageTk.PhotoImage(image1)
                # 列データと画像データを追加
                self.images.append(image1)
                rows1.append([wrap_file_name, image_size[0], image_size[1], 
                                "{:.1f}".format(file_size/1024), exif_str, gps_str])
        except Exception as e:
            msg1 = e
            print(f"error:{e}")
        finally:
            return columns1, rows1, self.images, msg1

if __name__ == '__main__':
    root = TkinterDnD.Tk()      # トップレベルウィンドウの作成  tkinterdnd2の適用
    root.title("画像 viewer")   # タイトル
    root.geometry("800x710")    # サイズ
    root.iconbitmap("fukuro32.ico", True)
    listview = ListView(root)   # ListViewクラスのインスタンス作成
    root.drop_target_register(DND_FILES)            # ドロップ受け取りを登録
    root.dnd_bind("<<Drop>>", listview.open_file_and_get_data)    # ドロップ後に実行するメソッドを登録
    # コマンドライン引数からドラッグ＆ドロップされたファイル情報を取得
    if len(sys.argv) > 1:
        listview.file_paths = tuple(sys.argv[1:])
        listview.open_file_and_get_data()			# オープン処理の実行
    root.mainloop()
