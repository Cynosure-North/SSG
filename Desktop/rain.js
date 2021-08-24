//Parameter
const pixSize = 8;
const dropSize = 4;

//TOOD: webassembly

//Other stuff
var ctx;		//The canvas
var pixWidth;	//In pixels
var pixHeight;
var offscreen;
var disabled = false;

function init(){
	ctx = document.getElementById('rain').getContext('2d', { alpha: false });
	ctx.imageSmoothingEnabled = false;

	resize();

	window.requestAnimationFrame(step);
}

function step(){
	if (!disabled){
		drawDrop(50,50,"0000FF");
		ctx.transferFromImageBitmap(offscreen.transferToImageBitmap());
	}

	window.requestAnimationFrame(step);
}

function drawDrop(x , y, colour){
	offscreen.fillStyle(colour);
	offscreen.beginPath();
    offscreen.arc(x, y, dropSize, 0, 2 * Math.PI);
    offscreen.fill();
}


function resize(){
	pixWidth = Math.ceil((window.innerWidth)/pixSize);
	pixHeight = Math.ceil((window.innerHeight)/pixSize);

	const offscreenCanvas = new OffscreenCanvas(pixWidth, pixHeight);
	offscreen = offscreenCanvas.getContext('2d');

	ctx.canvas.style.width = window.innerWidth;
	ctx.canvas.width = window.innerWidth;
	ctx.canvas.style.height = window.innerHeight;
	ctx.canvas.height = window.innerHeight;
}

function toggle(){
	disabled = !disabled;
	if (disabled){
		ctx.fillStyle = 'hsl(0,0%,0%)';
		ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
	}
}

/*
HTML:
<canvas id="rain"></canvas>

CSS:
#rain{
	position: absolute;
	top: 0;
	left: 0;
}
*/
