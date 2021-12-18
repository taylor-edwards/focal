import { useState } from 'react'
import { fetchWithTimeout, noop } from 'utils'
import Button from 'components/Button'
import Input from 'components/Input'

const SignInForm = ({
  className,
  onSubmit = noop,
  onSuccess = noop,
  onFailure = console.warn,
}) => {
  const [email, setEmail] = useState('')
  const handleSubmit = e => {
    const idx = email.indexOf('@')
    if (idx > 0 && idx < email.length - 1) {
      onSubmit({ email })
      e.preventDefault()
      e.stopPropagation()
      fetchWithTimeout('/api/session', {
        method: 'POST',
        body: JSON.stringify({ email }),
      })
    }
  }
  return (
    <form onSubmit={handleSubmit} className={className}>
      <Input
        label="Email"
        info="Your email address will not be shared with other users or third parties"
        required
        type="email"
        name="email"
        value={email}
        placeholder="you@example.com"
        onChange={e => setEmail(e.target.value ?? '')}
      />

      <div className="col">
        <Button type="submit">Sign in</Button>
        <small>- or -</small>
        <Button type="submit" appearance="link">Create account</Button>
      </div>
    </form>
  )
}

export default SignInForm
