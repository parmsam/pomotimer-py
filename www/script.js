// Helper functions
let playSound = (url) => {
    let a = new Audio(url);
    a.play();
}

let hmsToSeconds = (str) => {
    let p = str.split(':'),
        s = 0, m = 1;
    while (p.length > 0) {
        s += m * parseInt(p.pop(), 10);
        m *= 60;
    }
    return s;
}

// Objects to be used
let exampleSound = "https://github.com/JanLoebel/MMM-TouchAlarm/blob/master/sounds/alarm.mp3?raw=true"
let timeLeft
let secLeft

// Event listeners
$(document).ready(function(){
    $("#start").click(function(){
        console.log("Start/stop btn was clicked.")
    });
    $("#reset").click(function(){
        console.log("Reset btn was clicked.")
    });
    $(document).on('shiny:recalculated', function(event) {
        timeLeft = document.querySelector("#time_left").textContent;
        secLeft = hmsToSeconds(timeLeft)
        if(secLeft < 1.5){
            console.log("Play sounding alarm")
            playSound(exampleSound)
        }
    });
});