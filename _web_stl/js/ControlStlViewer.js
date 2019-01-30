//
//
//
function BackgroundWhiteBlack(ischecked) {
		if( ischecked == true ) {
			APP.setBackGroundColor( 0x000000 );
			APP.BackGroundColor = 'Black';
			APP.setBoundingBoxColor( 0xffffff );
   			}
		else {
		    APP.setBackGroundColor( 0xffffff );
      		APP.BackGroundColor = 'White';
      		APP.setBoundingBoxColor( 0x000000 );
			}
      }
function FrameOffOn(ischecked) {
		if( ischecked == true ) {
      		APP.addBoundingBox();
   			}
		else {
			APP.removeBoundingBox();
			}
      }
function DirLight(isnum) {
		APP.directionalLight.intensity = isnum / 100;
      }
function AmbLight(isnum) {
		APP.ambientLight.intensity = isnum / 100;
      }

function MarkerOffOn(ischecked) {
		if( ischecked == true ) {
      		APP.MarkerOffOn = 1;
   			}
		else {
			APP.MarkerOffOn = 0;
			}
      }

function SaveImage(ischecked) {
		console.log("Save Image")
		var type = 'image/png';
  		var myCanvas = document.getElementById('myCanvas');
  		var canvas = myCanvas.querySelector('canvas');
  		var base64 = canvas.toDataURL(type);

		// From Base64 to Binay
		var bin = atob(base64.replace(/^.*,/, ''));
		var buffer = new Uint8Array(bin.length);
		for (var i = 0; i < bin.length; i++) {
        	buffer[i] = bin.charCodeAt(i);
		}
  		var blob = new Blob([buffer.buffer], {type: type});
  		var a = document.createElement("a");
		a.href = URL.createObjectURL(blob);
		a.target = '_blank';
		a.download = 'Screenshot.png';
		a.click();
		}

