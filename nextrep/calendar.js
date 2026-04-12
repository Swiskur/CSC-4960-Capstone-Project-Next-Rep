const calendarBody = document.getElementById("calendar-body");

// Hours from 8 AM to 8 PM
const startHour = 8;
const endHour = 20;

for (let hour = startHour; hour < endHour; hour++) {
  // Time label column
  const timeLabel = document.createElement("div");
  timeLabel.className = "time-slot time-label";
  timeLabel.textContent = formatHour(hour);
  calendarBody.appendChild(timeLabel);

  // 7 days
  for (let day = 0; day < 7; day++) {
    const slot = document.createElement("div");
    slot.className = "time-slot slot";

    // Click to add event
    slot.addEventListener("click", () => {
      const text = prompt("Enter event:");
      if (text) {
        const event = document.createElement("div");
        event.className = "event";
        event.textContent = text;

        slot.innerHTML = "";
        slot.appendChild(event);
      }
    });

    calendarBody.appendChild(slot);
  }
}

// Helper function
function formatHour(hour) {
  const ampm = hour >= 12 ? "PM" : "AM";
  const h = hour % 12 || 12;
  return `${h}:00 ${ampm}`;
}