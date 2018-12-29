diameter = 50;
aruco_data_height= 3;
tol = 0.15;
white_cube_face_height = 2;

/////////////////////////// no touching
radius = diameter/2;
cw = radius/9;
/////////////////////////// cli variables
dodecahedron_export = 1;
aruco_export_all = 1;
aruco_number = 0;
color_to_export = 0;

aruco_data = [
// 0
[
[0, 1, 0, 0],
[1, 0, 1, 0],
[1, 1, 0, 0],
[1, 1, 0, 1],
],
// 1
[
[1, 1, 1, 1],
[0, 0, 0, 0],
[0, 1, 1, 0],
[0, 1, 0, 1],
],
// 2
[
[1, 1, 0, 0],
[1, 1, 0, 0],
[1, 1, 0, 1],
[0, 0, 1, 0],
],
// 3
[
[0, 1, 1, 0],
[0, 1, 1, 0],
[1, 0, 1, 1],
[1, 0, 0, 1],
],
// 4
[
[1, 0, 1, 0],
[1, 0, 1, 1],
[0, 1, 1, 0],
[0, 0, 0, 1],
],
// 5
[
[1, 0, 0, 0],
[0, 1, 1, 0],
[0, 0, 1, 1],
[0, 0, 1, 0],
],
// 6
[
[0, 1, 1, 0],
[0, 0, 0, 1],
[1, 1, 0, 1],
[0, 0, 0, 1],
],
// 7
[
[0, 0, 1, 1],
[1, 0, 1, 1],
[0, 0, 0, 0],
[1, 1, 0, 1],
],
// 8
[
[0, 0, 0, 0],
[0, 0, 0, 1],
[0, 0, 1, 0],
[0, 1, 0, 1],
],
// 9
[
[0, 0, 1, 1],
[0, 0, 0, 0],
[1, 0, 1, 0],
[1, 0, 0, 1],
],
// 10
[
[0, 0, 0, 0],
[0, 1, 1, 0],
[0, 1, 1, 0],
[1, 1, 1, 0],
],
// 11
[
[1, 1, 1, 0],
[1, 1, 1, 0],
[0, 1, 0, 1],
[1, 0, 0, 0],
],
];


module dodecahedron(height) {
	scale([height,height,height])
	{
		intersection(){
			cube([2,2,1], center = true); 
			intersection_for(i=[0:4]){ 
				rotate([0,0,72*i]) rotate([116.565,0,0]) cube([2,2,1], center=true); 
			}
		}
	}
}

module aruco_content(black_cube, row, col, color=1, flat=0){
    if (black_cube == color){
        translate([cw*(row+1), cw*(col+1)])
        if (flat==0) cube([cw, cw, aruco_data_height]);
        else square([cw,cw]);
    }
}

module aruco_borders(){
    difference(){
        cube([cw*(4+2), cw*(4+2), aruco_data_height]); // must fit in face_intrusion
        translate([cw, cw]) cube([cw*4, cw*4, aruco_data_height]);
    }
}

module aruco(data, color=1, flat=0, ) {
    // data is matrix. 1 is black and 0 is white
    // translate([-cw*(4+2)/2, -cw*(4+2)/2, -aruco_data_height/2]){  // if printed with dodecahedron
    translate([-cw*(4+2)/2, -cw*(4+2)/2, 0]){
        if (color==1) {
            aruco_borders();
        }
        
        idx = [0:3];
        for(row = idx) {
            for(col = idx){
                aruco_content(data[row][col], row, col, color=color, flat=flat);
            }
        }
    }
}

module face_intrusion() {
    translate([-(cw*(4+2)+tol)/2, -(cw*(4+2)+tol)/2, -(aruco_data_height+white_cube_face_height+tol)])
    cube([cw*(4+2)+tol, cw*(4+2)+tol, 2*(aruco_data_height+white_cube_face_height+tol)]); // must contain aruco_borders
}


module face_intrude() {
    t_length = radius-aruco_data_height/2+1;
    for(i=[0:4]){
        rotate([0,0,72*i]) rotate([116.565,0,0]) translate([0, 0, t_length]) face_intrusion();
        rotate([0,0,72*i]) rotate([116.565,0,0]) translate([0, 0, -t_length]) face_intrusion();
    }
    translate([0, 0, t_length]) face_intrusion();
    translate([0, 0, -t_length]) face_intrusion();
}

module white_part(data) {
    translate([-(cw*(4+2)+tol)/2, -(cw*(4+2)+tol)/2, -(white_cube_face_height-tol)])
    cube([cw*(4+2), cw*(4+2), white_cube_face_height-tol]); // must contain aruco_borders

    linear_extrude(height=aruco_data_height+0.27) offset(delta=-tol) aruco(data, color=0, flat=1);
}

module black_part(data) {
    aruco(data, color=1);
}

// dodecahedron
if (dodecahedron_export==1){
   
    difference(){
        difference(){
            dodecahedron(diameter);
            face_intrude();
        }
        // stylus hole
        rotate([116.565/3,0,0]) cylinder(h=diameter/1.5, r1=3, r2=4.6);
    }
}


if (aruco_export_all==1) {
    translate([diameter, -(diameter*2), -radius + (aruco_data_height/2)])
    for(i = [0:11]) {
        if (i<5) {
            translate([0, i*cw*(4+2+1)+50]) black_part(aruco_data[i]);  // black
            translate([40, i*cw*(4+2+1)+50]) white_part(aruco_data[i]);  // white

        }
        else {
            translate([20, (i-5)*cw*(4+2+1)+40]) black_part(aruco_data[i]);  // black
            translate([20+40, (i-5)*cw*(4+2+1)+40]) white_part(aruco_data[i]);  // white
        }
    }
}
else {
    echo(aruco_number);
    if (color_to_export==0) {white_part(aruco_data[aruco_number]);}
    else {black_part(aruco_data[aruco_number]);}
}
