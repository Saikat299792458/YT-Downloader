#add more audio codecs and make a choice algorithm for them in case of playlist abr failure
import Cetrion
x=Cetrion.Animator()
x.start()
from tkinter import messagebox
import tkinter.ttk as j
import threading,time,os,subprocess,shutil
import moviepy.editor as me
from pytube import YouTube,request,Playlist
from tkinter import *
from tkinter import filedialog
top=x.stop()
global asizes
asizes=[]
top.geometry('500x300')
top.wm_attributes('-topmost',1)
w1,yt=Button(top),0
w2=w3=w4=w5=w6=w7=w8=w9=w10=w11=w12=w13=w14=w1
top.title('YouTube Downloader')
top.resizable(False,False)
top.iconbitmap('D:/Python/logox.ico')
fname=''
def se(err):
    messagebox.showerror('Error!','An Error Occured! Error Code:'+str(err))
def namefilter(type,spec):
    unacceptables,out=['/','\\','"',':','*','?','|','<','>','&','(',')'],''
    for i in range(len(spec)):
        if spec[i] in unacceptables:
            if type=='a':
                return '-1'
            out+='_'
        else:
            out+=spec[i]
    return out
def info(sample):
    temp=streams.filter(res=sample)
    if list(temp)==[]:
        return
    #Fuckin brackets man! I thought filesize was a method and wasted 1 hour on it
    f=temp.first().filesize/1048576
    if temp.first().is_adaptive:
        if sample!='144p' and sample!='240p':
            if len(asizes)>1:
                f+=asizes[1]
            else:
                f+=asizes[0]
        else:
            f+=asizes[0]
    if mode!=1:
        sample+=', '+str(f)[0:5]+'MB'
    res.append(sample)
def ainfo(sample):
    temp=streams.filter(abr=sample)
    if list(temp)==[]:
        return
    asizes.append(temp.first().filesize/1048576)
    if mode!=1:
        sample+=', '+str(asizes[len(asizes)-1])[0:5]+'MB'
    abr.append(sample)
def go():
    global fname,yt,streams,res,abr,captions,clist,filename,vdos,qt
    vdos=[]
    if mode:
        for x in Playlist(fname).videos:
            vdos.append(x)
        yt=vdos[0]
    else:
        yt=YouTube(fname)
    res,abr,clist=[],[],[]
    streams=yt.streams
    if mode:
        filename=Playlist(fname).title
    else:
        filename=yt.title
    captions=yt.captions
    ainfo('128kbps')
    ainfo('256kbps')
    info('360p')
    info('144p')#More processing will be required for getting the size of dash streams
    info('240p')
    info('480p')
    info('720p')
    info('1080p')
    info('2160p')
    if captions.get('en'):#I'm Not sure about this
        clist.append('Engilsh')#Add more languages
    if qt!=True:
        page2()
def dthread():
    atemp,div,fs,convert,resos=0,1,0,False,['2160p','1080p','720p','480p','360p','240p','144p']
    if var.get()==0:
        if svar.get()==1 and clist!=[]:
            f=open(filepath+fsname[:len(fsname)-3]+'srt','w',encoding='utf-8')#A serious exception
            cap=captions.get(ssvar.get()[0:2].lower())
            f.write(cap.generate_srt_captions())
            f.close()
        ind=resos.index(vvar.get().split(',')[0]);dif=1;mul=-1
        temp=streams.filter(res=resos[ind]).first()
        while temp==None:#Do the same shit for audio codecs
            if ind+dif*mul>=0 and ind+dif*mul<7:
                temp=streams.filter(res=resos[ind+dif*mul]).first()
            if mul==1:
                mul=-1
                dif+=1
            else:
                mul=1
        if temp.is_adaptive:
            atemp=streams.filter(abr=avar.get().split(',')[0]).first()
            fs+=atemp.filesize
            div=2
            convert=True
            f=open(filepath+'Yolo.mp4','wb')
        else:
            f=open(filepath+fsname,'wb')
    else:
        temp=streams.filter(abr=avar.get().split(',')[0]).first()
        f=open(filepath+fsname,'wb')
    fs+=temp.filesize
    temp=request.stream(temp.url)
    downloaded=0
    def dele():
        global filepath,fsname
        try:
            os.remove(filepath+fsname)
        except:
            pass
        try:
            os.remove(filepath+'Yolo.mp4')
        except:
            pass
        try:
            os.remove(filepath+'temp.mp3')
        except:
            pass
    while 1:
        global paused,cancelled,www3,pbv
        if cancelled:
            f.close()
            dele()
            return
        while paused:
            top.update_idletasks()
            time.sleep(1)
        chunk=next(temp,None)
        if chunk:
            f.write(chunk)
            downloaded+=len(chunk)
            mtemp=int(downloaded*100/(fs*div))
            if qt!=1 and cancelled!=1:
                if w3['text']=='Paused':
                    www3=str(mtemp)+'% Complete'
                    pbv=int(mtemp*4/div)
                else:
                    w3['text']=str(mtemp)+'% Complete'
                    w2['value']=int(mtemp*4/div)
        else:
            if div==2:
                div=1
                f.close()
                temp=request.stream(atemp.url)
                f=open(filepath+'temp.mp3','wb')
                continue
            f.close()
            if convert==True and qt!=1 and cancelled!=1:
                while paused:
                    top.update_idletasks()
                    time.sleep(1)
                w3['text']='Converting...'
                clip1=me.VideoFileClip(filepath+'Yolo.mp4')
                clip2=clip1.set_audio(me.AudioFileClip(filepath+'temp.mp3'))
                clip2.write_videofile(filepath+fsname)
                os.remove(filepath+'Yolo.mp4')
                os.remove(filepath+'temp.mp3')
            if mode!=1 and qt!=1:
                page4()
            break
class chc(threading.Thread):
    def run(self):
        try:
            go()
        except Exception as e:
            if qt!=1:
                page1()
                se(e)#https://www.youtube.com/watch?v=IVMquMDUQZY
class down(threading.Thread):
    def run(self):
        try:
            if mode:
                for i in range(len(vdos)):
                    global fsname,streams,cancelled
                    if cancelled==True:
                        break
                    if paused:
                        top.update_idletasks()
                        time.sleep(1)
                    yt=vdos[i]
                    streams=yt.streams
                    fsname=namefilter('b',yt.title)
                    if var.get()==0:
                        fsname+='.mp4'
                    else:
                        fsname+='.mp3'
                    sth='Downloading('+str(i+1)+'/'+str(len(vdos))+'):'+fsname[0:22]
                    if fsname[38:]!='':
                        sth+='...'
                    w1['text']=sth
                    w3['text']='0% Complete'
                    dthread()
                if qt!=1:
                    page4()
            else:
                dthread()
        except Exception as e:
            if qt!=1:
                page1()
                se(e)
def destroyer():
    w1.destroy()
    w2.destroy()
    w3.destroy()
    w4.destroy()
    w5.destroy()
    w6.destroy()
    w7.destroy()
    w8.destroy()
    w9.destroy()
    w10.destroy()
    w11.destroy()
    w12.destroy()
    w13.destroy()
    w14.destroy()
def launch():
    top.wm_attributes('-topmost',0)
    try:
        if mode:
            path=filepath.rstrip('/')
            path=os.path.realpath(path)
            os.startfile(path)
        else:
            subprocess.call(filepath+fsname,shell=True)
    except Exception as e:
        se(e)
def page4():
    destroyer()
    global w1,w2,w3
    frame=Frame(top)
    frame.place(anchor='w',relx=.08,rely=.18)
    w1=Label(frame,font=('Calibri',17))
    w1.pack(side=TOP)
    if mode:
        str='Download Comlete: '+namefilter('a',filename[0:19])
    else:
        str='Download Complete: '+fsname[0:19]
    if fsname[38:]!='':
        str+='...'
    w1['text']=str
    framex=Frame(top)
    framex.place(anchor='e',relx=.9,rely=.8)
    w2=Button(framex,text='Open',command=launch)
    w3=Button(framex,text='Main Menu',command=page1)
    w3.pack(side=RIGHT)
    w2.pack(side=RIGHT)
    w2.focus()
    w2.bind('<Right>',lambda e:w3.focus())
    w3.bind('<Left>',lambda e:w2.focus())
    w2.bind('<Return>',lambda e:w2.invoke())
    w3.bind('<Return>',lambda e:w3.invoke())
def page3():
    global filepath,fsname,w1,w2,w3,w4,w5,uvalue,paused,cancelled,t2,pg3,forsave,www3,pbv
    pg3,www3,pbv=True,'',0#For the closing protocol
    filepath=forsave=w2.get()+'/'
    fsname=w14.get()
    if namefilter('a',fsname)=='-1':
        messagebox.showerror('Error','A file name cannot contain any of the following characters:\n                  \/:*?"<>|&()')
        return
    if mode:
        if os.path.isdir(filepath+fsname):
            shutil.rmtree(filepath+fsname)
        os.mkdir(filepath+fsname)#Permission error could be raised
        filepath+=fsname+'/'
    else:
        str=fsname[len(fsname)-3:len(fsname)]
        if str!='mp4' and str!='mp3':
            if var.get()==0:
                fsname+='.mp4'
            else:
                fsname+='.mp3'
    destroyer()
    uvalue=0
    w1,paused,cancelled=Label(top,font=('Calibri',17)),False,False
    w1.place(anchor='w',relx=.08,rely=.18)
    str='Downloading: '+fsname[0:25]
    if fsname[38:]!='':
        str+='...'
    w1['text']=str
    #ProgressBAR
    w2,t2=j.Progressbar(top,orient=HORIZONTAL,length=400,mode='determinate'),down()
    w2.place(anchor='w',relx=.08,rely=.3)
    w2.start(25)
    frame=Frame(top)
    frame.place(anchor='e',relx=.9,rely=.8)
    w3=Label(top,text='0% Complete',font=('Calibri',17))
    w3.place(anchor='w',relx=.08,rely=.4)
    def changestate():
        global paused,www3,pbv
        if w5['text']=='Pause':
            paused=True
            www3=w3['text']
            pbv=w2['value']
            w3['text']='Paused'
            w2.stop()
            w5.config(text='Resume')
        else:
            paused=False
            w3['text']=www3
            w2['value']=pbv
            w2.start(25)
            w5.config(text='Pause')
    w5=Button(frame,text='Pause',command=changestate)
    w4=Button(frame,text='Cancel',command=page2)
    w4.pack(side=RIGHT)
    w5.pack(side=RIGHT)
    w5.focus()
    w4.bind('<Left>',lambda e:w5.focus())
    w5.bind('<Right>',lambda e:w4.focus())
    w4.bind('<Return>',lambda e:w4.invoke())
    w5.bind('<Return>',lambda e:w5.invoke())
    t2.start()
def chpg():
    global w1,w2,w3,fname,t1#fname=URL,fsname=filtered filename/foldername,filename=video title
    fname=w2.get()
    destroyer()
    fprogress=StringVar(top)
    w1=Label(top,font=('Calibri',17))
    w1.place(anchor='w',relx=.08,rely=.18)
    w1['text']='Checking...'
    #https://www.youtube.com/watch?v=IVMquMDUQZY
    w3=Button(top,text='Cancel',command=page1)
    w3.place(anchor='e',relx=.9,rely=.8)
    w3.focus()
    w3.bind('<Return>',lambda e:w3.invoke())
    t1=chc()
    t1.start()
    w2=j.Progressbar(top,orient=HORIZONTAL,length=400,mode='indeterminate')
    w2.place(anchor='w',relx=.08,rely=.3)
    w2.start(25)
def page2():
    global pg2,cancelled
    cancelled=pg2=True
    destroyer()
    global w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13,w14,var,svar,vvar,avar,ssvar
    frame=Frame(top)
    frame.place(anchor="c", relx=.5, rely=.5)
    frame2,frame3,frame4,frame5,frame6,frame7=Frame(frame),Frame(frame),Frame(frame),Frame(top),Frame(top),Frame(frame)
    frame3.pack(side=BOTTOM,anchor=W)
    frame4.pack(side=BOTTOM)
    frame2.pack(side=BOTTOM,anchor=W)
    frame7.pack(side=BOTTOM,anchor=W)
    frame5.place(anchor='e',relx=.9,rely=.8)
    frame6.place(anchor='w',relx=.08,rely=.18)
    var,svar=IntVar(),IntVar(top)
    vvar,avar,ssvar=StringVar(top),StringVar(top),StringVar(top)
    w1=Label(frame,text='Download To:')
    w2=Entry(frame)
    def bff():
        tfn=filedialog.askdirectory()
        if tfn!='':
            w2.delete(0,END)
            w2.insert(0,tfn)
            w2.select_range(0,'end')
    def da():
        l=w14.get()
        if mode!=1:
            w14.delete(len(l)-1)
            w14.insert(len(l),'4')
        w6.config(state=NORMAL)
        if clist!=[]:
            w8.config(state=NORMAL)
            w9.config(state=NORMAL)
        w7.config(state=DISABLED)
    def dv():
        l=w14.get()
        if mode!=1:
            w14.delete(len(l)-1)
            w14.insert(len(l),'3')
        w7.config(state=NORMAL)
        w6.config(state=DISABLED)
        w8.config(state=DISABLED)
        w9.config(state=DISABLED)
    w12=Label(frame6,font=('Calibri',17))
    str=filename[0:38]
    if filename[38:]!='':
        str+='...'
    w12['text']=str
    w12.pack(side=RIGHT)
    w13=Label(frame7,text='Save As:')
    w14=Entry(frame7)
    w13.pack(side=LEFT)
    w14.pack(side=LEFT)
    if mode:
        w14.insert(0,namefilter('b',filename))
    else:
        w14.insert(0,namefilter('b',filename)+'.mp4')
    w3=Button(frame,text='Change',command=bff)
    w4=Radiobutton(frame2,text='Download Video:',variable=var,value=0,command=da)
    w4.pack(side=LEFT)
    w6=OptionMenu(frame2,vvar,*res)#unpacking list for arguments
    w6.pack(side=RIGHT)
    w8=Checkbutton(frame4,text='Download Subtitle:',variable=svar,onvalue=1,offvalue=0)
    w8.pack(side=LEFT)
    w9=OptionMenu(frame4,ssvar,'English')
    if clist==[]:
        w8.config(state=DISABLED)
        w9.config(state=DISABLED)
    w9.pack(side=RIGHT)
    w5=Radiobutton(frame3,text='Download Audio:',variable=var,value=1,command=dv)
    w5.pack(side=LEFT)
    w7=OptionMenu(frame3,avar,*abr)
    w7.pack(side=RIGHT)
    w10=Button(frame5,text='Cancel',command=page1)
    w10.pack(side=RIGHT)
    w11=Button(frame5,text='Download',command=page3)
    w11.pack(side=RIGHT)
    w2.select_range(0,END)
    w1.pack(side=LEFT)
    w2.pack(side=LEFT)
    w3.pack(side=LEFT)
    global dir,issub,av,sublan,vr,abr1
    dir,av,issub,sublan,vr,abr1='C:/Users/Dell',0,1,'English',res[0],abr[0]
    try:
        fstream=open('preferences.txt','r')
        fo=fstream.readline()
        dir=fo.rstrip('\n')
        fo=fstream.readline()
        fo=fo.split()
        av=int(fo[0])
        issub=int(fo[1])
        sublan=fo[2]
        for i in res:
            if i.split(',')[0]==fo[3]:
                vr=i
                break
        for i in abr:
            if i.split(',')[0]==fo[3]:
                abr1=i
                break
        fstream.close()
    except:
        pass
    w2.insert(0,dir)
    var.set(av);
    if av==0:da()
    else:dv()
    svar.set(issub)
    ssvar.set(sublan)
    vvar.set(vr)
    avar.set(abr[0])
    w11.focus()
    w11.bind('<Up>',lambda e:w4.invoke())
    w11.bind('<Down>',lambda e:w5.invoke())
    w10.bind('<Up>',lambda e:w4.invoke())
    w10.bind('<Down>',lambda e:w5.invoke())
    w11.bind('<Right>',lambda e:w10.focus())
    w10.bind('<Left>',lambda e:w11.focus())
    w11.bind('<Return>',lambda e:w11.invoke())
    w10.bind('<Return>',lambda e:w10.invoke())
def closing():
    global t1,t2,cancelled,pg2,pg3,qt,top
    mdir=''#Do something for checking...
    if pg3:
        if t2.is_alive():
            if messagebox.askokcancel('Quit','Are you sure to quit?\nDownload is in progress.'):
                cancelled=True
            else:
                return
    if pg2:
        if pg3:
            mdir=forsave.rstrip('/')
        else:
            mdir=w2.get()
        fo=open('preferences.txt','w')
        fo.write(mdir+'\n')#python D:\Python\YouTubeDownloader.py
        fo.write(str(var.get())+' ')
        fo.write(str(svar.get())+' ')
        fo.write(ssvar.get()+' ')
        fo.write(vvar.get().split(',')[0]+' ')
        fo.write(avar.get().split(',')[0]+' ')
        fo.close()
    qt=True
    #import gc
    #del top
    #gc.collect()
    quit()
def page1():
    destroyer()
    global w1,w2,w3,w4,mode,pg3,pg2,qt
    pg3=pg2=qt=False
    frame=Frame(top)
    frame.place(anchor='c',relx=.5,rely=.5)
    w1,mode=Button(frame,text='Check',command=chpg),False
    w2,cbdata=Entry(frame,fg='grey'),''
    php,phv=PhotoImage(file=r'D:/Python/playlist2.png'),PhotoImage(file=r'D:/Python/video2.png')
    try:
        cbdata=top.clipboard_get()
    except:
        pass
    def clear(_):#it takes a blank positional argument
        w2.delete(0,END)
        w2.config(fg='black')
    def mess():
        global mode
        w2.delete(0,END)
        w2.config(fg='grey')
        if mode==False:
            mode=True
            w3.config(image=phv)
            w4.config(text='Enter a Video URL Instead.')
            if 'https://www.youtube.com/playlist?' in cbdata[0:33]:
                w2.insert(0,cbdata)
            else:
                w2.insert(0,'Enter Playlist URL')
        else:
            mode=False
            w3.config(image=php)
            w4.config(text='Enter a Playlist URL Instead.')
            if 'https://www.youtube.com/watch?' in cbdata[0:30]:
                w2.insert(0,cbdata)
            else:
                w2.insert(0,'Enter Video URL')
    w2.bind('<FocusIn>',clear)#This bad boy gets it when entry gets focus
    w3=Button(frame,image=php,command=mess,height='20',width='20')
    w3.image=php#Its called keeping a reference,image won't show without it.
    w4=Label(top,text='Enter a Playlist URL Instead.',bg='yellow')
    w1.pack(side=BOTTOM)
    w2.pack(side=LEFT)
    w3.pack(side=RIGHT)
    w3.bind('<Enter>',lambda e:w4.place(anchor='w',relx=0.6,rely=0.53))
    w3.bind('<Leave>',lambda e:w4.place_forget())
    w1.focus()
    w1.bind('<Return>',lambda e:w1.invoke())
    w1.bind('<Up>',lambda e:w3.invoke())
    w1.bind('<Down>',lambda e:w3.invoke())
    if 'https://www.youtube.com/watch?' in cbdata[0:30]:
        w2.insert(0,top.clipboard_get())
    else:
        w2.insert(0,'Enter Video URL')
    top.focus_force()
page1()
top.protocol('WM_DELETE_WINDOW',closing)
top.mainloop()
