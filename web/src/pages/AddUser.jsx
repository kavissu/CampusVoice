import { useState } from 'react'
import './AddUser.css'
import { createUser } from '../services/users.js'

function AddUser({ token, onSessionExpired }) {
  const [role, setRole] = useState('LECTURER')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [createdUser, setCreatedUser] = useState(null)

  const isTechnician = role === 'TECHNICIAN'

  async function handleSubmit(event) {
    event.preventDefault()

    if (isSubmitting) return

    const form = event.currentTarget
    const formData = new FormData(form)

    const departmentId = Number(formData.get('department_id'))
    const maintenanceTeamId = Number(
      formData.get('maintenance_team_id')
    )

    setMessage('')
    setCreatedUser(null)

    if (!Number.isInteger(departmentId) || departmentId <= 0) {
      setMessage('Select a department before creating the account.')
      return
    }

    if (
      isTechnician &&
      (!Number.isInteger(maintenanceTeamId) || maintenanceTeamId <= 0)
    ) {
      setMessage('Select a maintenance team for this technician.')
      return
    }

    const userDetails = {
      full_name: String(formData.get('full_name')).trim(),
      email: String(formData.get('email')).trim().toLowerCase(),
      role,
      department_id: departmentId,
      maintenance_team_id: isTechnician ? maintenanceTeamId : null,
    }

    setIsSubmitting(true)

    try {
      const result = await createUser(token, userDetails)
      setCreatedUser(result)
      form.reset()
      setRole('LECTURER')
    } catch (error) {
      if (error.status === 401) {
        onSessionExpired()
        return
      }

      setMessage(error.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="add-user-panel" aria-labelledby="add-user-title">
      <header className="add-user-heading">
        <h2 id="add-user-title">Account details</h2>
        <p>
          Create a managed account for a lecturer or technician.
        </p>
      </header>

      <form onSubmit={handleSubmit} aria-busy={isSubmitting}>
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
            {message && (
  <p role="alert" className="user-form-message">
    {message}
  </p>
)}

{createdUser && (
  <section
    className="user-password-note"
    aria-labelledby="created-user-title"
    aria-live="polite"
  >
    <h3 id="created-user-title">Account created successfully</h3>

    <p>
      <strong>Name:</strong> {createdUser.full_name}
    </p>

    <p>
      <strong>Email:</strong> {createdUser.email}
    </p>

    <p>
      <strong>Role:</strong> {createdUser.role}
    </p>

    <p>
      <strong>Temporary password:</strong>{' '}
      <code>{createdUser.temporary_password}</code>
    </p>

    <p>
      Share these credentials privately with the account owner.
      They must change their password when they first sign in.
      The temporary password will disappear when you leave this page.
    </p>

    <button
      type="button"
      onClick={() => setCreatedUser(null)}
    >
      Dismiss account details
    </button>
  </section>
)}
        <div className="user-form-actions">
          <p id="user-submit-help">
  Account creation will become available when department and
  maintenance-team options are connected.
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