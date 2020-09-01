from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import sys



class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Photo Bill Mart")
        self.minsize(640, 400)

        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)

        self.labelFrame_res = ttk.LabelFrame(self, text="Generated Bill")
        self.labelFrame_res.grid(column = 3, row = 4, padx = 20, pady = 20)

        self.button()


    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse File and Generate Bill",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)


    def fileDialog(self):

        self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
        (("jpeg files","*.jpg"),("all files","*.*")) )
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)

        #following details are available in Azure Portal
        
        ENDPOINT = "<insert Resource EndPoint>"
        PROJECT_ID = "<insert Project ID>"

        items=["cinthol_soap",
            "nima",
            "comfort_liquid",
            "himalaya_neem_soap",
            "himalaya_baby_shampoo",
            "genteel",
            "honey_apis",
            "crompton_15w_bulb"]


        index={"cinthol_soap":0 ,
            "nima":1 ,
            "comfort_liquid":2,
            "himalaya_neem_soap":3,
            "himalaya_baby_shampoo":4,
            "genteel":5,
            "honey_apis":6,
            "crompton_15w_bulb":7}
                
        name={"cinthol_soap":"Cinthol Soap" ,
            "nima":"Nima Soap" ,
            "comfort_liquid":"Comfort Fabric Conditioner",
            "himalaya_neem_soap":"Himalaya Neem Soap",
            "himalaya_baby_shampoo":"Himalaya Baby Shampoo",
            "genteel":"Genteel Liquid Detergent",
            "honey_apis":"Apis Himalayan Honey",
            "crompton_15w_bulb":"Crompton Light Bulb 15W"}

        cost=[0 for i in range(8)]

        price=[49.0,14.0,218.0,45.0,160.0,320.0,440.0,160.0]

        #following details are available in custom vision project 

        prediction_key = "<enter Prediction Key >"
        prediction_resource_id = "<enter Resource ID>"
        publish_iteration_name = "<enter Iteration name>"

        credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        predictor = CustomVisionPredictionClient(endpoint=ENDPOINT, credentials=credentials)

        location = self.filename

        location=list(location)
        destination=[]
        for itr in range(len(location)):
            if(location[itr]=="/"):
                destination.append("\\")
            else:
                destination.append(location[itr])
        pic = ''.join(destination)        
        with open(pic, mode="rb") as test_data:
            results = predictor.detect_image(PROJECT_ID, published_name="Iteration1",image_data =test_data.read(),iteration_id= ' e32a6cd8-9a11-42a6-852c-0ec836455726')

        for prediction in results.predictions:
            if(prediction.tag_name in items):
                print ("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))
                cost[index[prediction.tag_name]]+=1

        dash=['-' for i in range(60)]
        tot=0
        qty=0

        #location of test file to store the result
        sys.stdout=open("<enter the location of destination text file>","w")

        print("".join(dash))
        print("Photo Bill Mart")
        print("".join(dash))
        print('{:30s} {:3s}  {:10s} {:3s}'.format("Item Name","Qty","Cost","MRP"))
        print("".join(dash))
        for i in range(8):
            if(cost[i]>0):
                qty+=cost[i]
                print('{:30s} {:3d}  {:7.2f} {:7.2f}'.format(name[items[i]], cost[i], price[i]*cost[i],price[i]))
                tot+=(price[i]*cost[i])
        print("".join(dash))
        print('{:30s} {:3d}  {:7.2f}'.format("Total",qty,tot))
        print("".join(dash))
        sys.stdout.close()
    
        #print("break\n")  

        img = Image.open(self.filename)
        img = img.resize((450, 350), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)


        self.label2 = Label(image=photo,text="Captured Image",compound='bottom')
        self.label2.image = photo 
        self.label2.grid(column=1, row=4)

        self.configfile = Text(self.labelFrame_res, wrap=WORD, width=60, height= 20)
        with open("<enter the location of destination text file>", 'r') as f:
            self.configfile.insert(INSERT, f.read())
        self.configfile.grid(column=3,row=4)



root = Root()
root.mainloop()

























    