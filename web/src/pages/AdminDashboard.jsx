import './AdminDashboard.css'
import { useState } from 'react'
import AddUser from './AddUser.jsx'

function SummaryIcon({ label }) {
  const iconPaths = {
    'Total tickets': (
      <>
        <rect x="5" y="3" width="14" height="18" rx="2" />
        <path d="M9 8h6M9 12h6M9 16h4" />
      </>
    ),
    Open: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 7v5l3 2" />
      </>
    ),
    'In progress': (
      <>
        <path d="M20 7v5h-5M4 17v-5h5" />
        <path d="M6 7a7 7 0 0 1 11-2l3 3" />
        <path d="M18 17a7 7 0 0 1-11 2l-3-3" />
      </>
    ),
    Resolved: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="m8 12 3 3 5-6" />
      </>
    ),
  }

  return (
    <svg
      width="26"
      height="26"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {iconPaths[label]}
    </svg>
  )
}
const sampleTickets = [
  {
    id: 'DEMO-001',
    issue: 'Projector not working',
    location: 'Sample Hall A',
    priority: 'High',
    status: 'Open',
  },
  {
    id: 'DEMO-002',
    issue: 'Microphone issue',
    location: 'Sample Hall B',
    priority: 'Medium',
    status: 'In Progress',
  },
  {
    id: 'DEMO-003',
    issue: 'Smart-board pen missing',
    location: 'Sample Hall C',
    priority: 'Low',
    status: 'Resolved',
  },
]

const futurePages = [
  'Users',
  'Maintenance',
  'Campus',
  'Notifications',
  'Reports',
  'Settings',
]

function AdminDashboard({ onBack, token }) {
      const [activePage, setActivePage] = useState('Dashboard')
      const [ticketSearch, setTicketSearch] = useState('')
const [statusFilter, setStatusFilter] = useState('All')
const [priorityFilter, setPriorityFilter] = useState('All')
      const resolvedCount = sampleTickets.filter(
    (ticket) => ticket.status === 'Resolved'
  ).length

  const resolutionPercentage =
    sampleTickets.length === 0
      ? 0
      : Math.round((resolvedCount / sampleTickets.length) * 100)
  const summaryCards = [
    { label: 'Total tickets', value: sampleTickets.length },
    {
      label: 'Open',
      value: sampleTickets.filter((ticket) => ticket.status === 'Open').length,
    },
    {
      label: 'In progress',
      value: sampleTickets.filter(
        (ticket) => ticket.status === 'In Progress'
      ).length,
    },
    {
      label: 'Resolved',
      value: sampleTickets.filter(
        (ticket) => ticket.status === 'Resolved'
      ).length,
    },
  ]
  const filteredTickets = sampleTickets.filter((ticket) => {
  const searchText = ticketSearch.trim().toLowerCase()

  const matchesSearch = [
    ticket.id,
    ticket.issue,
    ticket.location,
  ].some((value) => value.toLowerCase().includes(searchText))

  const matchesStatus =
    statusFilter === 'All' || ticket.status === statusFilter

  const matchesPriority =
    priorityFilter === 'All' || ticket.priority === priorityFilter

  return matchesSearch && matchesStatus && matchesPriority
})

const visibleTickets =
  activePage === 'Tickets' ? filteredTickets : sampleTickets
  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="admin-brand">
          <span aria-hidden="true">CV /</span>
          CampusVoice
        </div>

        <p className="sidebar-label">ADMINISTRATION</p>

        <nav className="admin-navigation" aria-label="Admin navigation">
          {['Dashboard', 'Tickets', 'Add User'].map((page) => (
  <button
    key={page}
    type="button"
    aria-current={activePage === page ? 'page' : undefined}
    onClick={() => setActivePage(page)}
  >
    <span>{page === 'Tickets' ? 'Complaints / Tickets' : page}</span>
    <span aria-hidden="true">
      {activePage === page ? '↗' : '→'}
    </span>
  </button>
))}

          {futurePages.map((page) => (
            <button key={page} type="button" disabled>
              <span>{page}</span>
              <span className="coming-soon">Soon</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <p>Development preview</p>
          <button type="button" onClick={onBack}>
            ← Back to login
          </button>
        </div>
      </aside>

      <main className="admin-main">
        <header className="admin-topbar">
          <span>
  Workspace / {activePage === 'Tickets' ? 'Complaints / Tickets' : activePage}
</span>
          <span className="admin-preview-badge">Preview mode</span>
        </header>

        <div className="admin-content">
          <section className="dashboard-heading">
            <p className="admin-eyebrow">CAMPUS OVERVIEW</p>
            <h1 id="dashboard-heading">
  {activePage === 'Tickets' ? 'Complaints / Tickets' : activePage}
</h1>

<p>
  {activePage === 'Dashboard'
    ? 'A clear view of campus issues and maintenance activity.'
    : activePage === 'Tickets'
      ? 'Browse campus issues and review their progress.'
      : 'Create lecturer and technician accounts.'}
</p>
          </section>

          <p className="admin-demo-notice" role="note">
  Account creation is connected. Ticket records and dashboard statistics currently use sample data.
</p>

         {activePage === 'Dashboard' && (
  <>
            <section className="overview-strip" aria-label="Sample ticket overview">
  <div className="admin-stats">
    {summaryCards.map((card) => (
      <article className="admin-stat-card" key={card.label}>
        <span className="summary-icon">
          <SummaryIcon label={card.label} />
        </span>

        <h2>{card.label}</h2>
        <p>{card.value}</p>
        <span>Sample tickets</span>
      </article>
    ))}
  </div>

  <article className="resolution-panel">
    <div
      className="resolution-ring"
      style={{ '--resolution': `${resolutionPercentage}%` }}
      role="img"
      aria-label={
        sampleTickets.length === 0
          ? 'No sample tickets to measure'
          : `${resolvedCount} of ${sampleTickets.length} sample tickets resolved, ${resolutionPercentage} percent`
      }
    >
      <div className="resolution-ring-centre" aria-hidden="true">
        <span>Resolved</span>
        <strong>
          {sampleTickets.length === 0
            ? '—'
            : `${resolutionPercentage}%`}
        </strong>
      </div>
    </div>

    <p>
      {resolvedCount} of {sampleTickets.length} sample tickets
    </p>
  </article>
</section>
            
<section
  className="priority-overview"
  aria-labelledby="priority-overview-title"
>
  <h2 id="priority-overview-title">Tickets by priority</h2>

  <p>
    Distribution of the sample tickets shown below.
  </p>

  <div className="priority-breakdown">
    {['Critical', 'High', 'Medium', 'Low'].map((priority) => {
      const count = sampleTickets.filter(
        (ticket) => ticket.priority === priority
      ).length

      const percentage =
        sampleTickets.length === 0
          ? 0
          : (count / sampleTickets.length) * 100

      return (
        <div className="priority-item" key={priority}>
          <div className="priority-item-heading">
            <span>{priority}</span>
            <strong>
              {count} / {sampleTickets.length}
            </strong>
          </div>

          <div className="priority-track" aria-hidden="true">
            <span
              className={`priority-fill priority-fill-${priority.toLowerCase()}`}
              style={{ width: `${percentage}%` }}
            />
          </div>
        </div>
      )
    })}
  </div>
</section>
  </>
)}{activePage === 'Add User' && (
  <AddUser token={token} onSessionExpired={onBack} />
)}

{activePage !== 'Add User' && (
          <section className="admin-ticket-panel">
            <div className="admin-panel-heading">
              <div>
                <h2 id="recent-tickets-heading">
  {activePage === 'Dashboard' ? 'Recent tickets' : 'All tickets'}
</h2>
                <p>A preview of the ticket-management layout.</p>
              </div>
              <span className="admin-preview-badge">Sample records</span>
            </div>
{activePage === 'Tickets' && (
  <div className="ticket-filter-area">
    <div className="ticket-filters">
  <div className="ticket-search">
    <label className="filter-sr-only" htmlFor="admin-ticket-search">
      Search tickets
    </label>

    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <circle cx="10.5" cy="10.5" r="6.5" />
      <path d="m16 16 4 4" />
    </svg>

    <input
      id="admin-ticket-search"
      type="search"
      placeholder="Search tickets…"
      value={ticketSearch}
      onChange={(event) => setTicketSearch(event.target.value)}
    />
  </div>

  <div className="ticket-select">
    <label htmlFor="admin-status-filter">Status:</label>

    <select
      id="admin-status-filter"
      value={statusFilter}
      onChange={(event) => setStatusFilter(event.target.value)}
    >
      <option value="All">All</option>

      {[...new Set(sampleTickets.map((ticket) => ticket.status))].map(
        (status) => (
          <option key={status} value={status}>
            {status}
          </option>
        )
      )}
    </select>
  </div>

  <div className="ticket-select">
    <label htmlFor="admin-priority-filter">Priority:</label>

    <select
      id="admin-priority-filter"
      value={priorityFilter}
      onChange={(event) => setPriorityFilter(event.target.value)}
    >
      <option value="All">All</option>
      <option value="Critical">Critical</option>
      <option value="High">High</option>
      <option value="Medium">Medium</option>
      <option value="Low">Low</option>
    </select>
  </div>

  <button
    className="ticket-reset-button"
    type="button"
    onClick={() => {
      setTicketSearch('')
      setStatusFilter('All')
      setPriorityFilter('All')
    }}
  >
    Reset
  </button>
</div>

    <p className="ticket-result-count" role="status">
      Showing {filteredTickets.length} of {sampleTickets.length} sample tickets
    </p>
  </div>
)}
            <div
              className="admin-table-scroll"
              role="region"
              aria-labelledby="recent-tickets-heading"
              tabIndex={0}
            >
              <table className="admin-ticket-table">
                <thead>
                  <tr>
                    <th scope="col">Ticket ID</th>
                    <th scope="col">Issue</th>
                    <th scope="col">Location</th>
                    <th scope="col">Priority</th>
                    <th scope="col">Status</th>
                  </tr>
                </thead>

                <tbody>
                  {visibleTickets.map((ticket) => (
                    <tr key={ticket.id}>
                      <td>{ticket.id}</td>
                      <td>{ticket.issue}</td>
                      <td>{ticket.location}</td>
                      <td>
                        <span
                          className={`admin-priority priority-${ticket.priority.toLowerCase()}`}
                        >
                          {ticket.priority}
                        </span>
                      </td>
                      <td>
                        <span className="admin-status">{ticket.status}</span>
                      </td>
                    </tr>
                  ))}
                  {visibleTickets.length === 0 && (
  <tr>
    <td colSpan={5} className="ticket-empty-state">
      No tickets match your search and filters. Try resetting the filters.
    </td>
  </tr>
)}
                </tbody>
              </table>
            </div>
          </section>
          )}
        </div>
      </main>
    </div>
  )
}

export default AdminDashboard