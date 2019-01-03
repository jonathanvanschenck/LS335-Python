import serial
import numpy as np
class LS335:
    def __init__(self,comport="COM3",verbose=True):
        self.ser = serial.Serial(comport,baudrate=57600,parity=serial.PARITY_ODD,stopbits=1,bytesize=7,timeout=0.1)
        self._t = "\r\n"
        self.verbose = verbose
        self._rdic = {"Off":"0","Low":"1","Medium":"2","High":"3"}
        self._rlist = np.array(["Off","Low","Medium","High"])
        self.getPID()
        self.getSP()
        self.getRange()
        
    def getPID(self):
        self._pid = np.array([[float(i[1:]) for i in (self.query("PID? "+j).split(self._t)[-2]).split(",")[-3:]] for j in ["1","2"]])
        #self._pid = np.array([[float(i[1:]) for i in (self.query("PID? "+j)[:-2]).split(",")[-3:]] for j in ["1","2"]])
        if self.verbose:
            print()#Fix
        return self._pid
    def setPID(self,pid=None,p=None,i=None,d=None,which=1):
        if pid:
            pt,it,dt=pid
        else:
            pt,it,dt=p,i,d
        pt2,it2,dt2 = self.getPID()[which-1]
        if pt:
            assert pt>=0.1 and pt<=1000
            pt2=1*pt
        if it:
            assert it>=0.1 and it<=1000
            it2=1*it
        if dt:
            assert dt>=0 and dt<=200
            dt2=1*dt
        self.query("PID "+str(which)+","+str(pt2)+","+str(it2)+","+str(dt2))
        return self.getPID()
    
    def getSP(self):
        self._sp = np.array([float(self.query("SETP? "+j).split(self._t)[-2]) for j in ["1","2"]])
        #self._sp = np.array([float(self.query("SETP? "+j)[-8:-2]) for j in ["1","2"]])
        return self._sp
    def setSP(self,Temp,which=1):
        self.query("SETP "+str(which)+","+str(Temp))
        return self.getSP()

    def getRange(self):
        self._range = [self._rlist[int(self.query("RANGE? "+j)[-3:-2])] for j in ["1","2"]]
        return self._range
    def setRange(self,rangeStr=None,rangeInd=None,which=1):
        if rangeStr:
            self.query("RANGE "+str(which)+","+self._rdic[rangeStr])
            return self.getRange()
        if rangeInd:
            assert rangeInd in [0,1,2,3]
            self.query("RANGE "+str(which)+","+str(rangeInd))
            return self.getRange()
        return self.getRange()
    
    def getTemp(self,which=1,unit="K"):
        return float(self.query(unit+"RDG? "+str(which)).split(self._t)[-2])

    def getHeat(self,which=1):
        return float(self.query("HTR? "+str(which)).split(self._t)[-2])/100
    
    def off(self):
        self.setRange("Off",which=1)
        self.setRange("Off",which=2)
    def query(self,message):
        self.ser.write((str(message)+self._t).encode())
        return self.ser.read(1000).decode()
    def close(self):
        self.ser.close()
