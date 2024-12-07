/** @type {CanvasRenderingContext2D} */
let canvas = document.getElementById("canvas");
var pixsiz=6;
let x1=10;
let x2=20;
let y1=10;
let y2=20;
canvas.addEventListener("mousedown", function (e) {
    x1=e.pageX/pixsiz;
    y1=e.pageY/pixsiz;
});
canvas.addEventListener("mousemove", function (e) {});
canvas.addEventListener("mouseup", function (e) {
    x2=e.pageX/pixsiz;
    y2 = e.pageY / pixsiz;
    let rr = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1);
    for (let x = -Math.round(Math.sqrt(rr)); x < Math.round(Math.sqrt(rr)); x++) {
        ctx.fillRect((x1 + x) * pixsiz, (y1 + Math.round(Math.sqrt((rr - x * x)))) * pixsiz, pixsiz, pixsiz);
        ctx.fillRect((x1 + x) * pixsiz, (y1 - Math.round(Math.sqrt((rr - x * x)))) * pixsiz, pixsiz, pixsiz);
    }
        
});
canvas.addEventListener("wheel", function (e) {});
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