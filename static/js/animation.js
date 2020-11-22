var tl = gsap.timeline({ defaults: { ease: "powe1.out" } });
var tl_news = gsap.timeline({ defaults: { ease: "powe1.out" } });

//the following two lines do the SAME thing:
tl.to(".data-card", {
  y: 0,
  opacity: 1,
  duration: 1,
  stagger: 0.25,
});

tl_news.to(".card", {
  y: 0,
  opacity: 1,
  duration: 2,
  stagger: 0.25,
});
