import os,time
os.environ['love']='1'
time.sleep(0.2)
from pytube import YouTube,Playlist,request
os.environ['love']='2'
time.sleep(0.2)
import Main
os.environ['love']='3'
time.sleep(0.2)
from PyQt5 import QtWidgets as q
os.environ['love']='4'
time.sleep(0.2)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
os.environ['love']='5'
time.sleep(0.2)
from PyQt5.QtGui import QPalette,QColor,QIcon
os.environ['love']='6'
time.sleep(0.2)
import sys,subprocess,shutil
os.environ['love']='7'
me=None
os.environ['love']='8'
time.sleep(0.2)
darkPalette = QPalette()
darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
darkPalette.setColor(QPalette.WindowText, Qt.white)
darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor
(127, 127, 127))
darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
darkPalette.setColor(QPalette.ToolTipText, Qt.white)
darkPalette.setColor(QPalette.Text, Qt.white)
darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127,
127, 127))
darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
darkPalette.setColor(QPalette.ButtonText, Qt.white)
darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor
(127, 127, 127))
darkPalette.setColor(QPalette.BrightText, Qt.red)
darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80,
80, 80))
darkPalette.setColor(QPalette.HighlightedText, Qt.white)
darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText,
QColor(127, 127, 127))
os.environ['love']='9'
class downloadThread(QThread):
	change,error,filestream=pyqtSignal(int),pyqtSignal(Exception),None
	def __init__(self,MainWindow):
		super().__init__()
		self.mw=MainWindow
	def delete(self,filenames):
		try:
			for i in filenames:
				if os.path.isfile(i):
					os.remove(i)
		except Exception as e:
			self.mw.ErrorMessage(e)
			quit()
	def Stop(self):
		if self.filestream:
			while not self.filestream.closed:
				name=self.filestream.name
				self.filestream.close()
				self.delete([name])
		self.delete(['Yolo.mp4','temp.mp3'])
	def download(self,Mediadict=None,cap=None,altname='',extra=''):
		if cap:
			self.mw.label33.setText(extra+'Subtitle-'+altname)
			self.change.emit(0)
			self.filestream=open(altname+'.srt','w',encoding='utf-8')
			self.filestream.write(cap.generate_srt_captions())
			self.filestream.close()
			self.change.emit(100)
		for i in Mediadict:
			self.mw.label33.setText(extra+i['filestream'].type+'-'+altname)
			self.change.emit(0)
			self.filestream,filesize,downloaded=open(i['filename'],'wb'),i['filestream'].filesize,0
			stream=request.stream(i['filestream'].url)
			while 1:
				while self.mw.paused:
					time.sleep(1)
				chunk=next(stream,None)
				if chunk and not self.filestream.closed:
					self.filestream.write(chunk)
					downloaded+=len(chunk)
					self.change.emit(int((downloaded*100)/filesize))
				else:
					self.filestream.close()
					break
		if len(Mediadict)==2:
			global me
			self.mw.label33.setText('')
			if not me:
				self.mw.label32.setText('Importing...')
				self.mw.thread3.wait()
			self.mw.label32.setText('Merging...')
			self.mw.label33.setText(extra+altname)
			self.change.emit(0)
			clip1=me.VideoFileClip('Yolo.mp4')
			clip2=me.AudioFileClip('temp.mp3')
			clip3=clip1.set_audio(clip2)
			clip3.write_videofile(altname+'.mp4')
			clip1.close()
			clip2.close()
			clip3.close()
			self.change.emit(100)
			self.delete(['Yolo.mp4','temp.mp3'])
	def run(self):
		if self.mw.Mode=='Video':
			payload,cap,FileName=[],None,self.mw.FileName
			if self.mw.state:
				self.mw.FileName+='.mp4'
				payload.append({'filestream':self.mw.filteredVidStreams[self.mw.CurrentResolution]})
				if self.mw.filteredVidStreams[self.mw.CurrentResolution].is_adaptive:
					self.delete(['Yolo.mp4','temp.mp3'])
					payload[0]['filename']='Yolo.mp4'
					payload.append({'filestream':self.mw.filteredAudStreams[self.mw.CurrentAbr],'filename':'temp.mp3'})
				else:
					payload[0]['filename']=FileName+'.mp4'
				if self.mw.comboBox22.isEnabled() and self.mw.checkBox21.isChecked():
					for i in self.mw.CaptionList:
						if i.name==self.mw.CurrentCaption:
							cap=i
			else:
				self.mw.FileName+='.mp3'
				payload.append({'filestream':self.mw.filteredAudStreams[self.mw.CurrentAbr],'filename':self.mw.FileName})
			try:
				self.download(payload,cap,FileName)
			except Exception as e:
				self.error.emit(str(e))
		else:
			for i in range(len(self.mw.videos)):
				root,payload,cap=self.mw.videos[i],[],None
				FileName=self.mw.NameFilter('b',root.title)
				ind,dif,mul,streams,resos=self.mw.CurrentResolution,1,-1,root.streams,self.mw.Resolutions
				temp=streams.filter(res=resos[ind]).first()
				while temp==None:#for choosing alternative streams
					if ind+dif*mul>=0 and ind+dif*mul<7:
						temp=streams.filter(res=resos[ind+dif*mul]).first()
					if mul==1:
						mul=-1
						dif+=1
					else:
						mul=1
				ind,dif,mul,abrs=self.mw.CurrentAbr,1,-1,self.mw.abrs
				atemp=streams.filter(abr=abrs[ind]).first()
				while atemp==None:
					if ind+dif*mul>=0 and ind+dif*mul<7:
						atemp=streams.filter(abr=abrs[ind+dif*mul]).first()
					if mul==1:
						mul=-1
						dif+=1
					else:
						mul=1
				if self.mw.state:#we require videostream, audiostream, caption. can't they be used as arguments instead of dicts?
					payload.append({'filestream':temp})
					if temp.is_adaptive:
						self.delete(['Yolo.mp4','temp.mp3'])
						payload[0]['filename']='Yolo.mp4'
						payload.append({'filestream':atemp,'filename':'temp.mp3'})
						altname=FileName
					else:
						payload[0]['filename']=FileName+'.mp4'
					if self.mw.comboBox22.isEnabled() and self.mw.checkBox21.isChecked():
						self.CaptionList=list(root.captions)
						self.captions=list(set(i.name for i in self.CaptionList))
						for i in self.CaptionList:
							if i.name==self.mw.CurrentCaption:
								cap=i
				else:
					payload.append({'filestream':atemp,'filename':FileName+'.mp3'})
				try:
					self.download(payload,cap,FileName,'('+str(i+1)+'/'+str(len(self.mw.videos))+')-')
				except Exception as e:
					self.error.emit(e)
					return
		self.mw.Page3()
class importer(QThread):
	def run(self):
		global me
		import moviepy.editor as me
class Worker(QThread):
	change,error,canceled=pyqtSignal(int),pyqtSignal(Exception),False
	def __init__(self,wind):
		super().__init__()
		self.mw=wind
	def run(self):
		try:
			self.mw.root=YouTube(self.mw.link) if self.mw.Mode=='Video' else Playlist(self.mw.link)
			self.change.emit(10)
			time.sleep(.2)
			self.mw.VideoName=self.mw.root.title
			self.mw.Resolutions,self.mw.abrs,self.mw.filteredVidStreams,self.mw.filteredAudStreams,temp=[],[],[],[],[]
			self.change.emit(20)
			if self.mw.Mode=='Video':
				self.mw.streams=self.mw.root.streams
				self.change.emit(30)
				time.sleep(.2)
				for i in self.mw.streams.filter(progressive=1):
					if i.resolution not in self.mw.Resolutions:
						self.mw.Resolutions.append(i.resolution)
						temp.append(', '+str(i.filesize/1048576)[:5]+'MB')
						self.mw.filteredVidStreams.append(i)
				self.change.emit(40)
				time.sleep(.2)
				for i in self.mw.streams.filter(only_video=1):
					if i.resolution not in self.mw.Resolutions:
						self.mw.Resolutions.append(i.resolution)
						temp.append(', '+str(i.filesize/1048576)[:5]+'+MB')
						self.mw.filteredVidStreams.append(i)
				self.change.emit(50)
				time.sleep(.2)
				for i in range(len(self.mw.Resolutions)):
					self.mw.Resolutions[i]+=temp[i]
				self.change.emit(60)
				time.sleep(.2)
				temp=[]
				for i in self.mw.streams.filter(only_audio=1):
					if i.abr not in self.mw.abrs:
						self.mw.abrs.append(i.abr)
						temp.append(', '+str(i.filesize/1048576)[:5]+'MB')
						self.mw.filteredAudStreams.append(i)
				self.change.emit(70)
				time.sleep(.2)
				for i in range(len(self.mw.abrs)):
					self.mw.abrs[i]+=temp[i]
				self.change.emit(80)
				time.sleep(.2)
				self.mw.CaptionList=list(self.mw.root.captions)
				self.mw.captions=list(set(i.name for i in self.mw.CaptionList))
				self.change.emit(90)
				time.sleep(.2)
			else:
				time.sleep(.2)
				self.mw.videos=[]
				self.change.emit(30)
				time.sleep(.2)
				for i in self.mw.root.videos:
					self.mw.videos.append(i)
				self.change.emit(40)
				time.sleep(.2)
				self.mw.Resolutions=['144p','240p','360p','480p','720p','1080p','2160p']
				self.mw.abrs=['128kbps','256kbps']
				self.mw.captions=['English']
				self.change.emit(80)
				time.sleep(.2)
			self.change.emit(100)
			if not self.canceled:
				self.mw.Page2()
		except Exception as e:
			self.error.emit(e)
			self.mw.Page1()
			return
class mw(q.QMainWindow,Main.Ui_MainWindow):
	def ErrorMessage(self,err):
		reply=q.QMessageBox.critical(self,'Error!','An Error Occured! Error code:'+str(err))
	def NameFilter(self,type,spec):
		unacceptables,out=['/','\\','"',':','*','?','|','<','>','&','(',')'],''
		for i in range(len(spec)):
			if spec[i] in unacceptables:
				if type=='a':
					return '-1'#Can we directly call ErrorMessage here?
				out+='_'
			else:
				out+=spec[i]
		return out
	def changeProp(self,text=''):
		if self.Mode=='Video':
			self.Mode='Playlist'
			self.pushButton13.setToolTip('Enter Video URL instead.')
			self.pushButton13.setIcon(QIcon(':/Logo/video2.png'))
			if 'https://www.youtube.com/playlist?' in text[0:33]:
				self.link=text
				self.lineEdit11.setPlaceholderText(text)
			else:
				self.lineEdit11.setPlaceholderText('Enter Playlist URL...')
		else:
			self.Mode='Video'
			self.pushButton13.setToolTip('Enter Playlist URL instead.')
			self.pushButton13.setIcon(QIcon(':/Logo/playlist2.png'))
			if 'https://www.youtube.com/watch?' in text[0:30]:
				self.link=text
				self.lineEdit11.setPlaceholderText(text)
			else:
				self.lineEdit11.setPlaceholderText('Enter Video URL...')
		self.lineEdit11.setFocus()
	def PageTransform12(self):
		self.link=self.lineEdit11.text() if self.lineEdit11.text()!='' else self.lineEdit11.placeholderText()
		self.label32.setText('Loading...')
		self.pushButton33.hide()
		self.label33.setText('')
		self.progressBar31.setValue(0)
		self.pushButton34.setDefault(1)
		self.progressBar31.setTextVisible(0)
		self.stackedWidget.setCurrentIndex(2)
		self.thread1=Worker(self)
		self.thread1.change.connect(self.progressBar31.setValue)
		self.thread1.error.connect(self.ErrorMessage)
		self.thread1.start()
	def PageTransform23(self):
		self.FilePath=self.lineEdit21.text()
		self.FileName=self.lineEdit22.text()
		if self.NameFilter(self.FileName,'a')=='-1':
			self.ErrorMessage('Invalid File/Directory name! A name cannot contain any of the following characters:\n/,\\,",:,*,?,|,<,>,&,(,)')
			return
		try:
			os.chdir(self.FilePath)
			if self.Mode=='Playlist':
				if os.path.isdir(self.FileName):
					shutil.rmtree(self.FileName)
				os.mkdir(self.FileName)
				os.chdir(self.FileName)
		except Exception as e:
			self.ErrorMessage(e)
			return
		self.label32.setText('Downloading...')
		self.pushButton33.show()
		self.progressBar31.setValue(0)
		self.pushButton34.setDefault(1)
		self.progressBar31.setTextVisible(1)
		self.stackedWidget.setCurrentIndex(2)
		self.CurrentCaption=self.comboBox22.currentText()
		self.CurrentResolution=self.comboBox21.currentIndex()
		self.CurrentAbr=self.comboBox23.currentIndex()
		self.thread2=downloadThread(self)
		self.thread2.change.connect(self.progressBar31.setValue)
		self.thread2.error.connect(self.ErrorMessage)
		self.thread2.start()
	def back(self):
		if self.currentIndex==0:
			self.thread1.canceled=True
			self.Page1()
		else:
			a=q.QMessageBox.question(self,'Cancel Download','Are you sure?')
			if a==q.QMessageBox.Yes:
				self.thread2.Stop()
				self.Page2()
	def OpenFile(self):
		try:
			if self.Mode=='Playlist':
				path=os.path.realpath(os.getcwd())
				os.startfile(path)
			else:
				subprocess.call(self.FileName,shell=True)
		except Exception as e:
			self.ErrorMessage(e)
	def setState(self,state):
		self.state=state
		if state:
			if not self.radioButton21.isChecked():
				self.radioButton21.setChecked(1)
			self.comboBox23.setEnabled(0)
			self.comboBox21.setEnabled(1)
			self.comboBox22.setEnabled(1)
			self.checkBox21.setEnabled(1)
		else:
			if not self.radioButton22.isChecked():
				self.radioButton22.setChecked(1)
			self.comboBox23.setEnabled(1)
			self.comboBox21.setEnabled(0)
			self.comboBox22.setEnabled(0)
			self.checkBox21.setEnabled(0)
	def Page1(self):
		self.currentIndex=0
		self.stackedWidget.setCurrentIndex(0)
	def closeEvent(self,event=None):
		if self.stackedWidget.currentIndex()==2:
			if self.currentIndex==1:
				a=q.QMessageBox.question(self,'Cancel Download','Download in progress. Do you want to quit?')
				if a==q.QMessageBox.Yes:
					self.thread2.Stop()
					self.close()
				else:
					if event:
						event.ignore()
			else:
				self.thread1.canceled=True
		else:
			self.close()
	def Page2(self):
		self.currentIndex=1
		self.label22.setText(self.VideoName)
		self.lineEdit22.setText(self.NameFilter('b',self.VideoName))
		self.comboBox21.clear()
		self.comboBox22.clear()
		self.comboBox23.clear()
		self.comboBox21.addItems(self.Resolutions)
		if self.captions!=[]:
			self.comboBox22.addItems(self.captions)
		else:
			self.checkBox21.setEnabled(0)
			self.comboBox22.setEnabled(0)
		self.comboBox23.addItems(self.abrs)
		if self.prevData==[]:
			try:
				filestream=open(sys.path[0]+'\\preferences.ytd','r')
				self.prevData=filestream.read().splitlines()
				if len(self.prevData)!=6:
					raise Exception('blank')
			except:
				self.prevData=[sys.path[0],'1','0','360p','128kbps','English']
		self.lineEdit21.setText(self.prevData[0])
		self.setState(int(self.prevData[1]))
		self.checkBox21.setChecked(int(self.prevData[2]))
		for i in range(len(self.Resolutions)):
			if self.Resolutions[i].split(',')[0]==self.prevData[3]:
				self.comboBox21.setCurrentIndex(i)
				break
		for i in range(len(self.abrs)):
			if self.abrs[i].split(',')[0]==self.prevData[4]:
				self.comboBox23.setCurrentIndex(i)
				break
		for i in range(len(self.captions)):
			if self.captions[i]==self.prevData[5]:
				self.comboBox22.setCurrentIndex(i)
				break
		self.pushButton24.setDefault(1)
		self.pushButton24.setFocus()
		self.stackedWidget.setCurrentIndex(1)
	def Page3(self):
		self.pushButton43.setDefault(1)
		self.label43.setText(self.VideoName)
		self.curData=[self.FilePath,str(int(self.state)),str(int(self.checkBox21.isChecked())),self.Resolutions[self.CurrentResolution].split(',')[0],self.abrs[self.CurrentAbr].split(',')[0]]
		if self.CurrentCaption!='':
			self.curData.append(self.CurrentCaption)
		else:
			self.curData.append(self.prevData[5])
		if self.curData!=self.prevData:
			filestream=open(sys.path[0]+'\\preferences.ytd','w')
			for i in self.curData:
				filestream.write(i+'\n')
			self.prevData=self.curData
		self.stackedWidget.setCurrentIndex(3)
	def changeFilePath(self):
		filepath=q.QFileDialog.getExistingDirectory(self,'Select Folder')
		if filepath!='':
			self.lineEdit21.setText(filepath)
			self.lineEdit21.selectAll()
	def mouseDoubleClickEvent(self,e):
		q.QMessageBox.information(self,'Info','YT Downloader version 1.1\nCopyright- Cetrion 2021\nsaikatchakraborty4444@gmail.com')
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.Mode,self.prevData,self.paused,self.link='Playlist',[],False,''
		#Page1*********************************************
		clipboard=q.QApplication.clipboard()
		self.changeProp(clipboard.text())
		self.pushButton13.clicked.connect(lambda:self.changeProp(clipboard.text()))
		self.pushButton11.clicked.connect(self.showMinimized)
		self.pushButton12.clicked.connect(self.close)
		self.lineEdit11.returnPressed.connect(self.PageTransform12)
		#Page2****************************************************
		self.pushButton21.clicked.connect(self.showMinimized)
		self.pushButton22.clicked.connect(self.close)
		style=self.pushButton23.style()
		icon=style.standardIcon(q.QStyle.SP_DirOpenIcon)
		self.pushButton23.setIcon(icon)
		self.pushButton23.clicked.connect(self.changeFilePath)
		self.pushButton24.clicked.connect(self.PageTransform23)
		self.pushButton25.clicked.connect(self.back)
		self.radioButton21.toggled.connect(self.setState)
		#Page3****************************************************(Loading page)
		self.pushButton31.clicked.connect(self.showMinimized)
		self.pushButton32.clicked.connect(self.closeEvent)
		self.pushButton34.clicked.connect(self.back)
		#Page4****************************************************
		self.pushButton41.clicked.connect(self.showMinimized)
		self.pushButton42.clicked.connect(self.close)
		self.pushButton43.clicked.connect(self.OpenFile)
		self.pushButton44.clicked.connect(self.Page1)
		self.Page1()
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.stackedWidget.setGraphicsEffect(q.QGraphicsDropShadowEffect(blurRadius=30,xOffset=0,yOffset=0,color=QColor(0,0,0,255)))
		self.thread3=importer()
		self.thread3.start()
	def out(self):
		self.close()
	os.environ['love']='10'
	time.sleep(0.2)
