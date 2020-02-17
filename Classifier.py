import ttk
from Tkinter import*

from tkFileDialog import*
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import random


canvas_width = 800   #the area for canvas
canvas_height = 400
                                #GUI PART OF CODE
class project:
    def __init__  (self,root):

        self.font = 'Calibri 20'
        self.blue= 'skyblue'
        self.frame_header = Frame(root)
        self.frame_header.pack(fill=X)
        self.title= Label(self.frame_header, text='Short Message Classifier', bg=self.blue, font= self.font)
        self.title.pack(side= TOP, fill=X, expand= YES)

        self.canvas_line = Canvas(self.frame_header, width=(canvas_width)/8,height=(canvas_height)/50, bg='orange')
        self.canvas_line.pack(fill=BOTH, expand=YES)


        self.frame2= Frame(root, bg=self.blue) 
        self.frame2.pack(fill=X)
        self.frame2_1= Frame(self.frame2, bg=self.blue)
        self.frame2_1.pack(fill=X)
        self.subtitle= Label(self.frame2_1, text='Enter Input File Name', bg=self.blue)
        self.subtitle.pack(side= LEFT, padx= 30, pady = 10)


        self.frame1_2 = Frame(root, bg=self.blue)
        self.frame1_2.pack(fill=X)

        self.statusText = StringVar() # String Variable to hold the display text
        self.statusLabel = Label(self.frame2_1, textvariable=self.statusText, bg='yellow').pack(side=LEFT)
        self.statusText.set("File Not Loaded")
        self.click= Button(self.frame2_1, text='Browse', bg='yellow', command= self.open_file)
        self.click.pack(side= LEFT, padx=60, pady = 10)


        self.subtitle2= Label( self.frame1_2, text=' Choose Classifier', bg=self.blue)
        self.subtitle2.pack(side= LEFT, padx= 30, pady = 10)

        self.subtitle3= Label( self.frame1_2, text=' Set Thresholds', bg=self.blue)
        self.subtitle3.pack(side= RIGHT, padx= 30, pady = 10)

        self.frame2_mid = Frame(root, bg=self.blue)
        self.frame2_mid.pack(fill=X)


        self.frame2_2= Frame(self.frame2_mid, bg=self.blue)
        self.frame2_2.pack(side=LEFT)

        self.modeVar = IntVar()
        self.modeVar.set(0)


        Radiobutton(self.frame2_2, bg=self.blue, text="Naive Bayes", variable=self.modeVar, value=0, command=self.setMode).pack(anchor=W, padx=30, pady=10)
        Radiobutton(self.frame2_2, bg=self.blue, text="Fischer", variable=self.modeVar, value=1, command=self.setMode).pack(anchor=W, padx=30, pady=10)

        self.mode = self.modeVar.get() # mode 0 : Bayes and 1 : Fisher

        self.frame2_3 = Frame(self.frame2_mid, bg=self.blue)
        self.frame2_3.pack(side=RIGHT)

        self.thresholdBox = Entry(self.frame2_3, width=5)
        self.thresholdBox.pack(side=LEFT, padx=10, pady=10)




        self.box_value = StringVar()
        self.threshCombBox = ttk.Combobox(self.frame2_3, textvariable=self.box_value)
        self.threshCombBox['values'] = ("SPAM", "HAM")
        self.threshCombBox.current(0)
        self.threshCombBox.pack(side=LEFT, padx=10, pady=10)
        self.toSet = "SPAM"
        self.threshCombBox.bind("<<ComboboxSelected>>", self.newselection)

        self.clickThresh = Button(self.frame2_3, text="Set Threshold",
                                  bg='yellow', command=self.setThresh)
        self.clickThresh.pack(side=LEFT, padx=10)


        self.threshList = Listbox(self.frame2_3, height=2)
        self.threshList.pack(side=LEFT, padx=10)
        
        self.removeButton = Button(self.frame2_3, text="Remove Selected",
                                   bg='yellow', command=self.removeThresh)
        self.removeButton.pack(side=RIGHT, padx=10)

        self.frame3=Frame(root, bg=self.blue)
        self.frame3.pack(fill=X)
        self.canvas_line2= Canvas (self.frame3, width = (canvas_width)/8, height= (canvas_height)/200, bg='orange')
        self.canvas_line2.pack(fill= BOTH, expand= YES )
        self.click2=Button(self.frame3,text= 'Calculate', bg='yellow', command=self.calculateAccuracy)
        self.click2.pack(side= LEFT, padx= 210, pady= 15)
        self.click3 = Button(self.frame3,text= 'Clear', bg='yellow', command= self.delete)
        self.click3.pack(side= LEFT, padx= 1, pady= 15)

        self.frame_canvas= Frame(root, bg= self.blue)
        self.frame_canvas.pack(side= TOP, fill= BOTH)
        self.canvas = Canvas(self.frame_canvas, bg='white')
        self.canvas.pack(expand=YES)

                #FUNCTIONAL PART OF CODE
        self.folder = {}
        self.folder['defaultextension'] = '.txt'     #you find the type of folder
        self.folder['filetypes'] = [('all files', '.*')] 
        self.folder['initialdir'] = "E:\\Code\\"    #where your folder is

        self.threshold = 1
        self.spamThresh = 0
        self.hamThresh = 0



    def newselection(self, event): # Event when Combobox changed
        self.toSet = self.threshCombBox.get()


    def setThresh(self):        # Set appropriate threshold values
        self.threshold = self.thresholdBox.get()

        if float(self.threshold) > 1.0: # Condition check for threshold values
            self.threshold = 1  
            print "Threshold cannot be greater than 1. Setting it to 1" 
        if float(self.threshold) < 0.0:
            self.threshold = 0    
            print "Threshold cannot be less than 0. Setting it to 0"
        addFlag = 0
        if self.threshList.size()>0:
            for i in range(self.threshList.size()):
                lineText = self.threshList.get(i)
                if self.toSet in lineText: # Checks whether the current toSet threshold is present in the list
                    self.threshList.delete(i)
                    self.threshList.insert(END, self.toSet+" = "+str(self.threshold))
                    if "SPAM" in self.toSet:
                        self.spamThresh = self.threshold
                    else:
                        self.hamThresh = self.threshold
                    addFlag = 0
                    break
                else:
                    addFlag = 1
            if addFlag==1:
                self.threshList.insert(END, self.toSet+" = "+str(self.threshold))
                if "SPAM" in self.toSet:
                    self.spamThresh = self.threshold
                else:
                    self.hamThresh = self.threshold

        else:
            self.threshList.insert(END, self.toSet+" = "+str(self.threshold))
            if "SPAM" == self.toSet:
                self.spamThresh = self.thresholdBox.get()

            else:
                self.hamThresh = self.thresholdBox.get()


    def removeThresh(self):     # Remove threshold values and set it to default
        if self.threshList.size()>0:
            if "SPAM" in self.threshList.get(self.threshList.curselection()):
                self.spamThresh = 0
                self.threshold = 1
            else:
                self.hamThresh = 0
                self.threshold = 1
            self.threshList.delete(self.threshList.curselection())


    def setMode(self):
        self.mode = self.modeVar.get()

    def open_file(self):
        dataFile= askopenfilename(**self.folder)    #to open the folder
        with open(dataFile, 'r') as dfp:
            data = dfp.read()
        data = data.split("\n")

        dataArr = []
        for line in data:
            dataArr.append(line.split("\t"))
        if [''] in dataArr:
            dataArr.remove([''])

        self.statusText.set("File Loaded Successfully") # Change Display text when file loaded
        self.X = []
        self.Y = []

        self.generateFeature(dataArr)

    def calculateAccuracy(self): # Calculate the 10-fold Accuracy of the classifier
        self.delete()
        avgHamAcc = 0
        avgSpamAcc = 0

        for iter in range(10):
            spamAccuracy = 0.0
            hamAccuracy = 0.0
            nHam = 0
            nSpam = 0
            xTrain, yTrain, xTest, yTest = self.generateTrainTest(self.X, self.Y) # Generate Random training and testing set
            y_pred_B = []
        
            if self.mode==0:    # Bayes Classifier
                gnb = GaussianNB()
                gnb.fit(xTrain, yTrain)
                y_pred_B = gnb.predict(xTest)
                prob_pred = gnb.predict_proba(xTest)


                for i in range(len(prob_pred)): # Checking thresholds
                    if y_pred_B[i]==0:
                        if prob_pred[i][0] * float(self.threshold) <prob_pred[i][1]:
                            y_pred_B[i] = -1
                    else:
                        if prob_pred[i][1] * float(self.threshold) <prob_pred[i][0]:
                            y_pred_B[i] = -1
            elif self.mode==1:  # Fisher Classifier
                fld = LinearDiscriminantAnalysis()
                fld.fit(xTrain, yTrain)
                y_pred_B = fld.predict(xTest)
                prob_pred = fld.predict_proba(xTest)


                for i in range(len(prob_pred)): # # Checking thresholds
                    if y_pred_B[i]==0:
                        if prob_pred[i][0]<self.hamThresh:
                            y_pred_B[i] = -1
                    else:
                        if prob_pred[i][1]<self.spamThresh:
                            y_pred_B[i] = -1
            else:
                print "Incorrect Mode"


            for i in range(len(yTest)):
                if yTest[i]==0:
                    nHam = nHam + 1
                    if y_pred_B[i]==0:
                        hamAccuracy = hamAccuracy + 1
                elif yTest[i]==1:
                    nSpam = nSpam + 1
                    if y_pred_B[i]==1:
                        spamAccuracy = spamAccuracy + 1

    
            hamAccuracy = hamAccuracy / float(nHam)
            spamAccuracy = spamAccuracy /float(nSpam)

            avgHamAcc = avgHamAcc + hamAccuracy # Calculating the average accuracy for all 10 trials
            avgSpamAcc = avgSpamAcc + spamAccuracy

        self.label_ham= Label(self.canvas, bg= 'white', text= 'Ham Accuracy :' + str(avgHamAcc*10.) + "%") # Display the results
        self.label_ham.pack(side=TOP)
        self.label_spam = Label(self.canvas, bg='white', text= 'Spam Accuracy: ' + str(avgSpamAcc*10.) + "%")
        self.label_spam.pack(side=TOP)

    def delete(self):
        self.canvas.destroy()      #for canvas
        self.canvas = Canvas(self.frame_canvas, bg='white')
        self.canvas.pack(expand=YES)



    def generateFeature(self, dataArr): # Generate Feature set (As spam messages mostly contain these words they are selected for generating the training set)
        # 0 - Free, 1-Call, 2-isDigit
        featureArr = []
        classArr = []
        for data in dataArr:
            dataFeature = [0, 0, 0]
            dataFeature[0] = dataFeature[0] + data[1].count("Free")
            dataFeature[0] = dataFeature[0] + data[1].count("free")
            dataFeature[0] = dataFeature[0] + data[1].count("FREE")

            dataFeature[1] = dataFeature[1] + data[1].count("Call")
            dataFeature[1] = dataFeature[1] + data[1].count("call")
            dataFeature[1] = dataFeature[1] + data[1].count("CALL")

            digits = "0123456789"
            for dig in digits:
                dataFeature[2] = dataFeature[2] + data[1].count(dig)

            # dataFeature[3] = dataFeature[3] + data[1].count("I")
            # dataFeature[3] = dataFeature[3] + data[1].count(" i ")

            # dataFeature[4] = dataFeature[4] + data[1].count("he")
            # dataFeature[4] = dataFeature[4] + data[1].count("He")
            # dataFeature[4] = dataFeature[4] + data[1].count("she")
            # dataFeature[4] = dataFeature[4] + data[1].count("She")
            # dataFeature[4] = dataFeature[4] + data[1].count("his")
            # dataFeature[4] = dataFeature[4] + data[1].count("His")
            # dataFeature[4] = dataFeature[4] + data[1].count("her")
            # dataFeature[4] = dataFeature[4] + data[1].count("Her")
        
            featureArr.append(dataFeature)
            if "ham" in data[0]: # Class 0 : Ham
                classArr.append(0)
            elif "spam" in data[0]: # Class 1 : Spam
                classArr.append(1)
            else:
                print "Error"
        self.X = featureArr
        self.Y = classArr
        # return featureArr, classArr

    def generateTrainTest(self, X, Y):
        nData = len(X)

        nTest = int(0.1*nData)
        nTrain = nData-nTest
        random.seed()

        divisionPoint = random.randint(0, nTrain)
        xTest = [X[i] for i in range(divisionPoint, divisionPoint+nTest)]
        yTest = [Y[i] for i in range(divisionPoint, divisionPoint+nTest)]
        xTrain = [X[i] for i in range(0, nData) if i<divisionPoint or i>divisionPoint+nTest]
        yTrain = [Y[i] for i in range(0, nData) if i<divisionPoint or i>divisionPoint+nTest]

        return xTrain, yTrain, xTest, yTest



root = Tk()
app = project(root)   #important teacher gave
root.geometry('750x500') # area of root
root.title('Short Message Classifier')
root.mainloop()
