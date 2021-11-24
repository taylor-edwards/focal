import { useState } from 'react'
import { authenticateAccount } from 'api'
import Button from 'components/Button'

const noop = () => {}

const loginFormState = () => ({
  account_email: '',
  account_name: '',
})

const LoginForm = ({ onSubmit = noop }) => {
  const [loginForm, setLoginForm] = useState(loginFormState())
  const handleSubmit = e => {
    e.preventDefault()
    e.stopPropagation()
    authenticateAccount(loginForm)
      .then(response => response.json())
      .then(json => onSubmit(e, json))
  }
  return (
    <form onSubmit={handleSubmit}>
      <label>
        <p>Username</p>
        <input
          required
          type="text"
          name="account_name"
          value={loginForm.account_name}
          onChange={e => setLoginForm(f => ({
            ...f,
            account_name: e.target.value,
          }))}
        />
      </label>
      <label>
        <p>Email</p>
        <input
          required
          type="email"
          name="account_email"
          value={loginForm.account_email}
          onChange={e => setLoginForm(f => ({
            ...f,
            account_email: e.target.value,
          }))}
        />
      </label>
      <Button type="submit">Submit</Button>
    </form>
  )
}

export default LoginForm
