//
//
//
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
        
        mesh.translateX( -64 );
        mesh.translateY( -128-59 );
        mesh.translateZ( -64 );
        
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

	// Rendererを用意
	APP.renderer = new THREE.WebGLRenderer({ alpha: true });
	APP.renderer.setSize(window.innerWidth, window.innerHeight);
	document.body.appendChild( APP.renderer.domElement );
	//APP.renderer.enable(APP.renderer.CULL_FACE);

	 // Cameraを用意
	APP.camera = new THREE.PerspectiveCamera();
	APP.camera.position.z = 400;
	// APP.camera.lookAt(new THREE.Vector3(64, 64, 64));

	// Sceneを用意
	APP.scene = new THREE.Scene();
	APP.scene.add( APP.camera );

	//ライトを用意
	var directionalLight = new THREE.DirectionalLight(0xffffff);
	directionalLight.position.y = 1000;
	directionalLight.position.z = 1000;
	APP.scene.add( directionalLight );
	var aLight = new THREE.AmbientLight( 0x909090 ,1 );
	APP.scene.add( aLight );
	
    //Grid
    // grid = new THREE.GridHelper(400, 10, 0x000000, 0x000000);
    // grid.position.y = 0;
    // APP.scene.add(grid);
	
	
	//Add Stl object
	onum = 20
	APP.ids = new Array(onum);
	for (  var i = 0;  i < onum;  i++  ) {
		APP.ids[i] = sprintf("%d", i );
	}
	
	var min = 0 ;
	var max = 255 ;
	for (  var i = 0;  i < onum;  i++  ) {
		var filename = sprintf("./imgs/i%d.stl", i );
		var id       = sprintf("%d", i );
		console.log(filename);
		var r = Math.floor( Math.random() * (max + 1 - min) ) + min ;
		var g = Math.floor( Math.random() * (max + 1 - min) ) + min ;
		var b = Math.floor( Math.random() * (max + 1 - min) ) + min ;
		APP.addSTLObject(filename, id, r*256*256+g*256+b*1);
	}

	
	//var obj = APP.scene.getObjectByName('test_name');
	//console.log(obj);
	//APP.scene.remove(obj);

	// Controlsを用意
	APP.controls = new THREE.TrackballControls( APP.camera );
	APP.controls.rotateSpeed = 20.0;
	APP.animate();

	//removeSTLObject('test_name1');
};


