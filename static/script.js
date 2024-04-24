//typing effect
var typed = new Typed('#animate', {
    strings: ['SignSense!'], //content to show in the animation
    typeSpeed: 100, //typing speed in ms
    backSpeed: 100, //backspeed in ms
    loop:true, // infinite loop of the animation
  });

//gsap
const tl = gsap.timeline();

tl.from("#nav li, #nav img , #nav button , #main2 h1 , #main3 p" , {
    y: -100,
    duration: 1,
    delay :0.5,
    opacity: 0,
    stagger: 0.2
});

// tl.from("#get-started",{
//   scrollTrigger: "#get-started"
// })