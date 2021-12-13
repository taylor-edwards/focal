import { useState } from 'react'
import { noop } from 'utils'
import { requestMagicLink } from 'api'
import Button from 'components/Button'
import Input from 'components/Input'

const loginFormState = () => ({
  account_email: '',
  account_name: '',
})

const SignInForm = ({
  className,
  onSubmit = noop,
  onSuccess = noop,
  onFailure = console.warn,
}) => {
  const [loginForm, setSignInForm] = useState(loginFormState())
  const handleSubmit = e => {
    onSubmit(e)
    e.preventDefault()
    e.stopPropagation()
    requestMagicLink(loginForm)
      .then(onSuccess)
      .catch(onFailure)
  }
  return (
    <form onSubmit={handleSubmit} className={className}>
      <Input
        label="Email"
        required
        type="email"
        name="account_email"
        value={loginForm.account_email}
        onChange={e => setSignInForm(f => ({
          ...f,
          account_email: e.target.value,
        }))}
      />

      <div className="col">
        <Button type="submit">Sign in</Button>
      </div>
    </form>
  )
}

export default SignInForm
