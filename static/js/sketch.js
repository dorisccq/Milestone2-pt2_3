// Javascript Code Goes here
let divData, story_text, speech, startBtn, stopBtn//, bgImage;

/*function preload() {
    // 加载背景图片，确保在 setup() 之前完成加载
    bgImage = loadImage('abstractColors.jpg');  // 在这里替换为你的图片路径
}*/

function setup() {
    let c = createCanvas(600, 600);
    c.parent('canvas-div');

    divData = document.querySelector('#canvas-div');
    speech = new p5.Speech();

    let startBtnDiv = document.querySelector("#startBtnDiv");
    startBtn = createButton('Start Narrating!');
    startBtn.parent(startBtnDiv);
    startBtn.class('btn btn-primary');
    startBtn.mousePressed(startSpeaking);

    let stopBtnDiv = document.querySelector("#stopBtnDiv");
    stopBtn = createButton('Stop Narrating!');
    stopBtn.parent(stopBtnDiv);
    stopBtn.class('btn btn-danger');
    stopBtn.mousePressed(stopSpeaking);
}

function draw() {
    //image(bgImage, 0, 0, width, height);

    background(0);
    fill(255);

    rectMode(CENTER);

    story_text = divData.dataset.story;

    textSize(18);
    textWrap(WORD);
    text(story_text, width / 2, height / 2, width - 100, height - 100);
}

function startSpeaking() {
    if (story_text !== "Waiting for the story...") {
        speech.speak(story_text);
    }
}

function stopSpeaking() {
    speech.stop();
}