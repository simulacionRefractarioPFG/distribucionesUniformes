import os
import glob

# Aproxima
os.system('mpirun -np * liggghts < in1.MgO_proporcion_Rmin_radioMinimo_Rmax_radioMaximo')
# Comprime
os.system('mpirun -np * liggghts < in2.MgO_proporcion_Rmin_radioMinimo_Rmax_radioMaximo')
# Relaja
os.system('mpirun -np * liggghts < in3.MgO_proporcion_Rmin_radioMinimo_Rmax_radioMaximo')

# Recupera el ultimo archivo con la configuracion del sistema
newest = max(glob.iglob('./post/dump*.pruebas'), key=os.path.getctime)
os.system('mv %s ./dump1' % (newest))

#Libera
os.system('mpirun -np * liggghts < in4.MgO_proporcion_Rmin_radioMinimo_Rmax_radioMaximo')

# Recupera el ultimo archivo con la configuracion del sistema
newest = max(glob.iglob('./post/dump*.pruebas'), key=os.path.getctime)
os.system('mv %s ./dump2' % (newest))
