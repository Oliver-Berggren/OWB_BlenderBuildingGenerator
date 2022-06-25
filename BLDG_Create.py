import bpy
#import math
import mathutils
from random import randrange
from math import radians
from pprint import pprint

def printGrid(grid): #, sWallNumWallsX, sWallNumWallsY):
    print("printGrid:")
    #for i in range(0, len(grid[0])):
        #for j in range(
        #print(grid[i - 1])
        #print(grid[i])
    #print(len(grid))
    for i in range(0, len(grid)):
        print(grid[i])
    #print(grid[0])
    #print(grid[1])
    #print(grid[2])
    #print(grid[3])
    #print(grid[4])
    #print(grid[3])
    #print(grid[4])
    #for i in range(0, len(grid[0])):
        #print(*grid[i], sep = '\n')
    #print(grid[0][1])
    #print(grid[0][1][2])
    #for word in grid:
        #print(word)
    #print(grid)
    #print(*op, sep = '\n', grid)
    #print(grid[4])

def getCoord(inCoord):
    outCoord = [0, 0]
    outCoord[0] = inCoord[1] + 1 #inCoord[0] + 1
    outCoord[1] = inCoord[0] + 1#inCoord[1] + 1
    #outCoord[2] = 0
    return outCoord

def create_plane_mesh(objname, sx, sy, px, py, pz, rx, ry, rz, norm):
    # Define arrays for holding data    
    myvertex = []
    myfaces = []

    # Create all Vertices
    # vertex 0
    mypoint = [(-sx, -sy, 0.0)]
    myvertex.extend(mypoint)

    # vertex 1
    mypoint = [(sx, -sy, 0.0)]
    myvertex.extend(mypoint)

    # vertex 2
    mypoint = [(-sx, sy, 0.0)]
    myvertex.extend(mypoint)

    # vertex 3
    mypoint = [(sx, sy, 0.0)]
    myvertex.extend(mypoint)

    # -------------------------------------
    # Create all Faces
    # -------------------------------------
    myface = [(0, 1, 3, 2)]
    myfaces.extend(myface)

    mymesh = bpy.data.meshes.new(objname)

    myobject = bpy.data.objects.new(objname, mymesh)

    bpy.context.scene.collection.objects.link(myobject)
    
    # Generate mesh data
    mymesh.from_pydata(myvertex, [], myfaces)
    # Calculate the edges
    mymesh.update(calc_edges=True)

    # Set Location
    myobject.location.x = px
    myobject.location.y = py
    myobject.location.z = pz
    
    # Set Rotation
    previous_mode = myobject.rotation_mode
    myobject.rotation_mode = "XYZ"
    #print(myobject.rotation_euler)
    myobject.rotation_euler = (radians(rx), radians(ry), radians(rz))
    myobject.rotation_mode  = previous_mode
    
    rotX = myobject.rotation_euler[0]
    rotY = myobject.rotation_euler[1]
    rotZ = myobject.rotation_euler[2]
    #print(str(rotX), ", ", str(rotY), ", ", str(rotZ) + "")
    
    if norm == True:
        mymesh.flip_normals()   
    
    return myobject

def sCreateInterior(sBdgNumFloor, sWallSize, sWallNumWallsX, sWallNumWallsY):
    print("")
    offset = sWallSize * 2
    corners = [(0,0,0), (offset * sWallNumWallsX, 0, 0), (0, offset * sWallNumWallsY, 0), (offset * sWallNumWallsX, offset * sWallNumWallsY, 0)]
    #grid = [][]
    w = sWallNumWallsX
    h = sWallNumWallsY
    grid = []
    floor = []
    #for f in range (0, sBdgNumFloors):
    for i in range (0, sWallNumWallsY):
        #print(str(i))
        row = []
        for j in range (0, sWallNumWallsX):
            row.append([j,i])
            #row.append([i,j])
            #print([i,j])
            x = offset * i
            y = offset * j
            z = offset * sBdgNumFloor
            create_plane_mesh("sFlr", sWallSize, sWallSize, x + sWallSize, y + sWallSize, z, 0, 0, 0, False)
            #print(row)
        grid.append(row)
        
    testCoord = getCoord(grid[0][0])
    print(str(testCoord))
    bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=((offset * testCoord[0]) - (offset / 2), (offset * testCoord[1]) - (offset / 2), z), scale=(1, 1, 1))
    printGrid(grid)
        
        #grid.append(row)
        #printGrid(grid, sWallNumWallsX, sWallNumWallsY)
        #print(grid)
        #print("testCoord:")
    

def sCreateExtWall(sWallSize, sWallNumWalls, target, rz, norm):
    print("    sCreateExtWall:")
    print("    | sWallSize = ", str(sWallSize))
    print("    | sWallNumWalls = ", str(sWallNumWalls))
    print("    | target = ", str(target))
    print("    | rz = ", str(rz))
    print("    | norm = ", str(norm))
    #print("########")
    sWall = create_plane_mesh("sWall", sWallSize, sWallSize, target[0], target[1], target[2], 90, 0, rz, norm)
    #print(sWall)
    sWallMod_Array = sWall.modifiers.new(name = 'Array', type = 'ARRAY')
    sWallMod_Array.count = sWallNumWalls
    
def sCreateBdg(coord, sBdgNumSides, sBdgNumFloors, sWallSize, sWallNumWallsX, sWallNumWallsY):
    offset = sWallSize * 2
    rz = 90
    coord[2] = sWallSize
    
    # create exterior walls
    print("sCreateBdg:")
    #print("| target = ", coord)
    #print("########")
    sBdgTopFloor = sBdgNumFloors - 1
    for f in range (0, sBdgNumFloors):
        print("| f = ", str(f))
        print("| target = ", coord)
        if f == sBdgTopFloor:
            print("    | top floor!")
            #sWallNumWallsX = randrange(2, sWallNumWallsX + 1)
            #sWallNumWallsY = randrange(2, sWallNumWallsY + 1)
            #sWallNumWallsX -= 1
            #sWallNumWallsY -= 1
        sCreateInterior(f, sWallSize, sWallNumWallsX, sWallNumWallsY)
        for i in range (0,sBdgNumSides):
            #print(str(i))
            # each wall is either rotated X or Y, opposite of previous
            # 1st wall
            if i == 0:
                coord[0] = 0
                coord[1] = sWallSize
                rz = 90
                #print("1!")
                sCreateExtWall(sWallSize, sWallNumWallsY, coord, rz, True)
            # 2nd wall
            elif i == 1:
                #print("2!")
                coord[0] = sWallSize
                coord[1] = coord[1] + (sWallSize + offset * (sWallNumWallsY - 1))
                rz = 0
                sCreateExtWall(sWallSize, sWallNumWallsX, coord, rz, True)
            # 3rd wall
            elif i == 2: 
                #print("3!")
                coord[0] = coord[0] + (sWallSize + offset * (sWallNumWallsX - 1))
                coord[1] = 0 + sWallSize
                rz = 90
                sCreateExtWall(sWallSize, sWallNumWallsY, coord, rz, False)
                coord[0] = (sWallSize * sWallNumWallsX)
            # 4th wall
            elif i == 3: 
                #print("4!")
                coord[0] = sWallSize
                coord[1] = 0
                rz = 0
                sCreateExtWall(sWallSize, sWallNumWallsX, coord, rz, False)
        coord[0] = 0
        coord[1] = 0
        coord[2] += (sWallSize * 2)
    coord[0] = 0
    coord[1] = 0
    coord[2] = 0
    
    # create interior
    #sCreateInterior(sBdgNumFloors, sWallSize, sWallNumWallsX, sWallNumWallsY)

print("\n########")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


# Building properties
sBdgNumSides = 4
sBdgNumFloors = 3
sWallSize = 3
sWallNumWallsX = 5
sWallNumWallsY = 7

# Building origin
curloc = bpy.context.scene.cursor.location
curloc[0] = 0
curloc[1] = 0
curloc[2] = 0
#print(curloc)

sCreateBdg(curloc, sBdgNumSides, sBdgNumFloors, sWallSize, sWallNumWallsX, sWallNumWallsY)

# offsetx = sWallSize * 2
# offsety = sWallSize * 2
# for i in range(0,10): # x-dir walls
    #create_plane_mesh("sWall", size, size, curloc[0] + (i * offsetx), curloc[1], 90, 0)