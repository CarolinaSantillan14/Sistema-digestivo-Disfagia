"""
Proyecto final: Sistema Digestivo


Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: 
    Cabrera Perez Angelica Xileme
    Lopez Garrido Amy Stephany
    Santillan Cardenas Ana Carolina 
Número de control: 
    21212144
    21212164
    21212181
Correo institucional: 
    l21212144@tectijuana.edu.mx
    l21212164@tectijuana.edu.mx
    l21212181@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tF, dt, w, h=0, 0, 10, 1E-3, 8, 5
N = round((tF-t0)/dt)+1
t = np.linspace(t0,tF,N)
u = np.zeros(N); u[round(1/dt):round(2/dt)]=1 #Impulso

#Función de transferencia: Individuo Saludable (Control)
R1= 500
L=0.1E-6
R2=300
C1=10E-6
C2=5E-6
num = [1]
den = [(L*(C1+C2)),(R1*C2+R2*C1),(R1*C2*R2*C1+1)]
sys = ctrl.tf(num,den)
print('Individuo sano (control):')
print(sys)

#Función de transferencia: Individuo Enfermo (Caso)
R1= 15000
L=0.1E-6
R2=7500
C1=10E-6
C2=5E-6
num = [1]
den = [(L*(C1+C2)),(R1*C2+R2*C1),(R1*C2*R2*C1+1)]
sysE = ctrl.tf(num,den)
print('Individuo enfermo (caso):')
print(sysE)


# Componentes del controlador
Rr = 291094.4388
Re = 15894.6401
Cr = 0.1E-6
Ce= 1.5184E-7
numPID = [Rr*Re*Cr*Ce,Re*Ce+Rr*Cr,1]
denPID = [Re*Cr, 0]
PID = ctrl.tf(numPID, denPID)
print(PID) 

#Sistema de control de tratamiento
X = ctrl.series(PID,sysE)
sysPID = ctrl.feedback(X,1,sign=-1)
print('Sistema con tratamiento')
print(sysPID)

fig = plt.figure()
#plt.plot(t, u, '-', color = 'y', label = 'Ventrada')
ts,Vs = ctrl.forced_response(sys,t,u,x0)
plt.plot(t, Vs, '-', color = 'b', label = 'V(t):Control')
ts,Ve = ctrl.forced_response(sysE,t,u,x0)
plt.plot(t,Ve, "-" ,color = 'g',label = "V(t):Caso")
ts,pid = ctrl.forced_response(sysPID,t,Vs,x0)
plt.plot(t,pid,':', linewidth = 3, color = 'r', label = 'V(t):Tratamiento')
plt.grid(False)

#Configuracion de limites
plt.xlim(0,10.1)
plt.xticks(np.arange(0, 10, 1))
plt.ylim(-0.1,1.1)
plt.yticks(np.arange(-0.1, 1.1, 0.1))
 
#Personalizacion de la grafica   
#plt.title("Sistema Digestivo", fontsize = 13) #Titulo de la grafica        
plt.xlabel('$t$[segundos]', fontsize = 11) #Etiqueta EjeX
plt.ylabel('$V(t)$ [Deglución]', fontsize = 11) #Etiqueta EjeY
plt.legend(bbox_to_anchor = (0.5,-0.23),loc = 'center',ncol = 4) #Caja de leyendas

fig.set_size_inches(w, h) #Configuracion de tamaño de imagen
fig.tight_layout() 
namepng = 'sistema_digestivo' + '.png'
namepdf = 'sistema_digestivo' + '.pdf'
fig.savefig(namepng, dpi = 600,bbox_inches = 'tight')
fig.savefig(namepdf, bbox_inches = 'tight')
    


# Respuesta del sistema en lazo abierto y en lazo cerrado
#for i in range(1,6):
#    plotsignals(u[:, i-1], sys,sysE, sysPID, signal[i-1])