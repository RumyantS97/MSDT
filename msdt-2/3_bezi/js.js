/** @type {CanvasRenderingContext2D} */
let canvas = document.getElementById("canvas");
var pixsiz=4;
let x1=10;
let x2=20;
let y1=10;
let y2=20;
let dots=[];
function recur(dotss,t){
    trt=[]
    for(let i=0;i<dotss.length-1;i++){
        let xr=dotss[i][0]+t*(dotss[i+1][0]-dotss[i][0])
        let yr=dotss[i][1]+t*(dotss[i+1][1]-dotss[i][1])
        trt.push([xr,yr])
    }
    if (trt.length==1)
        return trt[0];
    else
        return recur(trt,t);
}
canvas.addEventListener("mousedown", function (e) {
    x1=e.pageX/pixsiz;
    y1=e.pageY/pixsiz;
    dots.push([x1,y1]);
    console.log(dots);
    if(dots.length>=2){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        console.log("im here");
        for(let i = 0;i<dots.length-1;i++)
            for(let t = 0;t<=1.0;t+=0.03)
                {
                    let dot=recur([dots[i],dots[i+1]],t);
                    ctx.fillRect((dot[0])*pixsiz, (dot[1])*pixsiz, pixsiz, pixsiz);    
                }
            for(let t = 0;t<=1.0;t+=0.01){
                let dot=recur(dots,t);
                    ctx.fillRect(dot[0] * pixsiz, dot[1] * pixsiz, pixsiz, pixsiz);
            }
    }
});
let width = window.innerWidth;
let height = window.innerHeight;
let ctx = canvas.getContext('2d');
if (ctx) {
width = window.innerWidth;
height = window.innerHeight;
canvas.width = width;
canvas.height = height;
ctx.fillStyle = "rgb(0,0,0)";
}