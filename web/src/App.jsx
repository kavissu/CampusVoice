import AdminDashboard from './pages/AdminDashboard.jsx'
import { useState } from 'react'
import './App.css'

function App() {
  const [showPassword, setShowPassword] = useState(false)
  const [message, setMessage] = useState('')
  const [previewDashboard, setPreviewDashboard] = useState(false)

  function handleLogin(event) {
    event.preventDefault()

    setMessage(
      'This is a design preview. Backend login is not connected yet.'
    )
  }
if (import.meta.env.DEV && previewDashboard) {
  return (
    <AdminDashboard onBack={() => setPreviewDashboard(false)} />
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

              <button className="signin-button" type="submit">
                Sign in
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

      <p className="preview-note">
        Interface preview — administrator authentication is not connected yet.
      </p>
      {import.meta.env.DEV && (
  <button
    className="dashboard-preview-button"
    type="button"
    onClick={() => setPreviewDashboard(true)}
  >
    Open dashboard preview — sample data
  </button>
)}
    </main>
  )
}

export default App