import { useState } from 'react'
import { noop } from 'utils'
import { createAccount } from 'api'
import Button from 'components/Button'
import Input from 'components/Input'

const loginFormState = () => ({
  account_email: '',
  account_name: '',
})

const SignUpForm = ({
  className,
  onSubmit = noop,
  onSuccess = noop,
  onFailure = console.warn,
}) => {
  const [loginForm, setSignUpForm] = useState(loginFormState())
  const handleSubmit = e => {
    onSubmit(e)
    e.preventDefault()
    e.stopPropagation()
    createAccount(loginForm)
      .then(onSuccess)
      .catch(onFailure)
  }
  return (
    <form onSubmit={handleSubmit} className={className}>
      <Input
        label="Display name"
        info="This is how other people will see you on Focal"
        required
        type="text"
        name="account_name"
        value={loginForm.account_name}
        onChange={e => setSignUpForm(f => ({
          ...f,
          account_name: e.target.value,
        }))}
      />

      <Input
        label="Email"
        info="Your email address will not be shared with other users or third parties"
        required
        type="email"
        name="account_email"
        value={loginForm.account_email}
        onChange={e => setSignUpForm(f => ({
          ...f,
          account_email: e.target.value,
        }))}
      />

      <div className="col">
        <Button type="submit">Sign up</Button>
      </div>
    </form>
  )
}

export default SignUpForm
