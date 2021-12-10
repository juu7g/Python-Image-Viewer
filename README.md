# Python-Image-Viewer


## 概要 Description
画像ビューア  
Image viewer

画像ファイルを選択し、ファイルのサムネイル画像とファイル情報をリストビューで表示する   
Select image files and display the thumbnail image of the file and the file information in the list view.  

## 特徴 Features

- GIF、PNG、JPEG、WebP ファイルを読み込みファイル情報を画面に表示  
	Read GIF, PNG, JPEG, WebP files and display file information on the screen  
- 画像のサムネイルを表示  
	Show thumbnail of image  
- 画像の Exif 情報、GPS 情報を表示  
	Display Exif information and GPS information of images  
- チェックボックスを提供  
	Provide checkbox  
- ドラッグアンドドロップでファイルを指定可能(TkinterDnD2使用)
	File can be specified by drag and drop(using TkinterDnD2)  
- exeにドラッグアンドドロップでファイルを指定可能(TkinterDnD2使用でも)
	File can be specified by dragging and dropping to exe(using TkinterDnD2)  
- 元サイズの画像をダイアログ表示  
	Dialog display of original size image  
- TkinterのTreeviewを使用  
	Use Treeview in Tkinter  
- １行おきに背景色を変える  
	Change the background color every other line  
- 列の幅を自動調整  
	Automatically adjust column width    
- 行の高さを自動調整  
	Automatically adjust row height    
- 縦横スクロールバーを表示  
	Display vertical and horizontal scroll bars   

## 依存関係 Requirement

- Python 3.8.5  
- Pillow 8.3.0  
- TkinterDnD2 0.3.0  

## 使い方 Usage

```dosbatch
	image_viewer.exe
```
またはimage_viewer.exeのアイコンに表示したいファイルをドラッグ＆ドロップします

- 操作 Operation  
	- ドラッグ＆ドロップでの操作  
		Drag and drop operation  
		- アプリ画面上の任意の位置に表示したいファイルをドラッグ＆ドロップ  
			Drag and drop the file you want to display anywhere on the application screen  
	- ファイル選択での操作  
		Operation by file selection  
		- ファイル選択ボタンをクリックしファイルを選択  
			Click the file selection button and select the file  
	- 画像の表示  
		Image display
		- 表示したい画像の行で右ボタンでダブルクリックします  
			Double-click on the line of the image you want to display with the right button  
		- 表のチェックボックスをオン(行をクリックで切り替わる)にして「プレビュー」ボタンをクリック  
			Select the check box of the table (click the row to switch) and click the "Preview" button.
	- 画像の選択(チェックボックスのオン/オフ)  
		Image selection (checkbox on / off)  
		- 選択したい画像の行でマウスクリック  
			Mouse click on the line of the image you want to select  
			再度クリックすると選択解除  
			Click again to deselect  
		- 「すべて選択」ボタンをクリックするとすべての画像を選択  
			Click the "Select All" button to select all images  
		- 「選択解除」ボタンをクリックするとすべての画像の選択を解除  
			Click the "Deselect" button to deselect all images  
- 画面の説明 Screen description  
	- 指定したファイルのサムネイルとファイル情報を表形式で表示します  
		Displays thumbnails and file information of the specified file in tabular format  
	- サムネイル、ファイル名、画像の幅、高さ、ファイルサイズ、Exif情報(あれば)、GPS情報(あれば)を表示します  
		Show thumbnails, file names, image widths, heights, file sizes, Exif information (if any), GPS information (if any)  

## インストール方法 Installation

- pip install tkinterdnd2  
- pip install pillow  

## プログラムの説明サイト Program description site

[画像ビューアの作り方(Treeviewに画像と疑似チェックボックス)【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/image/viewer)  

## 作者 Authors
juu7g

## ライセンス License
このソフトウェアは、MITライセンスのもとで公開されています。LICENSE.txtを確認してください。  
This software is released under the MIT License, see LICENSE.txt.

