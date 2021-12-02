import { useState } from 'react'
import { authenticateAccount } from 'api'
import Button from 'components/Button'
import Input from 'components/Input'

const noop = () => {}

const loginFormState = () => ({
  account_email: '',
  account_name: '',
})

const SignupForm = ({ className = '', onSubmit = noop }) => {
  const [loginForm, setSignupForm] = useState(loginFormState())
  const handleSubmit = e => {
    e.preventDefault()
    e.stopPropagation()
    authenticateAccount(loginForm)
      .then(response => response.json())
      .then(json => onSubmit(e, json))
      .catch(console.log)
  }
  return (
    <form onSubmit={handleSubmit} className={className}>
      <Input
        label="Username"
        required
        type="text"
        name="account_name"
        value={loginForm.account_name}
        onChange={e => setSignupForm(f => ({
          ...f,
          account_name: e.target.value,
        }))}
      />

      <Input
        label="Email"
        required
        type="email"
        name="account_email"
        value={loginForm.account_email}
        onChange={e => setSignupForm(f => ({
          ...f,
          account_email: e.target.value,
        }))}
      />

      <div className="col">
        <Button type="submit">Login</Button>
        <Button type="submit" appearance="link">Sign up</Button>
      </div>
    </form>
  )
}

export default SignupForm
