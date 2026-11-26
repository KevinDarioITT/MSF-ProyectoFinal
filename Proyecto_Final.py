
# Proyecto Final: Retinosis en los fotorreceptores

# Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
# Tecnológico Nacional de México [TecNM - Tijuana]
# Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

# Nombre del alumno: De La Cruz Bojorquez Kevin Dario, Del Toro Nuñez Eduardo, Rodriguez Padilla Kevin 
# Número de control: 20210777, C23212399, 22210428
# Correo institucional: L20210777@TIJUANA.TECNM.MX,LC23212399@TIJUANA.TECNM.MX L22210428@TIJUANA.TECNM.MX

# Asignatura: Modelado de Sistemas Fisiológicos
# Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx

# Instalar librerias en consola
# pip install numpy control matplotlib

# Librerias
import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

# Datos generales de la simulacion
x0,t0,tend,dt,w,h = 0,0,1E-3,1E-8,11,5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)

F = np.zeros(N)
F[round(1E-4/dt):] = 1

# Funcion de transferencia: Control
numControl = [150,1500000]
denControl = [7.2897E-10,0.0024515247,252.21325,2792500]

sysControl = ctrl.tf(numControl,denControl)

print(f"Funcion de transferencia Control: {sysControl}\n")

# Funcion de transferencia: Caso
numCaso = [122.4,1224000]
denCaso = [1.0237536E-9,0.002482227936,313.099072,3505600]

sysCaso = ctrl.tf(numCaso,denCaso)

print(f"Funcion de transferencia Caso: {sysCaso}\n")

# Polos del sistema
pControl = np.roots(denControl)
pCaso = np.roots(denCaso)

print(f"Polos del sistema de Control: {pControl}\n")
print(f"Polos del sistema de Caso: {pCaso}\n")

# Componentes del controlador
kP,kI,kD = 100,1E7,0

numPID = [kD,kP,kI]
denPID = [1,0]

PID = ctrl.tf(numPID,denPID)

print(f"Funcion de transferencia del controlador: {PID}\n")

# Sistema de control en lazo cerrado
sysPID = ctrl.feedback(ctrl.series(PID,sysCaso),1,sign=-1)

# Referencia del sistema de control
sysPID = ctrl.series(sysControl,sysPID)

print(f"Funcion de transferencia en lazo cerrado: {sysPID}\n")

# Colores
clr1 = np.array([0,114,189])/255
clr2 = np.array([237,177,32])/255
clr3 = np.array([34,139,34])/255
clr4 = np.array([128,128,128])/255

# Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t,sys,u):
    _,Vs = ctrl.forced_response(sys,t,u,x0)
    return Vs

def closedloop(t,sysPID,u):
    _,VsPID = ctrl.forced_response(sysPID,t,u,x0)
    return VsPID

# Respuestas: Simulaciones numericas
Fs1 = openloop(t,sysControl,F)
FsC = openloop(t,sysCaso,F)
VsPID = closedloop(t,sysPID,F)

# Funcion: Respuestas de la simulacion
def plotsignals(t,c,c1,c2,c3):

    fg = plt.figure(1)
    fg.set_size_inches(w,h)

    plt.rcParams['font.size'] = 11
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']

    plt.plot(t,c,'-',color=clr1,
             linewidth=1.5,label=r'$V_e(t)$')

    plt.plot(t,c1,':',color=clr2,
             linewidth=1.5,label=r'$V_s(t): Control$')

    plt.plot(t,c2,'--',color=clr3,
             linewidth=1.5,label=r'$V_s(t): Caso$')

    plt.plot(t,c3,'--',color=clr4,
             linewidth=1.5,label=r'$V_s(t): Tratamiento\ PID$')

    plt.xlim(0,1E-3)
    plt.xticks(np.linspace(0,1E-3,11))

    plt.ylim(0,1.1)
    plt.yticks(np.arange(0,1.2,0.1))

    plt.ticklabel_format(axis='x',style='sci',
                         scilimits=(-3,-3),useMathText=True)

    plt.xlabel(r'$t$ [s]')
    plt.ylabel(r'$V_s(t)$ [V]')

    plt.legend(title='Control y caso',
               bbox_to_anchor=(0.5,1.0),
               loc='lower center',
               ncol=4,frameon=True)

    fg.savefig('Control_caso_python.pdf',
               bbox_inches='tight')

    plt.show()

# Respuesta al escalon: Control y caso
plotsignals(t,F,Fs1,FsC,VsPID)
