const calendarBody = document.getElementById("calendar-body");
const personSelect = document.getElementById("personSelect");

const startHour = 9;
const endHour = 18;

// Store schedules for each person
const schedules = {
  john: {},
  sarah: {},
  alex: {}
};

// Build calendar grid
function buildCalendar() {
  calendarBody.innerHTML = "";

  for (let hour = startHour; hour < endHour; hour++) {
    const timeLabel = document.createElement("div");
    timeLabel.className = "time-slot time-label";
    timeLabel.textContent = formatHour(hour);
    calendarBody.appendChild(timeLabel);

    for (let day = 0; day < 7; day++) {
      const slot = document.createElement("div");
      slot.className = "time-slot slot";

      slot.dataset.day = day;
      slot.dataset.hour = hour;

      // 🔹 CLICK TO ADD EVENT
      slot.addEventListener("click", () => {
        const person = personSelect.value;
        const key = `${day}-${hour}`;

        const text = prompt("Enter event:");
        if (text) {
          schedules[person][key] = text;
          loadSchedule(person);
        }
      });

      calendarBody.appendChild(slot);
    }
  }
}

// Load selected person's schedule
function loadSchedule(person) {
  const slots = document.querySelectorAll(".slot");

  slots.forEach(slot => {
    slot.innerHTML = "";

    const key = `${slot.dataset.day}-${slot.dataset.hour}`;
    const eventText = schedules[person][key];

    if (eventText) {
      const event = document.createElement("div");
      event.className = "event";
      event.textContent = eventText;
      slot.appendChild(event);
    }
  });
}

// Format time
function formatHour(hour) {
  const ampm = hour >= 12 ? "PM" : "AM";
  const h = hour % 12 || 12;
  return `${h}:00 ${ampm}`;
}

// Dropdown change
personSelect.addEventListener("change", () => {
  loadSchedule(personSelect.value);
});

// Init
buildCalendar();
loadSchedule(personSelect.value);