async function authRequest(path, { method = 'GET', body, token } = {}) {
  const headers = {
    Accept: 'application/json',
  }

  if (body) {
    headers['Content-Type'] = 'application/json'
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  let response

  try {
    response = await fetch(`/api/v1/auth${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    })
  } catch {
    throw new Error(
      'Cannot connect to the server. Check that both servers are running.'
    )
  }

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const detail = data?.detail

    const message =
      typeof detail === 'string'
        ? detail
        : response.status === 422
          ? 'Please check the information you entered.'
          : 'The request could not be completed. Please try again.'

    const error = new Error(message)
    error.status = response.status
    throw error
  }

  if (!data) {
    throw new Error('The server returned an unexpected response.')
  }

  return data
}

export async function login(email, password) {
  const data = await authRequest('/login', {
    method: 'POST',
    body: { email, password },
  })

  if (!data.access_token) {
    throw new Error('The server did not return a login token.')
  }

  return data
}

export function getCurrentUser(token) {
  return authRequest('/me', { token })
}

export function changePassword(token, currentPassword, newPassword) {
  return authRequest('/change-password', {
    method: 'POST',
    token,
    body: {
      current_password: currentPassword,
      new_password: newPassword,
    },
  })
}