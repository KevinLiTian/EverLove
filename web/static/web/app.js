// Collapsible
if (document.querySelector("nav")) {
  const navLinks = document.querySelectorAll(".nav-item");
  const menuToggle = document.getElementById("navmenu");
  const bsCollapse = new bootstrap.Collapse(menuToggle, { toggle: false });
  navLinks.forEach((l) => {
    l.addEventListener("click", () => {
      if (window.innerWidth < 992) {
        bsCollapse.toggle();
      }
    });
  });
}

// Sign Form Button Enable/Disable
if (document.querySelector(".sign-form")) {
  const button = document.querySelector(".disabled");
  const all_input = document.querySelectorAll("input");
  all_input.forEach((input) => {
    input.oninput = () => {
      let all_filled = true;
      all_input.forEach((ipt) => {
        if (ipt.value === "") {
          all_filled = false;
        }
      });
      if (all_filled) {
        button.classList.remove("disabled");
      } else {
        button.classList.add("disabled");
      }
    };
  });
}
