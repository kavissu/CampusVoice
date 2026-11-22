import AdminDashboard from './pages/AdminDashboard.jsx'
import { useState } from 'react'
import ChangePassword from './pages/ChangePassword.jsx'
import './App.css'
import {
  login,
  getCurrentUser,
  changePassword,
} from './services/auth.js'

function App() {
  const [showPassword, setShowPassword] = useState(false)
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [session, setSession] = useState(null)

  function signOut() {
    setSession(null)
    setMessage('')
    setShowPassword(false)
  }

  async function handleLogin(event) {
    event.preventDefault()

    if (isLoading) return

    const formData = new FormData(event.currentTarget)
    const email = String(formData.get('email')).trim()
    const password = String(formData.get('password'))

    setMessage('')
    setIsLoading(true)

    try {
      const result = await login(email, password)
      const user = await getCurrentUser(result.access_token)

      if (!user.is_active || user.role !== 'ADMIN') {
        setMessage('This portal is available to administrators only.')
        return
      }

      setSession({
        token: result.access_token,
        user,
      })
    } catch (error) {
      setMessage(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  async function handlePasswordChange(currentPassword, newPassword) {
    try {
      await changePassword(
        session.token,
        currentPassword,
        newPassword
      )
    } catch (error) {
      if (error.status === 401) {
        signOut()
        setMessage('Your session has expired. Please sign in again.')
        return
      }

      throw error
    }

    signOut()
    setMessage('Password changed successfully. Sign in with your new password.')
  }

  if (session?.user.must_change_password) {
    return (
      <ChangePassword
        onBack={signOut}
        onSubmitPassword={handlePasswordChange}
      />
    )
  }

    if (session) {
    return (
  <AdminDashboard
    onBack={signOut}
    token={session.token}
  />
)
  }

  return (
    <main className="login-page">
      <div className="login-shell">
        <section className="login-panel" aria-labelledby="login-title">
          <div className="login-brand">
            <span aria-hidden="true">CV /</span>
            CampusVoice
          </div>

          <div className="login-content">
            <p className="eyebrow">ADMINISTRATION PORTAL</p>

            <h1 id="login-title">Welcome back.</h1>

            <p className="login-description">
              Sign in to manage your campus.
            </p>

            <form onSubmit={handleLogin}>
              <div className="login-field">
                <label htmlFor="email">Email address</label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="Enter your email"
                  autoComplete="username"
                  required
                />
              </div>

              <div className="login-field">
                <label htmlFor="password">Password</label>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                />
              </div>

              <label className="password-toggle">
                <input
                  type="checkbox"
                  checked={showPassword}
                  onChange={(event) =>
                    setShowPassword(event.target.checked)
                  }
                />
                Show password
              </label>

              <button
  className="signin-button"
  type="submit"
  disabled={isLoading}
>
  {isLoading ? 'Signing in…' : 'Sign in'}
  <span aria-hidden="true">↗</span>
</button>

              <p className="login-message" role="status">
                {message}
              </p>
            </form>

            <p className="login-help">
              Need account access? Contact your system administrator.
            </p>
          </div>

          <p className="login-footer">
            CampusVoice · Faculty of Engineering
            <br />
            University of Sri Jayewardenepura
          </p>
        </section>

        <aside className="login-visual" aria-label="About CampusVoice">
          <div className="visual-content">
            <span className="visual-label">YOUR CAMPUS, CONNECTED</span>

            <h2>
              A better campus.
              <br />
              A shared responsibility.
            </h2>

            <p>
              Coordinate resources, manage issues and support
              your university community.
            </p>
          </div>
        </aside>
      </div>

      
    </main>
  )
}

export default App