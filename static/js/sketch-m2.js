let divData, story_text, speech, startBtn, stopBtn, canvas;

let slectedImg, Img1, Img2, Img3, Img4, Img5, Img6;

let img_is_selected = false;


function preload(){
    Img1 = loadImage("imgs/1.jpg"); 
    Img2 = loadImage("imgs/2.jpg"); 
    Img3 = loadImage("imgs/3.jpg"); 
    Img4 = loadImage("imgs/4.jpg"); 
    Img5 = loadImage("imgs/5.jpg"); 
    Img6 = loadImage("imgs/6.jpg"); 
   
}


function setup(){
    canvas = createCanvas(600,800);
    canvas.parent('canvas-div');
    divData = document.querySelector("#canvas-div");

    speech = new p5.Speech(); // speech synthesis object
    
    story_style = divData.dataset.style;

    //start button setup
    let startBtnDiv = document.querySelector('#startBtnDiv');
    startBtn = createButton('Start Narrating!');
    startBtn.parent(startBtnDiv);
    startBtn.class('btn btn-primary');
    startBtn.mousePressed(startSpeaking);

    //stop button setup
    let stopBtnDiv = document.querySelector('#stopBtnDiv');
    stopBtn = createButton('Stop Narrating!');
    stopBtn.parent(stopBtnDiv);
    stopBtn.class('btn btn-danger');
    stopBtn.mousePressed(stopSpeaking);

}

function draw(){
    background(100);
    fill(255);

    rectMode(CENTER);

    story_text = divData.dataset.story;

    display_text = "Artist: "+story_style+"\n"+"\n"+story_text

    if(img_is_selected ===true){
        tint(95,95,95, 255);
        image(slectedImg,0,0,600,800);
        
    }

    

    textSize(18);
    textWrap(WORD);
    text(display_text, width/2,height/2, width-100, height-100);
    
    
}


function startSpeaking(){
    if(story_text !== "Waiting for the lyric..."){

        if(story_style === "Ariana_Grande"){
            slectedImg = Img1;
            img_is_selected = true;
            speech.setVoice(0);
            speech.setPitch(0.01);
            speech.setRate(0.5);
            speech.speak(story_text);
        }
        else if(story_style === "Justin_Bieber"){
            slectedImg = Img2;
            img_is_selected = true;
            speech.setVoice(1);
            speech.setPitch(1);
            speech.setRate(1);
            speech.speak(story_text);
        }
        else if(story_style === "Taylor_Swift"){
            slectedImg = Img3;
            img_is_selected = true;
            speech.setVoice(1);
            speech.setPitch(1.5);
            speech.setRate(1.5);
            speech.speak(story_text);
        }
        else if(story_style === "Dua_Lipa"){
            slectedImg = Img4;
            img_is_selected = true;
            speech.setVoice(2);
            speech.setPitch(2);
            speech.setRate(1);
            speech.speak(story_text);
        }
        else if(story_style === "Lady_Gaga"){
            slectedImg = Img5;
            img_is_selected = true;
            speech.setVoice(0);
            speech.setPitch(2);
            speech.setRate(1);
            speech.speak(story_text);
        }
        else if(story_style === "Charlie_Puth"){
            slectedImg = Img6;
            img_is_selected = true;
            speech.setVoice(2);
            speech.setPitch(1);
            speech.setRate(1);
            speech.speak(story_text);
        }
        else{
            speech.setVoice(0);
            speech.setPitch(1.0);
            speech.setRate(1.0);
            speech.speak(story_text);

        }

        // speech.listVoices();
        
    }
}

function stopSpeaking(){
    speech.stop();
}