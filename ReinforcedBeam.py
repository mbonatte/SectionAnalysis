"""##Reinforced Beam"""
import math
import numpy as np
import matplotlib.pyplot as plt

class ReinforcedBeam:
    def __init__(self, section, rebars):
        self.section = section
        self.rebars = rebars
    
    def get_moment_res(self,e0,k):
        return self.section.get_section_moment_res(e0,k) + self.rebars.get_rebars_moment_res(e0,k,self.section.center)
    
    def get_normal_res(self,e0,k):
        return self.section.get_section_normal_res(e0,k) + self.rebars.get_rebars_normal_res(e0,k,self.section.center)
    
    def get_stiff(self,e0,k):
        return self.section.get_section_stiff(e0,k) + self.rebars.get_rebars_stiff(e0,k,self.section.center)
    
    def get_e0(self,k = 0, normal_force=0,n_ite = 10):
        e0 = 0
        normal = self.get_normal_res(e0,k)
        n=0
        while(abs(normal)>10 and n!=n_ite):
            stiff = self.get_stiff(e0,k)[0,0]
            e0 = (normal_force - self.get_normal_res(e0,k))/stiff + e0
            normal = self.get_normal_res(e0,k)
        return e0
    
    def check_section(self, normal, moment, n_ite =10):
        norm = 10
        stiff = 10
        n = 0
        e0 = 0
        k = 0
        n_int = self.get_normal_res(e0,k)
        m_int = self.get_moment_res(e0,k)
        while((norm > 0.01) and (stiff > 0.01) and (n <n_ite)):
            stiff = self.get_stiff(e0,k)
            inv_stiff = np.linalg.inv(stiff)
            e0 = e0 + (np.matmul(inv_stiff,np.array([[normal-n_int],[moment-m_int]])))
            e0=(e0[0][0])
            k = k +   (np.matmul(inv_stiff,np.array([[normal-n_int],[moment-m_int]])))
            k=(k[1][0])
            n_int = self.get_normal_res(e0,k)            
            m_int = self.get_moment_res(e0,k)
            norm = math.sqrt((normal-n_int)**2 + (moment-m_int)**2 )
            stiff = np.linalg.det(self.get_stiff(e0,k))
            n+=1
        if (norm > 0.01):
            print ("Section is not stable")
        else:
          print("Section moment resistance: ",self.section.get_section_moment_res(e0,k))
          print("Rebar moment resistance: ",self.rebars.get_rebars_moment_res(e0,k,self.section.center))
          print("Total moment resistance: ",self.get_moment_res(e0,k))
          print()
          print("Section normal resistance: ",self.section.get_section_normal_res(e0,k))
          print("Rebar normal resistance: ",self.rebars.get_rebars_normal_res(e0,k,self.section.center))
          print("Total normal resistance: ",self.get_normal_res(e0,k))
          print()
          fig = plt.subplots(figsize=(5,5))
          ax1 = fig.add_subplot()
          ax2 = fig.add_subplot()
          ax1.set_title("Stress Driagram")
          ax1.set_xlabel('Concrete - Stress')
          ax1.set_ylabel('Height')
          ax1.grid()
          self.section.plot_stress(ax1,e0,k)
          ax2 = ax1.twiny()
          ax2.set_xlabel("Rebar - Stress")
          self.rebars.plot_stress(ax2,e0,k,self.section.center)    
    
    def plot_moment(self,graph, k_max, n_points = 50):
        k = [(k_max/n_points)*i for i in range(n_points)]
        total_moment = [0 for i in k]
        concrete_moment = [0 for i in k]
        rebar_moment = [0 for i in k]
        e0 = 0
        for i in range(n_points):
            e0 = self.get_e0(k[i])
            total_moment[i] = self.get_moment_res(e0,k[i])
            concrete_moment[i]= self.section.get_section_moment_res(e0,k[i])
            rebar_moment[i]= self.rebars.get_rebars_moment_res(e0,k[i],self.section.center)
        graph.plot(k,total_moment)
        graph.grid()
        graph.set(xlabel='Curvature')
        graph.set(ylabel ='Moment')
        graph.set_title("Total moment")
        
        
    def plot_interaction_curve(self,n_points=100):
        fig, graph = plt.subplots(figsize=(5,5))
        graph.grid()
        graph.set_title("Interaction curve")
        graph.set(xlabel='Normal')
        graph.set(ylabel ='Moment')
        failure = [i/n_points for i in range(n_points+1)]
        for i in range (2):
          nu = []
          mu = []
          for f in failure:
            if(f<1/3):
              eb = 10/1000
              et = -40.5*f/1000 + 10/1000
            if(1/3<=f<=2/3):
              eb = -30*f/1000+20/1000
              et = -3.5/1000
            if(1>=f>2/3):
              eb = -6*f/1000+4/1000
              et = 4.5*f/1000-6.5/1000
            if(i==1):
              a=eb
              eb=et
              et=a
            k = (eb-et)/self.section.get_section_height()
            e0 = (eb - k *self.section.center)
            normal = self.get_normal_res(e0,k)
            moment = self.get_moment_res(e0,k)
            nu.append(normal / (self.section.material.fck *self.section.get_area()))
            mu.append(moment / (self.section.material.fck *self.section.get_area()*self.section.get_section_height()))
          graph.plot(nu,mu, color ='b')
