import sys
import os	

'''
	Crea los casos a simular a partir de una plantilla.
	Con distintas proporciones de oxidos, diferentes radios minimos y a su vez distintos radios maximos
	de particula. Entre estos se aproxima una distribucion uniforme con 'n_sizes' tamanos discretos. 
	Los scripts input que comparten la misma proporcion se guardan en un mismo directorio.
'''

#############
# Variables #
#############

# Radios minimo y maximo considerados
Rmin_lab  = 100 	# micras
Rmax_lab  = 1500 	# micras
# Steps
prop_step = 5       # Paso porcentual en la proporcion de MgO en la mezcla
R_step    = 200	    # micras
# Numero de diferentes radios para aproximar la distribucion uniforme con valores discretos
n_sizes   = 20


##########################################
# Experimentos con distribucion uniforme #
##########################################

# Crea o vacia el contenido de scripts para dejar lugar a los nuevos experimentos
os.system("sudo mkdir ./scripts")
os.system("sudo rm -r ./scripts/*")

# Variacion de las proporciones en la mezcla
for percen_MgO in range(50,100+prop_step,prop_step):
	# Directorios para ordenar por proporciones
	os.system("sudo mkdir ./scripts/input_MgO-%.1f" % (percen_MgO))
	# Variacion del radio minimo de particula
	for Rmin in range(Rmin_lab, Rmax_lab, R_step):
		# Variacion del radio maximo de particula
		for Rmax in range(Rmin, Rmax_lab, R_step):
			# Carpetas para albergar la geometria y resultados de la simulacion
			os.system("sudo mkdir ./scripts/input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f" % (percen_MgO, Rmin, Rmax))
			os.system("sudo cp -R ./meshes ./scripts/input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f/" % (percen_MgO, Rmin, Rmax))
			os.system("sudo mkdir ./scripts/input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f/post" % (percen_MgO, Rmin, Rmax))
			os.system("sudo chmod -R 777 ./scripts/")

			# Comando linux 'sed'(String EDitor)
			# Sustitucion de valores en in.plantilla1, in.plantilla2, in.plantilla3 para el nuevo script
			os.system("sed -e 's/VAR_n_sizes/%d/g' -e 's/VAR_percen_MgO/%.1f/g' -e 's/VAR_R_min/%.0f/g' \
			  -e 's/VAR_R_max/%.0f/g' in.plantilla1 > scripts/%s/in1.MgO_%.1f_Rmin_%.0f_Rmax_%.0f" % (n_sizes,
			  percen_MgO, Rmin, Rmax, 'input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f' % (percen_MgO, Rmin, Rmax), percen_MgO,
			  Rmin, Rmax))
			os.system("sed -e 's/VAR_n_sizes/%d/g' -e 's/VAR_percen_MgO/%.1f/g' -e 's/VAR_R_min/%.0f/g' \
			  -e 's/VAR_R_max/%.0f/g' in.plantilla2 > scripts/%s/in2.MgO_%.1f_Rmin_%.0f_Rmax_%.0f" % (n_sizes,
			  percen_MgO, Rmin, Rmax, 'input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f' % (percen_MgO, Rmin, Rmax), percen_MgO,
			  Rmin, Rmax))
			os.system("sed -e 's/VAR_n_sizes/%d/g' -e 's/VAR_percen_MgO/%.1f/g' -e 's/VAR_R_min/%.0f/g' \
			  -e 's/VAR_R_max/%.0f/g' in.plantilla3 > scripts/%s/in3.MgO_%.1f_Rmin_%.0f_Rmax_%.0f" % (n_sizes,
			  percen_MgO, Rmin, Rmax, 'input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f' % (percen_MgO, Rmin, Rmax), percen_MgO,
			  Rmin, Rmax))
			os.system("sed -e 's/VAR_n_sizes/%d/g' -e 's/VAR_percen_MgO/%.1f/g' -e 's/VAR_R_min/%.0f/g' \
			  -e 's/VAR_R_max/%.0f/g' in.plantilla4 > scripts/%s/in4.MgO_%.1f_Rmin_%.0f_Rmax_%.0f" % (n_sizes,
			  percen_MgO, Rmin, Rmax, 'input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f' % (percen_MgO, Rmin, Rmax), percen_MgO,
			  Rmin, Rmax))

			#############################################################################
			# Lineas para el input script con los radios y las plantillas de particulas #
			#############################################################################
			radiusString = ""
			templatesString = ""
			particledistibution = ("fix pdd2 all particledistribution/discrete 5430 ${n_templates} "
				"pts0 ${prop_MgO_size} pts1 ${prop_Al2O3_size} ")
			for i in range(1,n_sizes):
				r_i = i*(Rmax-Rmin)/(n_sizes-1)
				# Introduce los distintos radios
				radiusString = radiusString + "\n" + ("variable r%d equal ${R_min}+"
				  "((${R_max}-${R_min})/(${n_sizes}-1))*%d") % (i, i)
				# Introduce las diferentes plantillas de las particulas
				templatesString = templatesString + "\n" + ("fix pts%d all particletemplate/sphere "
				  "1 atom_type 1 density constant ${rho_MgO} radius constant ${r%d}") % (2*i, i)
				templatesString = templatesString + "\n" + ("fix pts%d all particletemplate/sphere "
				  "1 atom_type 2 density constant ${rho_Al2O3} radius constant ${r%d}") % (2*i+1, i)
				particledistibution = particledistibution + "pts%d ${prop_MgO_size} pts%d ${prop_Al2O3_size} " \
				% (2*i, 2*i+1)


			filename = "scripts/%s/in1.MgO_%.1f_Rmin_%.0f_Rmax_%.0f" % ('input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f' \
			  % (percen_MgO, Rmin, Rmax), percen_MgO, Rmin, Rmax)
			tempfileName = "scripts/%s/tempfile" % ('input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f' % (percen_MgO, Rmin, Rmax))
			file = open(filename,'r')
			tempfile = open(tempfileName,'a')
			# Lee cada linea y escribe en el archivo temporal
			for line in file.readlines():
				if line.startswith('-----'):
					tempfile.write(radiusString)

				elif line.startswith('~~~~~'):
					tempfile.write(templatesString)	

				elif line.startswith('*****'):
					tempfile.write(particledistibution)	

				else:
					tempfile.write(line)

			file.close
			tempfile.close

			# Sobreescribe el archivo input 1 con el contenido del archivo temporal recien creado
			os.system("sudo mv scripts/%s/tempfile scripts/%s/in1.MgO_%.1f_Rmin_%.0f_Rmax_%.0f" \
			  % ('input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f' % (percen_MgO, Rmin, Rmax), \
			  'input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f' % (percen_MgO, Rmin, Rmax), percen_MgO, Rmin, Rmax))

			# Genera archivos para la ejecucion de la simulacion completa
			#os.system("sudo cp ./ejecuta ./scripts/input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f/" % (percen_MgO, Rmin, Rmax))
			os.system("sed -e 's/proporcion/%.1f/g' -e 's/radioMinimo/%.0f/g' -e 's/radioMaximo/%.0f/g' \
			  ./ejecuta.py > scripts/%s/ejecuta.py" % (percen_MgO, Rmin, Rmax,
			  'input_MgO-%.1f/Rmin_%.0f_Rmax_%.0f' % (percen_MgO, Rmin, Rmax)))
