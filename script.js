fetch("jobs.json")
  .then(res => res.json())
  .then(jobs => {
    const sarkari = document.getElementById("sarkari");
    const other = document.getElementById("other");

    sarkari.innerHTML = "";
    other.innerHTML = "";

    jobs.forEach(job => {
      const card = document.createElement("div");
      card.className = "job-card";

      card.innerHTML = `
        <h3>${job.exam_name}</h3>
        <p><b>Department:</b> ${job.department}</p>
        <p><b>Qualification:</b> ${job.qualification || "—"}</p>
        <p><b>Last Date:</b> ${job.last_date}</p>
        <a href="${job.apply_link}" target="_blank" class="view-btn">
          Apply / Full Details
        </a>
      `;

      if (job.department.toLowerCase().includes("ssc")) {
        sarkari.appendChild(card);
      } else {
        other.appendChild(card);
      }
    });
  })
  .catch(err => console.error(err));
