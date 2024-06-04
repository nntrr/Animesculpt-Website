

function videoanimation(){
    var videoplay = document.querySelector("#video-container");
var playbtn = document.querySelector("#playing");

videoplay.addEventListener("mouseenter", function(){
    playbtn.style.opacity = 1;
    playbtn.style.transform = "scale(1)";
});

videoplay.addEventListener("mouseleave", function(){
    playbtn.style.opacity = 0;
    playbtn.style.transform = "scale(0)";
});

videoplay.addEventListener("mousemove", function(dets){

    gsap.to(playbtn,{
        left: dets.x - 70,
      top: dets.y - 80
    })
})
}
videoanimation()




function cursorAnimation() {
  document.addEventListener("mousemove", function (event) {
    gsap.to("#cursor", {
      left: event.x,
      top: event.y,
    });
  });
 
  document.querySelectorAll(".info").forEach(function (elem) {
    elem.addEventListener("mouseenter", function () {
      // Change cursor background color when entering each .info element
      var color;
      switch (elem.id) {
        case "info1":
          color = "#b5651d"; // Change color for info1
          break;
        case "info2":
          color = "#FF007F"; // Change color for info2
          break;
        case "info3":
          color = "orange"; // Change color for info3
          break;
        case "info4":
          color = "red"; // Change color for info4
          break;
        default:
          color = "red"; // Default color
          break;
      }
      gsap.to("#cursor", {
        backgroundColor: color, // Set cursor background color
        transform: "translate(-50%,-50%) scale(1)",
      });
    });
    elem.addEventListener("mouseleave", function () {
      gsap.to("#cursor", {
        transform: "translate(-50%,-50%) scale(0)",
      });
    });
  });
}

cursorAnimation();

