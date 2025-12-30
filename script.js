fetch("jobs.json")
  .then(res => res.json())
  .then(data => {
    const sarkariDiv = document.getElementById("sarkari-jobs");
    const otherDiv = document.getElementById("other-jobs");

    if (!data || data.length === 0) {
      sarkariDiv.innerHTML = "<p>No jobs available</p>";
      return;
    }

    data.forEach(job => {
      const card = document.createElement("div");
      card.className = "job-card";

      card.innerHTML = `
        <h3>${job.title}</h3>
        <p><b>Source:</b> ${job.source}</p>
        <p><b>Last Date:</b> ${job.last_date}</p>
        <a href="${job.apply_link}" target="_blank">Apply / Details</a>
      `;

      if (job.department === "Sarkari Result") {
        sarkariDiv.appendChild(card);
      } else {
        otherDiv.appendChild(card);
      }
    });
  })
  .catch(err => {
    console.error(err);
  });
