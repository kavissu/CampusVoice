import { useState } from 'react'

function ChangePassword({ onBack, onSubmitPassword }) {
  const [showPasswords, setShowPasswords] = useState(false)
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  async function handleSubmit(event) {
  event.preventDefault()

  if (isLoading) return

  const formData = new FormData(event.currentTarget)
  const currentPassword = String(formData.get('currentPassword'))
  const newPassword = String(formData.get('newPassword'))
  const confirmPassword = String(formData.get('confirmPassword'))

  setMessage('')

  if (newPassword.length < 8) {
    setMessage('Use at least 8 characters for your new password.')
    return
  }

  if (newPassword !== confirmPassword) {
    setMessage('The new passwords do not match.')
    return
  }

  if (currentPassword === newPassword) {
    setMessage('Choose a new password different from your current password.')
    return
  }

  setIsLoading(true)

  try {
    await onSubmitPassword(currentPassword, newPassword)
  } catch (error) {
    setMessage(error.message)
  } finally {
    setIsLoading(false)
  }
}

  return (
    <main className="login-page">
      <div className="login-shell">
        <section className="login-panel" aria-labelledby="password-title">
          <div className="login-brand">
            <span aria-hidden="true">CV /</span>
            CampusVoice
          </div>

          <div className="login-content">
            <p className="eyebrow">ACCOUNT SECURITY</p>

            <h1 id="password-title">Set your password.</h1>

            <p className="login-description">
              If your account requires a password change, you must
              complete it before accessing the administration portal.
            </p>

            <form
              onSubmit={handleSubmit}
              onChange={() => setMessage('')}
            >
              <div className="login-field">
                <label htmlFor="current-password">
                  Current or temporary password
                </label>

                <input
                  id="current-password"
                  name="currentPassword"
                  type={showPasswords ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                />
              </div>

              <div className="login-field">
                <label htmlFor="new-password">New password</label>

                <input
                  id="new-password"
                  name="newPassword"
                  type={showPasswords ? 'text' : 'password'}
                  autoComplete="new-password"
                  minLength={8}
                  aria-describedby="password-guidance"
                  required
                />

                <p id="password-guidance" className="password-guidance">
                  Use at least 8 characters.
                </p>
              </div>

              <div className="login-field">
                <label htmlFor="confirm-password">
                  Confirm new password
                </label>

                <input
                  id="confirm-password"
                  name="confirmPassword"
                  type={showPasswords ? 'text' : 'password'}
                  autoComplete="new-password"
                  minLength={8}
                  required
                />
              </div>

              <label className="password-toggle">
                <input
                  type="checkbox"
                  checked={showPasswords}
                  onChange={(event) =>
                    setShowPasswords(event.target.checked)
                  }
                />
                Show passwords
              </label>

              <button
  className="signin-button"
  type="submit"
  disabled={isLoading}
>
  {isLoading ? 'Saving…' : 'Save new password'}
  <span aria-hidden="true">↗</span>
</button>

              <p className="login-message" role="status">
                {message}
              </p>
            </form>
          </div>

          <button
  className="password-back-button"
  type="button"
  onClick={onBack}
  disabled={isLoading}
>
  ← Back to login
</button>
        </section>

        <aside className="login-visual" aria-label="Account security">
          <div className="visual-content">
            <span className="visual-label">A PERSONAL PASSWORD</span>

            <h2>
              Your account.
              <br />
              Your responsibility.
            </h2>

            <p>
              Replace your temporary password with one that
              you do not use for other accounts.
            </p>
          </div>
        </aside>
      </div>

      
    </main>
  )
}

export default ChangePassword