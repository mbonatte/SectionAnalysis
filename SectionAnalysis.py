{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Beam_section.ipynb",
      "provenance": [],
      "collapsed_sections": [
        "j97zFO-XNbww",
        "hKE8RqMeytQj",
        "DC856U2EyxNt",
        "02eZclAuy1r0",
        "xCJJ4oRty5a4"
      ],
      "toc_visible": true,
      "authorship_tag": "ABX9TyOwjN809B803BYLv60rLwLw"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "atQHpAX1M6A5"
      },
      "source": [
        "# Initial libraries"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "o3hXjSu9NAt0"
      },
      "source": [
        "import numpy as np\r\n",
        "import math\r\n",
        "import matplotlib.pyplot as plt"
      ],
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "XsrdKebpNBtE"
      },
      "source": [
        "# Classes"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "j97zFO-XNbww"
      },
      "source": [
        "##Material"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "hrzq1H5uNXnX"
      },
      "source": [
        "import abc \r\n",
        "from abc import ABC, abstractmethod \r\n",
        "class Material(ABC):\r\n",
        "    @abstractmethod\r\n",
        "    def get_stiff(self):\r\n",
        "      pass\r\n",
        "    @abstractmethod\r\n",
        "    def get_stress(self):\r\n",
        "      pass\r\n",
        "    def plot(self, plot=None):\r\n",
        "      print(\"Plot is not implemented for this material\")"
      ],
      "execution_count": 2,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "hKE8RqMeytQj"
      },
      "source": [
        "###Concrete"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "VRzh6Q8oNdux"
      },
      "source": [
        "class Concrete(Material):\r\n",
        "    def __init__(self, young=0, fck=0):\r\n",
        "        self.young = young\r\n",
        "        self.fck = fck\r\n",
        "        self.ftk = fck/10 * 0\r\n",
        "    def get_stiff(self, strain =0):\r\n",
        "        ec2 = -2/1000\r\n",
        "        ec35 = -3.5/1000\r\n",
        "        et1 = self.ftk/self.young\r\n",
        "        if (ec2 <= strain <= 0):\r\n",
        "            return 2*self.fck*(strain/ec2-1)/ec2\r\n",
        "        elif (ec35 <= strain <= ec2):\r\n",
        "            return 0\r\n",
        "        elif (strain <= ec35):\r\n",
        "            return 0\r\n",
        "        elif (0 < strain <= et1):\r\n",
        "            return self.young\r\n",
        "        elif (et1 < strain):\r\n",
        "            return 0\r\n",
        "    def get_stress(self, strain =0):\r\n",
        "        ec2 = -2/1000\r\n",
        "        ec35 = -3.5/1000\r\n",
        "        et1 = self.ftk/self.young\r\n",
        "        if (ec2 <= strain <= 0):\r\n",
        "            return -self.fck*(1-(1-strain/ec2)**2)\r\n",
        "        elif (ec35 <= strain <= ec2):\r\n",
        "            return -self.fck\r\n",
        "        elif (strain <= ec35):\r\n",
        "            return 0\r\n",
        "        elif (0 < strain <= et1):\r\n",
        "            return self.young*strain\r\n",
        "        elif (et1 < strain):\r\n",
        "            return 0\r\n",
        "    def plot(self,graph):\r\n",
        "        strain = np.arange(-3.7/1000,1/5000,1/50000)\r\n",
        "        stress = [self.get_stress(strain[i]) for i in range(len(strain))]\r\n",
        "        graph.set(xlabel='Strain')\r\n",
        "        graph.set(ylabel ='Stress')\r\n",
        "        graph.set_title(\"Concrete Driagram\")\r\n",
        "        graph.grid()\r\n",
        "        graph.plot(strain,stress)"
      ],
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "DC856U2EyxNt"
      },
      "source": [
        "###Steel"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "sQ-rGJphyybm"
      },
      "source": [
        "class Steel(Material):\r\n",
        "    def __init__(self, young=0, fy=0, ult_strain=0):\r\n",
        "        self.young = young\r\n",
        "        self.fy = fy\r\n",
        "        self.ult_strain = ult_strain\r\n",
        "    def get_stiff(self, strain =0):\r\n",
        "        ey = self.fy / self.young\r\n",
        "        if (-ey <= strain <= ey):\r\n",
        "            return self.young\r\n",
        "        else:\r\n",
        "            return 0\r\n",
        "    def get_stress(self, strain =0):\r\n",
        "        ey = self.fy / self.young\r\n",
        "        if (-ey <= strain <= ey):\r\n",
        "            return self.young*strain\r\n",
        "        elif (ey < strain <=self.ult_strain):\r\n",
        "            return self.fy\r\n",
        "        elif (-ey > strain>=-self.ult_strain):\r\n",
        "            return -self.fy\r\n",
        "        else:\r\n",
        "            return 0\r\n",
        "    def plot(self,graph):\r\n",
        "        strain = np.arange(-self.ult_strain,self.ult_strain+self.ult_strain/100,self.ult_strain/100)\r\n",
        "        stress = [self.get_stress(strain[i]) for i in range(len(strain))]\r\n",
        "        graph.set(xlabel='Strain')\r\n",
        "        graph.set(ylabel ='Stress')\r\n",
        "        graph.set_title(\"Steel Driagram\")\r\n",
        "        graph.grid()\r\n",
        "        graph.plot(strain,stress)"
      ],
      "execution_count": 4,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "CX3ZyIE2NSSz"
      },
      "source": [
        "##Geometry"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "xEa0nrXtmss4"
      },
      "source": [
        "import abc \r\n",
        "from abc import ABC, abstractmethod \r\n",
        "class CrossSection(ABC):\r\n",
        "    @abstractmethod\r\n",
        "    def get_section_height(self):\r\n",
        "        pass\r\n",
        "    def get_area(self):\r\n",
        "        pass\r\n",
        "    @abstractmethod\r\n",
        "    def get_area_discret(self,n=0):\r\n",
        "        pass\r\n",
        "    @abstractmethod\r\n",
        "    def get_strain(self,e0=0,k=0,pos=0):\r\n",
        "        pass\r\n",
        "    @abstractmethod\r\n",
        "    def get_strains(self,e0=0,k=0):\r\n",
        "        pass\r\n",
        "    @abstractmethod\r\n",
        "    def get_section_normal_res(self,e0,k):\r\n",
        "      pass\r\n",
        "    @abstractmethod\r\n",
        "    def get_section_moment_res(self,e0=0,k=0):\r\n",
        "      pass\r\n",
        "    @abstractmethod\r\n",
        "    def get_section_stiff(self,e0,k):\r\n",
        "      pass\r\n",
        "    def plot(self, plot=None,e0=0,k=0):\r\n",
        "      print(\"Plot is not implemented for this section\")"
      ],
      "execution_count": 5,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "02eZclAuy1r0"
      },
      "source": [
        "###Rectangle"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "EA7NLyDoNMca"
      },
      "source": [
        "class Rect_section(CrossSection):\r\n",
        "    def __init__(self, width, height, material, n_discret = 200):\r\n",
        "        self.width = width\r\n",
        "        self.height = height\r\n",
        "        self.center = height/2\r\n",
        "        self.material = material\r\n",
        "        self.n_discret = n_discret\r\n",
        "        self.h_discret = [(self.height/2+self.height*i)/n_discret for i in range(n_discret)]\r\n",
        "    \r\n",
        "    def get_section_height(self):\r\n",
        "        return self.height\r\n",
        "\r\n",
        "    def get_area(self):\r\n",
        "        return self.width*self.height\r\n",
        "    \r\n",
        "    def get_area_discret(self,n=0):\r\n",
        "        return self.width*self.height/self.n_discret\r\n",
        "    \r\n",
        "    def get_strain(self,e0=0,k=0,pos=0):\r\n",
        "        return e0+k*(self.center-pos)\r\n",
        "    \r\n",
        "    def get_strains(self,e0,k):\r\n",
        "        strains = [e0+k*(self.center-self.h_discret[i]) for i in range(len(self.h_discret))]\r\n",
        "        return strains\r\n",
        "    \r\n",
        "    def get_section_normal_res(self,e0,k):\r\n",
        "        strains = self.get_strains(e0,k)\r\n",
        "        normal = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            normal += self.get_area_discret(i)*self.material.get_stress(strains[i])\r\n",
        "        return normal\r\n",
        "    \r\n",
        "    def get_section_moment_res(self,e0=0,k=0):\r\n",
        "        strains = self.get_strains(e0,k)\r\n",
        "        moment = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            moment += self.get_area_discret(i)*(self.center-self.h_discret[i])*self.material.get_stress(strains[i])\r\n",
        "        return moment\r\n",
        "      \r\n",
        "    def get_section_stiff(self,e0,k):\r\n",
        "        strains = self.get_strains(e0,k)\r\n",
        "        a00 = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            a00 += self.get_area_discret(i)*self.material.get_stiff(strains[i])\r\n",
        "        a01 = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            a01 += self.get_area_discret(i)*(self.center-self.h_discret[i])*self.material.get_stiff(strains[i])\r\n",
        "        a10 = a01\r\n",
        "        a11 = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            a11 += self.get_area_discret(i)*(self.center-self.h_discret[i])**2*self.material.get_stiff(strains[i])\r\n",
        "        return np.array(([a00,a01],[a10,a11]))\r\n",
        "    \r\n",
        "    def plot_stress(self,graph,e0,k):\r\n",
        "        strain = self.get_strains(e0,k)\r\n",
        "        stress = [self.material.get_stress(strain[i]) for i in range(len(strain))]\r\n",
        "        graph.set(ylim = [0,self.get_section_height()])\r\n",
        "        graph.plot(stress,self.h_discret)\r\n",
        "        xabs_max = abs(max(graph.get_xlim(), key=abs))\r\n",
        "        graph.set_xlim(xmin=-xabs_max, xmax=xabs_max)"
      ],
      "execution_count": 6,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "xCJJ4oRty5a4"
      },
      "source": [
        "###T"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "5dBxx3iXy6YS"
      },
      "source": [
        "class T_section(CrossSection):\r\n",
        "    def __init__(self, h, t, bf, bw, material, n_discret = 100):\r\n",
        "        self.h = h\r\n",
        "        self.t = t\r\n",
        "        self.bf = bf\r\n",
        "        self.bw = bw\r\n",
        "        self.center = (t*bf*(h-t/2)+(h-t)*bf*(h-t)/2)/self.get_area()\r\n",
        "        print(self.center)\r\n",
        "        self.material = material\r\n",
        "        self.n_discret = n_discret\r\n",
        "        self.h_discret = [(self.h/2+self.h*i)/n_discret for i in range(n_discret)]\r\n",
        "    \r\n",
        "    def get_section_height(self):\r\n",
        "        return self.h\r\n",
        "\r\n",
        "    def get_area(self):\r\n",
        "        return self.t*self.bf+(self.h-self.t)*self.bf\r\n",
        "    \r\n",
        "    def get_area_discret(self,n=0):\r\n",
        "        if (self.h_discret[n] < (self.h-self.t)):\r\n",
        "          return self.bw*self.h/self.n_discret\r\n",
        "        else:\r\n",
        "          return self.bf*self.h/self.n_discret\r\n",
        "    \r\n",
        "    def get_strain(self,e0=0,k=0,pos=0):\r\n",
        "        return e0+k*(self.center-pos)\r\n",
        "    \r\n",
        "    def get_strains(self,e0,k):\r\n",
        "        strains = [e0+k*(self.center-self.h_discret[i]) for i in range(len(self.h_discret))]\r\n",
        "        return strains\r\n",
        "\r\n",
        "    def get_section_normal_res(self,e0,k):\r\n",
        "        strains = self.get_strains(e0,k)\r\n",
        "        normal = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            normal += self.get_area_discret(i)*self.material.get_stress(strains[i])\r\n",
        "        return normal\r\n",
        "    \r\n",
        "    def get_section_moment_res(self,e0=0,k=0):\r\n",
        "        strains = self.get_strains(e0,k)\r\n",
        "        moment = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            moment += self.get_area_discret(i)*(self.center-self.h_discret[i])*self.material.get_stress(strains[i])\r\n",
        "        return moment\r\n",
        "      \r\n",
        "    def get_section_stiff(self,e0,k):\r\n",
        "        strains = self.get_strains(e0,k)\r\n",
        "        a00 = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            a00 += self.get_area_discret(i)*self.material.get_stiff(strains[i])\r\n",
        "        a01 = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            a01 += self.get_area_discret(i)*(self.center-self.h_discret[i])*self.material.get_stiff(strains[i])\r\n",
        "        a10 = a01\r\n",
        "        a11 = 0\r\n",
        "        for i in range(self.n_discret):\r\n",
        "            a11 += self.get_area_discret(i)*(self.center-self.h_discret[i])**2*self.material.get_stiff(strains[i])\r\n",
        "        return np.array(([a00,a01],[a10,a11]))\r\n",
        "    \r\n",
        "    def plot(self,graph,e0,k):\r\n",
        "        strain = self.get_strains(e0,k)\r\n",
        "        stress = [self.material.get_stress(strain[i]) for i in range(len(strain))]\r\n",
        "        graph.set(xlabel='Stress')\r\n",
        "        graph.set(ylabel ='Height')\r\n",
        "        graph.set_title(\"Stress Driagram\")\r\n",
        "        graph.grid()\r\n",
        "        graph.plot(stress,self.h_discret)\r\n",
        "\r\n",
        "    def plot_stress(self,graph,e0,k):\r\n",
        "        strain = self.get_strains(e0,k)\r\n",
        "        stress = [self.material.get_stress(strain[i]) for i in range(len(strain))]\r\n",
        "        graph.plot(stress,self.h_discret)\r\n",
        "        xabs_max = abs(max(graph.get_xlim(), key=abs))\r\n",
        "        graph.set_xlim(xmin=-xabs_max, xmax=xabs_max)"
      ],
      "execution_count": 7,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "aHkacbw9y-oF"
      },
      "source": [
        "###Rebar"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "YGjIfwVmlIdd"
      },
      "source": [
        "class Rebar:\r\n",
        "    def __init__(self, area, material):\r\n",
        "        self.area = area\r\n",
        "        self.material = material\r\n",
        "    \r\n",
        "    def get_normal_stress(self,strain=0):\r\n",
        "        return self.area*self.material.get_stress(strain)\r\n",
        "\r\n",
        "class Rebar_Detailing:\r\n",
        "    def __init__(self, detail):\r\n",
        "      self.rebars   = [detail[i][0] for i in range(len(detail))]\r\n",
        "      self.position = [detail[i][1] for i in range(len(detail))]\r\n",
        "\r\n",
        "    def get_rebars_normal_res(self,e0,k,center):\r\n",
        "        normal = 0\r\n",
        "        for i in range(len(self.rebars)):\r\n",
        "            strain = e0+k*(center-self.position[i])\r\n",
        "            normal += self.rebars[i].get_normal_stress(strain)\r\n",
        "        return normal\r\n",
        "    \r\n",
        "    def get_rebars_moment_res(self,e0=0,k=0,center=0):\r\n",
        "        moment = 0\r\n",
        "        for i in range(len(self.rebars)):\r\n",
        "            strain = e0+k*(center-self.position[i])\r\n",
        "            moment += self.rebars[i].get_normal_stress(strain)*(center-self.position[i])\r\n",
        "        return moment\r\n",
        "    \r\n",
        "    def get_rebars_stiff(self,e0,k,center):\r\n",
        "        a00 = 0\r\n",
        "        for i in range(len(self.rebars)):\r\n",
        "            strain = e0+k*(center-self.position[i])\r\n",
        "            a00 += self.rebars[i].area*self.rebars[i].material.get_stiff(strain)\r\n",
        "        a01 = 0\r\n",
        "        for i in range(len(self.rebars)):\r\n",
        "            strain = e0+k*(center-self.position[i])\r\n",
        "            a01 += self.rebars[i].area*(center-self.position[i])*self.rebars[i].material.get_stiff(strain)\r\n",
        "        a10 = a01\r\n",
        "        a11 = 0\r\n",
        "        for i in range(len(self.rebars)):\r\n",
        "            strain = e0+k*(center-self.position[i])\r\n",
        "            a11 += self.rebars[i].area*(center-self.position[i])**2*self.rebars[i].material.get_stiff(strain)\r\n",
        "        return np.array(([a00,a01],[a10,a11]))\r\n",
        "    \r\n",
        "    def plot_stress(self,graph,e0,k,center):\r\n",
        "        stress = [self.rebars[i].material.get_stress(e0+k*(center-self.position[i])) for i in range(len(self.rebars))]\r\n",
        "        pos = [self.position[i] for i in range(len(self.rebars))]\r\n",
        "        for i in range (len(pos)):\r\n",
        "            graph.plot([0,stress[i]],[pos[i],pos[i]],color ='r')\r\n",
        "        xabs_max = abs(max(graph.get_xlim(), key=abs))\r\n",
        "        graph.set_xlim(xmin=-xabs_max, xmax=xabs_max)"
      ],
      "execution_count": 8,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Ui95-V_c0C4V"
      },
      "source": [
        "##Reinforced Beam"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "QNMkvrif0BsZ"
      },
      "source": [
        "class ReinforcedBeam:\r\n",
        "    def __init__(self, section, rebars):\r\n",
        "        self.section = section\r\n",
        "        self.rebars = rebars\r\n",
        "    \r\n",
        "    def get_moment_res(self,e0,k):\r\n",
        "        return self.section.get_section_moment_res(e0,k) + self.rebars.get_rebars_moment_res(e0,k,self.section.center)\r\n",
        "    \r\n",
        "    def get_normal_res(self,e0,k):\r\n",
        "        return self.section.get_section_normal_res(e0,k) + self.rebars.get_rebars_normal_res(e0,k,self.section.center)\r\n",
        "    \r\n",
        "    def get_stiff(self,e0,k):\r\n",
        "        return self.section.get_section_stiff(e0,k) + self.rebars.get_rebars_stiff(e0,k,self.section.center)\r\n",
        "    \r\n",
        "    def get_e0(self,k = 0, normal_force=0,n_ite = 10):\r\n",
        "        e0 = 0\r\n",
        "        normal = self.get_normal_res(e0,k)\r\n",
        "        n=0\r\n",
        "        while(abs(normal)>10 and n!=n_ite):\r\n",
        "            stiff = self.get_stiff(e0,k)[0,0]\r\n",
        "            e0 = (normal_force - self.get_normal_res(e0,k))/stiff + e0\r\n",
        "            normal = self.get_normal_res(e0,k)\r\n",
        "        return e0\r\n",
        "    \r\n",
        "    def check_section(self, normal, moment, n_ite =10):\r\n",
        "        norm = 10\r\n",
        "        stiff = 10\r\n",
        "        n = 0\r\n",
        "        e0 = 0\r\n",
        "        k = 0\r\n",
        "        n_int = self.get_normal_res(e0,k)\r\n",
        "        m_int = self.get_moment_res(e0,k)\r\n",
        "        while((norm > 0.01) and (stiff > 0.01) and (n <n_ite)):\r\n",
        "            stiff = self.get_stiff(e0,k)\r\n",
        "            inv_stiff = np.linalg.inv(stiff)\r\n",
        "            e0 = e0 + (np.matmul(inv_stiff,np.array([[normal-n_int],[moment-m_int]])))\r\n",
        "            e0=(e0[0][0])\r\n",
        "            k = k +   (np.matmul(inv_stiff,np.array([[normal-n_int],[moment-m_int]])))\r\n",
        "            k=(k[1][0])\r\n",
        "            n_int = self.get_normal_res(e0,k)            \r\n",
        "            m_int = self.get_moment_res(e0,k)\r\n",
        "            norm = math.sqrt((normal-n_int)**2 + (moment-m_int)**2 )\r\n",
        "            stiff = np.linalg.det(self.get_stiff(e0,k))\r\n",
        "            n+=1\r\n",
        "        if (norm > 0.01):\r\n",
        "            print (\"Section is not stable\")\r\n",
        "        else:\r\n",
        "          print(\"Section moment resistance: \",self.section.get_section_moment_res(e0,k))\r\n",
        "          print(\"Rebar moment resistance: \",self.rebars.get_rebars_moment_res(e0,k,self.section.center))\r\n",
        "          print(\"Total moment resistance: \",self.get_moment_res(e0,k))\r\n",
        "          print()\r\n",
        "          print(\"Section normal resistance: \",self.section.get_section_normal_res(e0,k))\r\n",
        "          print(\"Rebar normal resistance: \",self.rebars.get_rebars_normal_res(e0,k,self.section.center))\r\n",
        "          print(\"Total normal resistance: \",self.get_normal_res(e0,k))\r\n",
        "          print()\r\n",
        "          fig, ax1 = plt.subplots(figsize=(8,6))\r\n",
        "          ax1.set_title(\"Stress Driagram\")\r\n",
        "          ax1.set_xlabel('Concrete - Stress')\r\n",
        "          ax1.set_ylabel('Height')\r\n",
        "          ax1.grid()\r\n",
        "          self.section.plot_stress(ax1,e0,k)\r\n",
        "          ax2 = ax1.twiny()\r\n",
        "          ax2.set_xlabel(\"Rebar - Stress\")\r\n",
        "          self.rebars.plot_stress(ax2,e0,k,self.section.center)    \r\n",
        "    \r\n",
        "    def plot_moment(self,graph,k_max = 0.02,n_points = 50):\r\n",
        "        k = [(k_max/n_points)*i for i in range(n_points)]\r\n",
        "        total_moment = [0 for i in k]\r\n",
        "        concrete_moment = [0 for i in k]\r\n",
        "        rebar_moment = [0 for i in k]\r\n",
        "        e0 = 0\r\n",
        "        for i in range(n_points):\r\n",
        "            e0 = self.get_e0(k[i])\r\n",
        "            total_moment[i] = self.get_moment_res(e0,k[i])\r\n",
        "            concrete_moment[i]= self.section.get_section_moment_res(e0,k[i])\r\n",
        "            rebar_moment[i]= self.rebars.get_rebars_moment_res(e0,k[i],self.section.center)\r\n",
        "        graph[0].plot(k,total_moment)\r\n",
        "        graph[0].grid()\r\n",
        "        graph[0].set(xlabel='Curvature')\r\n",
        "        graph[0].set(ylabel ='Moment')\r\n",
        "        graph[0].set_title(\"Total moment\")\r\n",
        "        graph[1].plot(k,concrete_moment)\r\n",
        "        graph[1].grid()\r\n",
        "        graph[1].set(xlabel='Curvature')\r\n",
        "        graph[1].set(ylabel ='Moment')\r\n",
        "        graph[1].set_title(\"Concrete moment\")\r\n",
        "        graph[2].plot(k,rebar_moment)\r\n",
        "        graph[2].grid()\r\n",
        "        graph[2].set(xlabel='Curvature')\r\n",
        "        graph[2].set(ylabel ='Moment')\r\n",
        "        graph[2].set_title(\"Rebar moment\")\r\n",
        "        \r\n",
        "    def plot_interaction_curve(self,n_points=100):\r\n",
        "        fig, graph = plt.subplots(1, 1,figsize=(6,6))\r\n",
        "        graph.grid()\r\n",
        "        graph.set_title(\"Interaction curve\")\r\n",
        "        graph.set(xlabel='Normal')\r\n",
        "        graph.set(ylabel ='Moment')\r\n",
        "        failure = [i/n_points for i in range(n_points+1)]\r\n",
        "        for i in range (2):\r\n",
        "          nu = []\r\n",
        "          mu = []\r\n",
        "          for f in failure:\r\n",
        "            if(f<1/3):\r\n",
        "              eb = 10/1000\r\n",
        "              et = -40.5*f/1000 + 10/1000\r\n",
        "            if(1/3<=f<=2/3):\r\n",
        "              eb = -30*f/1000+20/1000\r\n",
        "              et = -3.5/1000\r\n",
        "            if(1>=f>2/3):\r\n",
        "              eb = -6*f/1000+4/1000\r\n",
        "              et = 4.5*f/1000-6.5/1000\r\n",
        "            if(i==1):\r\n",
        "              a=eb\r\n",
        "              eb=et\r\n",
        "              et=a\r\n",
        "            k = (eb-et)/self.section.get_section_height()\r\n",
        "            e0 = (eb - k *self.section.center)\r\n",
        "            normal = self.get_normal_res(e0,k)\r\n",
        "            moment = self.get_moment_res(e0,k)\r\n",
        "            nu.append(normal / (self.section.material.fck *self.section.get_area()))\r\n",
        "            mu.append(moment / (self.section.material.fck *self.section.get_area()*self.section.get_section_height()))\r\n",
        "          graph.plot(nu,mu, color ='b')"
      ],
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "eMFK2OReOI37"
      },
      "source": [
        "#Beam 20x65"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "kDRH2y6nHuNS"
      },
      "source": [
        "##Geometry and material"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "-mMoIUc4ONsP",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "2d99af33-f3de-4bbe-f570-548b8a3f57c8"
      },
      "source": [
        "concrete_25 = Concrete(young=25e9,fck=25e6)\r\n",
        "steel_500 = Steel(young=210*10**9,fy=500*10**6,ult_strain=10e-3)\r\n",
        "\r\n",
        "rec_20x32 = Rect_section(width=0.2,height=0.32,material=concrete_25)\r\n",
        "t = T_section(h=0.5,t=0.1,bf=0.5,bw=0.2,material=concrete_25)\r\n",
        "\r\n",
        "d10_2_500  = Rebar(area=2*78e-6,material=steel_500)\r\n",
        "d12_2_500 = Rebar(2*113e-6,steel_500)\r\n",
        "d16_2_500 = Rebar(2*201e-6,steel_500)\r\n",
        "\r\n",
        "rebars_detail_01 = Rebar_Detailing([[d16_2_500,0.05],\r\n",
        "                                    [d16_2_500,0.16],\r\n",
        "                                    [d16_2_500,0.27]])\r\n",
        "\r\n",
        "rebars_detail_02 = Rebar_Detailing([[d12_2_500,0.05],\r\n",
        "                                    [d12_2_500,0.08],\r\n",
        "                                    [d12_2_500,0.11]])\r\n",
        "\r\n",
        "column_01 = ReinforcedBeam(rec_20x32,rebars_detail_01)\r\n",
        "t_beam_01 = ReinforcedBeam(t,rebars_detail_02)"
      ],
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "0.25000000000000006\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "cr0QPNPUOYbl"
      },
      "source": [
        "#Material plot"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 0
        },
        "id": "rSHsp5CfOavm",
        "outputId": "5e3bdb40-98a7-4b93-ae52-63f401077051"
      },
      "source": [
        "fig, material_plot = plt.subplots(2, 1,figsize=(8,12))\r\n",
        "concrete_25.plot(material_plot[0])\r\n",
        "steel_500.plot(material_plot[1])"
      ],
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 576x864 with 2 Axes>"
            ]
          },
          "metadata": {
            "tags": [],
            "needs_background": "light"
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2rPprHGQOma1"
      },
      "source": [
        "#Moment Plot"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "D_0w36_BOrIU",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 910
        },
        "outputId": "6819a0b7-1370-4112-9d30-adea1fe0813c"
      },
      "source": [
        "fig, ax = plt.subplots(3, 1,figsize=(8,15))\r\n",
        "t_beam_01.plot_moment(graph=ax,k_max=0.04,n_points=100)"
      ],
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "/usr/local/lib/python3.6/dist-packages/ipykernel_launcher.py:21: RuntimeWarning: divide by zero encountered in double_scalars\n"
          ],
          "name": "stderr"
        },
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 576x1080 with 3 Axes>"
            ]
          },
          "metadata": {
            "tags": [],
            "needs_background": "light"
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ATtLrurFPWlK"
      },
      "source": [
        "#Check Section"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "JrG1MgT5Pa1p",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 574
        },
        "outputId": "c5facd5a-300b-470e-948e-388f5cadcd48"
      },
      "source": [
        "t_beam_01.check_section(normal =0, moment = 135e3)"
      ],
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Section moment resistance:  77369.99999997942\n",
            "Rebar moment resistance:  57630.00000000002\n",
            "Total moment resistance:  134999.99999997945\n",
            "\n",
            "Section normal resistance:  -338999.99999990076\n",
            "Rebar normal resistance:  339000.0\n",
            "Total normal resistance:  9.924406185746193e-08\n",
            "\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 576x432 with 2 Axes>"
            ]
          },
          "metadata": {
            "tags": [],
            "needs_background": "light"
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "kwj-tX0ztqrX"
      },
      "source": [
        "#Interaction curve"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "52fYLWrJtx8D",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 404
        },
        "outputId": "04fee085-a642-4c31-ebe6-59416f984c23"
      },
      "source": [
        "column_01.plot_interaction_curve(n_points = 500)"
      ],
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 432x432 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": [],
            "needs_background": "light"
          }
        }
      ]
    }
  ]
}