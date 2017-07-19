from threading import Thread
from SlideShow import Slideshow
import tkinter
from peyetribe import EyeTribe
import csv
from random import shuffle
import os


from threading import Thread, Semaphore
import sys
import time


INTERVAL = 10

folderPath = list("C:/Users/Kevin/PycharmProjects/noQuestionnaire/slideShow/test_subject_")

#recursively looks for directory untill it finds one that doesn't exist



def checkFolder(pathName):

    folder_number = 0

    for test_nr in range(0,100):
        if(os.path.exists("".join(pathName)+str(test_nr))):
            print("Folder "+str(test_nr)+" exists")
        else:
            folder_number = test_nr
            os.mkdir("".join(pathName)+str(test_nr))
            break;

    return "".join(pathName)+str(test_nr)


current_folder_test_subject = checkFolder(folderPath)

class EyeTribeThread(Thread):

    def __init__(self):
        super(EyeTribeThread, self).__init__()
        self.closeThread = False
        self.threadIndex = 0
        self.imageNumber = 0
        self.group = "A"


    def run(self):

        tracker = EyeTribe()
        tracker.connect()
        n = tracker.next()
        tracker.pushmode()
        with open(current_folder_test_subject+'/eye_tribe_data_q_{}.csv_'.format(self.threadIndex), 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["eT;dT;aT;Fix;State;Rwx;Rwy;Avx;Avy;LRwx;LRwy;LAvx;LAvy;LPSz;LCx;LCy;RRwx;RRwy;RAvx;RAvy;RPSz;RCx;RCy;GRP"])
        #print("eT;dT;aT;Fix;State;Rwx;Rwy;Avx;Avy;LRwx;LRwy;LAvx;LAvy;LPSz;LCx;LCy;RRwx;RRwy;RAvx;RAvy;RPSz;RCx;RCy")

        while True:
                if self.closeThread == True:
                    print("Thread Closed")
                    break
                n = tracker.next()
                with open(current_folder_test_subject+'/eye_tribe_data_q_{}.csv_'.format(self.threadIndex), 'a') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=' ',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(["{}".format(n)+";"+self.group])
                    print("Thread: {}".format(self.threadIndex))

        tracker.pullmode()
        tracker.close()

class Counter():
    def __init__(self):
        self.value = 0

start_button_clicked = False
width = 768
height = 576

root = tkinter.Tk()

#this is the array of images

code_snippets_A = ["C:/Users/Kevin/Documents/Semester Project/Experiment/Group A/A.jpg", "C:/Users/Kevin/Documents/Semester Project/Experiment/Group A/B.jpg",
"C:/Users/Kevin/Documents/Semester Project/Experiment/Group A/C.jpg", "C:/Users/Kevin/Documents/Semester Project/Experiment/Group A/D.jpg","C:/Users/Kevin/Documents/Semester Project/Experiment/Group A/E.jpg"]
#print(indexOfImage)

code_snippets_B = ["C:/Users/Kevin/Documents/Semester Project/Experiment/Group B/F.jpg", "C:/Users/Kevin/Documents/Semester Project/Experiment/Group B/G.jpg",
"C:/Users/Kevin/Documents/Semester Project/Experiment/Group B/H.jpg", "C:/Users/Kevin/Documents/Semester Project/Experiment/Group B/I.jpg","C:/Users/Kevin/Documents/Semester Project/Experiment/Group B/J.jpg"]
#print(indexOfImage)

#shuffles the code snippets

#No Shuffling required for this one
#shuffle(code_snippets_A)

#creates a slideshow class to display array of images

newClass = Slideshow(root, code_snippets_A, slideshow_delay=3)

#Creates bottom 3 buttons

buttons_D = tkinter.Frame(root,width=500,height=20)

#A Thread so that the values  can be read from the eyetribe simulataneously as the interface is being run
#-------------------------------------------------------------------------------------------------------
#THREADS

threads = []

#Counter is used to keep track of which iteration of threads we are on
#counter.value keeps track of the iteration of threads starting from 0
# the function close_threads adds an iteration after closing current thread

count = Counter()


def start_threads():
    if len(threads) <= count.value:
        #code this to avoid error from double clicking
        threads.append(EyeTribeThread())
        # SEND THE THREAD INFORMATION ABOUT WHICH ITERATION IT IS
        threads[count.value].threadIndex = newClass.image_id
        #STARTS THE THREAD
        threads[count.value].start()
        Start_Button.configure(bg = "green")
    else:
        print("THREAD IS ALLREADY RUNNING")




def close_threads():
    #to avoid errors of shutting down non existing threads
    # we make sure that the length of the array is larger than the current iteration
    if(len(threads) > count.value):
        threads[count.value].closeThread = True
        threads[count.value].join()
        count.value += 1
        Start_Button.configure(bg= "grey")
    else:
        print("NO THREADS TO CLOSE")



def check_if_threads_alive():
    for _newthread in threads:
        print(_newthread.is_alive())


def B_button_clicked(slideshow,threads):
    slideshow.filenames = code_snippets_B
    Group_B_button.configure(bg="green")
    Group_A_button.configure(bg="grey")
    for thread in threads:
        thread.group = "B"


def A_button_clicked(slideshow,threads):
    slideshow.filenames = code_snippets_A
    Group_A_button.configure(bg="green")
    Group_B_button.configure(bg="grey")
    for thread in threads:
        thread.group = "A"



Start_Button = tkinter.Button(buttons_D, text="START", command= start_threads,bg = "grey")

Stop_Button = tkinter.Button(buttons_D, text="STOP", command=close_threads)

Next_Button = tkinter.Button(buttons_D, text="NEXT", command=newClass.if_next_button_clicked)
#Next_Button.bind("<Button-1>",when_next_clicked)

Group_A_button = tkinter.Button(buttons_D, text="A", command= lambda :A_button_clicked(newClass,threads))

Group_B_button = tkinter.Button(buttons_D, text="B", command=lambda :B_button_clicked(newClass,threads))



Start_Button.pack(side=tkinter.LEFT)
Next_Button.pack(side=tkinter.LEFT)
Stop_Button.pack(side=tkinter.LEFT)
Group_A_button.pack(side=tkinter.LEFT)
Group_B_button.pack(side=tkinter.LEFT)
buttons_D.pack()

root.mainloop()


