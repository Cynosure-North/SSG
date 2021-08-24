//Parameters
var pixSize = 8;

//Other stuff
var ctx;		//The canvas
var maskCtx;

function init(){
	ctx = document.getElementById('gradient').getContext('2d', { alpha: false });
	maskCtx = document.getElementById('mask').getContext('2d');

	resize();

	window.requestAnimationFrame(step);
}

function step(){
	var gradient = ctx.createLinearGradient(ctx.canvas.width/2,0,ctx.canvas.width/2,ctx.canvas.height);

	gradient.addColorStop(0, 'hsl(' + (Date.now()/30)%360 + ', 100%, 60%');
	gradient.addColorStop(1, 'white');

	// Set the fill style and draw a rectangle
	ctx.fillStyle = gradient;
	ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);

	window.requestAnimationFrame(step);
}


function resize(){
	let pixWidth = Math.ceil((window.innerWidth)/pixSize);
	let pixHeight = Math.ceil((window.innerHeight)/pixSize);
  
	ctx.canvas.style.width = window.innerWidth;
	ctx.canvas.width = window.innerWidth;
	ctx.canvas.style.height = window.innerHeight;
	ctx.canvas.height = window.innerHeight;

	maskCtx.canvas.style.width == window.innerWidth;
	maskCtx.canvas.width = window.innerWidth;
	maskCtx.canvas.style.height = window.innerHeight;
	maskCtx.canvas.height = window.innerHeight;

	for (let i=0; i<pixWidth; i++){
		for (let j=0; j<pixHeight; j++){
			if ((2*i+3*j)%4!=0){
				maskCtx.fillStyle = 'rgba(0,0,0,1)';
				maskCtx.fillRect(i*pixSize, j*pixSize, pixSize, pixSize);
			}
			else{
				maskCtx.fillStyle = 'rgba(0,0,0,0)';
				maskCtx.fillRect(i*pixSize, j*pixSize, pixSize, pixSize);
			}
		}
	}
}