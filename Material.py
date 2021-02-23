import numpy as np
from abc import ABC, abstractmethod 

class Material(ABC):
    @abstractmethod
    def get_stiff(self):
      pass
    @abstractmethod
    def get_stress(self):
      pass
    def plot(self, plot=None):
      print("Plot is not implemented for this material")

class Concrete(Material):
    def __init__(self, young=0, fck=0):
        self.young = young
        self.fck = fck
        self.ftk = fck/10 * 0
    def get_stiff(self, strain =0):
        ec2 = -2/1000
        ec35 = -3.5/1000
        et1 = self.ftk/self.young
        if (ec2 <= strain <= 0):
            return 2*self.fck*(strain/ec2-1)/ec2
        elif (ec35 <= strain <= ec2):
            return 0
        elif (strain <= ec35):
            return 0
        elif (0 < strain <= et1):
            return self.young
        elif (et1 < strain):
            return 0
    def get_stress(self, strain =0):
        ec2 = -2/1000
        ec35 = -3.5/1000
        et1 = self.ftk/self.young
        if (ec2 <= strain <= 0):
            return -self.fck*(1-(1-strain/ec2)**2)
        elif (ec35 <= strain <= ec2):
            return -self.fck
        elif (strain <= ec35):
            return 0
        elif (0 < strain <= et1):
            return self.young*strain
        elif (et1 < strain):
            return 0
    def plot(self,graph):
        strain = np.arange(-3.7/1000,1/5000,1/50000)
        stress = [self.get_stress(strain[i]) for i in range(len(strain))]
        graph.set(xlabel='Strain')
        graph.set(ylabel ='Stress')
        graph.set_title("Concrete Driagram")
        graph.grid()
        graph.plot(strain,stress)

class Steel(Material):
    def __init__(self, young=0, fy=0, ult_strain=0):
        self.young = young
        self.fy = fy
        self.ult_strain = ult_strain
    def get_stiff(self, strain =0):
        ey = self.fy / self.young
        if (-ey <= strain <= ey):
            return self.young
        else:
            return 0
    def get_stress(self, strain =0):
        ey = self.fy / self.young
        if (-ey <= strain <= ey):
            return self.young*strain
        elif (ey < strain <=self.ult_strain):
            return self.fy
        elif (-ey > strain>=-self.ult_strain):
            return -self.fy
        else:
            return 0
    def plot(self,graph):
        strain = np.arange(-self.ult_strain,self.ult_strain+self.ult_strain/100,self.ult_strain/100)
        stress = [self.get_stress(strain[i]) for i in range(len(strain))]
        graph.set(xlabel='Strain')
        graph.set(ylabel ='Stress')
        graph.set_title("Steel Driagram")
        graph.grid()
        graph.plot(strain,stress)
