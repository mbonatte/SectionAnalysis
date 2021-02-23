"""##Geometry"""
import numpy as np
from abc import ABC, abstractmethod 
class CrossSection(ABC):
    def set_material(self,material):
        self.material = material
    @abstractmethod
    def get_section_height(self):
        pass
    def get_area(self):
        pass
    @abstractmethod
    def get_area_discret(self,n=0):
        pass
    @abstractmethod
    def get_strain(self,e0=0,k=0,pos=0):
        pass
    @abstractmethod
    def get_strains(self,e0=0,k=0):
        pass
    @abstractmethod
    def get_section_normal_res(self,e0,k):
      pass
    @abstractmethod
    def get_section_moment_res(self,e0=0,k=0):
      pass
    @abstractmethod
    def get_section_stiff(self,e0,k):
      pass
    def plot(self, plot=None,e0=0,k=0):
      print("Plot is not implemented for this section")

"""###Rectangle"""

class Rect_section(CrossSection):
    def __init__(self, width, height, material, n_discret = 200):
        self.width = width
        self.height = height
        self.center = height/2
        self.material = material
        self.n_discret = n_discret
        self.h_discret = [(self.height/2+self.height*i)/n_discret for i in range(n_discret)]
    
    def get_section_height(self):
        return self.height

    def get_area(self):
        return self.width*self.height
    
    def get_area_discret(self,n=0):
        return self.width*self.height/self.n_discret
    
    def get_strain(self,e0=0,k=0,pos=0):
        return e0+k*(self.center-pos)
    
    def get_strains(self,e0,k):
        strains = [e0+k*(self.center-self.h_discret[i]) for i in range(len(self.h_discret))]
        return strains
    
    def get_section_normal_res(self,e0,k):
        strains = self.get_strains(e0,k)
        normal = 0
        for i in range(self.n_discret):
            normal += self.get_area_discret(i)*self.material.get_stress(strains[i])
        return normal
    
    def get_section_moment_res(self,e0=0,k=0):
        strains = self.get_strains(e0,k)
        moment = 0
        for i in range(self.n_discret):
            moment += self.get_area_discret(i)*(self.center-self.h_discret[i])*self.material.get_stress(strains[i])
        return moment
      
    def get_section_stiff(self,e0,k):
        strains = self.get_strains(e0,k)
        a00 = 0
        for i in range(self.n_discret):
            a00 += self.get_area_discret(i)*self.material.get_stiff(strains[i])
        a01 = 0
        for i in range(self.n_discret):
            a01 += self.get_area_discret(i)*(self.center-self.h_discret[i])*self.material.get_stiff(strains[i])
        a10 = a01
        a11 = 0
        for i in range(self.n_discret):
            a11 += self.get_area_discret(i)*(self.center-self.h_discret[i])**2*self.material.get_stiff(strains[i])
        return np.array(([a00,a01],[a10,a11]))
    
    def plot_stress(self,graph,e0,k):
        strain = self.get_strains(e0,k)
        stress = [self.material.get_stress(strain[i]) for i in range(len(strain))]
        graph.set(ylim = [0,self.get_section_height()])
        graph.plot(stress,self.h_discret)
        xabs_max = abs(max(graph.get_xlim(), key=abs))
        graph.set_xlim(xmin=-xabs_max, xmax=xabs_max)

"""###T"""

class T_section(CrossSection):
    def __init__(self, h, t, bf, bw, material, n_discret = 100):
        self.h = h
        self.t = t
        self.bf = bf
        self.bw = bw
        self.center = (t*bf*(h-t/2)+(h-t)*bf*(h-t)/2)/self.get_area()
        self.material = material
        self.n_discret = n_discret
        self.h_discret = [(self.h/2+self.h*i)/n_discret for i in range(n_discret)]
    
    def get_section_height(self):
        return self.h

    def get_area(self):
        return self.t*self.bf+(self.h-self.t)*self.bf
    
    def get_area_discret(self,n=0):
        if (self.h_discret[n] < (self.h-self.t)):
          return self.bw*self.h/self.n_discret
        else:
          return self.bf*self.h/self.n_discret
    
    def get_strain(self,e0=0,k=0,pos=0):
        return e0+k*(self.center-pos)
    
    def get_strains(self,e0,k):
        strains = [e0+k*(self.center-self.h_discret[i]) for i in range(len(self.h_discret))]
        return strains

    def get_section_normal_res(self,e0,k):
        strains = self.get_strains(e0,k)
        normal = 0
        for i in range(self.n_discret):
            normal += self.get_area_discret(i)*self.material.get_stress(strains[i])
        return normal
    
    def get_section_moment_res(self,e0=0,k=0):
        strains = self.get_strains(e0,k)
        moment = 0
        for i in range(self.n_discret):
            moment += self.get_area_discret(i)*(self.center-self.h_discret[i])*self.material.get_stress(strains[i])
        return moment
      
    def get_section_stiff(self,e0,k):
        strains = self.get_strains(e0,k)
        a00 = 0
        for i in range(self.n_discret):
            a00 += self.get_area_discret(i)*self.material.get_stiff(strains[i])
        a01 = 0
        for i in range(self.n_discret):
            a01 += self.get_area_discret(i)*(self.center-self.h_discret[i])*self.material.get_stiff(strains[i])
        a10 = a01
        a11 = 0
        for i in range(self.n_discret):
            a11 += self.get_area_discret(i)*(self.center-self.h_discret[i])**2*self.material.get_stiff(strains[i])
        return np.array(([a00,a01],[a10,a11]))
    
    def plot(self,graph,e0,k):
        strain = self.get_strains(e0,k)
        stress = [self.material.get_stress(strain[i]) for i in range(len(strain))]
        graph.set(xlabel='Stress')
        graph.set(ylabel ='Height')
        graph.set_title("Stress Driagram")
        graph.grid()
        graph.plot(stress,self.h_discret)

    def plot_stress(self,graph,e0,k):
        strain = self.get_strains(e0,k)
        stress = [self.material.get_stress(strain[i]) for i in range(len(strain))]
        graph.plot(stress,self.h_discret)
        xabs_max = abs(max(graph.get_xlim(), key=abs))
        graph.set_xlim(xmin=-xabs_max, xmax=xabs_max)

"""###Rebar"""

class Rebar:
    def __init__(self, area, material):
        self.area = area
        self.material = material
    
    def get_normal_stress(self,strain=0):
        return self.area*self.material.get_stress(strain)

class Rebar_Detailing:
    def __init__(self, detail):
      self.rebars   = [detail[i][0] for i in range(len(detail))]
      self.position = [detail[i][1] for i in range(len(detail))]

    def get_rebars_normal_res(self,e0,k,center):
        normal = 0
        for i in range(len(self.rebars)):
            strain = e0+k*(center-self.position[i])
            normal += self.rebars[i].get_normal_stress(strain)
        return normal
    
    def get_rebars_moment_res(self,e0=0,k=0,center=0):
        moment = 0
        for i in range(len(self.rebars)):
            strain = e0+k*(center-self.position[i])
            moment += self.rebars[i].get_normal_stress(strain)*(center-self.position[i])
        return moment
    
    def get_rebars_stiff(self,e0,k,center):
        a00 = 0
        for i in range(len(self.rebars)):
            strain = e0+k*(center-self.position[i])
            a00 += self.rebars[i].area*self.rebars[i].material.get_stiff(strain)
        a01 = 0
        for i in range(len(self.rebars)):
            strain = e0+k*(center-self.position[i])
            a01 += self.rebars[i].area*(center-self.position[i])*self.rebars[i].material.get_stiff(strain)
        a10 = a01
        a11 = 0
        for i in range(len(self.rebars)):
            strain = e0+k*(center-self.position[i])
            a11 += self.rebars[i].area*(center-self.position[i])**2*self.rebars[i].material.get_stiff(strain)
        return np.array(([a00,a01],[a10,a11]))
    
    def plot_stress(self,graph,e0,k,center):
        stress = [self.rebars[i].material.get_stress(e0+k*(center-self.position[i])) for i in range(len(self.rebars))]
        pos = [self.position[i] for i in range(len(self.rebars))]
        for i in range (len(pos)):
            graph.plot([0,stress[i]],[pos[i],pos[i]],color ='r')
        xabs_max = abs(max(graph.get_xlim(), key=abs))
        graph.set_xlim(xmin=-xabs_max, xmax=xabs_max)