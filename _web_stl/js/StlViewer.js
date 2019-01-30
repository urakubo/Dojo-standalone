//
//
//

var xratio = 0.6;
var yratio = 0.95;
//var ysize = 600;

var frustumSize = 1000;
var xshift = -64;
var yshift = -128-59;
var zshift = -64

xshift = 0;
yshift = 0;
zshift = 0;


var APP = { };
APP.animate = function() {
	APP.renderer.render( APP.scene, APP.camera );
	APP.controls.update();
	requestAnimationFrame( APP.animate );
};


// ObtainWindowSize
function onWindowResize() {
    var aspect = window.innerWidth / window.innerHeight;
    APP.camera.left   = - frustumSize * aspect / 2;
    APP.camera.right  =   frustumSize * aspect / 2;
    APP.camera.top    =   frustumSize / 2;
    APP.camera.bottom = - frustumSize / 2;
    APP.camera.updateProjectionMatrix();
    APP.renderer.setSize( window.innerWidth * xratio, window.innerHeight * yratio);
	}

// Add stl objects and a name
APP.addSTLObject = function(url, name, objcolor) {
    var loader = new THREE.STLLoader();
    loader.load(url, function (geometry) {
		var material = new THREE.MeshLambertMaterial( { color: objcolor } ); //ambient: 0xff0000, 
        var mesh = new THREE.Mesh(geometry, material);
        // APP.scene.add(mesh);
        mesh.name = name;
        mesh.scale.set(1,1,1);
		mesh.material.side = THREE.DoubleSide;
        APP.scene.add(mesh);
        
        mesh.translateX( xshift );
        mesh.translateY( yshift );
        mesh.translateZ( zshift );
        
		//APP.scene.getObjectByName('test_name2').rotation.x += 0.005;
		//APP.scene.getObjectByName('test_name2').rotation.y += 0.005;
		//console.log('Object name:');
		//console.log(name);
        //APP.scene.remove(mesh);
    	});
	}


// Change the color of the stl object specified by a name after generation.
APP.changecolorSTLObject = function(name, objcolor){
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    		obj.material.color.setHex( objcolor );
		}
	}

// Remove a stl object by a name after generation.
APP.removeSTLObject = function(name){
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    		APP.scene.remove(obj);
		}
	}

// Draw bounding box
APP.addBoundingBox = function(){

	if ( APP.BackGroundColor == 'Black'){
		var mat = new THREE.LineBasicMaterial( { color: 0xFFFFFF, linewidth: 2 } );
		}
	else{
		var mat = new THREE.LineBasicMaterial( { color: 0x000000, linewidth: 2 } );
		}

	var geometry = new THREE.BoxBufferGeometry( APP.BoundingboxZ, APP.BoundingboxY, APP.BoundingboxX );
	var geo = new THREE.EdgesGeometry( geometry ); // or WireframeGeometry( geometry )

	var boundingbox = new THREE.LineSegments( geo, mat );
	boundingbox.name = 'BoundingBox';
	boundingbox.scale.set(1,1,1);
	APP.scene.add(boundingbox);
	APP.BoundingBox = 'On';
	boundingbox.translateX( APP.BoundingboxZ / 2 );
	boundingbox.translateY( APP.BoundingboxY / 2 );
	boundingbox.translateZ( APP.BoundingboxX / 2 );
	}

APP.removeBoundingBox = function(){
	var obj = APP.scene.getObjectByName('BoundingBox');
	if ( obj != undefined ) {
    		APP.scene.remove(obj);
		}
	APP.BoundingBox = 'Off';
	}

APP.setBoundingBoxColor = function(objcolor){
	var obj = APP.scene.getObjectByName('BoundingBox');
	if ( obj != undefined ) {
    	obj.material.color.setHex( objcolor );
		}
	}

// Set background color
APP.setBackGroundColor = function( backcolor ){
		APP.scene.background = new THREE.Color( backcolor );
	}

function rgb2hex ( rgb ) {
	return "#" + rgb.map( function ( value ) {
		return ( "0" + value.toString( 16 ) ).slice( -2 ) ;
	} ).join( "" ) ;
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
	
	// Write the most proximal one.
	var obj = {};
	if (Object.keys(intersects).length > 0) {
		var objid = intersects[0].object.name;
 		target = document.getElementById("ClickedObjectID");
		target.innerHTML = objid;

		if (APP.MarkerOffOn == 1) {
			x = intersects[ 0 ].point.x;
			y = intersects[ 0 ].point.y;
			z = intersects[ 0 ].point.z;
			col = rgb2hex( [ APP.MarkerR, APP.MarkerG, APP.MarkerB ] );

			// Add sphere
			var geometry = new THREE.SphereGeometry( 1 );
			var material = new THREE.MeshBasicMaterial( {color: col} );
			var sphere = new THREE.Mesh( geometry, material );
			sphere.scale.set(APP.MarkerRadius,APP.MarkerRadius,APP.MarkerRadius);
			sphere.position.set(x, y, z);
			sphere.name = 'm'+ APP.MarkerID.toString();
			APP.scene.add( sphere );
			
			
			//console.log(APP.scene);
			
			//Append Jsontable
			markername = APP.MarkerPrefix+String(APP.MarkerSuffix);
			
			var NewMarker = {
				"act": 1,
				"id":  APP.MarkerID,
				"name": markername,
				"parentid": objid,
    			"radius": APP.MarkerRadius,
    			"r": APP.MarkerR,
    			"g": APP.MarkerG,
    			"b": APP.MarkerB,
    			"x": x,
    			"y": y,
    			"z": z
    			};

    		console.log(NewMarker);
			ObjMarkerTable.addData(NewMarker);  // Change database MarkerTable (setData)
			
			APP.MarkerSuffix = APP.MarkerSuffix + 1;
			APP.MarkerID     = APP.MarkerID + 1;
			$('#SetSuffixNum').val(APP.MarkerSuffix); // Change suffix for index.html
			}

	}else{
 		target = document.getElementById("ClickedObjectID");
		target.innerHTML = "Background";
	}
	}

// Change the color of the stl object specified by a name after generation.
APP.changeMarkerRadius = function(id, r){
	name = 'm'+ id.toString();
	var obj = APP.scene.getObjectByName(name);
	console.log(obj);
	if ( obj != undefined ) {
    		obj.scale.set(r,r,r);
		}
	}

// Change the color of the stl object specified by a name after generation.
APP.changeMarkerColor = function(id, objcolor){
	name = 'm'+ id.toString();
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    		obj.material.color.setHex( objcolor );
		}
	}

// Remove a stl object by a name after generation.
APP.removeMarker = function(id){

	// Remove from scene
	name = 'm'+ id.toString();
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    		APP.scene.remove(obj);
		}
	
	// Remove from json variable
	//var newData = APP.MarkerTable.filter(function(item, index){ if (item.id != id) return true;});
	//APP.MarkerTable = newData
	
	}

function getJSON(url) {
	
}

function StlViewer() {

	// Renderer
	var container = document.getElementById('myCanvas');
	APP.renderer = new THREE.WebGLRenderer( { preserveDrawingBuffer: true } );
	APP.renderer.setSize(window.innerWidth * xratio, window.innerHeight * yratio);
	container.appendChild( APP.renderer.domElement );

	 // Camera
	APP.camera = new THREE.PerspectiveCamera();
	APP.camera.position.z = 400;
	// APP.camera.lookAt(new THREE.Vector3(64, 64, 64));

	// Scene
	APP.scene = new THREE.Scene();
	APP.scene.add( APP.camera );

	// Background Color
	APP.scene.background = new THREE.Color( 0xffffff );
	APP.BackGroundColor == 'White';

	// Light
	APP.directionalLight = new THREE.DirectionalLight(0xffffff);
	APP.directionalLight.position.set(1, 1, 1);
	APP.directionalLight.intensity = 0.8;
	APP.camera.add( APP.directionalLight );
	APP.ambientLight = new THREE.AmbientLight( 0xffffff );
	APP.ambientLight.intensity = 0.5;
	APP.camera.add( APP.ambientLight );

	var min = 0 ;
	var max = 255 ;

	// Controlsを用意
	APP.controls = new THREE.TrackballControls( APP.camera, APP.renderer.domElement );
	APP.controls.rotateSpeed = 20.0;
	APP.animate();

	// Response to mouse click
	APP.renderer.domElement.addEventListener( 'mousedown', clickPosition, false );

	// Marker Variables
	APP.MarkerOffOn = 0;
	APP.MarkerR = 255;
	APP.MarkerG = 0;
	APP.MarkerB = 0;
	APP.MarkerPrefix = "Marker";
	APP.MarkerSuffix = 0;
	APP.MarkerRadius = 2.0;
	APP.MarkerID     = 1;

	// Boundingbox variables
	var prot = location.protocol;
	var url = prot +"/data/Boundingbox.json";

	var req = new XMLHttpRequest();		  // XMLHttpRequest オブジェクトを生成する
		req.onreadystatechange = function() {		  // XMLHttpRequest オブジェクトの状態が変化した際に呼び出されるイベントハンドラ
    	if(req.readyState == 4 && req.status == 200){ // サーバーからのレスポンスが完了し、かつ、通信が正常に終了した場合
			data = req.responseText;
			var jsondata = JSON.parse(data);
			APP.BoundingboxX = jsondata.x;
			APP.BoundingboxY = jsondata.y;
			APP.BoundingboxZ = jsondata.z;
    		};
  		};
  	req.open("GET", url, false);
  	req.send(null);	

	console.log(APP.BoundingboxX)
	console.log(APP.BoundingboxY)
	console.log(APP.BoundingboxZ)

};

window.addEventListener( 'resize', onWindowResize, false );

