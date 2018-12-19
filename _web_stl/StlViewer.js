//
//
//

var frustumSize = 1000;
var xshift = -64;
var yshift = -128-59;
var zshift = -64

var APP = { };
APP.animate = function() {
	APP.renderer.render( APP.scene, APP.camera );
	APP.controls.update();
	requestAnimationFrame( APP.animate );
};

// Read CSV file
function csvToArray2(path) {
        var csvData = new Array();
        var data = new XMLHttpRequest();        
        data.open("GET", path, false);
        data.send(null);
        var lines = data.responseText.split(/\r\n|\n/);
        //alert(lines.length);
        for (var i = 0; i < lines.length;++i) {
        	if(lines[i] == '') break;
            csvData.push(lines[i]);
          	}
        return csvData;
	}

function csvToArray(path) {
	var csvData = new Array();
	var data = new XMLHttpRequest();        
	data.open("GET", path, false);
	data.send(null);
	var lines = data.responseText.split(/\r\n|\n/);
	for (var i = 0; i < lines.length;++i) {
		if(lines[i] == '') break;
		var cells = lines[i].split(",");
		if( cells.length == 1 ) {
			csvData.push(lines[i]);
			}
		if( cells.length != 1 ) {
			csvData.push(cells);
			}
		}
	return csvData;
	}

// ObtainWindowSize
function onWindowResize() {
    var aspect = window.innerWidth / window.innerHeight;
    APP.camera.left   = - frustumSize * aspect / 2;
    APP.camera.right  =   frustumSize * aspect / 2;
    APP.camera.top    =   frustumSize / 2;
    APP.camera.bottom = - frustumSize / 2;
    APP.camera.updateProjectionMatrix();
    APP.renderer.setSize( window.innerWidth, window.innerHeight );
	}

// Add stl objects and a name
APP.addSTLObject = function(url, name, objcolor) {
    var loader = new THREE.STLLoader();
    loader.load(url, function (geometry) {
		var material = new THREE.MeshLambertMaterial( { color: objcolor } ); //ambient: 0xff0000, 
        var mesh = new THREE.Mesh(geometry, material);
        APP.scene.add(mesh);
        mesh.name = name;
        mesh.scale.set(1,1,1);
		mesh.material.side = THREE.DoubleSide;
        APP.scene.add(mesh);
        
        mesh.translateX( xshift );
        mesh.translateY( yshift );
        mesh.translateZ( zshift );
        
		//APP.scene.getObjectByName('test_name2').rotation.x += 0.005;
		//APP.scene.getObjectByName('test_name2').rotation.y += 0.005;
		console.log('Object name:');
		console.log(name);
        //APP.scene.remove(mesh);
    	});
	}


// Remove a stl object by a name after generation.
APP.removeSTLObject = function(name){
	var obj = APP.scene.getObjectByName(name);
	console.log(obj);
	APP.scene.remove(obj);
	}

// Draw bounding box
APP.addBoundingBox = function(){
	var geometry = new THREE.BoxBufferGeometry( 128*2, 128*2, 128*2 );
	var geo = new THREE.EdgesGeometry( geometry ); // or WireframeGeometry( geometry )
	var mat = new THREE.LineBasicMaterial( { color: 0x000000, linewidth: 3 } );
	var boundingbox = new THREE.LineSegments( geo, mat );
	
	APP.scene.add(boundingbox);
	//boundingbox.translateX( xshift );
	//boundingbox.translateY( yshift );
	//boundingbox.translateZ( zshift );
	}


// Operation on mouse click
function clickPosition( event ) {
	// Location of mouse
	var x = event.clientX;
	var y = event.clientY;
 
	// Normalization of location
	var mouse = new THREE.Vector2();
	mouse.x = ( ( x - APP.renderer.domElement.offsetLeft ) / APP.renderer.domElement.clientWidth ) * 2 - 1;
	mouse.y = - ( ( y - APP.renderer.domElement.offsetTop ) / APP.renderer.domElement.clientHeight ) * 2 + 1;
 
	// Raycasterインスタンス作成
	var raycaster = new THREE.Raycaster();
	// 取得したX、Y座標でrayの位置を更新
	raycaster.setFromCamera( mouse, APP.camera );

	// Indetify crossing objects.
	var intersects = raycaster.intersectObjects( APP.scene.children );
	
	// Hide the most proximal one.
	var obj = {};
	if (Object.keys(intersects).length > 0) {
		var objname = intersects[0].object.name;
		if (APP.ids.includes(objname)) {
			console.log('Object to be deleted:');
			console.log(objname);
 			intersects[0].object.visible = false;
 		}
	}
	
//	for ( var i = 0; i < intersects.length; i++ ) {
//		intersects[ i ].object.material.color.set( 0xff0000 );
//		intersects[ i ].object.visible = false;
//		}
	
	}


function StlViewer() {

	// Renderer
	APP.renderer = new THREE.WebGLRenderer({ alpha: true });
	APP.renderer.setSize(window.innerWidth, window.innerHeight);
	document.body.appendChild( APP.renderer.domElement );
	//APP.renderer.enable(APP.renderer.CULL_FACE);

	 // Camera
	APP.camera = new THREE.PerspectiveCamera();
	APP.camera.position.z = 400;
	// APP.camera.lookAt(new THREE.Vector3(64, 64, 64));

	// Scene
	APP.scene = new THREE.Scene();
	APP.scene.add( APP.camera );

	// Light
	var directionalLight = new THREE.DirectionalLight(0xffffff);
	directionalLight.position.y = 1000;
	directionalLight.position.z = 1000;
	APP.scene.add( directionalLight );
	var aLight = new THREE.AmbientLight( 0x909090 ,1 );
	APP.scene.add( aLight );
	
    // Grid
	// APP.addBoundingBox();
	
	// Read target ids of stls as a csv file.
	// https://algorithm.joho.info/programming/javascript/csv-to-array/
	
	var data = csvToArray("./stls/stl_ids.csv");

//	alert(data.length);
//	alert(data);
//	alert(data[0]);
//	alert(data[0][0]);

	var min = 0 ;
	var max = 255 ;
	console.log(data.length);
	APP.ids = new Array(data.length);
	for (  var i = 0;  i <  data.length;  i++  ) {
		var filename = sprintf("./stls/i%d.stl", data[i][0] );
		var id       = sprintf("%d", i );
		APP.ids[i] = sprintf("%d", i );
		console.log(filename);
		//var r = Math.floor( Math.random() * (max + 1 - min) ) + min ;
		//var g = Math.floor( Math.random() * (max + 1 - min) ) + min ;
		//var b = Math.floor( Math.random() * (max + 1 - min) ) + min ;
		var r = data[i][1] ;
		var g = data[i][2] ;
		var b = data[i][3] ;
		APP.addSTLObject(filename, id, r*256*256+g*256+b*1);
	}
	var onum = data.length


	
	//var obj = APP.scene.getObjectByName('test_name');
	//console.log(obj);
	//APP.scene.remove(obj);

	// Controlsを用意
	APP.controls = new THREE.TrackballControls( APP.camera );
	APP.controls.rotateSpeed = 20.0;
	APP.animate();

	//removeSTLObject('test_name1');
};


