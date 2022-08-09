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

if (document.querySelector("#profile")) {
  const btn = document.querySelector("#update");
  btn.onclick = () => {
    btn.blur();

    const username = document.querySelector('[name="username"]').value;
    const fullname = document.querySelector('[name="fullname"]').value;
    const gender = document.querySelector('[name="gender"]').value;
    const age = document.querySelector('[name="age"]').value;
    const personality = document.querySelector('[name="mbti"]').value;
    const job = document.querySelector('[name="job"]').value;
    const sexuality = document.querySelector('[name="sexuality"]').value;
    const lifestyle = document.querySelector('[name="lifestyle"]').value;
    const description = document.querySelector('[name="description"]').value;
    const hobby1 = document.querySelector('[name="hobby1"]').value;
    const hobby2 = document.querySelector('[name="hobby2"]').value;
    const hobby3 = document.querySelector('[name="hobby3"]').value;

    fetch(`/profile/${username}`, {
      method: "PUT",
      body: JSON.stringify({
        fullname: fullname,
        gender: gender,
        age: age,
        personality: personality,
        job: job,
        sexuality: sexuality,
        lifestyle: lifestyle,
        description: description,
        hobby1: hobby1,
        hobby2: hobby2,
        hobby3: hobby3,
      }),
    })
      .then((response) => response.json())
      .catch((err) => console.log(err));
  };
}
