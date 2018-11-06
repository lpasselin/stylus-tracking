diameter = 50;
aruco_data_height= 3*2;

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

/////////////////////////// no touching
radius = diameter/2;
cw = radius/9;


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

module aruco_content(black_cube, row, col){
    if (black_cube == 1){
        translate([cw*(row+1), cw*(col+1)])
        cube([cw, cw, aruco_data_height]);
    }
}

module aruco_borders(){
    difference(){
        cube([cw*(4+2), cw*(4+2), aruco_data_height]);
        translate([cw, cw]) cube([cw*4, cw*4, aruco_data_height]);
    }
}

module aruco(data) {
    // data is matrix. 1 is black and 0 is white
    translate([-cw*(4+2)/2, -cw*(4+2)/2, -aruco_data_height/2]){
        aruco_borders();
        
        idx = [0:3];
        for(row = idx) {
            for(col = idx){
                aruco_content(data[row][col], row, col);
            }
        }
    }
}

module aruco_on_all_faces() {
    t_length = radius-aruco_data_height/2+1;
    for(i=[0:4]){
        rotate([0,0,72*i]) rotate([116.565,0,0]) translate([0, 0, t_length]) aruco(aruco_data[i]);
        rotate([0,0,72*i]) rotate([116.565,0,0]) translate([0, 0, -t_length]) aruco(aruco_data[i*2+1]);
    }
    translate([0, 0, t_length]) aruco(aruco_data[10]);
    translate([0, 0, -t_length]) aruco(aruco_data[11]);
}

//aruco(aruco0);

difference(){
    difference(){
        dodecahedron(diameter);
        aruco_on_all_faces();
    }
    // stylus hole
    
    //rotate([116.565/3,0,0]) translate([0, 0, t_length]) cylinder(h=diameter, r1=3, r2=4.5); // perfectly symetrical to center of other aruco
    rotate([116.565/3-4,0,0]) translate([0, 0, t_length]) cylinder(h=diameter, r1=3.6, r2=5);
}
translate([diameter, -(diameter*2), -radius + (aruco_data_height/2)])
for(i = [0:11]) {
    if (i<5) {translate([0, i*cw*(4+2+1)+50]) aruco(aruco_data[i]);}
    else {translate([20, (i-5)*cw*(4+2+1)+40]) aruco(aruco_data[i]);}
}





