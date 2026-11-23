import { useEffect, useRef, useState } from 'react'
import { createUser } from '../services/users.js'
import './AddUser.css'

async function loadOptions(path, token, signal) {
  const response = await fetch(`/api/v1/admin/${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'application/json',
    },
    signal,
  })

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const error = new Error(
      typeof data?.detail === 'string'
        ? data.detail
        : 'Unable to load departments and teams.'
    )
    error.status = response.status
    throw error
  }

  if (!Array.isArray(data)) {
    throw new Error('The server returned an unexpected list format.')
  }

  return data
}

function AccountCreatedDialog({ user, onDismiss }) {
  const dialogRef = useRef(null)

  useEffect(() => {
    const dialog = dialogRef.current
    const previousFocus = document.activeElement

    dialog.showModal()

    return () => {
      dialog.close()
      previousFocus?.focus()
    }
  }, [])

  return (
    <dialog
      ref={dialogRef}
      className="account-created-dialog"
      aria-labelledby="account-created-title"
      aria-describedby="account-created-description"
      onCancel={(event) => {
        event.preventDefault()
        onDismiss()
      }}
    >
      <div className="account-created-content">
        <p className="account-created-label">ACCOUNT READY</p>

        <h2 id="account-created-title">
          Account created successfully
        </h2>

        <p id="account-created-description">
          Save these details privately before dismissing this window.
        </p>

        <dl className="account-created-details">
          <div>
            <dt>Full name</dt>
            <dd>{user.full_name}</dd>
          </div>

          <div>
            <dt>Email address</dt>
            <dd>{user.email}</dd>
          </div>

          <div>
            <dt>Role</dt>
            <dd>
              {user.role === 'LECTURER' ? 'Lecturer' : 'Technician'}
            </dd>
          </div>
        </dl>

        <div className="account-created-password">
          <p>Temporary password</p>
          <code>{user.temporary_password}</code>
        </div>

        <p className="account-created-guidance">
          Share these credentials privately with the account owner.
          They must change their password when they first sign in.
          These details disappear when you dismiss this window.
        </p>

        <button
          className="account-created-dismiss"
          type="button"
          autoFocus
          onClick={onDismiss}
        >
          Dismiss
        </button>
      </div>
    </dialog>
  )
}

function AddUser({ token, onSessionExpired }) {
  const [role, setRole] = useState('LECTURER')
  const [departments, setDepartments] = useState([])
  const [teams, setTeams] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [loadError, setLoadError] = useState('')
  const [reloadCount, setReloadCount] = useState(0)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [createdUser, setCreatedUser] = useState(null)

  const isTechnician = role === 'TECHNICIAN'

  useEffect(() => {
    const controller = new AbortController()

    async function loadLists() {
      setIsLoading(true)
      setLoadError('')

      try {
        const [departmentList, teamList] = await Promise.all([
          loadOptions('departments', token, controller.signal),
          loadOptions('maintenance-teams', token, controller.signal),
        ])

        if (controller.signal.aborted) return

        setDepartments(departmentList)
        setTeams(teamList)
      } catch (error) {
        if (controller.signal.aborted) return

        if (error.status === 401) {
          onSessionExpired()
          return
        }

        setLoadError(
          error instanceof TypeError
            ? 'Cannot reach the server. Check that the backend is running.'
            : error.message
        )
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false)
        }
      }
    }

    loadLists()

    return () => controller.abort()
  }, [token, onSessionExpired, reloadCount])

  const optionsUnavailable =
    isLoading ||
    Boolean(loadError) ||
    departments.length === 0 ||
    (isTechnician && teams.length === 0)

  const helpText = isLoading
    ? 'Loading departments and teams…'
    : loadError
      ? 'Retry loading the options before creating an account.'
      : departments.length === 0
        ? 'No departments are available.'
        : isTechnician && teams.length === 0
          ? 'No active maintenance teams are available.'
          : 'Complete the required fields to create an account.'

  async function handleSubmit(event) {
    event.preventDefault()

    if (isSubmitting || optionsUnavailable || createdUser) return

    const form = event.currentTarget
    const formData = new FormData(form)
    const fullName = String(formData.get('full_name')).trim()
    const departmentId = Number(formData.get('department_id'))
    const teamId = Number(formData.get('maintenance_team_id'))

    setMessage('')

    if (fullName.length < 2) {
      setMessage('Enter a full name containing at least two characters.')
      return
    }

    if (!departments.some((item) => item.id === departmentId)) {
      setMessage('Select a valid department.')
      return
    }

    if (
      isTechnician &&
      !teams.some((item) => item.id === teamId)
    ) {
      setMessage('Select an active maintenance team.')
      return
    }

    setIsSubmitting(true)

    try {
      const result = await createUser(token, {
        full_name: fullName,
        email: String(formData.get('email')).trim().toLowerCase(),
        role,
        department_id: departmentId,
        maintenance_team_id: isTechnician ? teamId : null,
      })

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
        <p>Create a managed account for a lecturer or technician.</p>
      </header>

      {loadError && (
        <div>
          <p role="alert">{loadError}</p>
          <button
            type="button"
            disabled={isLoading}
            onClick={() => setReloadCount((count) => count + 1)}
          >
            Retry loading options
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit} aria-busy={isSubmitting || isLoading}>
        <fieldset
          className="user-role-picker"
          disabled={isSubmitting}
        >
          <legend>Account role</legend>

          <div className="user-role-options">
            <label className={!isTechnician ? 'selected' : ''}>
              <input
                type="radio"
                name="role"
                value="LECTURER"
                checked={!isTechnician}
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
              disabled={isSubmitting}
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
              disabled={isSubmitting}
              required
            />
          </div>

          <div className="user-form-field">
            <label htmlFor="user-department">Department</label>
            <select
              id="user-department"
              name="department_id"
              defaultValue=""
              disabled={
                isLoading ||
                isSubmitting ||
                Boolean(loadError) ||
                departments.length === 0
              }
              required
            >
              <option value="" disabled>
                {isLoading ? 'Loading departments…' : 'Select a department'}
              </option>
              {departments.map((department) => (
                <option key={department.id} value={department.id}>
                  {department.name} ({department.code})
                </option>
              ))}
            </select>
          </div>

          {isTechnician && (
            <div className="user-form-field">
              <label htmlFor="user-team">Maintenance team</label>
              <select
                id="user-team"
                name="maintenance_team_id"
                defaultValue=""
                disabled={
                  isLoading ||
                  isSubmitting ||
                  Boolean(loadError) ||
                  teams.length === 0
                }
                required
              >
                <option value="" disabled>
                  {isLoading ? 'Loading teams…' : 'Select a maintenance team'}
                </option>
                {teams.map((team) => (
                  <option key={team.id} value={team.id}>
                    {team.name}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        <div className="user-password-note">
          <strong>Temporary password</strong>
          <p>
            The backend generates a temporary password when the account
            is created. The user must change it at first login.
          </p>
        </div>

        {message && (
          <p role="alert" className="user-form-message">
            {message}
          </p>
        )}

        {createdUser && (
  <AccountCreatedDialog
    user={createdUser}
    onDismiss={() => setCreatedUser(null)}
  />
)}

        <div className="user-form-actions">
          <p id="user-submit-help" role="status">
            {createdUser
              ? 'Save the temporary credentials privately, then dismiss them before creating another account.'
              : helpText}
          </p>

          <button
            type="submit"
            disabled={
              optionsUnavailable ||
              isSubmitting ||
              Boolean(createdUser)
            }
            aria-describedby="user-submit-help"
          >
            {isSubmitting ? 'Creating account…' : 'Create account'}
          </button>
        </div>
      </form>
    </section>
  )
}

export default AddUser