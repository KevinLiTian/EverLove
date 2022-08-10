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
  const cur_user = document.querySelector('[name="cur_user"]').value;
  const username = document.querySelector('[name="username"]').value;

  if (cur_user === username) {
    const btn = document.querySelector("#update");
    btn.onclick = () => {
      btn.blur();

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
  } else {
    document.querySelectorAll("input").forEach((input) => {
      input.disabled = true;
    });
    document.querySelectorAll("select").forEach((select) => {
      select.disabled = true;
    });
    document.querySelector("textarea").disabled = true;
  }
}

if (document.querySelector("#match")) {
  const filter_btn = document.querySelector("#filter-btn");
  const match_btn = document.querySelector("#match-btn");

  filter_btn.onclick = () => {
    filter_btn.blur();
    filter_btn.disabled = true;
    match_btn.disabled = true;

    const gender = document.querySelector('[name="gender"]').value;
    const age = document.querySelector('[name="age"]').value;
    const personality = document.querySelector('[name="mbti"]').value;
    const lifestyle = document.querySelector('[name="lifestyle"]').value;
    const hobby = document.querySelector('[name="hobby"]').value;

    document.querySelectorAll(".usr-box").forEach((box) => {
      if (box.classList.contains("hide-box")) {
        box.addEventListener("animationend", () => {
          box.remove();
        });
        box.style.animationPlayState = "running";
      }
    });

    fetch(`/filter_api`, {
      method: "POST",
      body: JSON.stringify({
        gender: gender,
        age: age,
        personality: personality,
        lifestyle: lifestyle,
        hobby: hobby,
      }),
    })
      .then((response) => response.json())
      .then((usrs) => {
        usrs.forEach((usr) => {
          const username = usr["username"];
          const fullname = usr["fullname"];

          const container = document.querySelector("#usr-boxes");
          const anchor = document.createElement("a");
          anchor.href = `/profile/${username}`;
          anchor.classList.add(
            "usr-box",
            "show-box",
            "d-flex",
            "flex-wrap",
            "text-center",
            "justify-content-center",
            "align-items-center",
            "rounded-custom",
            "m-3",
            "m-lg-4",
            "p-2",
            "text-decoration-none",
            "text-secondary"
          );
          const name = document.createElement("h4");
          if (fullname) {
            name.innerHTML = fullname;
          } else {
            name.innerHTML = username;
          }
          anchor.append(name);
          container.append(anchor);
          anchor.style.animationPlayState = "running";
          anchor.addEventListener("animationend", () => {
            anchor.style.animationPlayState = "paused";
            anchor.classList.remove("show-box");
            anchor.classList.add("hide-box");
          });
        });
      })
      .catch((err) => console.log(err));
    setTimeout(() => {
      filter_btn.disabled = false;
      match_btn.disabled = false;
    }, 2500);
  };

  match_btn.onclick = () => {
    filter_btn.disabled = true;
    match_btn.disabled = true;

    document.querySelectorAll(".usr-box").forEach((box) => {
      if (box.classList.contains("hide-box")) {
        box.addEventListener("animationend", () => {
          box.remove();
        });
        box.style.animationPlayState = "running";
      }
    });

    fetch("/match_api")
      .then((response) => response.json())
      .then((usrs) => {
        usrs.forEach((usr) => {
          const username = usr["username"];
          const fullname = usr["fullname"];

          const container = document.querySelector("#usr-boxes");
          const anchor = document.createElement("a");
          anchor.href = `/profile/${username}`;
          anchor.classList.add(
            "usr-box",
            "show-box",
            "d-flex",
            "flex-wrap",
            "text-center",
            "justify-content-center",
            "align-items-center",
            "rounded-custom",
            "m-3",
            "m-lg-4",
            "p-2",
            "text-decoration-none",
            "text-secondary"
          );
          const name = document.createElement("h4");
          if (fullname) {
            name.innerHTML = fullname;
          } else {
            name.innerHTML = username;
          }
          anchor.append(name);
          container.append(anchor);
          anchor.style.animationPlayState = "running";
          anchor.addEventListener("animationend", () => {
            anchor.style.animationPlayState = "paused";
            anchor.classList.remove("show-box");
            anchor.classList.add("hide-box");
          });
        });
      })
      .catch((err) => console.log(err));
    setTimeout(() => {
      filter_btn.disabled = false;
      match_btn.disabled = false;
    }, 2500);
  };
}
