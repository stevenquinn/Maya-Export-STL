#file takes selected object(s) and exports them to ASCII STL file

import maya.cmds as cmds

def exportSTL():
	
	#grab the selected object(s)	
	selected = cmds.ls(sl=True)
	
	
	#only do this if there's something selected
	if(selected > 0):
	
		#bring up the file dialog so the user can tell you where to save this
		filename = cmds.fileDialog2(caption='Export selected as STL')
		
		#find the asterik in the name (stl isn't a file type in maya)		
		extensionIndex =  str(filename[0]).find("*")
		
		#append the stl extension to the filename
		filename = str(filename[0][0: extensionIndex]) + "STL"
		
		#open a file at the filename specified	
		f = open(str(filename), 'w')
		
		#use this for the progress bar
		totalFaces = 0    #progress bar max value
		currentFace = 0   # progress bar current value
		
		#get total number of faces
		for k in range(0, len(selected)):
		
			cmds.select(selected[k])
			
			#Convert that object to faces and select them
			cmds.ConvertSelectionToFaces()
			
			#get the number of faces for that object
			totalFaces += int(cmds.polyEvaluate(f=True))
		
			if(cmds.window("ExportSTL", ex = True)):
				cmds.deleteUI("ExportSTL")
			
			window = cmds.window("ExportSTL", title="ExportSTL", width=100, height=130, s = False)
			cmds.columnLayout( columnAttach=('both', 5), rowSpacing=10, columnWidth=250 )
			
			#create progress bar
			progressControl = cmds.progressBar(maxValue=100, width=100, vis = False)
			
			#show window
			cmds.showWindow(window)
			
		
		#for each object
		for k in range(0, len(selected)):
			
			#opening line for each object
			f.write("solid " + str(selected[k]) + "\n")
			
			#duplicate the current mesh item
			newObj = cmds.duplicate(selected[k])
			
			cmds.select(newObj)
			
			#stl requires objects to be triangulated (why we duplicated the original)
			triangulated = cmds.polyTriangulate(newObj)
			
			#Convert that object to faces and select them
			cmds.ConvertSelectionToFaces() 
				
			#get the number of faces selected
			numFaces = cmds.polyEvaluate( f=True )
						
			for i in range(0, numFaces):
			
				#increment how much progress has been made
				currentFace += 1
			
				#update the progress bar
				progressInc = cmds.progressBar(progressControl, edit=True, maxValue = totalFaces, pr = currentFace, vis = True)
			
				#get the normal vector of the current face
				normals = cmds.polyInfo(str(newObj[0])+".f[" + str(i) + "]", fn = True)
				normalString =  normals[0][20: len(normals[0])]
				normalVector = normalString.split(" ")
				
				#write the normal vector values
				f.write("\t facet normal " + str(normalVector[0]) + " " + str(normalVector[1]) + " " + str(normalVector[2]) + "\n")
				f.write("\t \t outer loop \n")
				
				vertices = cmds.polyListComponentConversion(str(newObj[0]) + ".f[" + str(i) + "]", ff = True, tv = True)
				cmds.select(vertices)
				
				#store the vertices in an array
				vertices = cmds.ls(sl = True, fl = True)
				
				#for every vertex selected, write that to the file
				for j in range(0, len(vertices)):
					pp = cmds.pointPosition(vertices[j], w = True)
					f.write("\t \t \t vertex " + str(pp[0]) + " " + str(pp[1]) + " " + str(pp[2]) + "\n")
				
				
				#close the current face in the file
				f.write("\t \t endloop \n")
				f.write("\t endfacet \n")
			
			#close the current mesh in the file
			f.write("endsolid")
			
			#delete the duplicated object
			cmds.delete(newObj)
		
		#close the file	
		f.close()
		
		#remove the progress window
		cmds.deleteUI("ExportSTL")
		
		#let the user know it's done
		cmds.headsUpMessage(str(filename) + " created.")
		
		#clear the selection
		cmds.select(cl=True)
