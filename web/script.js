const statusFilter = document.querySelector("#status-filter");
const ticketSearch = document.querySelector("#ticket-search");

function filterTickets() {
  const ticketRows = document.querySelectorAll("#tickets-table tbody tr");

  const selectedStatus = statusFilter.value;
  const searchText = ticketSearch.value.trim().toLowerCase();
  let visibleCount = 0;

  ticketRows.forEach(function (row) {
    const ticketStatus = row.cells[3].textContent.trim();

    const ticketDetails = [
      row.cells[0].textContent,
      row.cells[1].textContent,
      row.cells[2].textContent
    ].join(" ").toLowerCase();

    const matchesStatus =
      selectedStatus === "all" || ticketStatus === selectedStatus;

    const matchesSearch = ticketDetails.includes(searchText);
    const shouldShow = matchesStatus && matchesSearch;

    row.hidden = !shouldShow;

    if (shouldShow) {
      visibleCount++;
    }
  });

  const emptyMessage = document.querySelector("#empty-message");
  emptyMessage.hidden = visibleCount > 0;
}

statusFilter.addEventListener("change", filterTickets);
ticketSearch.addEventListener("input", filterTickets);

function updateSummary() {
  const ticketRows = document.querySelectorAll("#tickets-table tbody tr");

  let openCount = 0;
  let acceptedCount = 0;
  let progressCount = 0;
  let resolvedCount = 0;

  ticketRows.forEach(function (row) {
    const status = row.cells[3].textContent.trim();

   if (status === "Open") {
  openCount++;
} else if (status === "Accepted") {
  acceptedCount++;
} else if (status === "In Progress") {
  progressCount++;
} else if (status === "Resolved") {
  resolvedCount++;
}
  });

  document.querySelector("#total-count").textContent = ticketRows.length;
  document.querySelector("#open-count").textContent = openCount;
  document.querySelector("#accepted-count").textContent = acceptedCount;
  document.querySelector("#progress-count").textContent = progressCount;
  document.querySelector("#resolved-count").textContent = resolvedCount;
}

updateSummary();

const resetButton = document.querySelector("#reset-filters");

resetButton.addEventListener("click", function () {
  ticketSearch.value = "";
  statusFilter.value = "all";

  filterTickets();
  ticketSearch.focus();
});

const ticketForm = document.querySelector("#ticket-form");
const locationInput = document.querySelector("#ticket-location");
const issueInput = document.querySelector("#ticket-issue");
const tableBody = document.querySelector("#tickets-table tbody");

// Find the highest existing ticket number.
let nextTicketNumber = 1;

tableBody.querySelectorAll("tr").forEach(function (row) {
  const ticketId = row.cells[0].textContent.trim();
  const number = Number(ticketId.replace("CV-", ""));

  if (number >= nextTicketNumber) {
    nextTicketNumber = number + 1;
  }
});

ticketForm.addEventListener("submit", function (event) {
  event.preventDefault();

  const location = locationInput.value.trim();
  const issue = issueInput.value.trim();

  if (location === "" || issue === "") {
    alert("Please enter a location and an issue description.");
    return;
  }

  const ticketId =
    "CV-" + String(nextTicketNumber).padStart(3, "0");

  const row = document.createElement("tr");

  [ticketId, location, issue].forEach(function (value) {
    const cell = document.createElement("td");
    cell.textContent = value;
    row.appendChild(cell);
  });

  const statusCell = document.createElement("td");
  const badge = document.createElement("span");

  badge.className = "status-badge status-open";
  badge.textContent = "Open";

  statusCell.appendChild(badge);
  row.appendChild(statusCell);
  tableBody.appendChild(row);
  addStatusControl(row);

  nextTicketNumber++;

  ticketForm.reset();

  // Show all tickets so the newly added ticket is visible.
  ticketSearch.value = "";
  statusFilter.value = "all";

  updateSummary();
  filterTickets();
  locationInput.focus();
});

function addStatusControl(row) {
  const statusCell = row.cells[3];
  const badge = statusCell.querySelector(".status-badge");

  const actionCell = document.createElement("td");
  const select = document.createElement("select");

  select.className = "status-select";
  select.setAttribute(
    "aria-label",
    "Change status for " + row.cells[0].textContent.trim()
  );

  const badgeClasses = {
  "Open": "status-open",
  "Accepted": "status-accepted",
  "In Progress": "status-progress",
  "Resolved": "status-resolved"
};

  ["Open", "Accepted", "In Progress", "Resolved"].forEach(function (status) {
    const option = document.createElement("option");

    option.value = status;
    option.textContent = status;
    select.appendChild(option);
  });

  select.value = badge.textContent.trim();

  select.addEventListener("change", function () {
    const newStatus = select.value;

    badge.textContent = newStatus;
    badge.className = "status-badge " + badgeClasses[newStatus];

    updateSummary();
    filterTickets();
  });

  actionCell.appendChild(select);
  row.appendChild(actionCell);
}

// Add controls to the tickets already in the HTML.
tableBody.querySelectorAll("tr").forEach(function (row) {
  addStatusControl(row);
});

