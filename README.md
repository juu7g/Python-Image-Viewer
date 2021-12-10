# Python-Image-Viewer


## �T�v Description
�摜�r���[�A  
Image viewer

�摜�t�@�C����I�����A�t�@�C���̃T���l�C���摜�ƃt�@�C���������X�g�r���[�ŕ\������   
Select image files and display the thumbnail image of the file and the file information in the list view.  

## ���� Features

- GIF�APNG�AJPEG�AWebP �t�@�C����ǂݍ��݃t�@�C��������ʂɕ\��  
	Read GIF, PNG, JPEG, WebP files and display file information on the screen  
- �摜�̃T���l�C����\��  
	Show thumbnail of image  
- �摜�� Exif ���AGPS ����\��  
	Display Exif information and GPS information of images  
- �`�F�b�N�{�b�N�X���  
	Provide checkbox  
- �h���b�O�A���h�h���b�v�Ńt�@�C�����w��\(TkinterDnD2�g�p)
	File can be specified by drag and drop(using TkinterDnD2)  
- exe�Ƀh���b�O�A���h�h���b�v�Ńt�@�C�����w��\(TkinterDnD2�g�p�ł�)
	File can be specified by dragging and dropping to exe(using TkinterDnD2)  
- ���T�C�Y�̉摜���_�C�A���O�\��  
	Dialog display of original size image  
- Tkinter��Treeview���g�p  
	Use Treeview in Tkinter  
- �P�s�����ɔw�i�F��ς���  
	Change the background color every other line  
- ��̕�����������  
	Automatically adjust column width    
- �s�̍�������������  
	Automatically adjust row height    
- �c���X�N���[���o�[��\��  
	Display vertical and horizontal scroll bars   

## �ˑ��֌W Requirement

- Python 3.8.5  
- Pillow 8.3.0  
- TkinterDnD2 0.3.0  

## �g���� Usage

```dosbatch
	image_viewer.exe
```
�܂���image_viewer.exe�̃A�C�R���ɕ\���������t�@�C�����h���b�O���h���b�v���܂�

- ���� Operation  
	- �h���b�O���h���b�v�ł̑���  
		Drag and drop operation  
		- �A�v����ʏ�̔C�ӂ̈ʒu�ɕ\���������t�@�C�����h���b�O���h���b�v  
			Drag and drop the file you want to display anywhere on the application screen  
	- �t�@�C���I���ł̑���  
		Operation by file selection  
		- �t�@�C���I���{�^�����N���b�N���t�@�C����I��  
			Click the file selection button and select the file  
	- �摜�̕\��  
		Image display
		- �\���������摜�̍s�ŉE�{�^���Ń_�u���N���b�N���܂�  
			Double-click on the line of the image you want to display with the right button  
		- �\�̃`�F�b�N�{�b�N�X���I��(�s���N���b�N�Ő؂�ւ��)�ɂ��āu�v���r���[�v�{�^�����N���b�N  
			Select the check box of the table (click the row to switch) and click the "Preview" button.
	- �摜�̑I��(�`�F�b�N�{�b�N�X�̃I��/�I�t)  
		Image selection (checkbox on / off)  
		- �I���������摜�̍s�Ń}�E�X�N���b�N  
			Mouse click on the line of the image you want to select  
			�ēx�N���b�N����ƑI������  
			Click again to deselect  
		- �u���ׂđI���v�{�^�����N���b�N����Ƃ��ׂẲ摜��I��  
			Click the "Select All" button to select all images  
		- �u�I�������v�{�^�����N���b�N����Ƃ��ׂẲ摜�̑I��������  
			Click the "Deselect" button to deselect all images  
- ��ʂ̐��� Screen description  
	- �w�肵���t�@�C���̃T���l�C���ƃt�@�C������\�`���ŕ\�����܂�  
		Displays thumbnails and file information of the specified file in tabular format  
	- �T���l�C���A�t�@�C�����A�摜�̕��A�����A�t�@�C���T�C�Y�AExif���(�����)�AGPS���(�����)��\�����܂�  
		Show thumbnails, file names, image widths, heights, file sizes, Exif information (if any), GPS information (if any)  

## �C���X�g�[�����@ Installation

- pip install tkinterdnd2  
- pip install pillow  

## �v���O�����̐����T�C�g Program description site

[�摜�r���[�A�̍���(Treeview�ɉ摜�Ƌ^���`�F�b�N�{�b�N�X)�yPython�z - �v���O�����ł��������ł��邩��](https://juu7g.hatenablog.com/entry/Python/image/viewer)  

## ��� Authors
juu7g

## ���C�Z���X License
���̃\�t�g�E�F�A�́AMIT���C�Z���X�̂��ƂŌ��J����Ă��܂��BLICENSE.txt���m�F���Ă��������B  
This software is released under the MIT License, see LICENSE.txt.

