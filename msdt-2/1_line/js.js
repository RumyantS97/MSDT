/** @type {CanvasRenderingContext2D} */
let canvas = document.getElementById("canvas");
let x1=10;
let x2=20;
let y1=10;
let y2=20;
canvas.addEventListener("mousedown", function (e) {
x1=e.pageX/4;
y1=e.pageY/4;
});
canvas.addEventListener("mousemove", function (e) {});
canvas.addEventListener("mouseup", function (e) {
x2=e.pageX/4;
y2=e.pageY/4;
let a = (y2-y1)/(x2-x1);
let b = y1-a*x1;
for(let i = x1;i<=x2;i++)
ctx.fillRect(i*4, Math.round(a*i+b)*4, 4, 4);
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