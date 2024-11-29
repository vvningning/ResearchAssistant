import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import  axios  from 'axios';
//import gsap from "gsap";
import TWEEN from '@tweenjs/tween.js';
import Stats from 'three/examples/jsm/libs/stats.module';

let getNum = {x:1, y:2};
let nums = [];


//读取数据库接口
axios.get('http://localhost:8088/axios-server2',{
  headers:{
      name: 'atguigu',
      age:20
  }
}).then(value => {
  // console.log(value.data);
  getNum.x = value.data[0].x;
  getNum.y = value.data[0].y;
  nums = Array.from(value.data);
});

const scene = new THREE.Scene()
scene.background = new THREE.Color(0xADD8E6);
scene.environment = new THREE.Color(0xADD8E6);

//城市
const loader = new GLTFLoader();
loader.load("/static/model/city.glb", (gltf) => {
    const bmw = gltf.scene;
    gltf.scene.traverse( function ( child ) {
    if ( child.isMesh ) {
        child.frustumCulled = false;
        //模型阴影
        child.castShadow = true;
        //模型自发光
        child.material.emissive =  child.material.color;
        child.material.emissiveMap = child.material.map ;
    }})
    scene.add(bmw);
})

//人物移动
let rider;
let mixer10;
var move;
const loader13 = new GLTFLoader();
// console.log("sad")
loader13.load('/static/model/riderBoy.glb', function(gltf) {
    rider = gltf.scene;
    mixer10 = new THREE.AnimationMixer(gltf.scene);
    const clipWalk = THREE.AnimationUtils.subclip(gltf.animations[1], 'walk', 0, 31);
    const clipStand = THREE.AnimationUtils.subclip(gltf.animations[1], 'stand', 32, 33);
    const action = mixer10.clipAction(clipWalk);
    const action2 = mixer10.clipAction(clipStand);
    action2.play();
    rider.position.set(5, 0, -16)
    rider.scale.set(1, 1, 1)
    rider.rotation.set(0, Math.PI * 0.5, 0)

    gltf.scene.traverse(function (child) {
        if(child.isMesh) {
            child.receiveShadow = true
            child.castShadow = true
            child.frustumCulled = false;
            //模型自发光
            child.material.emissive =  child.material.color;
            child.material.emissiveMap = child.material.map ;

        }
    })
    var x1 = 5;
    var y1 = -16;
    scene.add(rider);

    let clk = {i: 0};
    move = setInterval(() => {
      moveWithNum(gltf.scene, x1, y1, action, action2, nums[clk.i].position_x, nums[clk.i].position_y, clk);
    }, 500);
    
    x1 = gltf.scene.position.x;
    y1 = gltf.scene.position.z;
})

//渲染器
// const width = 1000;
// const height = 600;
const width = window.innerWidth * 0.64;
const height = window.innerHeight * 0.85;
//渲染
const renderer = new THREE.WebGLRenderer({
    antialias: true,
});
// const canvas = document.querySelector('#three')
// const renderer = new THREE.WebGLRenderer({ canvas, antialias: true })
renderer.setSize(width, height);

//可更改设定图像具体位置
// document.getElementById('test').appendChild(renderer.domElement);

//创建相机
const camera = new THREE.PerspectiveCamera(45, width / height, 1, 3000);
//设置相机位置
camera.position.set(150,150,150);
scene.add(camera);

//mapControl
var controls = new OrbitControls(camera, renderer.domElement)



// /* 属性参数 */
controls.enableDamping = true;// 启用动态阻尼时需要一个动画循环
controls.dampingFactor = 0.30;

controls.screenSpacePanning = false;// 若为 true 则可以平移

controls.maxDistance = 400;
controls.minDistance = 10;

controls.maxPolarAngle = Math.PI / 2.2;
controls.autoRotate = false;
controls.update();
//document.body.appendChild(document.getElementById("app"));
// document.document.getElementById("test").appendChild(renderer.domElement);

//Events
window.addEventListener('resize', onResize, false);

//帧率跟踪
const stats = new Stats();
stats.setMode(0);

//改变天空颜色
var iColor = {i:1};
var color = new THREE.Color(0x000000);//黑夜
var color4 = new THREE.Color(0xADD8E6);//白天

var tween2 = new TWEEN.Tween(scene.background).to(color, 500);
var tween4 = new TWEEN.Tween(scene.background).to(color4, 500);

setInterval(() => {
    if(iColor.i == 1) {
        tween4.start();
        iColor.i = 2;
    } else {
        tween2.start();
        iColor.i = 1;
    }
}, 50000);

//渲染图像
const clock = new THREE.Clock();
function render() {
    const delta = clock.getDelta();
    controls.update(delta)
    if ( mixer10 ) mixer10.update( delta );
    renderer.render(scene, camera);
    
    //渲染下一帧的时候就会调用render函数
    requestAnimationFrame(render);

    stats.update();
    TWEEN.update();
}

render();


//------------function------------
function onResize() {
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix()
}

function crossPlay(curAction, newAction) {
    curAction.fadeOut(0.03);
    newAction.reset();
    newAction.setEffectiveWeight(1);
    newAction.play();
    newAction.fadeIn(0.03);
}

function moveWithNum(body, x1, y1, action, action2, num1, num2, clk) {
    
    
    // console.log(body.position.x);
    // console.log(body.position.z);
    var t1 = Math.abs(body.position.x - num1) / 0.01;
    var d1 = 0;
    if( body.position.x > num1) {
        d1 = - Math.PI * 0.5;
    } else {
        d1 = Math.PI *  0.5;
    }
    var tween1 = new TWEEN.Tween(body.position).to({x : num1}, t1);
    var tween2 = new TWEEN.Tween(body.rotation).to({x: 0, y: d1, z: 0}, 20).onStart(() => {
        crossPlay(action2, action);
    });

    var d2 = 0;
    var t2 = Math.abs(body.position.z - num2) / 0.01;
    // console.log(Math.abs(body.position.z - num2));
    if( body.position.z > num2) {
        d2 = Math.PI;
    } else {
        d2 = 0;
    }
    var tween3 = new TWEEN.Tween(body.position).to({z: num2}, t2).onComplete(()=> {
        crossPlay(action, action2);
    });
    var tween4 = new TWEEN.Tween(body.rotation).to({x: 0, y: d2, z: 0}, 20);

    var tween5 = new TWEEN.Tween(body.rotation).to({x: 0, y: d1, z: 0}, 1).onComplete(()=> {
        crossPlay(action, action2);
    });

    var tween6 = new TWEEN.Tween(body.rotation).to({x: 0, y: d1, z: 0}, 1).onStart(() => {
        crossPlay(action2, action);
    });

    if(body.position.x == num1 && body.position.z == num2) {
        // console.log(100);
    }   else if(body.position.x == num1)  {
        // console.log(11);
        tween6.chain(tween4).start();
        tween4.chain(tween3);
        // console.log("t1", t1);
        // console.log("t2", t2);
    }   else if( body.position.z == num2) {
        // console.log(22);
        tween2.chain(tween1).start();
        tween1.chain(tween5);
        // console.log("t1", t1);
        // console.log("t2", t2);
    }   else {
        // console.log(33);
        tween2.chain(tween1).start();
        tween1.chain(tween4);
        tween4.chain(tween3);
        // console.log("t1", t1);
        // console.log("t2", t2);
    }
    ++clk.i;
    if(clk.i == 200) {
      clearInterval(move);
    }
}

export {renderer};