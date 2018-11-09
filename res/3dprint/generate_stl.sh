# dodecahedron only
openscad dodecahedron_aruco.scad -o stl/dodecahedron.stl -D "dodecahedron_export=1" -D "aruco_export_all=0"

# individual aruco faces
for i in {0..11}
do
    openscad dodecahedron_aruco.scad -o stl/aruco_white_$i.stl -D "aruco_number=$i" -D "dodecahedron_export=0" -D "aruco_export_all=0" -D "color_to_export=0"
    openscad dodecahedron_aruco.scad -o stl/aruco_black_$i.stl -D "aruco_number=$i" -D "dodecahedron_export=0" -D "aruco_export_all=0" -D "color_to_export=1"
done
