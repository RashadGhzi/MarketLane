let prevScrollPos = window.pageYOffset;

window.onscroll = function () {
  const currentScrollPos = window.pageYOffset;
  if (prevScrollPos > currentScrollPos) {
    document.getElementById("navbar").style.display = "flex";
  } else {
    document.getElementById("navbar").style.display = "none";
  }
  prevScrollPos = currentScrollPos;
};
