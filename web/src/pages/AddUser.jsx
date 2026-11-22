import { useState } from 'react'
import './AddUser.css'

function AddUser() {
  const [role, setRole] = useState('LECTURER')
  const isTechnician = role === 'TECHNICIAN'

  return (
    <section className="add-user-panel" aria-labelledby="add-user-title">
      <header className="add-user-heading">
        <h2 id="add-user-title">Account details</h2>
        <p>
          Create a managed account for a lecturer or technician.
        </p>
      </header>

      <form onSubmit={(event) => event.preventDefault()}>
        <fieldset className="user-role-picker">
          <legend>Account role</legend>

          <div className="user-role-options">
            <label className={role === 'LECTURER' ? 'selected' : ''}>
              <input
                type="radio"
                name="role"
                value="LECTURER"
                checked={role === 'LECTURER'}
                onChange={(event) => setRole(event.target.value)}
              />
              <span>
                <strong>Lecturer</strong>
                <small>Report faults and track submitted tickets.</small>
              </span>
            </label>

            <label className={isTechnician ? 'selected' : ''}>
              <input
                type="radio"
                name="role"
                value="TECHNICIAN"
                checked={isTechnician}
                onChange={(event) => setRole(event.target.value)}
              />
              <span>
                <strong>Technician</strong>
                <small>Manage assigned maintenance work.</small>
              </span>
            </label>
          </div>
        </fieldset>

        <div className="user-form-grid">
          <div className="user-form-field">
            <label htmlFor="user-full-name">Full name</label>
            <input
              id="user-full-name"
              name="full_name"
              type="text"
              placeholder="Enter full name"
              minLength={2}
              maxLength={150}
              required
            />
          </div>

          <div className="user-form-field">
            <label htmlFor="user-email">Email address</label>
            <input
              id="user-email"
              name="email"
              type="email"
              placeholder="Enter email address"
              required
            />
          </div>

          <div className="user-form-field">
            <label htmlFor="user-department">Department</label>
            <select
              id="user-department"
              name="department_id"
              defaultValue=""
              aria-describedby="department-help"
              disabled
            >
              <option value="">Departments not connected</option>
            </select>
            <p id="department-help">
              Department options will come from verified backend records.
            </p>
          </div>

          {isTechnician && (
            <div className="user-form-field">
              <label htmlFor="user-team">Maintenance team</label>
              <select
                id="user-team"
                name="maintenance_team_id"
                defaultValue=""
                aria-describedby="team-help"
                disabled
              >
                <option value="">Maintenance teams not connected</option>
              </select>
              <p id="team-help">
                A technician must belong to an active maintenance team.
              </p>
            </div>
          )}
        </div>

        <div className="user-password-note">
          <strong>Temporary password</strong>
          <p>
            Once connected, the backend will generate a temporary
            password after creating the account. The user must
            change it at first login.
          </p>
        </div>

        <div className="user-form-actions">
          <p id="user-submit-help">
            Creation is unavailable until administrator authentication
            and department/team options are connected.
          </p>

          <button
            type="submit"
            disabled
            aria-describedby="user-submit-help"
          >
            Create account
          </button>
        </div>
      </form>
    </section>
  )
}

export default AddUser