var photo = new Image(1980, 1980);
photo.src = "Images/me.jpg"
var scale = 10;

function init(){
	ctx = document.getElementById('gradient').getContext('2d', { alpha: false });

	resize();

	window.requestAnimationFrame(step);
}

function step(){
	if (scale > 2.65*window.innerHeight){
		scale = 5
	}
	scale += 2 + 0.000001*scale*scale

    ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);

    ctx.save();
    ctx.translate(ctx.canvas.width/2, ctx.canvas.height/2);
    ctx.rotate(scale*Math.PI/180);
	ctx.drawImage(photo, -scale/2, -scale/2, scale, scale)
    ctx.restore();

	window.requestAnimationFrame(step);
}


function resize(){  
	ctx.canvas.style.width = window.innerWidth;
	ctx.canvas.width = window.innerWidth;
	ctx.canvas.style.height = window.innerHeight;
	ctx.canvas.height = window.innerHeight;
}

/*
CSS:
canvas{
	position: absolute;
	top: 0;
	left: 0;
}


HTML:
<body onload="init()" onresize="resize()">
			<canvas id="canvas"></canvas>
</body>


*/