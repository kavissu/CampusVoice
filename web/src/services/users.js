export async function createUser(token, userDetails) {
  let response

  try {
    response = await fetch('/api/v1/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(userDetails),
    })
  } catch {
    throw new Error('Cannot connect to the server. Please try again.')
  }

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const message =
      typeof data?.detail === 'string'
        ? data.detail
        : 'Unable to create the account. Check the entered details.'

    const error = new Error(message)
    error.status = response.status
    throw error
  }

  if (!data) {
    throw new Error('The server returned an unexpected response.')
  }

  return data
}